# Replication Scripts Guide

This directory contains scripts to facilitate the complete replication of quantization experiments for the DeepSeek-R1-Distill-Qwen-1.5B model.

## Overview

The replication process consists of three main phases:

1. **Quantization**: Apply various quantization methods to the model
2. **Evaluation**: Test quantized models on reasoning benchmarks
3. **Documentation**: Collect and document results and resource usage

## Scripts

### 1. Master Replication Script

**`run_all_quantization_1.5b.sh`**

Automated execution of all quantization experiments.

**Usage:**
```bash
# Run all experiments on GPU 0
bash scripts/run_all_quantization_1.5b.sh 0

# Or specify different GPU
bash scripts/run_all_quantization_1.5b.sh 1
```

**What it does:**
- Checks prerequisites (model and datasets)
- Runs all 13 quantization methods
- Evaluates each method on 6 benchmarks with 3 seeds
- Generates summary tables

**Requirements:**
- Model: `./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B`
- Datasets: `./datasets/` (see main README.md)
- GPU: 16GB+ VRAM recommended
- Time: 24-48 hours total

**Output:**
- Quantized models: `outputs/modelzoo/`
- Inference results: `outputs/inference/`
- Logs: `logs/`

---

### 2. Results Analysis Script

**`analyze_quantization_results.py`**

Analyze and visualize quantization results.

**Usage:**
```bash
# Basic analysis (print to console)
python scripts/analyze_quantization_results.py \
    --model_name DeepSeek-R1-Distill-Qwen-1.5B

# Generate markdown report
python scripts/analyze_quantization_results.py \
    --model_name DeepSeek-R1-Distill-Qwen-1.5B \
    --save_report

# Generate plots (requires matplotlib)
python scripts/analyze_quantization_results.py \
    --model_name DeepSeek-R1-Distill-Qwen-1.5B \
    --plot

# Full analysis with report and plots
python scripts/analyze_quantization_results.py \
    --model_name DeepSeek-R1-Distill-Qwen-1.5B \
    --save_report --plot
```

**What it does:**
- Reads evaluation results from `outputs/inference/`
- Computes accuracy statistics (mean, std) across seeds
- Calculates relative degradation vs baseline
- Generates comparison tables
- Creates visualization plots (optional)
- Produces markdown report

**Output:**
- Console tables (accuracy, degradation)
- Markdown report: `outputs/analysis/quantization_analysis.md`
- Plots: `outputs/analysis/plots/*.png`

---

### 3. Resource Monitoring Script

**`monitor_resources.py`**

Monitor GPU, CPU, and memory usage during experiments.

**Usage:**

**A. Start Monitoring (before running experiments):**
```bash
# Basic monitoring
python scripts/monitor_resources.py --output logs/resource_monitor.log

# Custom sampling interval (2 seconds)
python scripts/monitor_resources.py --output logs/resource_monitor.log --interval 2

# Monitor for specific duration (1 hour)
python scripts/monitor_resources.py --output logs/resource_monitor.log --duration 3600

# Monitor specific process
python scripts/monitor_resources.py --output logs/resource_monitor.log --pid 12345
```

**B. Analyze Monitoring Logs (after experiments):**
```bash
# Print summary to console
python scripts/monitor_resources.py --analyze logs/resource_monitor.log

# Generate markdown report
python scripts/monitor_resources.py \
    --analyze logs/resource_monitor.log \
    --report logs/resource_summary.md
```

**What it does:**
- Monitors GPU utilization, memory, power, temperature
- Tracks CPU usage, system memory
- Records disk I/O
- Logs all metrics to CSV
- Generates summary statistics

**Output:**
- CSV log: `logs/resource_monitor.log`
- Summary report: `logs/resource_summary.md`

**Dependencies:**
```bash
pip install psutil pynvml
```

---

### 4. Metrics Extraction Script

**`extract_metrics_to_docs.py`**

Extract results and populate documentation templates.

**Usage:**
```bash
# Basic extraction
python scripts/extract_metrics_to_docs.py \
    --model DeepSeek-R1-Distill-Qwen-1.5B

# Custom paths
python scripts/extract_metrics_to_docs.py \
    --model DeepSeek-R1-Distill-Qwen-1.5B \
    --inference-dir outputs/inference \
    --resource-dir logs \
    --output-dir filled_docs
```

**What it does:**
- Reads inference results from `outputs/inference/`
- Extracts model sizes from `outputs/modelzoo/`
- Reads resource logs from `logs/`
- Generates filled versions of documentation templates

**Output:**
- `filled_docs/REPLICATION_OUTPUTS_FILLED.md`
- `filled_docs/RESOURCE_BENCHMARKING_FILLED.md`

---

## Complete Replication Workflow

### Step 1: Prepare Environment

