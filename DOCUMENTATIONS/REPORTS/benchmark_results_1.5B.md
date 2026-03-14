# Benchmark Results Summary: DeepSeek-R1-Distill-Qwen-1.5B

**Generated**: 2026-02-06  
**Model**: DeepSeek-R1-Distill-Qwen-1.5B  
**Seeds**: 42, 43, 44 (3 runs per configuration)

---

## 1. Valid Result Files Found

**Location**: `outputs/inference/`

| Config | Method | Seeds | Files per Seed | Status |
|:-------|:-------|:------|:---------------|:-------|
| BF16 | Baseline | 42, 43, 44 | 5 | Complete |
| W4A16 | AWQ | 42, 43, 44 | 5 | Complete |
| W3A16 | AWQ | 42, 43, 44 | 5 | Complete |
| W4A16 | GPTQ | 42, 43, 44 | 5 | Complete |
| W3A16 | GPTQ | 42, 43, 44 | 5 | Complete |
| KV4 | KVQuant | 42, 43, 44 | 5 | Complete |
| KV3 | KVQuant | 42, 43, 44 | 5 | Complete |
| KV4 | QuaRot | 42, 43, 44 | 5 | Complete |
| KV3 | QuaRot | 42, 43 | 4-5 | Partial Data |
| W8A8KV8 | SmoothQuant | 42, 43, 44 | 5 | Complete |
| W8A8KV8 | QuaRot | 42, 43, 44 | 5 | Complete |
| W4A4KV4 | QuaRot | 42, 43, 44 | 5 | Complete |
| W8A8KV8 | FlatQuant | 42, 43, 44 | 5 | Complete |
| W4A4KV4 | FlatQuant | 42, 43, 44 | 5 | Complete |

**Total**: 14 configurations x 3 seeds = 42 experiment runs (41 with data)

---

## 2. Benchmark Results Summary Table

**Notes**: 
- GPQA-Diamond benchmark results are NOT AVAILABLE (0 files found across all experiments)
- Baseline uses BF16 (bfloat16); GPTQ models use FP16 due to gptqmodel framework requirements

| Model Config | Method | AIME-120 | MATH-500 | GSM8K | GPQA-Diamond | LiveCodeBench | Avg. |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| BF16 | Baseline | 24.44+/-1.27 | 85.27+/-0.81 | 84.76+/-0.95 | N/A | 17.29+/-1.14 | 52.94 |
| W4A16 | AWQ | 21.39+/-1.27 | 81.87+/-0.90 | 82.11+/-0.87 | N/A | 12.94+/-0.43 | 49.57 |
| W3A16 | AWQ | 5.28+/-1.27 | 43.87+/-1.33 | 63.13+/-0.99 | N/A | 3.36+/-0.75 | 28.91 |
| W4A16 | GPTQ | 18.06+/-2.10 | 82.87+/-0.31 | 83.09+/-0.13 | N/A | 12.56+/-0.57 | 49.14 |
| W3A16 | GPTQ | 8.89+/-3.76 | 70.60+/-1.80 | 75.54+/-0.32 | N/A | 7.46+/-1.63 | 40.62 |
| KV4 | KVQuant | 23.06+/-3.85 | 83.40+/-1.06 | 83.60+/-0.39 | N/A | 15.05+/-0.57 | 51.28 |
| KV3 | KVQuant | 6.11+/-0.96 | 63.87+/-0.90 | 69.02+/-0.89 | N/A | 8.46+/-1.51 | 36.86 |
| KV4 | QuaRot | 0.00+/-0.00 | 1.33+/-0.31 | 0.94+/-0.24 | N/A | 0.00+/-0.00 | 0.57 |
| KV3 (partial) | QuaRot | 0.00+/-0.00 | 1.40+/-1.13 | 0.99+/-0.00 | N/A | 0.00+/-0.00 | 0.60 |
| W8A8KV8 | SmoothQuant | 12.22+/-3.47 | 72.27+/-1.75 | 80.52+/-0.84 | N/A | 14.05+/-0.86 | 44.76 |
| W8A8KV8 | QuaRot | 0.00+/-0.00 | 1.53+/-0.50 | 1.11+/-0.18 | N/A | 0.00+/-0.00 | 0.66 |
| W4A4KV4 | QuaRot | 0.00+/-0.00 | 1.60+/-0.20 | 0.73+/-0.22 | N/A | 0.00+/-0.00 | 0.58 |
| W8A8KV8 | FlatQuant | 25.28+/-3.76 | 84.87+/-0.95 | 84.56+/-0.54 | N/A | 16.67+/-1.72 | 52.84 |
| W4A4KV4 | FlatQuant | 6.11+/-0.96 | 59.67+/-0.99 | 69.35+/-3.85 | N/A | 6.22+/-0.57 | 35.34 |

(partial) = Partial Data: fewer than 3 seeds available

---

## 3. Key Observations

### Top Performing Methods (by Avg. Accuracy)

1. BF16 Baseline: 52.94% (reference)
2. W8A8KV8 FlatQuant: 52.84% (-0.10% vs baseline)
3. KV4 KVQuant: 51.28% (-1.66% vs baseline)
4. W4A16 AWQ: 49.57% (-3.37% vs baseline)
5. W4A16 GPTQ: 49.14% (-3.80% vs baseline)

### Quantization Impact Analysis

| Category | Best Method | Accuracy Drop vs BF16 |
|:---------|:------------|:---------------------|
| Weight-Only 4-bit | AWQ W4A16 | -3.37% |
| Weight-Only 3-bit | GPTQ W3A16 | -12.32% |
| KV-Cache 4-bit | KVQuant KV4 | -1.66% |
| KV-Cache 3-bit | KVQuant KV3 | -16.08% |
| Full W8A8 | FlatQuant W8A8KV8 | -0.10% |
| Full W4A4 | FlatQuant W4A4KV4 | -17.60% |

### Critical Findings

1. QuaRot consistently fails on this model with near-zero accuracy across all configurations (KV-only and full quantization). This suggests incompatibility with the Qwen architecture or implementation issues.

2. FlatQuant W8A8KV8 preserves accuracy nearly perfectly (-0.10%) while enabling 8-bit quantization.

3. 3-bit quantization causes significant accuracy degradation (>10%) regardless of method.

4. KV-cache quantization has less impact than weight quantization at the same bit-width.

---

## 4. Data Gaps

### Missing Benchmarks
- GPQA-Diamond: 0 files found (not evaluated)

### Incomplete Configurations
- KV3 QuaRot: seed44 completely missing, seed43 missing LiveCodeBench

---

## 5. Files Reference

Each experiment directory contains:
- AIME-90.jsonl
- AIME-2025.jsonl
- MATH-500.jsonl
- GSM8K.jsonl
- LiveCodeBench.jsonl

AIME-120 is computed as: 0.75 x AIME-90 + 0.25 x AIME-2025
