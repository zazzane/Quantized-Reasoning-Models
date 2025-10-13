# Quantization Analysis Report: DeepSeek-R1-Distill-Qwen-1.5B

Generated: Mon Oct 13 04:34:45 AM +08 2025


## Overview

This report summarizes the impact of different quantization approaches on the DeepSeek-R1-Distill-Qwen-1.5B model across various reasoning benchmarks.

### Quantization Categories

1. **Weight-Only Quantization**: AWQ, GPTQ (3-bit, 4-bit)
2. **KV-Cache Quantization**: KVQuant*, QuaRot-KV (3-bit, 4-bit)
3. **Weight-Activation Quantization**: SmoothQuant, QuaRot, FlatQuant (4-bit, 8-bit)

## Accuracy Results

| Method | AIME-90 | AIME-2025 | MATH-500 | GSM8K | GPQA-Diamond | LiveCodeBench | Avg |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BF16 | - | - | - | - | - | - | - |
| AWQ-W4 | - | - | - | - | - | - | - |
| AWQ-W3 | - | - | - | - | - | - | - |
| GPTQ-W4 | - | - | - | - | - | - | - |
| GPTQ-W3 | - | - | - | - | - | - | - |
| KVQuant*-KV4 | - | - | - | - | - | - | - |
| KVQuant*-KV3 | - | - | - | - | - | - | - |
| QuaRot-KV4 | - | - | - | - | - | - | - |
| QuaRot-KV3 | - | - | - | - | - | - | - |
| SmoothQuant-W8A8KV8 | - | - | - | - | - | - | - |
| QuaRot-W8A8KV8 | - | - | - | - | - | - | - |
| QuaRot-W4A4KV4 | - | - | - | - | - | - | - |
| FlatQuant-W8A8KV8 | - | - | - | - | - | - | - |
| FlatQuant-W4A4KV4 | - | - | - | - | - | - | - |

## Relative Degradation vs Baseline

| Method | AIME-90 | AIME-2025 | MATH-500 | GSM8K | GPQA-Diamond | LiveCodeBench | Avg |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| AWQ-W4 | - | - | - | - | - | - | - |
| AWQ-W3 | - | - | - | - | - | - | - |
| GPTQ-W4 | - | - | - | - | - | - | - |
| GPTQ-W3 | - | - | - | - | - | - | - |
| KVQuant*-KV4 | - | - | - | - | - | - | - |
| KVQuant*-KV3 | - | - | - | - | - | - | - |
| QuaRot-KV4 | - | - | - | - | - | - | - |
| QuaRot-KV3 | - | - | - | - | - | - | - |
| SmoothQuant-W8A8KV8 | - | - | - | - | - | - | - |
| QuaRot-W8A8KV8 | - | - | - | - | - | - | - |
| QuaRot-W4A4KV4 | - | - | - | - | - | - | - |
| FlatQuant-W8A8KV8 | - | - | - | - | - | - | - |
| FlatQuant-W4A4KV4 | - | - | - | - | - | - | - |

## Key Findings


## Recommendations

Based on the analysis:

1. **For minimal accuracy loss**: Use weight-only quantization (AWQ/GPTQ 4-bit)
2. **For memory efficiency**: Consider KV-cache quantization
3. **For maximum compression**: Weight-activation quantization, but expect significant degradation
4. **For production use**: 4-bit weight-only quantization offers best accuracy-efficiency trade-off

## Future Work

To explore 2-bit and 1-bit quantization:

1. Implement mixed-precision strategies (keep critical layers at higher precision)
2. Use smaller group sizes for extreme quantization
3. Consider task-specific fine-tuning after quantization
4. Investigate ternary quantization as stepping stone to binary
5. Analyze per-layer sensitivity to guide mixed-precision decisions
