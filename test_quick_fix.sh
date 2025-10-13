#!/bin/bash
# Quick test to verify the fixes work before resubmitting SLURM jobs

echo "=== Testing Quick Fixes ==="
echo "Testing if the issues have been resolved..."

# Activate environment
cd /home/FYP/zane0001/FYP/Quantized-Reasoning-Models
source venv/bin/activate

echo "1. Testing vLLM import..."
python -c "import vllm; print('✓ vLLM import successful')" || echo "✗ vLLM import failed"

echo "2. Testing datasets availability..."
if [ -d "./datasets/wikitext" ] && [ -d "./datasets/pile-val-backup" ]; then
    echo "✓ Calibration datasets found"
else
    echo "✗ Calibration datasets missing"
fi

echo "3. Testing fast-hadamard-transform (optional)..."
python -c "import fast_hadamard_transform; print('✓ fast-hadamard-transform available')" 2>/dev/null || echo "⚠ fast-hadamard-transform not available (may not be needed)"

echo "4. Testing analysis script..."
python scripts/analyze_quantization_results.py --help | grep -q "output_prefix" && echo "✓ Analysis script supports new arguments" || echo "✗ Analysis script missing arguments"

echo "5. Testing model availability..."
if [ -d "./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B" ]; then
    echo "✓ Model found"
else
    echo "✗ Model missing"
fi

echo "6. Testing a simple AWQ quantization command..."
python -c "
import sys
sys.path.append('.')
try:
    from methods.awq.calib_data import get_calib_dataset
    print('✓ AWQ calibration data loading works')
except Exception as e:
    print(f'✗ AWQ calibration failed: {e}')
"

echo "=== Test Complete ==="
echo "If most tests pass, you can resubmit the SLURM jobs."
