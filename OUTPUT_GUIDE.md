## 📁 Output Directory Structure

The replication test outputs will be saved in the following locations:

### 1. **Quantized Models** 
```
outputs/modelzoo/
├── awq/                    # AWQ quantized models
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-awq-w3g128-tp1
│   └── DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1
├── gptq/                   # GPTQ quantized models
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-gptq-w3g128-tp1
│   └── DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1
├── kvquant_star/           # KVQuant* models
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv3-tp1
│   └── DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv4-tp1
├── quarot/                 # QuaRot models
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv3-tp1
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv4-tp1
│   ├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-w4a4kv4-tp1
│   └── DeepSeek-R1-Distill-Qwen-1.5B-quarot-w8a8kv8-tp1
├── smoothquant/            # SmoothQuant models
│   └── DeepSeek-R1-Distill-Qwen-1.5B-smoothquant-w8a8kv8-tp1
└── flatquant/              # FlatQuant models
    ├── DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w4a4kv4-tp1
    └── DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w8a8kv8-tp1
```

### 2. **Evaluation Results**
```
outputs/inference/
├── DeepSeek-R1-Distill-Qwen-1.5B-seed42/           # Baseline results
│   ├── AIME-90.jsonl
│   ├── AIME-2025.jsonl
│   ├── MATH-500.jsonl
│   ├── GSM8K.jsonl
│   ├── GPQA-Diamond.jsonl
│   └── LiveCodeBench.jsonl
├── DeepSeek-R1-Distill-Qwen-1.5B-seed43/           # Baseline results
├── DeepSeek-R1-Distill-Qwen-1.5B-seed44/           # Baseline results
├── DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1-seed42/  # AWQ 4-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1-seed43/
├── DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1-seed44/
├── DeepSeek-R1-Distill-Qwen-1.5B-awq-w3g128-tp1-seed42/  # AWQ 3-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1-seed42/ # GPTQ 4-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-gptq-w3g128-tp1-seed42/ # GPTQ 3-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv4-tp1-seed42/ # KVQuant* 4-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv3-tp1-seed42/ # KVQuant* 3-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv4-tp1-seed42/      # QuaRot-KV 4-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv3-tp1-seed42/      # QuaRot-KV 3-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-smoothquant-w8a8kv8-tp1-seed42/ # SmoothQuant results
├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-w8a8kv8-tp1-seed42/      # QuaRot 8-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-quarot-w4a4kv4-tp1-seed42/      # QuaRot 4-bit results
├── DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w8a8kv8-tp1-seed42/   # FlatQuant 8-bit results
└── DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w4a4kv4-tp1-seed42/   # FlatQuant 4-bit results
```

### 3. **Execution Logs**
```
logs/
├── gen_calib_task1.log                    # Calibration data generation
├── awq_task1.log                         # AWQ quantization logs
├── gptq_task1.log                        # GPTQ quantization logs
├── kvquant_star_task1.log                # KVQuant* quantization logs
├── quarot_kv_task1.log                   # QuaRot-KV quantization logs
├── inference_awq_w4_seed42.log           # AWQ 4-bit evaluation logs
├── inference_awq_w3_seed42.log           # AWQ 3-bit evaluation logs
├── inference_gptq_w4_seed42.log          # GPTQ 4-bit evaluation logs
├── inference_gptq_w3_seed42.log          # GPTQ 3-bit evaluation logs
├── inference_kvquant_star_kv4_seed42.log # KVQuant* 4-bit evaluation logs
├── inference_kvquant_star_kv3_seed42.log # KVQuant* 3-bit evaluation logs
├── inference_quarot_kv4_seed42.log       # QuaRot-KV 4-bit evaluation logs
├── inference_quarot_kv3_seed42.log       # QuaRot-KV 3-bit evaluation logs
├── analysis_task1.log                    # Task 1 results analysis
├── smoothquant_task2.log                 # SmoothQuant quantization logs
├── quarot_task2.log                      # QuaRot quantization logs
├── flatquant_task2.log                   # FlatQuant quantization logs
├── inference_baseline_seed42.log         # Baseline evaluation logs
├── inference_smoothquant_w8a8kv8_seed42.log # SmoothQuant evaluation logs
├── inference_quarot_w8a8kv8_seed42.log   # QuaRot 8-bit evaluation logs
├── inference_quarot_w4a4kv4_seed42.log   # QuaRot 4-bit evaluation logs
├── inference_flatquant_w8a8kv8_seed42.log # FlatQuant 8-bit evaluation logs
├── inference_flatquant_w4a4kv4_seed42.log # FlatQuant 4-bit evaluation logs
├── analysis_task2.log                    # Task 2 results analysis
└── analysis_combined.log                 # Combined results analysis
```

### 4. **Analysis Reports** (Generated after completion)
```
# In the main directory:
task1_quantization_results.md             # Task 1 detailed results
task2_quantization_results.md             # Task 2 detailed results
combined_quantization_results.md          # Combined analysis report
combined_quantization_comparison.png      # Performance comparison chart
```

## 🔍 How to Access Results

### During Execution:
```bash
# Monitor progress
tail -f logs/awq_task1.log
tail -f logs/inference_awq_w4_seed42.log

# Check SLURM job output
tail -f slurm-{job_id}.out
```

### After Completion:
```bash
# View quantized models
ls -la outputs/modelzoo/awq/
ls -la outputs/modelzoo/gptq/

# Check evaluation results
ls -la outputs/inference/
head outputs/inference/DeepSeek-R1-Distill-Qwen-1.5B-seed42/AIME-90.jsonl

# View analysis reports
cat task1_quantization_results.md
cat combined_quantization_results.md
```

### Key Result Files:
- **JSONL files**: Individual benchmark results with model responses
- **Analysis reports**: Formatted tables with accuracy, degradation percentages
- **Comparison charts**: Visual performance comparisons
- **Logs**: Detailed execution logs for debugging

The `REPLICATION_OUTPUTS.md` file you have open is a template that will be populated with the actual results once the experiments complete!