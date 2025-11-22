#!/usr/bin/env python
"""
VI-NEX-AI Gradio App - Enhanced video generation interface
"""

import argparse
import datetime
import importlib
import os
import subprocess
import sys
from tempfile import NamedTemporaryFile

import spaces
import torch
import gradio as gr

# VI-NEX-AI Configuration Mapping
VI_NEX_CONFIG_MAP = {
    "t2v_256px": "configs/diffusion/inference/vi_nex_256px.py",
    "t2v_512px": "configs/diffusion/inference/vi_nex_512px.py", 
    "t2v_768px": "configs/diffusion/inference/vi_nex_768px.py",
    "t2v_1024px": "configs/diffusion/inference/vi_nex_1024px.py",
    "t2v_2048px": "configs/diffusion/inference/vi_nex_2048px.py",
    "t2v_short": "configs/diffusion/inference/vi_nex_short_video.py",
    "t2v_standard": "configs/diffusion/inference/vi_nex_standard_video.py",
    "t2v_long": "configs/diffusion/inference/vi_nex_long_video.py",
    "t2v_hc": "configs/diffusion/inference/vi_nex_high_compression.py",
    "i2v_512px": "configs/diffusion/inference/t2i2v/vi_nex_t2i2v_512px.py",
    "i2v_1024px": "configs/diffusion/inference/t2i2v/vi_nex_t2i2v_1024px.py",
}

VI_NEX_MODEL_MAP = {
    "t2v_256px": "./ckpts/vi_nex_ai_256.safetensors",
    "t2v_512px": "./ckpts/vi_nex_ai_512.safetensors",
    "t2v_768px": "./ckpts/vi_nex_ai_768.safetensors", 
    "t2v_1024px": "./ckpts/vi_nex_ai_1024.safetensors",
    "t2v_2048px": "./ckpts/vi_nex_ai_2048.safetensors",
    "t2v_short": "./ckpts/vi_nex_ai_fast.safetensors",
    "t2v_standard": "./ckpts/vi_nex_ai_balanced.safetensors",
    "t2v_long": "./ckpts/vi_nex_ai_long.safetensors",
    "t2v_hc": "./ckpts/vi_nex_ai_hc.safetensors",
    "i2v_512px": "./ckpts/vi_nex_ai_i2v_512.safetensors",
    "i2v_1024px": "./ckpts/vi_nex_ai_i2v_1024.safetensors",
}

WATERMARK_PATH = "./assets/images/watermark/vi_nex_watermark.png"

# ============================
# VI-NEX-AI Environment Setup
# ============================
def install_vi_nex_dependencies(enable_optimization=True):
    """Install optimized dependencies for VI-NEX-AI"""
    
    def _is_package_available(name):
        try:
            importlib.import_module(name)
            return True
        except (ImportError, ModuleNotFoundError):
            return False

    # Always install optimized packages for VI-NEX-AI
    if not _is_package_available("flash_attn"):
        print("Installing Flash Attention for VI-NEX-AI...")
        subprocess.run(
            f"{sys.executable} -m pip install flash-attn --no-build-isolation",
            env={"FLASH_ATTENTION_SKIP_CUDA_BUILD": "TRUE"},
            shell=True,
            check=True
        )

    if not _is_package_available("xformers"):
        print("Installing xformers for VI-NEX-AI...")
        subprocess.run(
            f"{sys.executable} -m pip install -v -U git+https://github.com/facebookresearch/xformers.git@main#egg=xformers",
            shell=True,
            check=True
        )

    if not _is_package_available("ninja"):
        print("Installing ninja for VI-NEX-AI...")
        subprocess.run(f"{sys.executable} -m pip install ninja", shell=True, check=True)


# ============================
# VI-NEX-AI Model Management
# ============================
def read_vi_nex_config(config_path):
    """Read VI-NEX-AI configuration file"""
    from mmengine.config import Config
    return Config.fromfile(config_path)


