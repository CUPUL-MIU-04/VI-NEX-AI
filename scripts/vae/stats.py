from pprint import pformat

import colossalai
import torch
from colossalai.utils import get_current_device, set_seed
from tqdm import tqdm

from opensora.acceleration.parallel_states import get_data_parallel_group
from opensora.datasets.dataloader import prepare_dataloader
from opensora.registry import DATASETS, MODELS, build_module
from opensora.utils.config import parse_configs
from opensora.utils.logger import create_logger, is_distributed, is_main_process
from opensora.utils.misc import log_cuda_max_memory, log_model_params, to_torch_dtype


@torch.inference_mode()
def main():
    torch.set_grad_enabled(False)
    # ======================================================
    # configs & runtime variables
    # ======================================================
    # == parse configs ==
    cfg = parse_configs()

    # == get dtype & device ==
    dtype = to_torch_dtype(cfg.get("dtype", "bf16"))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if is_distributed():
        colossalai.launch_from_torch({})
        device = get_current_device()
    set_seed(cfg.get("seed", 1024))

    # == init logger ==
    logger = create_logger()
    logger.info("VI-NEX-AI VAE Stats Configuration:\n %s", pformat(cfg.to_dict()))
    verbose = cfg.get("verbose", 1)

    # ======================================================
    # build model & loss
    # ======================================================
    if cfg.get("ckpt_path", None) is not None:
        cfg.model.from_pretrained = cfg.ckpt_path
    logger.info("Building VI-NEX-AI VAE model...")
    model = build_module(cfg.model, MODELS, device_map=device, torch_dtype=dtype).eval()
    log_model_params(model)

    # ======================================================
    # build dataset and dataloader
    # ======================================================
    logger.info("Building dataset...")
    # == build dataset ==
    dataset = build_module(cfg.dataset, DATASETS)
    logger.info("Dataset contains %s samples.", len(dataset))
    # == build dataloader ==
    dataloader_args = dict(
        dataset=dataset,
        batch_size=cfg.get("batch_size", None),
        num_workers=cfg.get("num_workers", 4),
        seed=cfg.get("seed", 1024),
        shuffle=False,
        drop_last=False,
        pin_memory=True,
        process_group=get_data_parallel_group(),
        prefetch_factor=cfg.get("prefetch_factor", None),
    )

    if cfg.get("eval_setting", None) is not None:
        # e.g. 32x256x256, 1x1024x1024
        num_frames = int(cfg.eval_setting.split("x")[0])
        resolution = str(cfg.eval_setting.split("x")[-1])
        bucket_config = {
            resolution + "px_ar1:1": {num_frames: (1.0, 1)},
        }
        logger.info("Evaluation setting: %s", bucket_config)
    else:
        bucket_config = cfg.get("bucket_config", None)

    dataloader, _ = prepare_dataloader(
        bucket_config=bucket_config,
        num_bucket_build_workers=cfg.get("num_bucket_build_workers", 1),
        **dataloader_args,
    )
    dataiter = iter(dataloader)
    num_steps_per_epoch = len(dataloader)

    # ======================================================
    # inference
    # ======================================================
    num_samples = 0
    running_sum = running_var = 0.0

    logger.info("Starting VI-NEX-AI VAE statistics collection...")

    # Iter over the dataset
    with tqdm(
        enumerate(dataiter),
        disable=not is_main_process() or verbose < 1,
        total=num_steps_per_epoch,
        initial=0,
        desc="VI-NEX-AI VAE Stats"
    ) as pbar:
        for _, batch in pbar:
            # == load data ==
            x = batch["video"].to(device, dtype)  # [B, C, T, H, W]

            # == vae encoding ===
            z = model.encode(x)

            batch_size = x.shape[0]
            num_samples += batch_size
            
            # Welford's online algorithm for variance
            delta = z.mean() - running_sum / num_samples if num_samples > 0 else z.mean()
            running_sum += z.mean() * batch_size
            running_var += (z - running_sum / num_samples).pow(2).mean() * batch_size
            
            shift = running_sum / num_samples
            scale = (running_var / num_samples) ** 0.5
            pbar.set_postfix({"mean": f"{shift:.4f}", "std": f"{scale:.4f}"})

    logger.info("VI-NEX-AI VAE Statistics completed!")
    logger.info("Final results - Samples: %s, Mean: %.4f, Std: %.4f", num_samples, shift, scale)
    log_cuda_max_memory("inference")


if __name__ == "__main__":
    main()