```bash
# 1. Clone repository
git clone https://github.com/ruikangliu/Quantized-Reasoning-Models.git
cd Quantized-Reasoning-Models

# 2. Set up conda environment
conda create -n quantized-reasoning-models python=3.12 -y
conda activate quantized-reasoning-models

# 3. Install dependencies
pip install -r requirements.txt
pip install -e ./third-party/fast-hadamard-transform
VLLM_USE_PRECOMPILED=1 pip install -e ./third-party/vllm
pip install -e ./third-party/lighteval
pip install -e ./third-party/lighteval[math]
pip uninstall xformers -y && pip install -v -U -e third-party/xformers

# 4. Install monitoring dependencies
pip install psutil pynvml
```

### Step 2: Download Model and Datasets

```bash
# Download model
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B \
    --local-dir ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B

# Download datasets (see main README.md for full list)
# Example for one dataset:
huggingface-cli download openai/gsm8k --local-dir ./datasets/gsm8k
```

### Step 3: Start Resource Monitoring

```bash
# In terminal 1: Start monitoring
python scripts/monitor_resources.py --output logs/resource_monitor.log --interval 1
```

### Step 4: Run Experiments

```bash
# In terminal 2: Run all experiments
bash scripts/run_all_quantization_1.5b.sh 0

# This will take 24-48 hours depending on hardware
```

### Step 5: Analyze Results

```bash
# After experiments complete, stop monitoring (Ctrl+C in terminal 1)

# Generate resource summary
python scripts/monitor_resources.py \
    --analyze logs/resource_monitor.log \
    --report logs/resource_summary.md

# Analyze quantization results
python scripts/analyze_quantization_results.py \
    --model_name DeepSeek-R1-Distill-Qwen-1.5B \
    --save_report --plot

# Extract metrics to documentation templates
python scripts/extract_metrics_to_docs.py \
    --model DeepSeek-R1-Distill-Qwen-1.5B \
    --output-dir filled_docs
```

### Step 6: Complete Documentation

```bash
# Review auto-generated docs
cat filled_docs/REPLICATION_OUTPUTS_FILLED.md
cat filled_docs/RESOURCE_BENCHMARKING_FILLED.md
cat logs/resource_summary.md
cat outputs/analysis/quantization_analysis.md

# Manually fill in remaining details in:
# - REPLICATION_OUTPUTS.md
# - RESOURCE_BENCHMARKING.md
```

---

## Quick Individual Method Testing

If you want to test a single quantization method:

```bash
# 1. Start monitoring
python scripts/monitor_resources.py --output logs/gptq_monitor.log &
MONITOR_PID=$!

# 2. Run quantization
bash scripts/quantization/gptq.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0

# 3. Run evaluation
bash scripts/inference/inference.sh \
    ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1 0 42

# 4. Stop monitoring
kill $MONITOR_PID

# 5. Analyze
python scripts/monitor_resources.py --analyze logs/gptq_monitor.log
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

# Install monitoring tools
pip install psutil pynvml
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
│   │   ├── quarot/
│   │   ├── smoothquant/
│   │   └── flatquant/
│   ├── inference/          # Evaluation results
│   │   └── [model]/[method]/[benchmark]/seed_[N]/
│   └── analysis/           # Analysis reports
│       ├── quantization_analysis.md
│       └── plots/
├── logs/                   # Resource monitoring logs
│   ├── resource_monitor.log
│   ├── resource_summary.md
│   └── [quantization_method].log
├── filled_docs/            # Filled documentation
│   ├── REPLICATION_OUTPUTS_FILLED.md
│   └── RESOURCE_BENCHMARKING_FILLED.md
└── datasets/               # Evaluation datasets (~10-15GB)
    ├── AIME90/
    ├── aime_2025/
    ├── MATH-500/
    ├── gsm8k/
    ├── gpqa/
    └── ...
```

---

## Expected Timeline

| Phase | Time | Notes |
|-------|------|-------|
| Setup | 1-2 hours | Environment, model, datasets |
| Calibration Data Gen | 30-60 min | For GPTQ |
| Quantization (all methods) | 4-8 hours | Depends on hardware |
| Evaluation (baseline) | 2-3 hours | 6 benchmarks, 3 seeds |
| Evaluation (quantized) | 20-30 hours | 13 methods × 6 benchmarks × 3 seeds |
| Analysis | 30 min | Automated |
| **Total** | **24-48 hours** | Plus documentation time |

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
- **Replication Guide**: See [REPLICATION_GUIDE_1.5B.md](../REPLICATION_GUIDE_1.5B.md)
- **Output Templates**: See [REPLICATION_OUTPUTS.md](../REPLICATION_OUTPUTS.md)
- **Resource Templates**: See [RESOURCE_BENCHMARKING.md](../RESOURCE_BENCHMARKING.md)
- **Implementation Summary**: See [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)

---

## Support

For issues or questions:
1. Check the main [README.md](../README.md)
2. Review [REPLICATION_GUIDE_1.5B.md](../REPLICATION_GUIDE_1.5B.md)
3. Open an issue on GitHub

---

*Last Updated: 2025-10-12*
