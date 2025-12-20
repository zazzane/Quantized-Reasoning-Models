# Quick Start: DeepSeek-R1-Distill-Qwen-1.5B Quantization Experiments

This is a quick reference guide for running quantization experiments on the DeepSeek-R1-Distill-Qwen-1.5B model. For detailed documentation, see [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md).

## One-Command Full Replication

```bash
# Download the model first
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B \
    --local-dir ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B
```

**Note:** For complete replication of all methods, follow the individual experiment commands below. Running all 13 quantization configurations with evaluation on 6 benchmarks requires 30-50 hours total.

See [REPLICATION_GUIDE_1.5B.md](../DOCUMENTATIONS/REPLICATION_GUIDE_1.5B.md) for the complete step-by-step workflow.

## Individual Experiments

### 1. Baseline (BF16)

```bash
bash scripts/inference/inference.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0 42
```

### 2. Weight-Only Quantization

```bash
# AWQ (3-bit and 4-bit)
bash scripts/quantization/awq.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# GPTQ (3-bit and 4-bit)
bash scripts/quantization/gptq.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

### 3. KV-Cache Quantization

```bash
# KVQuant* (3-bit and 4-bit)
bash scripts/quantization/kvquant_star.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# QuaRot-KV (3-bit and 4-bit)
bash scripts/quantization/quarot_kv.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

### 4. Weight-Activation Quantization

```bash
# SmoothQuant (8-bit)
bash scripts/quantization/smoothquant.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# QuaRot (4-bit and 8-bit)
bash scripts/quantization/quarot.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# FlatQuant (4-bit and 8-bit)
bash scripts/quantization/flatquant.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

## Results Analysis

```bash
# Generate accuracy comparison table
python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B

# Generate response length analysis
python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B
```

## Quantization Methods Summary

| Method | Category | Bit-width | Models Generated |
|--------|----------|-----------|------------------|
| AWQ | Weight-Only | 3, 4 | 2 models |
| GPTQ | Weight-Only | 3, 4 | 2 models |
| KVQuant* | KV-Cache | 3, 4 | 2 models |
| QuaRot-KV | KV-Cache | 3, 4 | 2 models |
| SmoothQuant | Weight-Activation | 8 | 1 model |
| QuaRot | Weight-Activation | 4, 8 | 2 models |
| FlatQuant | Weight-Activation | 4, 8 | 2 models |
| **Total** | | | **13 quantized models** |

## Evaluation Benchmarks

1. **AIME-90**: 90 problems from historical AIME competitions
2. **AIME-2025**: 30 problems from AIME 2025
3. **MATH-500**: 500 problems from MATH dataset
4. **GSM8K**: Grade school math word problems
5. **GPQA-Diamond**: Graduate-level science questions
6. **LiveCodeBench**: Recent coding challenges

## Expected Results (from Paper)

Based on the research paper for similar-sized models:

### Baseline Performance (BF16)
- **AIME-120**: ~21-25%
- **MATH-500**: ~45-50%
- **GSM8K**: ~80-85%

### Quantization Impact
- **Weight-Only 4-bit**: < 5% relative degradation
- **Weight-Only 3-bit**: 5-15% relative degradation
- **KV-Cache 4-bit**: < 3% relative degradation
- **KV-Cache 3-bit**: 3-8% relative degradation
- **Weight-Activation 8-bit**: 10-20% relative degradation
- **Weight-Activation 4-bit**: > 20% relative degradation

*Note: Exact numbers will vary based on implementation and random seeds*

## File Structure

```
outputs/
├── modelzoo/              # Quantized models
│   ├── awq/
│   ├── gptq/
│   ├── kvquant_star/
│   ├── quarot/
│   ├── smoothquant/
│   └── flatquant/
├── inference/             # Evaluation results
│   └── {model-name}-seed{seed}/
│       ├── AIME-90.jsonl
│       ├── AIME-2025.jsonl
│       ├── MATH-500.jsonl
│       ├── GSM8K.jsonl
│       ├── GPQA-Diamond.jsonl
│       └── LiveCodeBench.jsonl
└── logs/                  # Execution logs
```

## Resource Requirements

### Storage
- Base model: ~3 GB
- Datasets: ~5-10 GB
- Quantized models: ~0.5-1.5 GB each (13 models = ~10-15 GB)
- Results: ~1-2 GB
- **Total**: ~20-30 GB

### GPU Memory
- Baseline evaluation: ~6-8 GB
- Quantization: ~10-12 GB peak
- Quantized model evaluation: ~4-6 GB

### Recommended Hardware
- **Minimum**: 1x GPU with 16 GB VRAM (RTX 4060 Ti, V100)
- **Recommended**: 1x GPU with 24 GB VRAM (RTX 3090, RTX 4090, A5000)
- **Optimal**: 1x GPU with 40+ GB VRAM (A100, H100)

## Troubleshooting

### Out of Memory During Quantization
```bash
# Reduce calibration samples in the quantization scripts
# Edit scripts/quantization/*.sh and reduce --nsamples parameter
```

### Missing Datasets
```bash
# Download datasets individually
# See REPLICATION_GUIDE_1.5B.md for dataset URLs
```

### Evaluation Taking Too Long
```bash
# Run on fewer seeds (just seed 42)
bash scripts/inference/inference.sh <model_path> 0 42
```

## Next Steps

1. **Reproduce Paper Results**: Run full replication and compare with paper
2. **Explore 2-bit/1-bit**: See [ULTRA_LOW_BIT_QUANTIZATION.md](./ULTRA_LOW_BIT_QUANTIZATION.md)
3. **Custom Quantization**: Modify scripts for different bit-widths or methods
4. **Other Models**: Apply same pipeline to 7B, 14B, 32B models

## Support

- **Detailed Guide**: [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md)
- **Ultra-Low Bit**: [ULTRA_LOW_BIT_QUANTIZATION.md](./ULTRA_LOW_BIT_QUANTIZATION.md)
- **Paper**: https://arxiv.org/abs/2504.04823
- **Issues**: https://github.com/zazzane/Quantized-Reasoning-Models/issues
