# Quick Submission Guide - DeepSeek-R1-Distill-Qwen-1.5B Quantization

## ✅ Setup Complete - Ready to Submit!

Your environment is fully configured and ready for SLURM job submission. Here's what has been accomplished:

### Completed Setup ✅
- ✅ Virtual environment activated (Python 3.9.21)
- ✅ Model downloaded (3.4GB) to `./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B`
- ✅ All dependencies verified (PyTorch, Transformers, Datasets)
- ✅ Quantization scripts available
- ✅ SLURM job scripts created and executable
- ✅ Output directories created
- ✅ System has sufficient memory (377GB total, 349GB available)

## 🚀 Submit Your Jobs

### Option 1: Submit Both Tasks (Recommended)
```bash
cd /home/FYP/zane0001/FYP/Quantized-Reasoning-Models

# Submit Task 1: Weight-Only + KV-Cache Quantization (4-5 hours)
sbatch slurm_task1.sh

# Submit Task 2: Weight-Activation + Baseline (4-5 hours)  
sbatch slurm_task2.sh
```

### Option 2: Submit One Task First (Conservative)
```bash
# Start with Task 1 (most promising methods)
sbatch slurm_task1.sh

# Wait for completion, then submit Task 2
sbatch slurm_task2.sh
```

## 📊 What Each Task Does

### Task 1: High-Performance Quantization
- **AWQ**: Weight-only 3-bit, 4-bit
- **GPTQ**: Weight-only 3-bit, 4-bit  
- **KVQuant***: KV-cache 3-bit, 4-bit
- **QuaRot-KV**: KV-cache 3-bit, 4-bit
- **Expected**: Minimal performance degradation (< 5%)

### Task 2: Aggressive Quantization + Baseline
- **Baseline**: BF16 evaluation (reference)
- **SmoothQuant**: Weight-activation 8-bit
- **QuaRot**: Weight-activation 4-bit, 8-bit
- **FlatQuant**: Weight-activation 4-bit, 8-bit
- **Expected**: Higher compression, more degradation (10-20%)

## 📈 Monitor Your Jobs

```bash
# Check job status
squeue -u $USER

# View job output (replace {job_id} with actual job ID)
tail -f slurm-{job_id}.out

# Check for errors
cat slurm-{job_id}.err

# View resource usage after completion
seff {job_id}
```

## 📁 Expected Results Structure

After completion, you'll find:

```
outputs/
├── modelzoo/           # 13 quantized models
├── inference/          # Evaluation results (3 seeds × 6 benchmarks)
└── logs/              # Execution logs

# Analysis reports
- task1_quantization_results.md
- task2_quantization_results.md  
- combined_quantization_results.md
```

## 🎯 Key Metrics to Look For

Based on the research paper, expect:

### Baseline (BF16)
- **AIME-120**: 21-25%
- **MATH-500**: 45-50%
- **GSM8K**: 80-85%

### Best Performing Methods
- **Weight-Only 4-bit**: < 5% degradation
- **KV-Cache 4-bit**: < 3% degradation
- **Weight-Only 3-bit**: 5-15% degradation

### Higher Compression Methods
- **Weight-Activation 8-bit**: 10-20% degradation
- **Weight-Activation 4-bit**: > 20% degradation

## ⚡ Quick Commands Reference

```bash
# Submit jobs
sbatch slurm_task1.sh && sbatch slurm_task2.sh

# Monitor
squeue -u $USER

# Check progress
tail -f slurm-{job_id}.out

# View results (after completion)
ls outputs/inference/
cat task1_quantization_results.md
cat task2_quantization_results.md
```

## 🔧 Troubleshooting

### If Jobs Fail
```bash
# Check logs
cat slurm-{job_id}.out
cat slurm-{job_id}.err

# Cancel and resubmit
scancel {job_id}
sbatch slurm_task1.sh
```

### If Out of Memory
- The scripts are already optimized for 64GB
- If issues persist, reduce calibration samples in the quantization scripts

### If Timeout
- Monitor job progress closely
- Consider reducing to single seed (42) if needed

## 📚 Additional Resources

- **Detailed Setup**: [SLURM_SETUP.md](./SLURM_SETUP.md)
- **Full Replication Guide**: [REPLICATION_GUIDE_1.5B.md](./REPLICATION_GUIDE_1.5B.md)
- **Ultra-Low Bit Guide**: [ULTRA_LOW_BIT_QUANTIZATION.md](./ULTRA_LOW_BIT_QUANTIZATION.md)
- **Paper**: https://arxiv.org/abs/2504.04823

## 🎉 Success Indicators

Your experiments are successful when:
1. ✅ Both jobs complete within 6 hours
2. ✅ All quantized models are generated
3. ✅ Evaluation results show expected performance patterns
4. ✅ Analysis reports are generated
5. ✅ Results align with paper expectations (±5%)

---

**Ready to submit? Run the commands above and monitor your jobs!** 🚀

Good luck with your quantization experiments!
