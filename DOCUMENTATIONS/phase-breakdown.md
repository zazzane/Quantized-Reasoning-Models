# Phase Breakdown

## Task 1: Phase 1: Environment Teardown & Fresh Virtual Environment Setup

Create a clean Python virtual environment using standard pip:
Remove any existing virtual environments (`.venv`, `env`, `venv`) to prevent dependency drift
Initialize fresh environment: `python3 -m venv .venv`
Activate and upgrade core tools: `pip install --upgrade pip setuptools wheel`
Document Python version (3.12 recommended per README)


## Task 2: Phase 2: Initialize Git Submodules & Verify Custom Components

Initialize all third-party git submodules and verify their presence:
Run `git submodule update --init --recursive` to fetch all custom libraries
Verify presence of critical directories: `file:third-party/vllm`, `file:third-party/fast-hadamard-transform`, `file:third-party/xformers`, `file:third-party/lighteval`
Check for additional submodules: `file:third-party/AutoAWQ`, `file:third-party/GPTQModel` (optional for real quantization)
Document submodule commit hashes for reproducibility


## Task 3: Phase 3: Install Generic Dependencies from requirements.txt

Install base dependencies that don't conflict with custom builds:
Install from `file:requirements.txt`: transformers, torch, accelerate, datasets, etc.
These are generic PyPI packages that won't be overwritten by local installations
Verify torch installation with CUDA support
Document installed versions for reproducibility


## Task 4: Phase 4: Priority Install - Custom Kernels (fast-hadamard-transform)

Install custom kernels FIRST to prevent PyPI conflicts:
Install fast-hadamard-transform: `pip install -e ./third-party/fast-hadamard-transform`
This kernel is required for QuaRot quantization methods
Verify installation by importing: `python -c "import fast_hadamard_transform"`
Document any compilation warnings or CUDA kernel build messages


## Task 5: Phase 5: Priority Install - Custom vLLM with Fake Quantization Support

Install the custom vLLM fork with precompiled binaries:
Install with: `VLLM_USE_PRECOMPILED=1 pip install -e ./third-party/vllm`
This custom vLLM includes fake-quantization model support via `file:vllm_custom/model_executor/fake_quantized_models/`
Verify the custom model registry is accessible: check `file:vllm_custom/model_executor/fake_quantized_models/registry.py`
Test import: `python -c "from vllm_custom.model_executor.fake_quantized_models.registry import register_fake_quantized_models"`


## Task 6: Phase 6: Install Custom LightEval with Math Extensions

Install the custom LightEval fork with reasoning benchmark support:
Install base: `pip install -e ./third-party/lighteval`
Install math extensions: `pip install -e ./third-party/lighteval[math]`
Verify custom tasks are accessible: check `file:lighteval_custom/tasks/reasoning.py` for AIME-90, AIME-2025, MATH-500, etc.
Test import: `python -c "from lighteval_custom.main_vllm import vllm"`


## Task 7: Phase 7: Build and Install Custom xformers from Source

Build xformers from source (this is time-intensive):
Uninstall any existing xformers: `pip uninstall xformers -y`
Build and install: `pip install -v -U -e third-party/xformers`
This step may take 30-60 minutes depending on hardware
Verify installation: `python -c "import xformers"`
Document build warnings and CUDA architecture targets


## Task 8: Phase 8: Download Model and Calibration Datasets

Download the 1.5B model and required calibration datasets:
Download DeepSeek-R1-Distill-Qwen-1.5B to `./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B`
Download calibration datasets to `./datasets/`: WikiText2, Pile, NuminaMath-1.5
Generate reasoning calibration data: `bash scripts/data/gen_calib.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0`
Verify calibration data is created at `./datasets/gen_data/DeepSeek-R1-Distill-Qwen-1.5B/NuminaMath-1.5.jsonl`


## Task 9: Phase 9: Execute Weight-Only Quantization (AWQ & GPTQ) for 1.5B Model

