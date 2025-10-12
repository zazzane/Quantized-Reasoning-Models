#!/bin/bash
# Master script to run all quantization experiments for DeepSeek-R1-Distill-Qwen-1.5B
# This script automates the complete replication pipeline as described in the paper

set -e  # Exit on error

# Configuration
MODEL_PATH="./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B"
MODEL_NAME="DeepSeek-R1-Distill-Qwen-1.5B"
TP=1  # Tensor Parallelism for 1.5B model
DEVICE=${1:-0}  # GPU device, default 0
SEEDS=(42 43 44)  # Evaluation seeds for robust statistics

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log_step() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if model exists
if [ ! -d "$MODEL_PATH" ]; then
    log_error "Model not found at $MODEL_PATH"
    log_error "Please download the model first:"
    log_error "  huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B --local-dir $MODEL_PATH"
    exit 1
fi

log_step "Starting comprehensive quantization experiments for $MODEL_NAME"
log_step "Configuration: TP=$TP, Device=$DEVICE, Seeds=${SEEDS[@]}"

# Create output directories
mkdir -p outputs/modelzoo/{awq,gptq,kvquant_star,quarot,smoothquant,flatquant}
mkdir -p outputs/inference
mkdir -p logs

# ============================================================================
# Step 1: Generate calibration data (if not already exists)
# ============================================================================
log_step "Step 1: Checking calibration data..."
CALIB_DATA_PATH="./datasets/reasoning-numina-math-1.5/${MODEL_NAME}.pkl"
if [ ! -f "$CALIB_DATA_PATH" ]; then
    log_step "Generating calibration data..."
    bash scripts/data/gen_calib.sh $MODEL_PATH $DEVICE 2>&1 | tee logs/calib_gen.log
    log_step "Calibration data generated"
else
    log_step "Calibration data already exists, skipping generation"
fi

# ============================================================================
# Step 2: Baseline Evaluation (BF16)
# ============================================================================
log_step "Step 2: Running baseline evaluation (BF16)..."
for seed in "${SEEDS[@]}"; do
    log_step "  Evaluating with seed $seed..."
    if bash scripts/inference/inference.sh $MODEL_PATH $DEVICE $seed 2>&1 | tee logs/baseline_seed${seed}.log; then
        log_step "  Baseline evaluation (seed $seed) completed"
    else
        log_error "Baseline evaluation (seed $seed) failed"
    fi
done

# ============================================================================
# Step 3: Weight-Only Quantization
# ============================================================================
log_step "Step 3: Weight-Only Quantization..."

# AWQ (W3, W4)
log_step "  3.1: Running AWQ quantization..."
if bash scripts/quantization/awq.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/awq_quant.log; then
    log_step "  AWQ quantization completed"
    
    # Evaluate AWQ W4
    log_step "  Evaluating AWQ W4..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/awq/${MODEL_NAME}-awq-w4g128-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/awq_w4_seed${seed}.log
    done
    
    # Evaluate AWQ W3
    log_step "  Evaluating AWQ W3..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/awq/${MODEL_NAME}-awq-w3g128-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/awq_w3_seed${seed}.log
    done
else
    log_error "AWQ quantization failed"
fi

# GPTQ (W3, W4)
log_step "  3.2: Running GPTQ quantization..."
if bash scripts/quantization/gptq.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/gptq_quant.log; then
    log_step "  GPTQ quantization completed"
    
    # Evaluate GPTQ W4
    log_step "  Evaluating GPTQ W4..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/gptq/${MODEL_NAME}-gptq-w4g128-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/gptq_w4_seed${seed}.log
    done
    
    # Evaluate GPTQ W3
    log_step "  Evaluating GPTQ W3..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/gptq/${MODEL_NAME}-gptq-w3g128-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/gptq_w3_seed${seed}.log
    done
else
    log_error "GPTQ quantization failed"
fi

# ============================================================================
# Step 4: KV-Cache Quantization
# ============================================================================
log_step "Step 4: KV-Cache Quantization..."

# KVQuant* (KV3, KV4)
log_step "  4.1: Running KVQuant* quantization..."
if bash scripts/quantization/kvquant_star.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/kvquant_star_quant.log; then
    log_step "  KVQuant* quantization completed"
    
    # Evaluate KVQuant* KV4
    log_step "  Evaluating KVQuant* KV4..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/kvquant_star/${MODEL_NAME}-kvquant_star-kv4-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/kvquant_star_kv4_seed${seed}.log
    done
    
    # Evaluate KVQuant* KV3
    log_step "  Evaluating KVQuant* KV3..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/kvquant_star/${MODEL_NAME}-kvquant_star-kv3-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/kvquant_star_kv3_seed${seed}.log
    done
else
    log_error "KVQuant* quantization failed"
fi

