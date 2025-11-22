# VI-NEX-AI #
<p align="center">
    <img src="https://github.com/VI-NEX-AI/VI-NEX-AI/blob/main/assets/logo.png" width="250"/>
</p>
<div align="center">
    <a href="https://github.com/VI-NEX-AI/VI-NEX-AI/stargazers"><img src="https://img.shields.io/github/stars/VI-NEX-AI/VI-NEX-AI?style=social"></a>
    <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
    <a href="https://python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-green"></a>
    <a href="https://pytorch.org/"><img src="https://img.shields.io/badge/PyTorch-2.0%2B-red"></a>
</div>

<div align="center">
    <a href="https://discord.gg/vi-nex-ai"><img src="https://img.shields.io/badge/Discord-join-blueviolet?logo=discord"></a>
    <a href="https://github.com/VI-NEX-AI/VI-NEX-AI/discussions"><img src="https://img.shields.io/badge/GitHub-Discussions-blueviolet"></a>
    <a href="https://x.com/vi_nex_ai"><img src="https://img.shields.io/badge/Twitter-Follow-blue?logo=twitter"></a>
</div>

## VI-NEX-AI: Next-Generation Open-Source Video Generation Framework

**VI-NEX-AI** is an advanced, community-driven fork of Open-Sora, dedicated to pushing the boundaries of efficient and high-quality video generation. We build upon the solid foundation of Open-Sora while introducing cutting-edge features, optimizations, and expanded capabilities for the open-source community.

🚀 **Key Enhancements in VI-NEX-AI:**
- **Multi-Resolution Support**: 256px to 2048px with optimized configurations
- **Advanced Style Controls**: Anime, 3D Animation, Hyper-Realistic, and more
- **Extended Duration**: Support for ultra-long video generation (25+ seconds)
- **High FPS Support**: Up to 50fps for smoother video output
- **Optimized Architectures**: Enhanced MMDiT and VAE implementations
- **Comprehensive Tooling**: Improved training pipelines and inference optimizations

## 🎥 VI-NEX-AI Demo Showcase

### Multi-Resolution Generation
| **512×512** | **1024×1024** | **2048×1152** |
|-------------|---------------|---------------|
| <img src="https://via.placeholder.com/200x200/0088cc/ffffff?text=512px" width="200"> | <img src="https://via.placeholder.com/200x200/0088cc/ffffff?text=1024px" width="200"> | <img src="https://via.placeholder.com/200x200/0088cc/ffffff?text=2048px" width="200"> |

### Style Variations
| **Anime Style** | **3D Animation** | **Hyper-Realistic** |
|-----------------|------------------|---------------------|
| <img src="https://via.placeholder.com/200x200/ff6b6b/ffffff?text=Anime" width="200"> | <img src="https://via.placeholder.com/200x200/4ecdc4/ffffff?text=3D" width="200"> | <img src="https://via.placeholder.com/200x200/45b7d1/ffffff?text=Realistic" width="200"> |

## 🚀 Quick Start

### Installation

```bash
# Create and activate virtual environment
conda create -n vi_nex_ai python=3.10
conda activate vi_nex_ai

# Clone repository
git clone https://github.com/CUPUL-MIU-04/VI-NEX-AI.git
cd VI-NEX-AI

# Install in development mode
pip install -v -e .

# Install additional dependencies
pip install xformers flash-attn