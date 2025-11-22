import argparse
import os
import sys

import numpy as np
import pandas as pd
from pandarallel import pandarallel
from torchvision.io.video import read_video
from tqdm import tqdm


def set_parallel(num_workers: int = None) -> callable:
    """Configurar procesamiento paralelo"""
    if num_workers == 0:
        return lambda x, *args, **kwargs: x.progress_apply(*args, **kwargs)
    else:
        if num_workers is not None:
            pandarallel.initialize(progress_bar=True, nb_workers=num_workers)
        else:
            pandarallel.initialize(progress_bar=True)
        return lambda x, *args, **kwargs: x.parallel_apply(*args, **kwargs)


def get_video_info(path: str) -> pd.Series:
    """Extraer información de video con manejo de errores mejorado"""
    try:
        vframes, _, vinfo = read_video(path, pts_unit="sec", output_format="TCHW")
        num_frames, C, height, width = vframes.shape
        fps = round(vinfo["video_fps"], 3)
        aspect_ratio = height / width if width > 0 else np.nan
        resolution = height * width

        ret = pd.Series(
            [height, width, fps, num_frames, aspect_ratio, resolution],
            index=[
                "height",
                "width",
                "fps",
                "num_frames",
                "aspect_ratio",
                "resolution",
            ],
            dtype=object,
        )
    except Exception as e:
        print(f"Error procesando {path}: {str(e)}", file=sys.stderr)
        # Retornar valores por defecto para errores
        ret = pd.Series(
            [0, 0, 0, 0, 0, 0],
            index=[
                "height",
                "width",
                "fps",
                "num_frames",
                "aspect_ratio",
                "resolution",
            ],
            dtype=object,
        )
    return ret


def parse_args():
    parser = argparse.ArgumentParser(description="Extraer metadatos de videos para VI-NEX-AI")
    parser.add_argument("--input", type=str, required=True, help="Archivo CSV de entrada con rutas de video")
    parser.add_argument("--output", type=str, required=True, help="Archivo CSV de salida con metadatos")
    parser.add_argument("--num_workers", type=int, default=None, 
                       help="Número de workers para procesamiento paralelo (0=secuencial)")
    parser.add_argument("--path-column", type=str, default="path",
                       help="Nombre de la columna que contiene las rutas de video")
    return parser.parse_args()


def validate_input(df: pd.DataFrame, path_column: str):
    """Validar que el archivo de entrada tenga la estructura correcta"""
    if path_column not in df.columns:
        raise ValueError(f"Columna '{path_column}' no encontrada en el archivo de entrada")
    
    # Verificar que las rutas existan (primeras 5 como muestra)
    sample_paths = df[path_column].head(5).tolist()
    for path in sample_paths:
        if not os.path.exists(path):
            print(f"Advertencia: Ruta no encontrada: {path}", file=sys.stderr)


def main():
    args = parse_args()
    input_path = args.input
    output_path = args.output
    num_workers = args.num_workers
    path_column = args.path_column

    # Validar archivo de entrada
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_path}")

    df = pd.read_csv(input_path)
    validate_input(df, path_column)
    
    tqdm.pandas(desc="Procesando videos")
    apply = set_parallel(num_workers)

    print(f"Procesando {len(df)} videos...")
    result = apply(df[path_column], get_video_info)
    
    # Combinar resultados
    for col in result.columns:
        df[col] = result[col]
    
    # Guardar resultados
    df.to_csv(output_path, index=False)
    print(f"Metadatos guardados en: {output_path}")
    
    # Estadísticas
    print(f"\nEstadísticas de videos procesados:")
    print(f"  - Resoluciones únicas: {df['resolution'].nunique()}")
    print(f"  - FPS promedio: {df['fps'].mean():.2f}")
    print(f"  - Frames promedio: {df['num_frames'].mean():.2f}")


if __name__ == "__main__":
    main()