# QuaRot-KV (KV3, KV4)
log_step "  4.2: Running QuaRot-KV quantization..."
if bash scripts/quantization/quarot_kv.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/quarot_kv_quant.log; then
    log_step "  QuaRot-KV quantization completed"
    
    # Evaluate QuaRot-KV KV4
    log_step "  Evaluating QuaRot-KV KV4..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/quarot/${MODEL_NAME}-quarot-kv4-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/quarot_kv4_seed${seed}.log
    done
    
    # Evaluate QuaRot-KV KV3
    log_step "  Evaluating QuaRot-KV KV3..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/quarot/${MODEL_NAME}-quarot-kv3-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/quarot_kv3_seed${seed}.log
    done
else
    log_error "QuaRot-KV quantization failed"
fi

# ============================================================================
# Step 5: Weight-Activation Quantization
# ============================================================================
log_step "Step 5: Weight-Activation Quantization..."

# SmoothQuant (W8A8KV8)
log_step "  5.1: Running SmoothQuant quantization..."
if bash scripts/quantization/smoothquant.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/smoothquant_quant.log; then
    log_step "  SmoothQuant quantization completed"
    
    # Evaluate SmoothQuant
    log_step "  Evaluating SmoothQuant W8A8KV8..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/smoothquant/${MODEL_NAME}-smoothquant-w8a8kv8-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/smoothquant_w8a8kv8_seed${seed}.log
    done
else
    log_error "SmoothQuant quantization failed"
fi

# QuaRot (W4A4KV4, W8A8KV8)
log_step "  5.2: Running QuaRot quantization..."
if bash scripts/quantization/quarot.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/quarot_quant.log; then
    log_step "  QuaRot quantization completed"
    
    # Evaluate QuaRot W8A8KV8
    log_step "  Evaluating QuaRot W8A8KV8..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/quarot/${MODEL_NAME}-quarot-w8a8kv8-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/quarot_w8a8kv8_seed${seed}.log
    done
    
    # Evaluate QuaRot W4A4KV4
    log_step "  Evaluating QuaRot W4A4KV4..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/quarot/${MODEL_NAME}-quarot-w4a4kv4-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/quarot_w4a4kv4_seed${seed}.log
    done
else
    log_error "QuaRot quantization failed"
fi

# FlatQuant (W4A4KV4, W8A8KV8)
log_step "  5.3: Running FlatQuant quantization..."
if bash scripts/quantization/flatquant.sh $MODEL_PATH $TP $DEVICE 2>&1 | tee logs/flatquant_quant.log; then
    log_step "  FlatQuant quantization completed"
    
    # Evaluate FlatQuant W8A8KV8
    log_step "  Evaluating FlatQuant W8A8KV8..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/flatquant/${MODEL_NAME}-flatquant-w8a8kv8-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/flatquant_w8a8kv8_seed${seed}.log
    done
    
    # Evaluate FlatQuant W4A4KV4
    log_step "  Evaluating FlatQuant W4A4KV4..."
    for seed in "${SEEDS[@]}"; do
        bash scripts/inference/inference.sh \
            ./outputs/modelzoo/flatquant/${MODEL_NAME}-flatquant-w4a4kv4-tp${TP} $DEVICE $seed \
            2>&1 | tee logs/flatquant_w4a4kv4_seed${seed}.log
    done
else
    log_error "FlatQuant quantization failed"
fi

# ============================================================================
# Step 6: Generate Results Summary
# ============================================================================
log_step "Step 6: Generating results summary..."

log_step "Generating accuracy table..."
python -m make_stats_table --stats acc --models $MODEL_NAME \
    2>&1 | tee results_accuracy_${MODEL_NAME}.txt

log_step "Generating response length analysis..."
python -m make_stats_table --stats length --models $MODEL_NAME \
    2>&1 | tee results_length_${MODEL_NAME}.txt

# ============================================================================
# Completion
# ============================================================================
log_step "All experiments completed!"
log_step "Results saved in:"
log_step "  - Accuracy: results_accuracy_${MODEL_NAME}.txt"
log_step "  - Length: results_length_${MODEL_NAME}.txt"
log_step "  - Logs: logs/"
log_step "  - Quantized models: outputs/modelzoo/"
log_step "  - Inference results: outputs/inference/"

echo ""
log_step "Summary of quantization methods tested:"
echo "  1. Weight-Only: AWQ (W3/W4), GPTQ (W3/W4)"
echo "  2. KV-Cache: KVQuant* (KV3/KV4), QuaRot-KV (KV3/KV4)"
echo "  3. Weight-Activation: SmoothQuant (W8A8KV8), QuaRot (W4A4KV4/W8A8KV8), FlatQuant (W4A4KV4/W8A8KV8)"
echo ""
log_step "To view results, check the generated text files or run:"
echo "  python -m make_stats_table --stats acc --models $MODEL_NAME"
