# Replication Guide: DeepSeek-R1-Distill-Qwen-1.5B Quantization Study

This guide provides a comprehensive walkthrough to replicate the quantization experiments for the DeepSeek-R1-Distill-Qwen-1.5B model as described in the research paper.

## Overview

The study evaluates the model under three quantization categories:
1. **Weight-Only Quantization**: AWQ, GPTQ
2. **KV-Cache Quantization**: KVQuant*, QuaRot-KV
3. **Weight-Activation Quantization**: SmoothQuant, QuaRot, FlatQuant

Each category is tested at multiple bit-widths: BF16 (baseline), 8-bit, 4-bit, and 3-bit.

## Prerequisites

### 1. Environment Setup

Follow the installation instructions in the main README.md:

```bash
conda create -n quantized-reasoning-models python=3.12 -y
conda activate quantized-reasoning-models
pip install -r requirements.txt
pip install -e ./third-party/fast-hadamard-transform
VLLM_USE_PRECOMPILED=1 pip install -e ./third-party/vllm
pip install -e ./third-party/lighteval
pip install -e ./third-party/lighteval[math]
pip uninstall xformers -y && pip install -v -U -e third-party/xformers
```

### 2. Download the Base Model

Download the DeepSeek-R1-Distill-Qwen-1.5B model:

```bash
# Using huggingface-cli
huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B \
    --local-dir ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B
```

Or manually download from: https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B

### 3. Download Evaluation Datasets

Download all required datasets into the `./datasets` directory:

- **Calibration datasets**: WikiText2, Pile, NuminaMath-1.5
- **Evaluation benchmarks**: AIME-90, AIME-2025, MATH-500, GSM8K, GPQA-Diamond, LiveCodeBench

See the main README.md for specific download URLs.

### 4. Generate Calibration Data

Generate reasoning-based calibration data for GPTQ:

```bash
bash scripts/data/gen_calib.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0
```

## Quantization Experiments

### Baseline (BF16)

First, evaluate the baseline model without quantization:

```bash
# Run inference on all benchmarks with seed 42
bash scripts/inference/inference.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0 42
bash scripts/inference/inference.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0 43
bash scripts/inference/inference.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0 44
```

### Category 1: Weight-Only Quantization

#### AWQ (W3A16KV16 & W4A16KV16)

Quantize with AWQ at 3-bit and 4-bit:

```bash
# TP=1 for 1.5B model (single GPU)
bash scripts/quantization/awq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w3g128-tp1`
- `./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1`

Evaluate quantized models:

```bash
# AWQ W4
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1 0 $seed
done

# AWQ W3
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w3g128-tp1 0 $seed
done
```

#### GPTQ (W3A16KV16 & W4A16KV16)

Quantize with GPTQ at 3-bit and 4-bit:

```bash
# TP=1 for 1.5B model
bash scripts/quantization/gptq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w3g128-tp1`
- `./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1`

Evaluate quantized models:

```bash
# GPTQ W4
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1 0 $seed
done

# GPTQ W3
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w3g128-tp1 0 $seed
done
```

### Category 2: KV-Cache Quantization

#### KVQuant* (W16A16KV3 & W16A16KV4)

Quantize KV cache with KVQuant*:

```bash
bash scripts/quantization/kvquant_star.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv3-tp1`
- `./outputs/modelzoo/kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv4-tp1`

Evaluate:

```bash
# KVQuant* KV4
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv4-tp1 0 $seed
done

# KVQuant* KV3
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv3-tp1 0 $seed
done
```

#### QuaRot-KV (W16A16KV3 & W16A16KV4)

Quantize KV cache with QuaRot-KV:

```bash
bash scripts/quantization/quarot_kv.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv3-tp1`
- `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv4-tp1`

Evaluate:

```bash
# QuaRot-KV KV4
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv4-tp1 0 $seed
done

# QuaRot-KV KV3
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv3-tp1 0 $seed
done
```

### Category 3: Weight-Activation Quantization

#### SmoothQuant (W8A8KV8)

Quantize with SmoothQuant at 8-bit:

```bash
bash scripts/quantization/smoothquant.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/smoothquant/DeepSeek-R1-Distill-Qwen-1.5B-smoothquant-w8a8kv8-tp1`

Evaluate:

```bash
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/smoothquant/DeepSeek-R1-Distill-Qwen-1.5B-smoothquant-w8a8kv8-tp1 0 $seed
done
```

#### QuaRot (W4A4KV4, W8A8KV8)

Quantize with QuaRot at 4-bit and 8-bit:

```bash
bash scripts/quantization/quarot.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w4a4kv4-tp1`
- `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w8a8kv8-tp1`

Evaluate:

```bash
# QuaRot W8A8KV8
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w8a8kv8-tp1 0 $seed
done

# QuaRot W4A4KV4
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w4a4kv4-tp1 0 $seed
done
```

#### FlatQuant (W4A4KV4, W8A8KV8)

Quantize with FlatQuant at 4-bit and 8-bit:

```bash
bash scripts/quantization/flatquant.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
```

This will create:
- `./outputs/modelzoo/flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w4a4kv4-tp1`
- `./outputs/modelzoo/flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w8a8kv8-tp1`

Evaluate:

```bash
# FlatQuant W8A8KV8
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w8a8kv8-tp1 0 $seed
done

# FlatQuant W4A4KV4
for seed in 42 43 44; do
    bash scripts/inference/inference.sh \
        ./outputs/modelzoo/flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w4a4kv4-tp1 0 $seed
done
```

## Results Analysis

After completing all experiments, analyze the results:

```bash
# Generate accuracy table
python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B

# Generate response length analysis
python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B
```

