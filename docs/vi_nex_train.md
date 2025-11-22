### **3. vi_nex_train.md**
```markdown
# VI-NEX-AI Training Guide

Optimized training procedures for VI-NEX-AI models.

## Quick Start

### Stage 1 - Base Training
```bash
torchrun --nproc_per_node 8 scripts/diffusion/train.py configs/diffusion/train/vi_nex_stage1.py --dataset.data-path your_dataset.csv