def build_vi_nex_models(config_key, enable_optimization=True):
    """
    Build VI-NEX-AI models for the given configuration
    """
    config_path = VI_NEX_CONFIG_MAP[config_key]
    model_path = VI_NEX_MODEL_MAP[config_key]
    
    print(f"🎯 VI-NEX-AI Loading: {config_key}")
    print(f"📁 Config: {config_path}")
    print(f"🤖 Model: {model_path}")
    
    config = read_vi_nex_config(config_path)
    
    # Build components
    from opensora.registry import MODELS, build_module
    
    # Build VAE
    if "vi_nex" in config_key:
        # Use VI-NEX-AI optimized VAE
        vae_config = config.get('ae', config.get('vae', {}))
        vae = build_module(vae_config, MODELS).cuda()
    else:
        vae = build_module(config.vae, MODELS).cuda()

    # Build text encoder
    text_encoder = build_module(config.text_encoder, MODELS)
    text_encoder.t5.model = text_encoder.t5.model.cuda()

    # Build diffusion model
    from opensora.models.mmdit import MMDiT
    model_kwargs = {k: v for k, v in config.model.items() 
                   if k not in ("type", "from_pretrained", "force_huggingface")}
    
    print(f"🚀 Loading VI-NEX-AI model from: {model_path}")
    model = MMDiT.from_pretrained(model_path, **model_kwargs).cuda()

    # Build scheduler
    from opensora.registry import SCHEDULERS
    scheduler = build_module(config.scheduler, SCHEDULERS)

    # Setup classifier-free guidance
    text_encoder.y_embedder = model.y_embedder

    # Optimize models
    vae = vae.to(torch.bfloat16).eval()
    text_encoder.t5.model = text_encoder.t5.model.eval()
    model = model.to(torch.bfloat16).eval()

    # Clear cache
    torch.cuda.empty_cache()
    
    return vae, text_encoder, model, scheduler, config


def parse_vi_nex_args():
    """Parse VI-NEX-AI specific arguments"""
    parser = argparse.ArgumentParser(description="VI-NEX-AI Gradio App")
    parser.add_argument("--output", default="./vi_nex_outputs", type=str, 
                       help="Output directory for generated content")
    parser.add_argument("--port", default=7860, type=int, help="Gradio app port")
    parser.add_argument("--host", default="0.0.0.0", type=str, help="Gradio app host")
    parser.add_argument("--share", action="store_true", help="Share the gradio app")
    parser.add_argument("--optimized", action="store_true", default=True,
                       help="Enable VI-NEX-AI optimizations")
    return parser.parse_args()


# ============================
# VI-NEX-AI Inference Core
# ============================
# Global variables for VI-NEX-AI
args = parse_vi_nex_args()
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Create output directory
os.makedirs(args.output, exist_ok=True)

# Install optimized dependencies
install_vi_nex_dependencies(enable_optimization=args.optimized)

# Import after installation
from opensora.datasets import IMG_FPS, save_sample
from opensora.datasets.aspect import get_image_size, get_num_frames
from opensora.models.text_encoder.t5 import text_preprocessing
from opensora.utils.inference_utils import (
    add_watermark,
    get_random_prompt_by_openai,
    has_openai_key,
    refine_prompts_by_openai,
)
from opensora.utils.misc import to_torch_dtype

# VI-NEX-AI specific utilities
def get_vi_nex_preset_config(mode, resolution, duration, quality_preset):
    """
    Get VI-NEX-AI configuration based on user selections
    """
    presets = {
        "fast": {
            "256px": "t2v_256px",
            "512px": "t2v_short", 
            "768px": "t2v_512px",
            "1024px": "t2v_512px"
        },
        "balanced": {
            "256px": "t2v_256px",
            "512px": "t2v_standard",
            "768px": "t2v_768px", 
            "1024px": "t2v_1024px"
        },
        "quality": {
            "256px": "t2v_512px",
            "512px": "t2v_1024px",
            "768px": "t2v_1024px",
            "1024px": "t2v_2048px"
        },
        "high_compression": {
            "256px": "t2v_hc",
            "512px": "t2v_hc",
            "768px": "t2v_hc",
            "1024px": "t2v_hc"
        }
    }
    
    if mode == "i2v":
        if resolution in ["512px", "360p"]:
            return "i2v_512px"
        else:
            return "i2v_1024px"
    
    return presets[quality_preset].get(resolution, "t2v_512px")


