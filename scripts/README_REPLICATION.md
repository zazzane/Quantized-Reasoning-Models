# Replication Scripts Guide

This directory contains scripts to facilitate the quantization experiments for the DeepSeek-R1-Distill-Qwen-1.5B model.

## Overview

The replication process consists of two main phases:

1. **Quantization**: Apply various quantization methods to the model
2. **Evaluation**: Test quantized models on reasoning benchmarks

## Available Scripts

This repository provides the original research scripts for:

- **Quantization methods** (`scripts/quantization/`): AWQ, GPTQ, KVQuant*, QuaRot-KV, SmoothQuant, QuaRot, FlatQuant
- **Inference evaluation** (`scripts/inference/`): Run benchmarks on quantized models
- **Data generation** (`scripts/data/`): Generate calibration datasets

See the sections below for usage examples.

---

## Complete Replication Workflow

### Step 1: Prepare Environment

```bash
# 1. Set up conda environment
conda create -n quantized-reasoning-models python=3.12 -y
conda activate quantized-reasoning-models

# 2. Install dependencies
pip install -r requirements.txt
pip install -e ./third-party/fast-hadamard-transform
VLLM_USE_PRECOMPILED=1 pip install -e ./third-party/vllm
pip install -e ./third-party/lighteval
pip install -e ./third-party/lighteval[math]
pip uninstall xformers -y && pip install -v -U -e third-party/xformers
```

### Step 2: Download Model and Datasets

```bash
# Download model
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B \
    --local-dir ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B

# Download evaluation datasets (see main README.md for URLs and local directories)
# Required datasets:
# - AIME-90 (datasets/AIME90)
# - AIME-2025 (datasets/aime_2025)
# - MATH-500 (datasets/MATH-500)
# - GSM8K (datasets/gsm8k)
# - GPQA-Diamond (datasets/gpqa)
# - LiveCodeBench (datasets/code_generation_lite)
```

### Step 3: Generate Calibration Data

```bash
# Generate calibration data for GPTQ (required for GPTQ quantization)
bash scripts/data/gen_calib.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0
```

### Step 4: Run Baseline Evaluation

```bash
# Evaluate baseline (BF16) model on all benchmarks
bash scripts/inference/inference.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0
```

### Step 5: Run Quantization Experiments

```bash
# Example: Quantize with GPTQ
bash scripts/quantization/gptq.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# Evaluate quantized model
bash scripts/inference/inference.sh \
    ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1 0
```

### Step 6: Analyze Results

```bash
# Use the built-in make_stats_table script from the original research
python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B

# Generate response length statistics
python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B
```

---

## Quick Individual Method Testing

To test a single quantization method:

```bash
# 1. Run quantization
bash scripts/quantization/gptq.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# 2. Run evaluation
bash scripts/inference/inference.sh \
    ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1 0

# 3. View results
python -m make_stats_table --stats acc
```

---

## Troubleshooting

### Out of Memory

**Problem:** GPU runs out of memory during quantization

**Solutions:**
- Reduce tensor parallelism (TP) if possible
- Close other GPU applications
- Use gradient checkpointing
- Try a larger GPU

### Slow Performance

**Problem:** Experiments taking too long

**Solutions:**
- Use fewer evaluation seeds (default is 3)
- Skip some benchmarks
- Use CPU for monitoring to reduce GPU overhead

### Missing Dependencies

**Problem:** Import errors or missing packages

**Solutions:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check CUDA version matches
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

### Results Not Found

**Problem:** Scripts can't find inference results

**Solutions:**
- Check that inference ran successfully
- Verify output paths: `ls outputs/inference/`
- Check for error logs: `cat logs/*.log`

---

## File Structure After Replication

```
Quantized-Reasoning-Models/
├── outputs/
│   ├── modelzoo/           # Quantized models (~10-15GB)
│   │   ├── awq/
│   │   ├── gptq/
│   │   ├── kvquant_star/
│   │   ├── quarot_kv/
│   │   ├── quarot/
│   │   ├── smoothquant/
│   │   └── flatquant/
│   └── inference/          # Evaluation results (JSONL files)
│       └── [model-name]-seed[N]/
│           ├── AIME-90.jsonl
│           ├── AIME-2025.jsonl
│           ├── MATH-500.jsonl
│           ├── GSM8K.jsonl
│           ├── GPQA-Diamond.jsonl
│           └── LiveCodeBench.jsonl
├── datasets/               # Evaluation datasets (~10-15GB)
│   ├── AIME90/
│   ├── aime_2025/
│   ├── MATH-500/
│   ├── gsm8k/
│   ├── gpqa/
│   └── code_generation_lite/
└── modelzoo/               # Pre-trained models
    └── DeepSeek-R1/
        └── DeepSeek-R1-Distill-Qwen-1.5B/
```

---

## Expected Timeline

| Phase | Time | Notes |
|-------|------|-------|
| Setup | 1-2 hours | Environment, model, datasets |
| Calibration Data Gen | 30-60 min | For GPTQ |
| Quantization (per method) | 30 min - 2 hours | Depends on method and hardware |
| Evaluation (per model) | 2-4 hours | 6 benchmarks, 3 seeds |
| **Total (all methods)** | **30-50 hours** | For complete study |

---

## Hardware Recommendations

### Minimum Configuration
- GPU: NVIDIA GPU with 16GB VRAM (e.g., RTX 4080)
- CPU: 8 cores
- RAM: 32GB
- Storage: 50GB SSD

### Recommended Configuration
- GPU: NVIDIA GPU with 24GB VRAM (e.g., RTX 4090, A5000)
- CPU: 16 cores
- RAM: 64GB
- Storage: 100GB NVMe SSD

### Optimal Configuration
- GPU: NVIDIA A100 (40GB or 80GB)
- CPU: 32+ cores
- RAM: 128GB+
- Storage: 200GB+ NVMe SSD

---

## Cost Estimates

**Cloud GPU Options:**

| Provider | GPU | Cost/Hour | Total Cost (48h) |
|----------|-----|-----------|------------------|
| AWS | p4d.24xlarge (A100) | $32.77 | $1,573 |
| AWS | g5.12xlarge (A10G) | $5.67 | $272 |
| GCP | a2-highgpu-1g (A100) | $3.67 | $176 |
| Azure | NC24ads_A100_v4 | $3.67 | $176 |

**Local Hardware:**
- RTX 4090 (Retail): ~$1,600 one-time
- Power cost (48h @ 400W, $0.12/kWh): ~$2.30

---

## Additional Resources

- **Main Documentation**: See [README.md](../README.md)
- **Original Paper**: [arXiv:2504.04823](https://arxiv.org/abs/2504.04823)
- **Model on HuggingFace**: [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)

---

## Support

For issues or questions:
1. Check the main [README.md](../README.md)
2. Refer to the original research paper
3. Open an issue on the original repository

---

*Last Updated: 2025-12-21*
