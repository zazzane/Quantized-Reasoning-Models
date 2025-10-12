# SLURM Setup Guide for DeepSeek-R1-Distill-Qwen-1.5B Quantization

This guide explains how to run the quantization experiments on the NTU TC1 GPU cluster with SLURM constraints.

## Overview

Due to the 6-hour time limit and 2-task maximum on the cluster, the experiments are split into two strategic tasks:

### Task 1: Weight-Only + KV-Cache Quantization (4-5 hours)
- **Focus**: Most promising quantization methods with minimal performance degradation
- **Methods**: AWQ, GPTQ, KVQuant*, QuaRot-KV
- **Bit-widths**: 3-bit, 4-bit
- **Expected Results**: Best performance retention

### Task 2: Weight-Activation + Baseline (4-5 hours)
- **Focus**: More aggressive quantization methods and baseline evaluation
- **Methods**: Baseline (BF16), SmoothQuant, QuaRot, FlatQuant
- **Bit-widths**: 4-bit, 8-bit
- **Expected Results**: Higher compression but more performance degradation

## Prerequisites

✅ **Completed Setup**:
- Virtual environment activated
- Model downloaded to `./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B`
- All dependencies installed

## SLURM Configuration

Both tasks use identical SLURM configuration optimized for the cluster:

```bash
#SBATCH --partition=UGGPU-TC1
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --mem=64G
#SBATCH --ntasks-per-node=8
#SBATCH --time=360
```

### Resource Allocation Rationale

- **GPU Memory (64G)**: Sufficient for 1.5B model quantization and inference
- **CPU Cores (8)**: Optimal for parallel data processing and calibration
- **Time (360 minutes = 6 hours)**: Maximum allowed time limit
- **Single GPU**: Sufficient for 1.5B model (TP=1)

## Submission Instructions

### 1. Submit Task 1 (Weight-Only + KV-Cache)

```bash
cd /home/FYP/zane0001/FYP/Quantized-Reasoning-Models
sbatch slurm_task1.sh
```

**What Task 1 does**:
1. Generates calibration data for GPTQ
2. Runs AWQ quantization (3-bit, 4-bit)
3. Runs GPTQ quantization (3-bit, 4-bit)
4. Runs KVQuant* quantization (3-bit, 4-bit)
5. Runs QuaRot-KV quantization (3-bit, 4-bit)
6. Evaluates all quantized models (3 seeds × 6 benchmarks)
7. Generates results summary

### 2. Submit Task 2 (Weight-Activation + Baseline)

```bash
cd /home/FYP/zane0001/FYP/Quantized-Reasoning-Models
sbatch slurm_task2.sh
```

**What Task 2 does**:
1. Runs baseline evaluation (BF16, 3 seeds)
2. Runs SmoothQuant quantization (8-bit)
3. Runs QuaRot quantization (4-bit, 8-bit)
4. Runs FlatQuant quantization (4-bit, 8-bit)
5. Evaluates all quantized models (3 seeds × 6 benchmarks)
6. Generates results summary
7. Creates combined analysis (if Task 1 completed)

## Expected Outputs

### File Structure After Completion

```
outputs/
├── modelzoo/                    # Quantized models
│   ├── awq/                    # AWQ quantized models
│   ├── gptq/                   # GPTQ quantized models
│   ├── kvquant_star/           # KVQuant* models
│   ├── quarot/                 # QuaRot models
│   ├── smoothquant/            # SmoothQuant models
│   └── flatquant/              # FlatQuant models
├── inference/                  # Evaluation results
│   └── {model-name}-seed{seed}/
│       ├── AIME-90.jsonl
│       ├── AIME-2025.jsonl
│       ├── MATH-500.jsonl
│       ├── GSM8K.jsonl
│       ├── GPQA-Diamond.jsonl
│       └── LiveCodeBench.jsonl
└── logs/                      # Execution logs
    ├── task1_*.log
    └── task2_*.log
```

### Results Analysis

After both tasks complete, you'll have:

1. **Individual Task Reports**:
   - `task1_quantization_results.md`
   - `task2_quantization_results.md`

2. **Combined Analysis**:
   - `combined_quantization_results.md`
   - Performance comparison charts (PNG)
   - Accuracy degradation tables

## Monitoring Jobs

### Check Job Status
```bash
squeue -u $USER
```

### View Job Output
```bash
# Check job logs
cat slurm-{job_id}.out
cat slurm-{job_id}.err

# Monitor progress in real-time
tail -f slurm-{job_id}.out
```

### Resource Usage
```bash
# After job completion
seff {job_id}
```

## Expected Results (Based on Paper)

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

## Troubleshooting

### Common Issues

1. **Out of Memory**:
   - Reduce calibration samples in quantization scripts
   - Check GPU memory usage with `nvidia-smi`

2. **Job Timeout**:
   - Monitor job progress with `squeue`
   - Consider reducing seeds (use only seed 42)

3. **Missing Datasets**:
   - Ensure all evaluation datasets are downloaded
   - Check dataset paths in scripts

### Quick Fixes

```bash
# Cancel stuck job
scancel {job_id}

# Check GPU availability
sinfo -N | grep idle

# Monitor resource usage
watch -n 1 nvidia-smi
```

## Next Steps After Completion

1. **Analyze Results**: Compare with paper expectations
2. **Identify Best Methods**: Focus on methods with minimal degradation
3. **Explore 2-bit/1-bit**: Use the provided guide for ultra-low bit quantization
4. **Scale to Larger Models**: Apply same pipeline to 7B, 14B, 32B models

## Support

- **Detailed Replication Guide**: [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md)
- **Ultra-Low Bit Guide**: [ULTRA_LOW_BIT_QUANTIZATION.md](./ULTRA_LOW_BIT_QUANTIZATION.md)
- **Quick Start**: [QUICK_START_1.5B.md](./QUICK_START_1.5B.md)
- **Paper**: https://arxiv.org/abs/2504.04823