@spaces.GPU(duration=180)
def run_vi_nex_inference(
    mode,
    prompt_text,
    resolution,
    aspect_ratio, 
    duration,
    quality_preset,
    motion_strength,
    aesthetic_score,
    use_enhancements,
    reference_image,
    refine_prompt,
    seed,
    sampling_steps,
    cfg_scale
):
    """
    VI-NEX-AI optimized inference function
    """
    if not prompt_text or prompt_text.strip() == "":
        gr.Warning("🚫 Please enter a valid prompt")
        return None

    try:
        # Determine configuration
        config_key = get_vi_nex_preset_config(mode, resolution, duration, quality_preset)
        
        # Build models
        vae, text_encoder, model, scheduler, config = build_vi_nex_models(config_key)
        
        torch.manual_seed(seed)
        with torch.inference_mode():
            # Prepare generation parameters
            if mode == "image":
                num_frames = 1
                fps = IMG_FPS
            else:
                num_frames = get_num_frames(duration)
                fps = 24  # VI-NEX-AI optimized FPS

            image_size = get_image_size(resolution, aspect_ratio)
            input_size = (num_frames, *image_size)
            latent_size = vae.get_latent_size(input_size)
            
            # Process prompt
            if refine_prompt and has_openai_key():
                prompt_text = refine_prompts_by_openai([prompt_text])[0]
            
            prompt_text = text_preprocessing(prompt_text)
            
            # Add VI-NEX-AI enhancements to prompt
            if use_enhancements:
                enhanced_prompt = f"{prompt_text}"
                if aesthetic_score and aesthetic_score != "none":
                    enhanced_prompt += f", aesthetic score: {aesthetic_score}"
                if motion_strength and motion_strength != "none" and mode != "image":
                    enhanced_prompt += f", motion strength: {motion_strength}"
                prompt_text = enhanced_prompt

            # Prepare sampling
            z = torch.randn(1, vae.out_channels, *latent_size, 
                           device=torch.cuda.current_device(), 
                           dtype=to_torch_dtype(config.dtype))

            # VI-NEX-AI optimized sampling
            scheduler_kwargs = config.scheduler.copy()
            scheduler_kwargs.pop("type")
            scheduler_kwargs["num_sampling_steps"] = sampling_steps
            scheduler_kwargs["cfg_scale"] = cfg_scale

            scheduler.__init__(**scheduler_kwargs)
            
            samples = scheduler.sample(
                model,
                text_encoder, 
                z=z,
                prompts=[prompt_text],
                device=torch.cuda.current_device(),
                progress=True,
            )

            # Decode and save
            if mode == "image":
                video = vae.decode(samples.to(torch.bfloat16), num_frames=1)
            else:
                video = vae.decode(samples.to(torch.bfloat16), num_frames=num_frames)

            video = video.squeeze(0)

            # Save output
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(args.output, f"vi_nex_{timestamp}")
            saved_path = save_sample(video, save_path=save_path, fps=fps)

            # Add VI-NEX-AI watermark
            if mode != "image" and os.path.exists(WATERMARK_PATH):
                watermarked_path = saved_path.replace(".mp4", "_watermarked.mp4")
                success = add_watermark(saved_path, WATERMARK_PATH, watermarked_path)
                if success:
                    return watermarked_path

            torch.cuda.empty_cache()
            return saved_path

    except Exception as e:
        gr.Warning(f"❌ VI-NEX-AI Generation Error: {str(e)}")
        torch.cuda.empty_cache()
        return None


