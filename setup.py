from typing import List

from setuptools import find_packages, setup


def fetch_requirements(paths) -> List[str]:
    """
    This function reads the requirements file.

    Args:
        path (str): the path to the requirements file.

    Returns:
        The lines in the requirements file.
    """
    if not isinstance(paths, list):
        paths = [paths]
    requirements = []
    for path in paths:
        with open(path, "r") as fd:
            requirements += [r.strip() for r in fd.readlines()]
    return requirements


def fetch_readme() -> str:
    """
    This function reads the README.md file in the current directory.

    Returns:
        The lines in the README file.
    """
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def get_version() -> str:
    """
    Get version from version file.
    """
    with open("VERSION", "r") as f:
        return f.read().strip()


setup(
    name="vi-nex-ai",
    version=get_version(),
    packages=find_packages(
        exclude=(
            "assets",
            "configs",
            "docs",
            "eval",
            "evaluation_results",
            "gradio",
            "logs",
            "notebooks",
            "outputs",
            "pretrained_models",
            "samples",
            "scripts",
            "tests",
            "*.egg-info",
            "build",
            "dist",
        )
    ),
    description="Next-Generation Open-Source Video Generation Framework",
    long_description=fetch_readme(),
    long_description_content_type="text/markdown",
    license="Apache Software License 2.0",
    url="https://github.com/CUPUL-MIU-04/VI-NEX-AI",
    project_urls={
        "Bug Tracker": "https://github.com/CUPUL-MIU-04/VI-NEX-AI/issues",
        "Documentation": "https://github.com/CUPUL-MIU-04/VI-NEX-AI/docs",
        "Examples": "https://github.com/CUPUL-MIU-04/VI-NEX-AI#vi-nex-ai-demo-showcase",
        "Source Code": "https://github.com/CUPUL-MIU-04/VI-NEX-AI",
        "Discord": "https://discord.gg/vi-nex-ai",
        "Twitter": "https://x.com/vi_nex_ai",
    },
    install_requires=fetch_requirements("requirements.txt"),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Graphics",
        "Environment :: GPU :: NVIDIA CUDA",
        "Framework :: Jupyter",
        "Framework :: FastAPI",
        "Framework :: Gradio",
    ],
    keywords=[
        "ai",
        "artificial-intelligence",
        "video-generation",
        "deep-learning",
        "diffusion-models",
        "computer-vision",
        "transformer",
        "pytorch",
    ],
    author="VI-NEX-AI Contributors",
    author_email="team@vi-nex-ai.org",
    entry_points={
        "console_scripts": [
            "vi-nex-inference=scripts.diffusion.inference:main",
            "vi-nex-train=scripts.diffusion.train:main",
            "vi-nex-vae=scripts.vae.inference:main",
        ],
    },
    include_package_data=True,
    package_data={
        "opensora": [
            "configs/**/*.py",
            "models/**/*.py",
            "utils/**/*.py",
        ]
    },
    extras_require={
        "dev": fetch_requirements("requirements-dev.txt"),
        "gpu": [
            "torch>=2.4.0",
            "torchvision>=0.19.0",
            "torchaudio>=2.4.0",
            "xformers==0.0.27.post2",
            "flash-attn>=2.5.0",
        ],
        "cpu": [
            "torch>=2.4.0+cpu",
            "torchvision>=0.19.0+cpu",
            "torchaudio>=2.4.0+cpu",
        ],
        "inference": [
            "gradio>=4.0.0",
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
        ],
        "training": [
            "colossalai>=0.4.4",
            "deepspeed>=0.14.0",
            "wandb>=0.17.0",
            "tensorboard>=2.14.0",
        ],
        "all": [
            "vi-nex-ai[gpu]",
            "vi-nex-ai[inference]",
            "vi-nex-ai[training]",
        ],
    },
    zip_safe=False,
)