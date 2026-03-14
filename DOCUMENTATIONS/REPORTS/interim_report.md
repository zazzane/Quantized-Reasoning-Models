# Quantized Reasoning Models - Comprehensive Progress Report

**Report Date:** January 29, 2026  
**Project:** Replication of Quantization Study for DeepSeek-R1-Distill-Qwen-1.5B  
**Reference Paper:** "Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models" (COLM 2025, arXiv:2504.04823)

---

## Table of Contents

1. [Current Progress](#current-progress)
2. [Upcoming Progress](#upcoming-progress)
3. [Research Tradeoffs](#research-tradeoffs)
4. [Referenced Research Papers & Repositories](#referenced-research-papers--repositories)
5. [Troubles Faced & Actions Taken](#troubles-faced--actions-taken)

---

## Current Progress

### Phase Completion Status

| Phase | Description | Status | Completion Date |
|-------|-------------|--------|-----------------|
| **Phase 1** | Environment Teardown & Fresh Virtual Environment Setup | ✅ COMPLETE | 2026-01-24 |
| **Phase 2** | Initialize Git Submodules & Verify Custom Components | ✅ COMPLETE | 2026-01-24 |
| **Phase 3** | Install Generic Dependencies from requirements.txt | ✅ COMPLETE | 2026-01-24 |
| **Phase 4** | Priority Install - Custom Kernels (fast-hadamard-transform) | ✅ COMPLETE | 2026-01-24 |
| **Phase 5** | Priority Install - Custom vLLM with Fake Quantization Support | ✅ COMPLETE | 2026-01-25 |
| **Phase 6** | Install Custom LightEval with Math Extensions | ✅ COMPLETE | 2026-01-25 |
| **Phase 7** | Build and Install Custom xformers from Source | ✅ COMPLETE (skipped source rebuild) | 2026-01-25 |
| **Phase 8** | Download Model and Calibration Datasets | ✅ COMPLETE | 2026-01-25 |
| **Phase 9** | Weight-Only Quantization (AWQ & GPTQ) | ✅ COMPLETE | 2026-01-25 |
| **Phase 10** | KV Cache Quantization (KVQuant* & QuaRot-KV) | ✅ COMPLETE | 2026-01-25 |
| **Phase 11** | Weight-Activation Quantization (SmoothQuant, QuaRot, FlatQuant) | ✅ COMPLETE | 2026-01-26 |
| **Phase 12** | Download Evaluation Benchmarks | ✅ COMPLETE (5/6 benchmarks) | 2026-01-25 |
| **Phase 13** | Baseline Evaluation (BF16) | ✅ COMPLETE | 2026-01-27 |
| **Phase 14** | Evaluation for All Quantized Models | 🔄 IN PROGRESS | - |
| **Phase 15** | Generate Table 1 Results and Statistical Analysis | ⏳ PENDING | - |

### Quantization Training Summary (All Complete)

#### Weight-Only Quantization (4 models)
- ✅ **AWQ W4G128**: `./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1`
- ✅ **AWQ W3G128**: `./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w3g128-tp1`
- ✅ **GPTQ W4G128**: `./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w4g128-tp1`
- ✅ **GPTQ W3G128**: `./outputs/modelzoo/gptq/DeepSeek-R1-Distill-Qwen-1.5B-gptq-w3g128-tp1`

#### KV-Cache Quantization (4 models)
- ✅ **KVQuant* KV4**: `./outputs/modelzoo/kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv4-tp1`
- ✅ **KVQuant* KV3**: `./outputs/modelzoo/kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv3-tp1`
- ✅ **QuaRot-KV KV4**: `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv4-tp1`
- ✅ **QuaRot-KV KV3**: `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv3-tp1`

#### Weight-Activation Quantization (5 models)
- ✅ **SmoothQuant W8A8KV8**: `./outputs/modelzoo/smoothquant/DeepSeek-R1-Distill-Qwen-1.5B-smoothquant-w8a8kv8-tp1`
- ✅ **QuaRot W8A8KV8**: `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w8a8kv8-tp1`
- ✅ **QuaRot W4A4KV4**: `./outputs/modelzoo/quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w4a4kv4-tp1`
- ✅ **FlatQuant W4A4KV4**: `./outputs/modelzoo/flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w4a4kv4-tp1`
- ✅ **FlatQuant W8A8KV8**: `./outputs/modelzoo/flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w8a8kv8-tp1`

**Total: 13 quantized models ready for inference**

### FlatQuant Training Details (Most Time-Intensive)

| Model | Training Duration | Final MSE (Layer 27) | Perplexity (WikiText2) |
|-------|-------------------|----------------------|------------------------|
| FlatQuant W4A4KV4 | ~5h 20m | 27.56 | 47.006 |
| FlatQuant W8A8KV8 | ~3h 34m | 0.139 | 49.362 |

### Inference Progress (as of 2026-01-27)

| Model Category | Completed Seeds | Completed Benchmarks |
|----------------|-----------------|----------------------|
| **Baseline BF16** | 42, 43, 44 | 5/6 per seed |
| **AWQ W4G128** | 42, 43, 44 | 5/6 per seed |
| **AWQ W3G128** | 42 (partial) | 3/6 |
| **GPTQ W4G128** | 42, 43, 44 | 5/6 per seed |
| **GPTQ W3G128** | 42, 43, 44 | 5/6 per seed |
| **KV-Cache Models** | 0/12 total | 0/72 total runs |
| **Weight-Activation Models** | 0/15 total | 0/90 total runs |

### Environment Configuration

- **Machine**: iZbp1fax8vub5x0s6qvjqbZ
- **GPU**: 4x NVIDIA H20 (Hopper architecture, sm_90, 96GB VRAM each)
- **Python**: 3.12.3
- **PyTorch**: 2.5.1+cu124
- **CUDA Toolkit**: 12.4 (PyTorch), 12.8.93 (System)
- **vLLM**: 0.7.0+precompiled (custom fork)
- **xformers**: 0.0.28.post3
- **LightEval**: 0.8.0 (custom fork with math extensions)
- **fast_hadamard_transform**: 1.0.4

### Datasets Downloaded

| Dataset | Purpose | Size | Status |
|---------|---------|------|--------|
| WikiText2 | Calibration | 615MB | ✅ Complete |
| Pile | Calibration | 450MB | ✅ Complete |
| NuminaMath-1.5 | Reasoning Calibration | 507MB | ✅ Complete |
| AIME-90 | Evaluation | 300KB | ✅ Complete |
| AIME-2024 | Evaluation | 80KB | ✅ Complete |
| AIME-2025 | Evaluation | 124KB | ✅ Complete |
| MATH-500 | Evaluation | 488KB | ✅ Complete |
| GSM8K | Evaluation | 5.8MB | ✅ Complete |
| LiveCodeBench | Evaluation | 4.2GB | ✅ Complete |
| GPQA-Diamond | Evaluation | 28KB | ❌ **GATED** (requires HuggingFace approval) |

---

## Upcoming Progress

### Immediate Tasks (Priority Order)

1. **Complete AWQ W3G128 Inference**
   - Finish seeds 43, 44 on remaining benchmarks
   - Currently running on GPU 2-3

2. **KV-Cache Model Inference (12 runs total)**
   - KVQuant* KV4/KV3: All 3 seeds × 5 benchmarks each
   - QuaRot-KV KV4/KV3: All 3 seeds × 5 benchmarks each
   - Estimated time: ~10-15 hours

3. **Weight-Activation Model Inference (15 runs total)**
   - SmoothQuant W8A8KV8
   - QuaRot W8A8KV8, W4A4KV4
   - FlatQuant W8A8KV8, W4A4KV4
   - Estimated time: ~15-20 hours

4. **Phase 15: Generate Final Statistics**
   - Run `python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B`
   - Run `python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B`
   - Compare results with paper's Table 1

### Total Remaining Work

| Metric | Completed | Remaining | Total |
|--------|-----------|-----------|-------|
| Total inference runs | ~23 | ~247 | 270 |
| Models evaluated | ~4 | ~11 | 15 |
| Estimated time | ~15h | ~30-44h | ~50h |

### Short-Term Goals (1-2 weeks)
- Complete full Table 1 replication
- Verify results match paper expectations
- Document any discrepancies or anomalies
- Fill in REPLICATION_OUTPUTS.md template

### Medium-Term Goals (1-2 months)
- Extend experiments to larger models (7B, 14B)
- Explore mixed-precision configurations
- Begin 2-bit quantization experiments
- Optimize quantization parameters

### Long-Term Goals (3-6 months)
- Implement full 2-bit quantization pipeline
- Explore ternary quantization (stepping stone to 1-bit)
- Research binary (1-bit) quantization approaches
- Publish findings on ultra-low bit quantization

---

## Research Tradeoffs

### Quantization Category Tradeoffs

#### 1. Weight-Only Quantization (AWQ, GPTQ)

| Aspect | 4-bit (W4) | 3-bit (W3) |
|--------|-----------|-----------|
| **Compression** | ~3.3x | ~4.3x |
| **Storage** | ~0.9 GB | ~0.7 GB |
| **Accuracy Degradation** | Minimal (expected) | Moderate (observable) |
| **Use Case** | Production deployment | Memory-constrained edge devices |

**Key Tradeoff:** Storage reduction vs. reasoning accuracy retention

#### 2. KV-Cache Quantization (KVQuant*, QuaRot-KV)

| Aspect | KV4 (4-bit) | KV3 (3-bit) |
|--------|------------|------------|
| **KV Cache Memory Reduction** | ~4x | ~5.3x |
| **Long Sequence Benefit** | ~75% memory savings | ~81% memory savings |
| **Impact on Reasoning** | Minimal for short chains | More degradation for long chains |
| **Best For** | Long-context inference | Extreme memory constraints |

**Key Tradeoff:** Memory efficiency during inference vs. long-chain reasoning quality

#### 3. Weight-Activation Quantization (SmoothQuant, QuaRot, FlatQuant)

| Aspect | W8A8KV8 | W4A4KV4 |
|--------|---------|---------|
| **Compression** | ~2x | ~3.3x |
| **Storage** | ~1.5 GB | ~0.9 GB |
| **Accuracy Impact** | Low | Moderate to High |
| **Complexity** | Lower | Higher (quantizes everything) |

**Key Tradeoff:** Full model compression vs. maintaining activation precision

### Method-Specific Tradeoffs

| Method | Strengths | Weaknesses | Best Use Case |
|--------|-----------|------------|---------------|
| **AWQ** | Fast quantization, good accuracy | Less flexibility | Quick deployment |
| **GPTQ** | Reasoning-focused calibration | Longer quantization time | Reasoning-critical tasks |
| **KVQuant*** | Memory efficiency | Some inference overhead | Long-context scenarios |
| **QuaRot-KV** | Rotation reduces outliers | Requires Hadamard transforms | High-precision KV requirements |
| **SmoothQuant** | Balanced approach | 8-bit minimum | Production inference |
| **QuaRot** | Handles activation outliers | Compute overhead for rotation | Activation-sensitive models |
| **FlatQuant** | Outlier flattening effectiveness | Longest training time (~8h for both configs) | Complex weight distributions |

### 2-bit/1-bit Quantization Research Tradeoffs

#### 2-bit Quantization Expectations

| Scenario | Expected Degradation | Viability |
|----------|---------------------|-----------|
| **Optimistic** | 30-40% (mixed-precision) | Usable for some tasks |
| **Realistic** | 50-60% (uniform 2-bit) | Limited to simple tasks |
| **Pessimistic** | >70% (extreme compression) | Not practical |

#### 1-bit (Binary) Quantization Expectations

| Scenario | Expected Degradation | Viability |
|----------|---------------------|-----------|
| **Optimistic** | 50-60% (extreme mixed-precision) | Simple tasks only |
| **Realistic** | >80% | Very limited |
| **Pessimistic** | Complete failure | Not recommended |

**Recommended Approach for Ultra-Low Bit:**
1. Start with small group sizes (32 or 64)
2. Use mixed precision to protect critical layers
3. Fine-tune after quantization on reasoning data
4. Use ternary quantization as stepping stone to binary

---

## Referenced Research Papers & Repositories

### Primary Paper

- **"Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models"**
  - arXiv: [2504.04823](https://arxiv.org/abs/2504.04823)
  - Conference: COLM 2025
  - Repository: [ruikangliu/Quantized-Reasoning-Models](https://github.com/ruikangliu/Quantized-Reasoning-Models)

### Quantization Methods

| Method | Paper/Source | Repository |
|--------|--------------|------------|
| **AWQ** | "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration" | [mit-han-lab/llm-awq](https://github.com/mit-han-lab/llm-awq) |
| **GPTQ** | arXiv:2210.17323 "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers" | [IST-DASLab/gptq](https://github.com/IST-DASLab/gptq) |
| **QuaRot** | "QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs" | [spcl/QuaRot](https://github.com/spcl/QuaRot) |
| **SmoothQuant** | "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models" | [mit-han-lab/smoothquant](https://github.com/mit-han-lab/smoothquant) |
| **FlatQuant** | "FlatQuant: Flatness Matters for LLM Quantization" | [ruikangliu/FlatQuant](https://github.com/ruikangliu/FlatQuant) |
| **KVQuant** | KV-cache quantization methods | Part of main repository |

### Model & Framework References

| Component | Source |
|-----------|--------|
| **DeepSeek-R1-Distill-Qwen-1.5B** | [HuggingFace: deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| **vLLM** | [vllm-project/vllm](https://github.com/vllm-project/vllm) (custom fork in `third-party/vllm`) |
| **LightEval** | [huggingface/lighteval](https://github.com/huggingface/lighteval) (custom fork in `third-party/lighteval`) |
| **xformers** | [facebookresearch/xformers](https://github.com/facebookresearch/xformers) |
| **fast-hadamard-transform** | [Dao-AILab/fast-hadamard-transform](https://github.com/Dao-AILab/fast-hadamard-transform) |

### Binary/Ultra-Low Bit Quantization References

| Method | Description |
|--------|-------------|
| **BiLLM** | Binary LLM approach - binarize weights, keep high-precision activations |
| **Ternary Quantization** | Intermediate step between 2-bit and 1-bit ({-1, 0, +1}) |

### Evaluation Benchmarks

| Benchmark | Description | Samples |
|-----------|-------------|---------|
| **AIME-90** | Historical AIME problems | 90 questions |
| **AIME-2024** | AIME 2024 edition | 30 questions |
| **AIME-2025** | AIME 2025 edition | 30 questions |
| **MATH-500** | Competition-level mathematics | 500 problems |
| **GSM8K** | Grade School Math 8K | 1,319 questions |
| **GPQA-Diamond** | Graduate-level science questions | 198 questions |
| **LiveCodeBench** | Recent coding challenges | Variable |

---

## Troubles Faced & Actions Taken

### Phase 4: fast-hadamard-transform Installation

**Problem:** Standard `pip install -e ./third-party/fast-hadamard-transform` failed because `setup.py` imports torch during build, and isolated build environments don't have torch available.

**Error:** Build isolation environment missing torch dependency.

**Solution:**
```bash
pip install -e ./third-party/fast-hadamard-transform --no-build-isolation
```

**Outcome:** Successfully installed version 1.0.4 with JIT-compiled CUDA kernels.

---

### Phase 5: vLLM Custom Fork Installation (Major Blocker)

This was the **most significant blocker** to the benchmarking trial, causing multiple environment dependency breaks and delays.

#### Problem 1: ABI Mismatch Error (Primary Blocker)

**Initial Command Used:**
```bash
VLLM_USE_PRECOMPILED=1 pip install -e ./third-party/vllm
```

**Error Encountered:**
```
undefined symbol: _ZN3c106ivalue14ConstantString6createE...
```

**Root Cause Analysis:**
- The nightly vLLM precompiled binaries from `wheels.vllm.ai` were compiled with `CXX11_ABI=True`
- PyTorch 2.5.1+cu124 from PyPI uses `CXX11_ABI=False`
- This C++ ABI (Application Binary Interface) incompatibility caused **runtime failures** even when installation appeared successful
- The undefined symbol error indicated binary incompatibility at the C++ level between vLLM's precompiled extensions and PyTorch

**Why This Was Critical:**
- vLLM is the core inference engine for all evaluation runs
- The custom fork contains 10 fake-quantized model implementations required for the study
- Without working vLLM, **all inference and evaluation work (Phases 13-15) was blocked**
- LightEval integration depends on vLLM being functional

#### Problem 2: Misleading Installation Success

**What Made This Difficult to Debug:**
- The `pip install` command completed without errors
- Package appeared correctly installed when checking with `pip list`
- Failure only occurred at **runtime** when importing vLLM modules
- The cryptic C++ symbol error required understanding of ABI compatibility issues

#### Workaround Solution (Two-Step Process)

**Step 1:** Download ABI-compatible wheel from PyPI (not nightly)
```bash
pip download vllm==0.7.0 --no-deps -d /tmp/vllm-wheels/
```

**Step 2:** Install custom fork using PyPI wheel as precompiled binary source
```bash
VLLM_USE_PRECOMPILED=1 \
VLLM_PRECOMPILED_WHEEL_LOCATION=/tmp/vllm-wheels/vllm-0.7.0-cp38-abi3-manylinux1_x86_64.whl \
pip install -e ./third-party/vllm --no-build-isolation
```

**Why This Worked:**
- PyPI's vllm==0.7.0 wheel was compiled with `CXX11_ABI=False`, matching PyTorch 2.5.1+cu124
- Using `VLLM_PRECOMPILED_WHEEL_LOCATION` environment variable forces vLLM to use the specified wheel for precompiled binaries instead of fetching from nightly
- The `--no-build-isolation` flag allows the build to access the already-installed PyTorch

**Result:** Successfully installed in ~8 seconds with all 10 custom fake-quantized models registered:
- LlamaFakeQuantizedForCausalLM
- LlamaFlatQuantForCausalLM
- LlamaKVQuantStarForCausalLM
- LlamaQuaRotKVForCausalLM
- LlamaQuaRotForCausalLM
- Qwen2FakeQuantizedForCausalLM
- Qwen2FlatQuantForCausalLM
- Qwen2KVQuantStarForCausalLM
- Qwen2QuaRotKVForCausalLM
- Qwen2QuaRotForCausalLM

#### Cascading Dependency Issues

After vLLM installation, additional resolutions were needed:

| Dependency | Issue | Resolution |
|------------|-------|------------|
| **scipy==1.17.0** | Required by `vllm_custom` flatquant_utils but not auto-installed | Manual installation: `pip install scipy==1.17.0` |
| **fast_hadamard_transform** | Needed rebuilding after vLLM modified environment | Reinstall with `--no-build-isolation` |
| **xformers** | Already installed via vLLM deps; source build unnecessary | Decision to skip source rebuild, saving ~30-60 minutes |

#### Impact on Benchmarking Timeline

| Impact Area | Description |
|-------------|-------------|
| **Blocked Phases** | All inference/evaluation work (Phases 13-15) completely blocked |
| **Dependent Components** | Custom model registry (10 models), LightEval integration, all quantization inference |
| **Investigation Time** | Multiple hours debugging ABI mismatch and testing solutions |
| **Critical Path** | vLLM is the inference engine; no benchmarking possible without it |

#### Constraints and Technical Context

**Environment Constraints:**
- PyTorch 2.5.1+cu124 (from PyPI) - uses `CXX11_ABI=False`
- CUDA Toolkit 12.8.93 (system) vs CUDA 12.4 (PyTorch internal)
- NVIDIA H20 GPUs (Hopper architecture, sm_90) - required compatible CUDA builds
- Python 3.12.3 - needed compatible wheel format

**Why Standard Approach Failed:**
1. The repository documentation suggested `VLLM_USE_PRECOMPILED=1 pip install -e ./third-party/vllm`
2. This fetches precompiled binaries from vLLM's nightly wheel server
3. Nightly wheels are built against a different PyTorch configuration (CXX11_ABI=True)
4. No error during installation; failure only at import time

#### Lessons Learned

1. **ABI Compatibility Verification**: Always verify `CXX11_ABI` compatibility between PyTorch and CUDA extension libraries before installation
2. **Precompiled Wheel Sources Matter**: Nightly wheels may have different ABI settings than PyPI releases
3. **Build Isolation**: Custom forks with local dependencies often require `--no-build-isolation`
4. **Testing Strategy**: Always run import tests **immediately** after installation, not just `pip list`
5. **Environment Documentation**: Record `PyTorch CXX11_ABI` setting as part of environment info

#### Verification Commands Used

```bash
# Check PyTorch ABI setting
python -c "import torch; print(torch._C._GLIBCXX_USE_CXX11_ABI)"
# Output: False

# Test vLLM import
python -c "import vllm; print(vllm.__version__)"
# Output: 0.7.0

# Test custom model registry
python -c "from vllm_custom.model_executor.fake_quantized_models.registry import register_fake_quantized_models; print('Success')"
```

---

### Phase 7: xformers Source Build Decision

**Problem:** Building xformers from source would take 30-60 minutes with no guaranteed benefit.

**Evaluation:**
- PyPI xformers 0.0.28.post3 was already installed during vLLM Phase 5 installation
- All import tests passed
- Memory efficient attention operations verified working
- Compatible with PyTorch 2.5.1+cu124 and CUDA 12.4

**Decision:** Skip source rebuild and use existing PyPI installation.

**Outcome:** Saved ~30-60 minutes build time with no functionality loss.

---

### Phase 8: GPQA-Diamond Dataset Access

**Problem:** GPQA-Diamond dataset download failed with 403 Forbidden error.

**Root Cause:** GPQA is a **gated dataset** requiring manual access request through HuggingFace.

**Error:**
```
403 Forbidden - Access denied to Idavidrein/gpqa
```

**Action Required:**
1. Visit https://huggingface.co/datasets/Idavidrein/gpqa
2. Request access to the dataset
3. Once approved, re-run download command

**Current Impact:** GPQA-Diamond evaluation skipped for all models (5/6 benchmarks completed instead of 6/6).

**Workaround:** Proceeding with 5 available benchmarks; GPQA can be added retroactively once access is granted.

---

### Phase 11: FlatQuant Long Training Time

**Problem:** FlatQuant training was the most time-intensive quantization method.

**Training Duration:**
- FlatQuant W4A4KV4: ~5 hours 20 minutes
- FlatQuant W8A8KV8: ~3 hours 34 minutes
- Total: ~9 hours for both configurations

**Comparison with Other Methods:**

| Method | Approximate Time | Relative Speed |
|--------|------------------|----------------|
| AWQ | ~10-15 minutes | Fastest |
| GPTQ | ~30-45 minutes | Fast |
| KVQuant* | ~15-20 minutes | Fast |
| QuaRot-KV | ~20-30 minutes | Medium |
| SmoothQuant | ~30-45 minutes | Medium |
| QuaRot | ~1-2 hours | Slow |
| FlatQuant | ~3-5 hours per config | Slowest |

**Outcome:** Successfully completed both FlatQuant configurations with acceptable perplexity values (47.006 and 49.362 on WikiText2).

---

### Phase 14: Inference Process Management

**Problem:** Managing multiple long-running inference processes across 4 GPUs with ~270 total evaluation runs.

**Challenges:**
- Tracking progress across multiple tmux sessions
- Some models experiencing KV cache preemption (slower inference for W3 variants)
- Need for notification system for completion alerts

**Solutions Implemented:**

1. **tmux Session Management:** Created dedicated sessions for different model categories
   - `phase13`: Baseline inference
   - `phase14a-d`: AWQ/GPTQ inference
   - `phase14_kv`: KV-Cache models
   - `phase14_wa`: Weight-Activation models

2. **ntfy Push Notifications:** Integrated push notifications for remote monitoring
   - Topic: `qrm-inference-zane`
   - Sends alerts for phase starts, completions, and errors
   - Allows monitoring via phone app

3. **Automatic Checkpointing:** Inference script automatically skips completed benchmarks, making interrupted runs safe to restart.

**Current Status:** Inference running in parallel on GPUs 2 and 3, with GPUs 0 and 1 available for remaining work.

---

## Summary

This report documents the comprehensive progress on replicating quantization experiments for DeepSeek-R1-Distill-Qwen-1.5B. The most significant technical challenge was the **vLLM custom fork ABI mismatch**, which blocked all benchmarking work until resolved through the PyPI wheel workaround. All 13 quantized models are now ready, and inference evaluation is in progress.

---

*Report Generated: January 29, 2026*  
*Last Updated: January 29, 2026*  
*Project Status: Phase 14 In Progress*  
*Next Milestone: Complete Phase 14 inference, generate Table 1 statistics*