Run weight-only quantization methods for Table 1:
Execute AWQ: `bash scripts/quantization/awq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (generates W3G128 and W4G128)
Execute GPTQ: `bash scripts/quantization/gptq.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (generates W3G128 and W4G128)
Verify quantized models are saved in `./outputs/modelzoo/awq/` and `./outputs/modelzoo/gptq/`
Note: TP=1 for 1.5B model (single GPU sufficient)


## Task 10: Phase 10: Execute KV Cache Quantization (KVQuant* & QuaRot-KV) with Pre-bias Flag

Run KV cache quantization methods with 1.5B-specific pre-bias flag:
Execute KVQuant*: `bash scripts/quantization/kvquant_star.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (includes `--k_pre_bias` flag for 1.5B/7B)
Execute QuaRot-KV: `bash scripts/quantization/quarot_kv.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (generates KV3 and KV4)
Verify the pre-bias flag is active in `file:scripts/quantization/kvquant_star.sh` lines 11-15
Verify quantized models in `./outputs/modelzoo/kvquant_star/` and `./outputs/modelzoo/quarot/`


## Task 11: Phase 11: Execute Weight-Activation Quantization (SmoothQuant, QuaRot, FlatQuant)

Run weight-activation quantization methods for Table 1:
Execute SmoothQuant: `bash scripts/quantization/smoothquant.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (W8A8KV8)
Execute QuaRot: `bash scripts/quantization/quarot.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (W4A4KV4, W8A8KV8)
Execute FlatQuant: `bash scripts/quantization/flatquant.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0` (W4A4KV4, W8A8KV8)
Note: FlatQuant uses seqlen=4096 for 1.5B model (line 10 in `file:scripts/quantization/flatquant.sh`)


## Task 12: Phase 12: Download Evaluation Benchmarks

Download all evaluation benchmarks required for Table 1:
Download to `./datasets/`: AIME-90, AIME-2025, MATH-500, GSM8K, GPQA-Diamond, LiveCodeBench
Verify dataset formats match expected structure in `file:lighteval_custom/tasks/reasoning.py`
Confirm local paths: `./datasets/AIME90`, `./datasets/aime_2025`, `./datasets/MATH-500`, etc.
Test dataset loading: `python -c "from lighteval_custom.tasks.reasoning import TASKS_TABLE"`


## Task 13: Phase 13: Run Baseline Evaluation (BF16) with LightEval Configuration

Evaluate the baseline 1.5B model on all benchmarks:
Run inference with seeds 42, 43, 44: `bash scripts/inference/inference.sh ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 0 42`
Verify LightEval parameters: temp=0.6, top_p=0.95, max_tokens=32768 (confirmed in `file:inference.py` lines 37-40)
Results saved to `./outputs/inference/DeepSeek-R1-Distill-Qwen-1.5B-seed{42,43,44}/`
Verify all 6 benchmarks produce .jsonl files


## Task 14: Phase 14: Run Evaluation for All Quantized Models (13 Configurations)

Evaluate all 13 quantized models on all benchmarks:
Run inference for each quantized model with seeds 42, 43, 44
Weight-only: AWQ-W3G128, AWQ-W4G128, GPTQ-W3G128, GPTQ-W4G128
KV cache: KVQuant*-KV3, KVQuant*-KV4, QuaRot-KV3, QuaRot-KV4
Weight-activation: SmoothQuant-W8A8KV8, QuaRot-W4A4KV4, QuaRot-W8A8KV8, FlatQuant-W4A4KV4, FlatQuant-W8A8KV8
Example: `bash scripts/inference/inference.sh ./outputs/modelzoo/awq/DeepSeek-R1-Distill-Qwen-1.5B-awq-w4g128-tp1 0 42`


## Task 15: Phase 15: Generate Table 1 Results and Statistical Analysis

Generate accuracy and response length statistics for Table 1:
Run accuracy analysis: `python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B`
Run response length analysis: `python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B`
The script in `file:make_stats_table.py` computes mean and std across seeds
Verify AIME-120 is computed as 0.75×AIME-90 + 0.25×AIME-2025 (line 118)
Compare results with paper's Table 1 expectations