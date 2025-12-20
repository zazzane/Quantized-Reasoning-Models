# Replication Outputs: DeepSeek-R1-Distill-Qwen-1.5B Quantization Study

This document records the detailed outputs from replicating the quantization experiments on the DeepSeek-R1-Distill-Qwen-1.5B model.

## Table of Contents
- [Experiment Overview](#experiment-overview)
- [Baseline Results (BF16)](#baseline-results-bf16)
- [Weight-Only Quantization](#weight-only-quantization)
- [KV-Cache Quantization](#kv-cache-quantization)
- [Weight-Activation Quantization](#weight-activation-quantization)
- [Summary and Analysis](#summary-and-analysis)
- [Model Size Comparison](#model-size-comparison)

---

## Experiment Overview

### Model Information
- **Model Name**: DeepSeek-R1-Distill-Qwen-1.5B
- **Model Architecture**: Qwen2-based transformer
- **Parameter Count**: 1.5 Billion
- **Base Precision**: BF16 (Brain Floating Point 16-bit)
- **Context Length**: 32,768 tokens

### Evaluation Benchmarks
The model is evaluated on six reasoning benchmarks:

1. **AIME-90**: Historical AIME problems (90 questions)
2. **AIME-2025**: AIME 2025 edition (30 questions)
3. **MATH-500**: Competition-level mathematics problems (500 questions)
4. **GSM8K**: Grade School Math 8K (test set: 1,319 questions)
5. **GPQA-Diamond**: Graduate-level science questions (198 questions)
6. **LiveCodeBench**: Recent coding challenges

### Quantization Methods Tested
This study evaluates 13 quantization configurations across three categories:

#### Weight-Only Quantization (4 configs)
- AWQ W3A16KV16 (3-bit weights)
- AWQ W4A16KV16 (4-bit weights)
- GPTQ W3A16KV16 (3-bit weights)
- GPTQ W4A16KV16 (4-bit weights)

#### KV-Cache Quantization (4 configs)
- KVQuant* W16A16KV3 (3-bit KV cache)
- KVQuant* W16A16KV4 (4-bit KV cache)
- QuaRot-KV W16A16KV3 (3-bit KV cache)
- QuaRot-KV W16A16KV4 (4-bit KV cache)

#### Weight-Activation Quantization (5 configs)
- SmoothQuant W8A8KV8 (8-bit weights, activations, KV cache)
- QuaRot W4A4KV4 (4-bit all components)
- QuaRot W8A8KV8 (8-bit all components)
- FlatQuant W4A4KV4 (4-bit all components)
- FlatQuant W8A8KV8 (8-bit all components)

---

## Baseline Results (BF16)

### Accuracy Results

*Record the baseline accuracy without any quantization. This serves as the reference for measuring degradation.*

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev |
|-----------|---------|---------|---------|------|---------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ |

### Model Size
- **Parameters**: 1.5B
- **Storage Size**: ~3.0 GB (BF16)
- **Memory Footprint (Inference)**: ~4-6 GB VRAM

### Response Statistics

| Benchmark | Avg Tokens/Response | Avg Reasoning Steps |
|-----------|---------------------|---------------------|
| AIME-90 | _____ | _____ |
| AIME-2025 | _____ | _____ |
| AIME-90 | _____ | _____ |
| MATH-500 | _____ | _____ |
| GSM8K | _____ | _____ |
| GPQA-Diamond | _____ | _____ |

---

## Weight-Only Quantization

Weight-only quantization reduces the precision of model weights while keeping activations and KV cache at full precision.

### AWQ (Activation-aware Weight Quantization)

#### AWQ W4A16KV16 (4-bit weights)

**Quantization Details:**
- **Method**: AWQ
- **Weight Bits**: 4
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 16 (BF16)
- **Group Size**: 128
- **Quantization Scheme**: Per-group asymmetric

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~0.9 GB (4-bit weights)
- Compression Ratio: ~3.3x
- Memory Footprint: ~2-3 GB VRAM

**Key Observations:**
- *Add observations about performance degradation patterns*
- *Note any benchmark-specific behaviors*
- *Comment on quality of reasoning outputs*

#### AWQ W3A16KV16 (3-bit weights)

**Quantization Details:**
- **Method**: AWQ
- **Weight Bits**: 3
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 16 (BF16)
- **Group Size**: 128
- **Quantization Scheme**: Per-group asymmetric

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~0.7 GB (3-bit weights)
- Compression Ratio: ~4.3x
- Memory Footprint: ~2-3 GB VRAM

**Key Observations:**
- *Compare degradation with 4-bit version*
- *Identify if there are catastrophic failures on specific benchmarks*

---

### GPTQ (Generative Pre-trained Transformer Quantization)

#### GPTQ W4A16KV16 (4-bit weights)

**Quantization Details:**
- **Method**: GPTQ
- **Weight Bits**: 4
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 16 (BF16)
- **Group Size**: 128
- **Act Order**: Enabled
- **Calibration Data**: NuminaMath-1.5 (reasoning-focused)

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~0.9 GB (4-bit weights)
- Compression Ratio: ~3.3x
- Memory Footprint: ~2-3 GB VRAM

**Key Observations:**
- *Compare with AWQ W4 results*
- *Note impact of reasoning-focused calibration data*

#### GPTQ W3A16KV16 (3-bit weights)

**Quantization Details:**
- **Method**: GPTQ
- **Weight Bits**: 3
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 16 (BF16)
- **Group Size**: 128
- **Act Order**: Enabled
- **Calibration Data**: NuminaMath-1.5 (reasoning-focused)

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~0.7 GB (3-bit weights)
- Compression Ratio: ~4.3x
- Memory Footprint: ~2-3 GB VRAM

**Key Observations:**
- *Compare with AWQ W3 results*
- *Assess quality vs quantity tradeoff at extreme compression*

---

## KV-Cache Quantization

KV-cache quantization reduces the memory footprint of the key-value cache during inference while keeping weights and activations at full precision.

### KVQuant* 

#### KVQuant* W16A16KV4 (4-bit KV cache)

**Quantization Details:**
- **Method**: KVQuant*
- **Weight Bits**: 16 (BF16)
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 4
- **KV Group Size**: 128
- **KV Quantization**: Per-channel asymmetric

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Memory Impact:**
- KV Cache Memory (per token): ~4x reduction
- Long sequence (32K tokens) benefit: ~75% memory savings

**Key Observations:**
- *Note impact on long reasoning chains*
- *Comment on generation quality*

#### KVQuant* W16A16KV3 (3-bit KV cache)

**Quantization Details:**
- **Method**: KVQuant*
- **Weight Bits**: 16 (BF16)
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 3
- **KV Group Size**: 128
- **KV Quantization**: Per-channel asymmetric

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Memory Impact:**
- KV Cache Memory (per token): ~5.3x reduction
- Long sequence (32K tokens) benefit: ~81% memory savings

**Key Observations:**
- *Compare degradation with KV4*
- *Assess if extreme KV compression breaks reasoning*

---

### QuaRot-KV

#### QuaRot-KV W16A16KV4 (4-bit KV cache)

**Quantization Details:**
- **Method**: QuaRot-KV (Rotation-based quantization)
- **Weight Bits**: 16 (BF16)
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 4
- **KV Group Size**: 128
- **Clip Ratio**: 0.95

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Key Observations:**
- *Compare with KVQuant* KV4*
- *Note impact of rotation-based approach*

#### QuaRot-KV W16A16KV3 (3-bit KV cache)

**Quantization Details:**
- **Method**: QuaRot-KV (Rotation-based quantization)
- **Weight Bits**: 16 (BF16)
- **Activation Bits**: 16 (BF16)
- **KV Cache Bits**: 3
- **KV Group Size**: 128
- **Clip Ratio**: 0.95

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Key Observations:**
- *Compare with KVQuant* KV3*
- *Assess rotation effectiveness at extreme compression*

---

## Weight-Activation Quantization

Weight-activation quantization reduces precision of weights, activations, AND KV cache simultaneously.

### SmoothQuant

#### SmoothQuant W8A8KV8 (8-bit all components)

**Quantization Details:**
- **Method**: SmoothQuant
- **Weight Bits**: 8
- **Activation Bits**: 8
- **KV Cache Bits**: 8
- **Smoothing Factor**: Alpha parameter tuned
- **Per-token Dynamic Quantization**: Enabled

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~1.5 GB (8-bit)
- Compression Ratio: ~2x
- Memory Footprint: ~3-4 GB VRAM

**Key Observations:**
- *Note impact of quantizing activations on reasoning*
- *Compare with weight-only and KV-only methods*

---

### QuaRot

#### QuaRot W8A8KV8 (8-bit all components)

**Quantization Details:**
- **Method**: QuaRot (Hadamard rotation)
- **Weight Bits**: 8
- **Activation Bits**: 8
- **KV Cache Bits**: 8
- **Online Rotation**: Enabled
- **Group Size**: 128

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~1.5 GB (8-bit)
- Compression Ratio: ~2x
- Memory Footprint: ~3-4 GB VRAM

**Key Observations:**
- *Compare with SmoothQuant W8A8KV8*
- *Note effectiveness of rotation approach*

#### QuaRot W4A4KV4 (4-bit all components)

**Quantization Details:**
- **Method**: QuaRot (Hadamard rotation)
- **Weight Bits**: 4
- **Activation Bits**: 4
- **KV Cache Bits**: 4
- **Online Rotation**: Enabled
- **Group Size**: 128

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~0.9 GB (4-bit)
- Compression Ratio: ~3.3x
- Memory Footprint: ~2-3 GB VRAM

**Key Observations:**
- *Assess viability of 4-bit full quantization for reasoning*
- *Compare with weight-only W4 methods*

---

### FlatQuant

#### FlatQuant W8A8KV8 (8-bit all components)

**Quantization Details:**
- **Method**: FlatQuant (Flattening outliers)
- **Weight Bits**: 8
- **Activation Bits**: 8
- **KV Cache Bits**: 8
- **Outlier Flattening**: Enabled
- **Group Size**: 128

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~1.5 GB (8-bit)
- Compression Ratio: ~2x
- Memory Footprint: ~3-4 GB VRAM

**Key Observations:**
- *Compare with QuaRot and SmoothQuant W8A8KV8*
- *Note effectiveness of outlier flattening for reasoning*

#### FlatQuant W4A4KV4 (4-bit all components)

**Quantization Details:**
- **Method**: FlatQuant (Flattening outliers)
- **Weight Bits**: 4
- **Activation Bits**: 4
- **KV Cache Bits**: 4
- **Outlier Flattening**: Enabled
- **Group Size**: 128

**Accuracy Results:**

| Benchmark | Seed 42 | Seed 43 | Seed 44 | Mean | Std Dev | Baseline | Degradation |
|-----------|---------|---------|---------|------|---------|----------|-------------|
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-2025 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| AIME-90 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| MATH-500 | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GSM8K | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |
| GPQA-Diamond | __%__ | __%__ | __%__ | __%__ | ±__%__ | __%__ | __% |

**Model Size:**
- Storage: ~0.9 GB (4-bit)
- Compression Ratio: ~3.3x
- Memory Footprint: ~2-3 GB VRAM

**Key Observations:**
- *Compare with QuaRot W4A4KV4*
- *Assess if FlatQuant handles 4-bit better than QuaRot*

---

## Summary and Analysis

### Overall Accuracy Comparison

*Create a comprehensive table comparing all methods across all benchmarks*

| Method | AIME-24 | AIME-25 | AIME-90 | MATH-500 | GSM8K | GPQA | Avg |
|--------|---------|---------|---------|----------|-------|------|-----|
| **Baseline (BF16)** | __% | __% | __% | __% | __% | __% | __% |
| AWQ W4 | __% | __% | __% | __% | __% | __% | __% |
| AWQ W3 | __% | __% | __% | __% | __% | __% | __% |
| GPTQ W4 | __% | __% | __% | __% | __% | __% | __% |
| GPTQ W3 | __% | __% | __% | __% | __% | __% | __% |
| KVQuant* KV4 | __% | __% | __% | __% | __% | __% | __% |
| KVQuant* KV3 | __% | __% | __% | __% | __% | __% | __% |
| QuaRot-KV KV4 | __% | __% | __% | __% | __% | __% | __% |
| QuaRot-KV KV3 | __% | __% | __% | __% | __% | __% | __% |
| SmoothQuant W8 | __% | __% | __% | __% | __% | __% | __% |
| QuaRot W8 | __% | __% | __% | __% | __% | __% | __% |
| QuaRot W4 | __% | __% | __% | __% | __% | __% | __% |
| FlatQuant W8 | __% | __% | __% | __% | __% | __% | __% |
| FlatQuant W4 | __% | __% | __% | __% | __% | __% | __% |

### Degradation Analysis

*Relative degradation from baseline*

| Category | Method | Avg Degradation | Best Case | Worst Case |
|----------|--------|-----------------|-----------|------------|
| **Weight-Only** | AWQ W4 | __% | __% (benchmark) | __% (benchmark) |
| | AWQ W3 | __% | __% | __% |
| | GPTQ W4 | __% | __% | __% |
| | GPTQ W3 | __% | __% | __% |
| **KV-Cache** | KVQuant* KV4 | __% | __% | __% |
| | KVQuant* KV3 | __% | __% | __% |
| | QuaRot-KV KV4 | __% | __% | __% |
| | QuaRot-KV KV3 | __% | __% | __% |
| **Weight-Act** | SmoothQuant W8 | __% | __% | __% |
| | QuaRot W8 | __% | __% | __% |
| | QuaRot W4 | __% | __% | __% |
| | FlatQuant W8 | __% | __% | __% |
| | FlatQuant W4 | __% | __% | __% |

### Key Findings

#### Best Methods by Category

1. **Weight-Only Quantization**:
   - Best 4-bit method: _______ (___% avg degradation)
   - Best 3-bit method: _______ (___% avg degradation)
   - Recommendation: *Fill in recommendation*

2. **KV-Cache Quantization**:
   - Best 4-bit method: _______ (___% avg degradation)
   - Best 3-bit method: _______ (___% avg degradation)
   - Recommendation: *Fill in recommendation*

3. **Weight-Activation Quantization**:
   - Best 8-bit method: _______ (___% avg degradation)
   - Best 4-bit method: _______ (___% avg degradation)
   - Recommendation: *Fill in recommendation*

#### Benchmark Sensitivity

*Which benchmarks are most sensitive to quantization?*

1. **Most Sensitive**: _______ (avg degradation: __%)
2. **Moderately Sensitive**: _______ (avg degradation: __%)
3. **Least Sensitive**: _______ (avg degradation: __%)

#### Task-Specific Observations

- **Mathematical Reasoning (AIME, MATH-500)**: *Add observations*
- **Grade-School Math (GSM8K)**: *Add observations*
- **Science Reasoning (GPQA)**: *Add observations*

---

## Model Size Comparison

### Storage Requirements

| Method | Disk Size | Compression Ratio | % Reduction |
|--------|-----------|-------------------|-------------|
| Baseline (BF16) | 3.0 GB | 1.0x | 0% |
| AWQ W4 | 0.9 GB | 3.3x | 70% |
| AWQ W3 | 0.7 GB | 4.3x | 77% |
| GPTQ W4 | 0.9 GB | 3.3x | 70% |
| GPTQ W3 | 0.7 GB | 4.3x | 77% |
| KVQuant* (storage same as baseline) | 3.0 GB | 1.0x | 0% |
| QuaRot-KV (storage same as baseline) | 3.0 GB | 1.0x | 0% |
| SmoothQuant W8 | 1.5 GB | 2.0x | 50% |
| QuaRot W8 | 1.5 GB | 2.0x | 50% |
| QuaRot W4 | 0.9 GB | 3.3x | 70% |
| FlatQuant W8 | 1.5 GB | 2.0x | 50% |
| FlatQuant W4 | 0.9 GB | 3.3x | 70% |

### Inference Memory Footprint

*VRAM requirements for inference (approximate, depends on batch size and sequence length)*

| Method | Min VRAM | Recommended VRAM | Max Batch Size (16GB GPU) |
|--------|----------|------------------|---------------------------|
| Baseline (BF16) | 4 GB | 6 GB | __ |
| Weight-Only W4 | 2 GB | 3 GB | __ |
| Weight-Only W3 | 2 GB | 3 GB | __ |
| KV-Cache KV4 | 3 GB | 5 GB | __ |
| KV-Cache KV3 | 3 GB | 4 GB | __ |
| Weight-Act W8 | 3 GB | 4 GB | __ |
| Weight-Act W4 | 2 GB | 3 GB | __ |

### Trade-off Analysis

*Accuracy vs. Efficiency*

| Method | Accuracy Retention | Model Size | Inference Speed | Overall Score |
|--------|-------------------|------------|-----------------|---------------|
| Baseline | 100% | Low (1x) | Baseline | Reference |
| Best W4 Method | __% | High (3.3x) | __ | __ |
| Best W3 Method | __% | Highest (4.3x) | __ | __ |
| Best KV4 Method | __% | Low (1x) | __ | __ |
| Best W8A8 Method | __% | Medium (2x) | __ | __ |
| Best W4A4 Method | __% | High (3.3x) | __ | __ |

---

## Recommendations

### For Different Use Cases

#### Production Deployment (Accuracy Priority)
- **Recommended Method**: _______
- **Reasoning**: *Explain why this method balances accuracy and efficiency*
- **Expected Performance**: ___% of baseline accuracy
- **Resource Savings**: ___% storage reduction

#### Edge Deployment (Size Priority)
- **Recommended Method**: _______
- **Reasoning**: *Explain the size vs. accuracy tradeoff*
- **Expected Performance**: ___% of baseline accuracy
- **Resource Savings**: ___% storage reduction

#### High-Throughput Serving (Memory Priority)
- **Recommended Method**: _______
- **Reasoning**: *Explain memory efficiency benefits*
- **Expected Performance**: ___% of baseline accuracy
- **Memory Savings**: ___% VRAM reduction

### Future Work

Based on these results, the following research directions are promising:

1. **Ultra-Low Bit Quantization**: *Can we push to 2-bit while maintaining >80% accuracy?*
2. **Mixed-Precision Strategies**: *Combining different methods for different components*
3. **Task-Specific Quantization**: *Optimizing for specific reasoning task types*
4. **Dynamic Quantization**: *Adapting bit-width based on input complexity*

---

## Conclusion

*Summary of the replication study*

This replication successfully evaluated 13 quantization configurations on the DeepSeek-R1-Distill-Qwen-1.5B model across 6 reasoning benchmarks. The results demonstrate that:

1. *Key finding 1*
2. *Key finding 2*
3. *Key finding 3*

**Overall Recommendation**: *Provide a balanced recommendation based on the data*

---

## Appendix

### Experiment Configuration

- **Hardware**: See RESOURCE_BENCHMARKING.md
- **Software Versions**:
  - PyTorch: 2.5.1
  - Transformers: 4.47.1
  - CUDA: [version]
  - Python: 3.12

### Reproduction Commands

All experiments can be reproduced using:

```bash
# Example: GPTQ quantization
bash scripts/quantization/gptq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0
bash scripts/inference/inference.sh ./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1 0 42
```

### Data Files

- Raw evaluation results: `outputs/inference/`
- Quantized model checkpoints: `outputs/modelzoo/`
- Analysis tool: `python -m make_stats_table`

---

*Document Date*: ___________  
*Completed By*: ___________  
*Review Status*: ___________
