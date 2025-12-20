# Quick Start: Replication Documentation

This guide provides a quick overview of the documentation and tools available for replicating the DeepSeek-R1-Distill-Qwen-1.5B quantization study.

## 📋 Documentation Overview

### Main Guides

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md) | Detailed step-by-step replication instructions | Before starting experiments |
| [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | Technical implementation details | Understanding the codebase |
| [QUICK_START_1.5B.md](./QUICK_START_1.5B.md) | Condensed quick reference | Fast lookup of commands |
| [scripts/README_REPLICATION.md](./scripts/README_REPLICATION.md) | Scripts and tools documentation | Using automation tools |

### Output Documentation Templates

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [REPLICATION_OUTPUTS.md](./REPLICATION_OUTPUTS.md) | Template for documenting quantization results | After running experiments |
| [RESOURCE_BENCHMARKING.md](./RESOURCE_BENCHMARKING.md) | Template for hardware/resource metrics | During and after experiments |

### Research Guide

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [ULTRA_LOW_BIT_QUANTIZATION.md](./ULTRA_LOW_BIT_QUANTIZATION.md) | 2-bit/1-bit quantization exploration | Future research directions |

---

## 🚀 Quick Command Reference

### Baseline Evaluation

```bash
# Evaluate baseline model
bash scripts/inference/inference.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0
```

### Individual Quantization Methods

```bash
# AWQ
bash scripts/quantization/awq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# GPTQ
bash scripts/quantization/gptq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# KVQuant*
bash scripts/quantization/kvquant_star.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# QuaRot-KV
bash scripts/quantization/quarot_kv.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# SmoothQuant
bash scripts/quantization/smoothquant.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# QuaRot
bash scripts/quantization/quarot.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# FlatQuant
bash scripts/quantization/flatquant.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

### Results Analysis

```bash
# View accuracy results
python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B

# View response length statistics
python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B
```

---

## 📊 What Gets Documented

### 1. Quantization Outputs (REPLICATION_OUTPUTS.md)

Documents the **performance** of each quantization method:

- ✅ Accuracy on 6 benchmarks (AIME-90, AIME-2025, MATH-500, GSM8K, GPQA-Diamond, LiveCodeBench)
- ✅ Performance across 3 random seeds
- ✅ Statistical analysis (mean, std dev)
- ✅ Degradation vs baseline
- ✅ Model sizes and compression ratios
- ✅ Inference speed comparisons
- ✅ Quality of reasoning outputs

**Key Tables:**
- Baseline (BF16) results
- Weight-only quantization (AWQ, GPTQ at 3-bit, 4-bit)
- KV-cache quantization (KVQuant*, QuaRot-KV at 3-bit, 4-bit)
- Weight-activation quantization (SmoothQuant, QuaRot, FlatQuant at 4-bit, 8-bit)
- Summary comparison across all methods

### 2. Resource Benchmarking (RESOURCE_BENCHMARKING.md)

Documents the **resources** used during experiments:

- ✅ Hardware specifications (GPU model, VRAM, CPU, cores, RAM)
- ✅ Quantization time for each method
- ✅ Memory usage (GPU, CPU)
- ✅ Disk I/O and storage requirements
- ✅ Power consumption
- ✅ Cost estimates (cloud vs local)
- ✅ Inference speed and throughput

**Key Metrics:**
- Time to quantize (per method)
- Peak memory usage
- Average GPU/CPU utilization
- Power draw (watts)
- Total energy consumption
- Inference tokens/second
- Time to first token (TTFT)

---

## 🛠️ Available Tools

The repository includes the original research scripts for:

- **Quantization scripts** (`scripts/quantization/`): Apply different quantization methods
- **Inference scripts** (`scripts/inference/`): Evaluate models on benchmarks  
- **Results analysis** (`make_stats_table.py`): Generate accuracy and length statistics
- **Visualization** (`methods/visualize/`): Create analysis plots

---

## 🎯 Quick Start Checklist

### Before Experiments

- [ ] Review [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md)
- [ ] Check hardware requirements (16GB+ GPU, 32GB+ RAM)
- [ ] Download model (~3GB)
- [ ] Download datasets (~10-15GB)
- [ ] Install dependencies

### During Experiments

- [ ] Run quantization methods
- [ ] Monitor GPU usage with `nvidia-smi`
- [ ] Check for errors in logs
- [ ] Save intermediate results

### After Experiments

- [ ] Generate statistics with `make_stats_table.py`
- [ ] Review accuracy results
- [ ] Document findings in templates
- [ ] Compare with paper results

---

## 📁 Output Directory Structure

After running experiments, you'll have:

```
Quantized-Reasoning-Models/
├── outputs/
│   ├── modelzoo/              # Quantized models (~10-15GB)
│   │   ├── awq/
│   │   ├── gptq/
│   │   ├── kvquant_star/
│   │   ├── quarot/
│   │   ├── smoothquant/
│   │   └── flatquant/
│   ├── inference/             # Evaluation results (JSON)
│   └── analysis/              # Analysis reports
│       ├── quantization_analysis.md
│       └── plots/
├── logs/                      # Resource monitoring
│   ├── resource_monitor.log
│   ├── resource_summary.md
│   └── [method].log
└── filled_docs/               # Filled documentation
    ├── REPLICATION_OUTPUTS_FILLED.md
    └── RESOURCE_BENCHMARKING_FILLED.md
```

---

## ⏱️ Expected Timeline

| Phase | Time | Cumulative |
|-------|------|------------|
| Environment Setup | 1-2 hours | 2h |
| Model & Dataset Download | 1-2 hours | 4h |
| Calibration Data Generation | 0.5-1 hour | 5h |
| Quantization (all methods) | 4-8 hours | 13h |
| Baseline Evaluation | 2-3 hours | 16h |
| Quantized Model Evaluation | 20-30 hours | 46h |
| Analysis & Documentation | 2-4 hours | 50h |
| **Total** | **~50 hours** | |

*Actual time varies based on hardware*

---

## 💰 Cost Estimates

### Cloud GPU Options

| Provider | Instance | GPU | $/hour | Total (50h) |
|----------|----------|-----|--------|-------------|
| AWS | g5.12xlarge | A10G (24GB) | $5.67 | $284 |
| GCP | a2-highgpu-1g | A100 (40GB) | $3.67 | $184 |
| Azure | NC24ads_A100_v4 | A100 (80GB) | $3.67 | $184 |

### Local Hardware

- **RTX 4090**: ~$1,600 (one-time) + ~$2.50 power (50h)
- **Amortized cost** (assuming 100 experiments): ~$18/experiment

---

## 🔍 Quick Debugging

### Issue: Out of Memory

**Solution:**
- Reduce batch size in config
- Use single GPU (TP=1)
- Close other applications
- Try smaller model first

### Issue: Missing Results

**Check:**
```bash
# Check inference outputs
ls outputs/inference/

# Check logs for errors
cat logs/*.log | grep -i error

# Verify quantized models exist
ls outputs/modelzoo/*/
```

### Issue: Slow Performance

**Optimize:**
- Use fewer seeds (1 instead of 3)
- Skip some benchmarks
- Use faster storage (NVMe)
- Monitor GPU utilization

---

## 📞 Getting Help

1. **Check Documentation:**
   - [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md) - Detailed instructions
   - [scripts/README_REPLICATION.md](./scripts/README_REPLICATION.md) - Tool usage
   - [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Technical details

2. **Review Examples:**
   - Paper results for comparison
   - Existing replication guides
   - Script comments and docstrings

3. **Troubleshooting:**
   - Check logs in `logs/` directory
   - Verify GPU with `nvidia-smi`
   - Test with minimal example first

---

## 🎓 Best Practices

1. **Start Small:**
   - Test with one method first (e.g., GPTQ W4)
   - Verify pipeline works before full replication

2. **Monitor Progress:**
   - Check GPU usage periodically with `nvidia-smi`
   - Keep logs for debugging
   - Take notes during experiments

3. **Document as You Go:**
   - Fill templates incrementally
   - Note any anomalies immediately
   - Save intermediate results

4. **Validate Results:**
   - Compare with paper results
   - Check for outliers
   - Run statistical tests

5. **Backup Data:**
   - Save quantized models
   - Keep raw logs
   - Store analysis outputs

---

## 📚 Further Reading

- **Paper**: [arXiv:2504.04823](https://arxiv.org/abs/2504.04823)
- **Model**: [DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)
- **Methods**:
  - [AWQ](https://github.com/mit-han-lab/llm-awq)
  - [GPTQ](https://arxiv.org/abs/2210.17323)
  - [QuaRot](https://github.com/spcl/QuaRot)
  - [SmoothQuant](https://github.com/mit-han-lab/smoothquant)
  - [FlatQuant](https://github.com/ruikangliu/FlatQuant)

---

## ✨ Summary

This documentation package provides:

✅ **Complete Documentation** - Templates for outputs and resources  
✅ **Original Research Scripts** - All quantization methods from the paper  
✅ **Step-by-Step Guides** - From setup to final documentation  
✅ **Quality Assurance** - Validation and troubleshooting  
✅ **Cost Transparency** - Time and resource estimates  

**Ready to use when model and datasets are available!**

---

*Last Updated: 2025-12-21*  
*Original Repository: [ruikangliu/Quantized-Reasoning-Models](https://github.com/ruikangliu/Quantized-Reasoning-Models)*
