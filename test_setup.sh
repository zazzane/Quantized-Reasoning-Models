#!/bin/bash
# Test script to verify the setup before submitting SLURM jobs
# Run this to ensure everything is working correctly

set -e

echo "=== DeepSeek-R1-Distill-Qwen-1.5B Quantization Setup Test ==="
echo "Testing setup before SLURM job submission..."
echo

# Color output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

test_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

test_fail() {
    echo -e "${RED}✗${NC} $1"
}

test_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Virtual Environment
echo "1. Testing virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    if [ -n "$VIRTUAL_ENV" ]; then
        test_pass "Virtual environment activated successfully"
        echo "   Virtual env path: $VIRTUAL_ENV"
    else
        test_fail "Virtual environment not activated properly"
        exit 1
    fi
else
    test_fail "Virtual environment not found"
    exit 1
fi

# Test 2: Python and Dependencies
echo "2. Testing Python and dependencies..."
python_version=$(python --version 2>&1)
test_pass "Python version: $python_version"

# Test key imports
python -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>/dev/null && test_pass "PyTorch available" || test_fail "PyTorch not available"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')" 2>/dev/null && test_pass "Transformers available" || test_fail "Transformers not available"
python -c "import datasets; print('Datasets available')" 2>/dev/null && test_pass "Datasets available" || test_fail "Datasets not available"

# Test 3: Model Download
echo "3. Testing model download..."
MODEL_PATH="./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B"
if [ -d "$MODEL_PATH" ]; then
    if [ -f "$MODEL_PATH/config.json" ] && [ -f "$MODEL_PATH/model.safetensors" ]; then
        test_pass "Model downloaded successfully"
        model_size=$(du -sh "$MODEL_PATH" | cut -f1)
        echo "   Model size: $model_size"
    else
        test_fail "Model files incomplete"
    fi
else
    test_fail "Model not found at $MODEL_PATH"
    echo "   Run: huggingface-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B --local-dir $MODEL_PATH"
fi

# Test 4: Script Availability
echo "4. Testing quantization scripts..."
scripts=(
    "scripts/quantization/awq.sh"
    "scripts/quantization/gptq.sh"
    "scripts/quantization/kvquant_star.sh"
    "scripts/quantization/quarot_kv.sh"
    "scripts/quantization/smoothquant.sh"
    "scripts/quantization/quarot.sh"
    "scripts/quantization/flatquant.sh"
    "scripts/inference/inference.sh"
    "scripts/data/gen_calib.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        test_pass "Script found: $script"
    else
        test_fail "Script missing: $script"
    fi
done

# Test 5: SLURM Scripts
echo "5. Testing SLURM job scripts..."
if [ -f "slurm_task1.sh" ] && [ -f "slurm_task2.sh" ]; then
    test_pass "SLURM scripts created"
    
    # Check if scripts are executable
    if [ -x "slurm_task1.sh" ] && [ -x "slurm_task2.sh" ]; then
        test_pass "SLURM scripts are executable"
    else
        test_warning "SLURM scripts not executable - run: chmod +x slurm_task*.sh"
    fi
else
    test_fail "SLURM scripts not found"
fi

# Test 6: GPU Availability (if on GPU node)
echo "6. Testing GPU availability..."
if command -v nvidia-smi &> /dev/null; then
    gpu_info=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
    if [ $? -eq 0 ]; then
        test_pass "GPU detected: $gpu_info"
    else
        test_warning "GPU not available (expected if not on GPU node)"
    fi
else
    test_warning "nvidia-smi not available"
fi

# Test 7: Directory Structure
echo "7. Testing directory structure..."
mkdir -p outputs/{modelzoo/{awq,gptq,kvquant_star,quarot,smoothquant,flatquant},inference,logs}
test_pass "Output directories created"

# Test 8: Memory Check
echo "8. Testing available memory..."
if command -v free &> /dev/null; then
    total_mem=$(free -g | awk 'NR==2{print $2}')
    available_mem=$(free -g | awk 'NR==2{print $7}')
    echo "   Total RAM: ${total_mem}GB"
    echo "   Available RAM: ${available_mem}GB"
    
    if [ "$total_mem" -ge 64 ]; then
        test_pass "Sufficient memory for SLURM job (64GB requested)"
    else
        test_warning "Limited memory available - consider reducing SLURM memory request"
    fi
fi

echo
echo "=== Setup Test Summary ==="
echo "If all tests passed, you're ready to submit SLURM jobs:"
echo
echo "  sbatch slurm_task1.sh  # Weight-Only + KV-Cache quantization"
echo "  sbatch slurm_task2.sh  # Weight-Activation + Baseline"
echo
echo "Monitor jobs with:"
echo "  squeue -u \$USER"
echo "  tail -f slurm-\{job_id\}.out"
echo
echo "Good luck with your experiments! 🚀"