def generate_vi_nex_random_prompt():
    """Generate random prompt with VI-NEX-AI style"""
    if not has_openai_key():
        gr.Warning("🔑 OpenAI API key not found - using built-in prompts")
        # VI-NEX-AI style built-in prompts
        prompts = [
            "A cyberpunk cityscape at night with flying cars and neon lights, futuristic atmosphere",
            "A majestic dragon flying over a medieval castle during sunset, cinematic style",
            "An astronaut floating in space with Earth in the background, realistic NASA footage",
            "A tranquil Japanese garden with cherry blossoms falling, serene and peaceful",
            "A steampunk laboratory with intricate brass machinery and glowing crystals"
        ]
        import random
        return random.choice(prompts)
    else:
        return get_random_prompt_by_openai()


# ============================
# VI-NEX-AI Gradio Interface
# ============================
def create_vi_nex_interface():
    """Create the VI-NEX-AI Gradio interface"""
    
    with gr.Blocks(theme=gr.themes.Soft(), title="VI-NEX-AI Video Generator") as demo:
        # Header
        gr.HTML("""
        <div style='text-align: center;'>
            <h1 style='color: #4F46E5; margin-bottom: 10px;'>🎬 VI-NEX-AI</h1>
            <h3 style='color: #6B7280; margin-top: 0;'>Enhanced Video Generation Platform</h3>
            <p style='color: #9CA3AF;'>Powered by optimized architectures and advanced training techniques</p>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=1):
                # Input Section
                gr.Markdown("## 📝 Input Settings")
                
                prompt_text = gr.Textbox(
                    label="Prompt",
                    placeholder="Describe your video... (e.g., 'A beautiful sunset over mountains with flying eagles')",
                    lines=3,
                    max_lines=6
                )
                
                with gr.Row():
                    random_prompt_btn = gr.Button("🎲 Random Prompt", size="sm")
                    refine_prompt = gr.Checkbox(
                        value=has_openai_key(), 
                        label="🤖 Enhance with AI",
                        interactive=has_openai_key()
                    )

                # Generation Mode
                mode = gr.Radio(
                    choices=["video", "image"],
                    value="video",
                    label="Generation Mode",
                    info="Generate video or image"
                )

                # Quality Presets
                quality_preset = gr.Radio(
                    choices=["fast", "balanced", "quality", "high_compression"],
                    value="balanced",
                    label="🎯 Quality Preset",
                    info="Speed vs Quality trade-off"
                )

                # Resolution & Aspect Ratio
                with gr.Row():
                    resolution = gr.Radio(
                        choices=["256px", "512px", "768px", "1024px", "2048px"],
                        value="512px",
                        label="📏 Resolution"
                    )
                    
                    aspect_ratio = gr.Radio(
                        choices=["16:9", "9:16", "1:1", "4:3", "3:4"],
                        value="16:9", 
                        label="🖼️ Aspect Ratio"
                    )

                # Duration (for video)
                duration = gr.Radio(
                    choices=["2s", "4s", "6s", "8s", "10s", "15s", "20s", "30s"],
                    value="6s",
                    label="⏱️ Duration",
                    visible=True
                )

                # Enhancement Controls
                gr.Markdown("## 🎨 Enhancement Controls")
                
                with gr.Row():
                    motion_strength = gr.Dropdown(
                        choices=["none", "very low", "low", "medium", "high", "very high"],
                        value="medium",
                        label="🎭 Motion Strength"
                    )
                    
                    aesthetic_score = gr.Dropdown(
                        choices=["none", "low", "medium", "high", "excellent"],
                        value="high", 
                        label="⭐ Aesthetic Quality"
                    )

                use_enhancements = gr.Checkbox(
                    value=True,
                    label="Enable Quality Enhancements",
                    info="Add motion and aesthetic controls to generation"
                )

                # Advanced Settings
                gr.Markdown("## ⚙️ Advanced Settings")
                
                with gr.Row():
                    seed = gr.Number(
                        value=42,
                        label="🔒 Seed",
                        precision=0
                    )
                    
                    sampling_steps = gr.Slider(
                        minimum=10, maximum=200, value=50, step=5,
                        label="🔄 Sampling Steps"
                    )
                    
                    cfg_scale = gr.Slider(
                        minimum=1.0, maximum=20.0, value=7.5, step=0.5,
                        label="🎛️ CFG Scale"
                    )

                # Reference Image
                gr.Markdown("## 🖼️ Reference Image (Optional)")
                reference_image = gr.Image(
                    label="Upload Reference Image",
                    type="numpy",
                    show_download_button=False
                )

                # Generate Buttons
                with gr.Row():
                    generate_btn = gr.Button(
                        "🚀 Generate Video/Image", 
                        variant="primary",
                        size="lg"
                    )
                    
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")

            with gr.Column(scale=1):
                # Output Section
                gr.Markdown("## 📺 Output")
                
                output_video = gr.Video(
                    label="Generated Content",
                    height=400,
                    show_download_button=True,
                    autoplay=True
                )
                
                # Generation Info
                info_text = gr.Textbox(
                    label="Generation Info",
                    placeholder="Generation information will appear here...",
                    lines=3,
                    max_lines=5,
                    interactive=False
                )

        # Event Handlers
        def update_duration_visibility(mode):
            return gr.update(visible=(mode == "video"))
        
        mode.change(update_duration_visibility, inputs=[mode], outputs=[duration])

        # Generate button click
        generate_btn.click(
            fn=run_vi_nex_inference,
            inputs=[
                mode,
                prompt_text,
                resolution,
                aspect_ratio,
                duration, 
                quality_preset,
                motion_strength,
                aesthetic_score,
                use_enhancements,
                reference_image,
                refine_prompt,
                seed,
                sampling_steps,
                cfg_scale
            ],
            outputs=[output_video]
        )

        # Random prompt button
        random_prompt_btn.click(
            fn=generate_vi_nex_random_prompt,
            outputs=[prompt_text]
        )

        # Clear button
        def clear_all():
            return None, None, None
        
        clear_btn.click(
            fn=clear_all,
            outputs=[prompt_text, reference_image, output_video]
        )

        # Examples
        gr.Markdown("## 💡 Example Prompts")
        gr.Examples(
            examples=[
                ["A tranquil forest with sunlight streaming through trees, peaceful atmosphere", "video", "512px", "balanced"],
                ["A futuristic city with flying vehicles and holographic advertisements", "video", "768px", "quality"],
                ["A majestic waterfall in a tropical jungle, cinematic drone shot", "image", "1024px", "quality"],
                ["A cute cartoon character dancing in a colorful room, animated style", "video", "512px", "fast"],
            ],
            inputs=[prompt_text, mode, resolution, quality_preset],
            outputs=[output_video],
            fn=run_vi_nex_inference,
            cache_examples=False
        )

        # Footer
        gr.HTML("""
        <div style='text-align: center; color: #6B7280; margin-top: 20px;'>
            <p>VI-NEX-AI • Enhanced Video Generation • Built on Open-Sora</p>
        </div>
        """)

        return demo


def main():
    """Main function to launch VI-NEX-AI Gradio app"""
    print("🚀 Starting VI-NEX-AI Gradio Application...")
    print("📁 Output directory:", args.output)
    print("🌐 Host:", args.host)
    print("🔌 Port:", args.port)
    
    demo = create_vi_nex_interface()
    
    # Launch with optimized settings
    demo.queue(
        max_size=3,
        default_concurrency_limit=1,
        api_open=False
    )
    
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        show_error=True,
        quiet=False
    )


if __name__ == "__main__":
    main()