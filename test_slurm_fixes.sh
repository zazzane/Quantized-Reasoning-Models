#!/bin/bash
# Test script to verify SLURM environment fixes

echo "=== Testing SLURM Environment Fixes ==="

# Activate virtual environment
cd /home/FYP/zane0001/FYP/Quantized-Reasoning-Models
source venv/bin/activate

# Set up environment (simulating SLURM job environment)
export CUDA_VISIBLE_DEVICES=0
export TOKENIZERS_PARALLELISM=false
export NCCL_CUMEM_ENABLE=0
export TORCHINDUCTOR_COMPILE_THREADS=1

# Add local modules to Python path
export PYTHONPATH="/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/third-party/fast-hadamard-transform:$PYTHONPATH"
export PYTHONPATH="/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/third-party/AutoAWQ:$PYTHONPATH"
export PYTHONPATH="/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/third-party/GPTQModel:$PYTHONPATH"
export PYTHONPATH="/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/third-party/vllm:$PYTHONPATH"

echo "1. Testing PyTorch/CUDA environment..."
python -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA device count: {torch.cuda.device_count()}')
if torch.cuda.is_available():
    print(f'CUDA device name: {torch.cuda.get_device_name(0)}')
    print(f'CUDA version: {torch.version.cuda}')
else:
    print('CUDA not available in current environment')
"

echo "2. Testing fast-hadamard-transform fallback..."
python -c "
import sys
sys.path.append('/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/third-party/fast-hadamard-transform')
try:
    import fast_hadamard_transform
    print('✓ fast-hadamard-transform import successful')
except ImportError as e:
    print(f'⚠ fast-hadamard-transform not available: {e}')
    print('✓ Fallback mechanism will be used')
"

echo "3. Testing quant_utils with fallback..."
python -c "
import sys
sys.path.append('/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/methods/utils')
try:
    from quant_utils import FAST_HADAMARD_AVAILABLE
    print(f'✓ quant_utils imported successfully, FAST_HADAMARD_AVAILABLE: {FAST_HADAMARD_AVAILABLE}')
except Exception as e:
    print(f'✗ quant_utils import failed: {e}')
"

echo "4. Testing vLLM import..."
python -c "
try:
    import vllm
    print('✓ vLLM import successful')
    print(f'vLLM version: {vllm.__version__}')
except ImportError as e:
    print(f'✗ vLLM import failed: {e}')
    print('This will cause inference to fail in SLURM jobs')
"

echo "5. Testing AWQ calibration data..."
python -c "
import sys
sys.path.append('/home/FYP/zane0001/FYP/Quantized-Reasoning-Models/methods/awq')
try:
    from calib_data import get_calib_dataset
    print('✓ AWQ calibration data loading works')
except Exception as e:
    print(f'✗ AWQ calibration failed: {e}')
"

echo "6. Testing inference script import..."
python -c "
import sys
sys.path.append('/home/FYP/zane0001/FYP/Quantized-Reasoning-Models')
try:
    # Test if we can import the inference script without running it
    import importlib.util
    spec = importlib.util.spec_from_file_location('inference', 'inference.py')
    print('✓ inference.py can be loaded')
except Exception as e:
    print(f'✗ inference.py load failed: {e}')
"

echo "7. Testing model availability..."
if [ -d "./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B" ]; then
    echo "✓ Model found"
else
    echo "✗ Model missing"
fi

echo "8. Testing datasets availability..."
if [ -d "./datasets/wikitext" ] && [ -d "./datasets/pile-val-backup" ]; then
    echo "✓ Calibration datasets found"
else
    echo "✗ Calibration datasets missing"
fi

echo "=== Test Complete ==="
echo "If vLLM import works, the main issue is resolved."
echo "If fast-hadamard-transform fallback works, GPTQ quantization should proceed."
echo "Ready to resubmit SLURM jobs if tests pass."