## Summary of Quantization Methods

| Category | Method | Bit-widths | Notation |
|----------|--------|------------|----------|
| Weight-Only | AWQ | 3-bit, 4-bit | W3A16KV16, W4A16KV16 |
| Weight-Only | GPTQ | 3-bit, 4-bit | W3A16KV16, W4A16KV16 |
| KV-Cache | KVQuant* | 3-bit, 4-bit | W16A16KV3, W16A16KV4 |
| KV-Cache | QuaRot-KV | 3-bit, 4-bit | W16A16KV3, W16A16KV4 |
| Weight-Activation | SmoothQuant | 8-bit | W8A8KV8 |
| Weight-Activation | QuaRot | 4-bit, 8-bit | W4A4KV4, W8A8KV8 |
| Weight-Activation | FlatQuant | 4-bit, 8-bit | W4A4KV4, W8A8KV8 |

## Future Exploration: 2-bit and 1-bit Quantization

### Considerations for Ultra-Low Bit Quantization

#### 2-bit Quantization

**Challenges:**
1. Extreme quantization error accumulation
2. Limited representation capacity (only 4 discrete levels)
3. Significant performance degradation expected for reasoning tasks

**Potential Approaches:**
1. **Mixed Precision**: Keep critical layers (e.g., first/last layers, attention layers) at higher precision
2. **Group-wise Quantization**: Use smaller group sizes to reduce quantization error
3. **Learnable Quantization**: Fine-tune quantization parameters on reasoning datasets
4. **Asymmetric Quantization**: Use asymmetric schemes to better capture weight/activation distributions

**Implementation Path:**
- Modify existing GPTQ/AWQ implementations to support 2-bit weights
- Adjust groupsize parameter (e.g., from 128 to 64 or 32)
- Implement mixed-precision strategies

**Example modification for GPTQ 2-bit:**
```bash
# Hypothetical 2-bit GPTQ command (requires code modification)
python -m methods.quarot_gptq.save_fake_quant \
    --model ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B \
    --w_bits 2 --w_clip --w_asym --w_groupsize 64 --act_order \
    --tp 1 \
    --save_qmodel_path ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w2g64-tp1 \
    --cal_dataset reasoning-numina-math-1.5
```

#### 1-bit Quantization (Binary Quantization)

**Challenges:**
1. Only two discrete values (-1, +1 or 0, 1)
2. Extreme loss of information
3. Likely catastrophic performance degradation for complex reasoning

**Potential Approaches:**
1. **BinaryConnect/BinaryNet**: Classic binary neural network techniques
2. **BiLLM**: Recent binary quantization for LLMs
3. **Ternary Quantization**: Use three levels (-1, 0, +1) as intermediate step
4. **Extreme Mixed Precision**: Binary for most weights, higher precision for critical components

**Research Directions:**
1. Investigate which model components are most sensitive to extreme quantization
2. Develop specialized loss functions for reasoning preservation
3. Explore post-training binary optimization techniques
4. Study the impact on different reasoning task types

### Recommended Experimental Pipeline

1. **Establish 3-bit Baseline**: First ensure 3-bit quantization is well-optimized
2. **Progressive Degradation Study**: Test 2.5-bit, 2-bit, 1.5-bit to understand degradation curves
3. **Component-wise Analysis**: Identify which layers/components can tolerate extreme quantization
4. **Task-specific Optimization**: Fine-tune quantization strategies per reasoning task type
5. **Hybrid Approaches**: Combine multiple techniques (e.g., 2-bit weights + 4-bit KV cache)

### Code Modifications Required

To implement 2-bit/1-bit quantization, you would need to modify:

1. `methods/quarot_gptq/save_fake_quant.py`: Add support for bits < 3
2. `methods/awq/run_awq.py`: Extend to 2-bit/1-bit
3. `methods/flatquant/flatquant/quant_utils.py`: Update quantization functions
4. `vllm_custom/model_executor/`: Add 2-bit/1-bit kernels and operators

**Key files to modify:**
- `methods/flatquant/flatquant/quant_utils.py`: Update `get_qmin_qmax()` function
- `methods/quarot_gptq/quant.py`: Add 2-bit/1-bit GPTQ algorithms
- Kernel implementations in vLLM for efficient 2-bit/1-bit inference

## Troubleshooting

### Common Issues

1. **Out of Memory**: Reduce batch size in calibration or use gradient checkpointing
2. **Quantization Fails**: Check calibration data quality and quantity
3. **Poor Results**: Verify model paths and that quantization completed successfully
4. **Inference Errors**: Ensure TP value matches between quantization and inference

### Performance Tips

1. Use reasoning-based calibration data (NuminaMath-1.5) for GPTQ
2. For 1.5B model, TP=1 is sufficient (single GPU)
3. Monitor GPU memory during quantization
4. Use multiple seeds (42, 43, 44) for robust evaluation

## Expected Results

Based on the research paper, you should expect:

- **Baseline (BF16)**: Highest accuracy across all benchmarks
- **Weight-Only (4-bit)**: Minimal degradation (< 5% relative)
- **Weight-Only (3-bit)**: Moderate degradation (5-15% relative)
- **KV-Cache (4-bit)**: Very minimal impact
- **KV-Cache (3-bit)**: Slight degradation
- **Weight-Activation (8-bit)**: Moderate degradation
- **Weight-Activation (4-bit)**: Significant degradation (> 20% relative)

Reasoning tasks (AIME, MATH-500) are generally more sensitive to quantization than simpler tasks (GSM8K).

## References

- Paper: [Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models](https://arxiv.org/abs/2504.04823)
- Model: [DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)
