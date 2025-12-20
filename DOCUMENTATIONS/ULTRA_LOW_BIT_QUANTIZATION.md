# Ultra-Low Bit Quantization: 2-bit and 1-bit Exploration Guide

This document provides a comprehensive guide for exploring 2-bit and 1-bit quantization for reasoning models, based on the findings from the main quantization study.

## Table of Contents

1. [Background](#background)
2. [Challenges](#challenges)
3. [2-bit Quantization](#2-bit-quantization)
4. [1-bit Quantization](#1-bit-quantization)
5. [Implementation Guide](#implementation-guide)
6. [Experimental Protocol](#experimental-protocol)
7. [Expected Outcomes](#expected-outcomes)

## Background

### Current State (from main study)

The main quantization study evaluated:
- **3-bit quantization**: Moderate degradation (observable but acceptable for some use cases)
- **4-bit quantization**: Minimal degradation (practical for production)
- **8-bit quantization**: Very minimal degradation

### Motivation for Ultra-Low Bit Quantization

**Benefits:**
- Extreme memory reduction (4-8x compared to 4-bit)
- Faster inference due to reduced memory bandwidth
- Enables deployment on highly resource-constrained devices
- Potential for specialized hardware acceleration

**Use Cases:**
- Edge devices with limited memory (smartphones, IoT)
- Large-scale deployment where memory is at premium
- Research on compression limits of reasoning models

## Challenges

### Technical Challenges

#### 2-bit Quantization (4 discrete levels)

1. **Limited Representation Capacity**
   - Only 4 possible values per weight/activation
   - Severe information loss compared to continuous values
   - Difficult to represent the range of values accurately

2. **Quantization Error Accumulation**
   - Errors compound through layers
   - Especially problematic for deep reasoning chains
   - Attention mechanisms highly sensitive to quantization

3. **Critical Component Identification**
   - Some layers/components are more critical than others
   - Need to identify and protect critical paths
   - Layer normalization and residual connections especially important

#### 1-bit Quantization (Binary)

1. **Extreme Information Loss**
   - Only two values: -1/+1 or 0/1
   - Fundamentally different from weight pruning
   - Most model capacity lost

2. **Reasoning Capability Preservation**
   - Multi-step reasoning requires precise representations
   - Mathematical operations need adequate precision
   - Likely catastrophic degradation for complex reasoning

3. **Training vs Post-Training**
   - Post-training quantization likely insufficient
   - May require quantization-aware training from scratch
   - Or at least extensive fine-tuning

## 2-bit Quantization

### Approach 1: Uniform 2-bit Post-Training Quantization

#### Modifications Required

**File: `methods/flatquant/flatquant/quant_utils.py`**

```python
def get_qmin_qmax(bits, sym):
    if sym:
        if bits == 2:
            return -2, 1  # [-2, -1, 0, 1]
        if bits == 3:
            return -4, 3  # Existing 3-bit
        # ... existing code
    else:
        if bits == 2:
            return 0, 3  # [0, 1, 2, 3]
        # ... existing code
```

**New Script: `scripts/quantization/gptq_2bit.sh`**

```bash
#!/bin/bash

model=${1}  # ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B
tp=${2}     # 1
device=${3} # 0

model_name=$(basename "$model")

CUDA_VISIBLE_DEVICES=${device} \
python -m methods.quarot_gptq.save_fake_quant \
    --model ${model} \
    --w_bits 2 --w_clip --w_asym --w_groupsize 64 --act_order \
    --tp ${tp} \
    --save_qmodel_path ./outputs/modelzoo/gptq/${model_name}-gptq-w2g64-tp${tp} \
    --cal_dataset reasoning-numina-math-1.5
```

### Approach 2: Mixed-Precision 2-bit

#### Strategy: Keep Critical Layers at Higher Precision

**Critical Layers to Preserve:**
1. First and last layers (embedding and output projection)
2. Attention query/key/value projections
3. Layer normalization parameters
4. Residual connection weights

**Implementation:**

```python
# Pseudo-code for mixed precision configuration
layer_bits = {
    'model.embed_tokens': 8,  # Embedding layer
    'model.layers.*.self_attn.q_proj': 4,  # Attention Q
    'model.layers.*.self_attn.k_proj': 4,  # Attention K
    'model.layers.*.self_attn.v_proj': 4,  # Attention V
    'model.layers.*.self_attn.o_proj': 2,  # Attention output
    'model.layers.*.mlp.gate_proj': 2,  # MLP layers
    'model.layers.*.mlp.up_proj': 2,
    'model.layers.*.mlp.down_proj': 2,
    'model.norm': 8,  # Final layer norm
    'lm_head': 8,  # Output projection
}
```

### Approach 3: Group-wise 2-bit with Small Groups

**Rationale:** Smaller quantization groups reduce error accumulation

```bash
# Example: Use group size of 32 instead of 128
bash scripts/quantization/gptq_2bit.sh \
    ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0 \
    --w_groupsize 32
```

### Approach 4: 2-bit with Learnable Quantization

**Method:** Fine-tune quantization scale/zero-point parameters

1. Apply 2-bit quantization
2. Freeze quantized weights
3. Fine-tune scale and zero-point parameters on reasoning dataset
4. Use small learning rate (1e-5 to 1e-4)

```python
# Pseudo-code for learnable quantization
def quantize_with_learnable_params(model, calibration_data):
    for layer in model.layers:
        # Quantize weights to 2-bit
        quantized_weights = quantize_2bit(layer.weight)
        
        # Make scale and zero_point learnable
        layer.quant_scale = nn.Parameter(compute_scale(layer.weight))
        layer.quant_zero = nn.Parameter(compute_zero_point(layer.weight))
        
    # Fine-tune on calibration data
    fine_tune(model, calibration_data, num_steps=1000)
```

## 1-bit Quantization

### Approach 1: Binary Neural Networks (BNN)

#### BiLLM-inspired Approach

Recent work on binary LLMs (BiLLM) suggests:
1. Use high-precision activations (8-bit or 16-bit)
2. Only binarize weights
3. Apply layer-wise reconstruction

**Key Components:**
- Binary weight: w_bin = sign(w)
- Scaling factor: alpha (per-layer or per-channel)
- Reconstruction: w_approx = alpha * w_bin

#### Implementation Outline

```python
def binarize_weight(weight):
    """
    Binarize weight tensor to {-1, +1}
    
    Args:
        weight: torch.Tensor of shape [out_features, in_features]
    
    Returns:
        binary_weight: torch.Tensor with values in {-1, +1}
        scale: torch.Tensor of shape [out_features, 1]
    """
    # Compute per-output-channel scale
    scale = weight.abs().mean(dim=1, keepdim=True)
    
    # Binarize
    binary_weight = torch.sign(weight)
    binary_weight[binary_weight == 0] = 1  # Handle zeros
    
    return binary_weight, scale

def apply_binary_quantization(model):
    """Apply binary quantization to model weights"""
    for name, module in model.named_modules():
        if isinstance(module, nn.Linear):
            weight = module.weight.data
            binary_weight, scale = binarize_weight(weight)
            
            # Store binary weight and scale
            module.weight.data = binary_weight
            module.register_buffer('weight_scale', scale)
            
            # Modify forward pass to use scaling
            original_forward = module.forward
            def scaled_forward(self, x):
                # Scale binary weights during forward pass
                scaled_weight = self.weight * self.weight_scale
                return F.linear(x, scaled_weight, self.bias)
            
            module.forward = types.MethodType(scaled_forward, module)
```

### Approach 2: Ternary Quantization (Stepping Stone)

**Rationale:** Ternary (-1, 0, +1) provides middle ground between 2-bit and 1-bit

**Benefits:**
- Allows for zero weights (natural sparsity)
- Better approximation than pure binary
- Still very memory efficient

```python
def ternarize_weight(weight, threshold=0.05):
    """
    Ternarize weight tensor to {-1, 0, +1}
    
    Args:
        weight: torch.Tensor
        threshold: Fraction of max weight magnitude to use as zero threshold
    
    Returns:
        ternary_weight: torch.Tensor with values in {-1, 0, +1}
        scale: torch.Tensor
    """
    max_val = weight.abs().max()
    threshold_val = threshold * max_val
    
    # Compute scale on non-zero elements
    mask = weight.abs() > threshold_val
    scale = weight[mask].abs().mean() if mask.any() else 1.0
    
    # Ternarize
    ternary_weight = torch.zeros_like(weight)
    ternary_weight[weight > threshold_val] = 1
    ternary_weight[weight < -threshold_val] = -1
    
    return ternary_weight, scale
```

### Approach 3: Extreme Mixed Precision

**Strategy:** Binary for most weights, 4-bit/8-bit for critical components

**Configuration:**
```python
layer_bits = {
    # High precision for critical components
    'model.embed_tokens': 16,
    'model.layers.*.self_attn.q_proj': 8,
    'model.layers.*.self_attn.k_proj': 8,
    'model.layers.*.self_attn.v_proj': 8,
    'model.layers.*.input_layernorm': 16,
    'model.layers.*.post_attention_layernorm': 16,
    'lm_head': 16,
    
    # Binary for MLP (bulk of parameters)
    'model.layers.*.mlp.*': 1,
    
    # Low precision for attention output
    'model.layers.*.self_attn.o_proj': 2,
}
```

## Implementation Guide

### Step 1: Modify Quantization Utilities

**File: `methods/flatquant/flatquant/quant_utils.py`**

Add support for 1-bit and 2-bit in all relevant functions:

```python
def get_qmin_qmax(bits, sym):
    """Get quantization range for given bits"""
    if sym:
        if bits == 1:
            return -1, 0  # Binary: {-1, 0} or could be {-1, 1}
        elif bits == 2:
            return -2, 1  # 4 levels: {-2, -1, 0, 1}
        elif bits == 3:
            return -4, 3
        # ... existing code
    else:
        if bits == 1:
            return 0, 1  # Binary: {0, 1}
        elif bits == 2:
            return 0, 3  # 4 levels: {0, 1, 2, 3}
        # ... existing code

# Existing quantization functions will automatically work with new bit-widths
```

### Step 2: Create Quantization Scripts

**2-bit GPTQ Script: `scripts/quantization/gptq_2bit.sh`**

```bash
#!/bin/bash

model=${1}
tp=${2}
device=${3}

model_name=$(basename "$model")

# Try different group sizes for 2-bit
for GROUPSIZE in 32 64 128; do
    CUDA_VISIBLE_DEVICES=${device} \
    python -m methods.quarot_gptq.save_fake_quant \
        --model ${model} \
        --w_bits 2 --w_clip --w_asym --w_groupsize ${GROUPSIZE} --act_order \
        --tp ${tp} \
        --save_qmodel_path ./outputs/modelzoo/gptq/${model_name}-gptq-w2g${GROUPSIZE}-tp${tp} \
        --cal_dataset reasoning-numina-math-1.5
done
```

**1-bit Binary Script: `scripts/quantization/binary_1bit.sh`**

```bash
#!/bin/bash

model=${1}
tp=${2}
device=${3}

model_name=$(basename "$model")

CUDA_VISIBLE_DEVICES=${device} \
python -m methods.binary.binarize_model \
    --model ${model} \
    --method bilm \
    --activation_bits 8 \
    --tp ${tp} \
    --save_qmodel_path ./outputs/modelzoo/binary/${model_name}-binary-w1a8-tp${tp}
```

### Step 3: Create Binary Quantization Module

**New File: `methods/binary/__init__.py`**

```python
"""Binary quantization methods for ultra-low bit quantization"""

from .binarize_model import binarize_model
from .binary_ops import BinaryLinear, TernaryLinear

__all__ = ['binarize_model', 'BinaryLinear', 'TernaryLinear']
```

**New File: `methods/binary/binarize_model.py`**

```python
"""
Main script for applying binary quantization to models.
Supports multiple binary quantization methods.
"""

import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM
import argparse

from .binary_ops import BinaryLinear, TernaryLinear


def replace_linear_with_binary(model, method='binary', exclude_layers=None):
    """
    Replace nn.Linear layers with binary/ternary equivalents.
    
    Args:
        model: HuggingFace model
        method: 'binary' or 'ternary'
        exclude_layers: List of layer name patterns to exclude from quantization
    """
    if exclude_layers is None:
        exclude_layers = ['embed_tokens', 'lm_head', 'norm']
    
    for name, module in model.named_modules():
        # Check if this layer should be excluded
        should_exclude = any(pattern in name for pattern in exclude_layers)
        if should_exclude:
            continue
        
        # Replace Linear layers
        if isinstance(module, nn.Linear):
            if method == 'binary':
                new_layer = BinaryLinear.from_linear(module)
            elif method == 'ternary':
                new_layer = TernaryLinear.from_linear(module)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            # Replace in parent module
            parent_name = '.'.join(name.split('.')[:-1])
            child_name = name.split('.')[-1]
            parent = model.get_submodule(parent_name) if parent_name else model
            setattr(parent, child_name, new_layer)
    
    return model


def binarize_model(model_path, method='binary', output_path=None):
    """
    Load and binarize a model.
    
    Args:
        model_path: Path to the model
        method: Quantization method ('binary' or 'ternary')
        output_path: Path to save quantized model
    
    Returns:
        Quantized model
    """
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map='auto'
    )
    
    # Apply binary quantization
    model = replace_linear_with_binary(model, method=method)
    
    # Save if output path provided
    if output_path:
        model.save_pretrained(output_path)
        print(f"Binarized model saved to {output_path}")
    
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--method', type=str, default='binary', 
                       choices=['binary', 'ternary'])
    parser.add_argument('--save_qmodel_path', type=str, required=True)
    parser.add_argument('--tp', type=int, default=1)
    parser.add_argument('--activation_bits', type=int, default=8)
    
    args = parser.parse_args()
    
    binarize_model(args.model, args.method, args.save_qmodel_path)
```

**New File: `methods/binary/binary_ops.py`**

```python
"""
Binary and ternary linear layer implementations.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class BinaryLinear(nn.Module):
    """
    Binary linear layer with {-1, +1} weights.
    Activations remain in higher precision.
    """
    
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        
        # Binary weights
        self.weight = nn.Parameter(torch.zeros(out_features, in_features))
        
        # Scaling factor
        self.register_buffer('weight_scale', torch.ones(out_features, 1))
        
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter('bias', None)
    
    @classmethod
    def from_linear(cls, linear_layer):
        """Create BinaryLinear from existing nn.Linear"""
        binary_layer = cls(
            linear_layer.in_features,
            linear_layer.out_features,
            bias=(linear_layer.bias is not None)
        )
        
        # Binarize weights
        weight = linear_layer.weight.data
        scale = weight.abs().mean(dim=1, keepdim=True)
        binary_weight = torch.sign(weight)
        binary_weight[binary_weight == 0] = 1
        
        binary_layer.weight.data = binary_weight
        binary_layer.weight_scale = scale
        
        if linear_layer.bias is not None:
            binary_layer.bias.data = linear_layer.bias.data
        
        return binary_layer
    
    def forward(self, x):
        # Scale binary weights for forward pass
        scaled_weight = self.weight * self.weight_scale
        return F.linear(x, scaled_weight, self.bias)


class TernaryLinear(nn.Module):
    """
    Ternary linear layer with {-1, 0, +1} weights.
    """
    
    def __init__(self, in_features, out_features, bias=True, threshold=0.05):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.threshold = threshold
        
        self.weight = nn.Parameter(torch.zeros(out_features, in_features))
        self.register_buffer('weight_scale', torch.ones(out_features, 1))
        
        if bias:
            self.bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter('bias', None)
    
    @classmethod
    def from_linear(cls, linear_layer, threshold=0.05):
        """Create TernaryLinear from existing nn.Linear"""
        ternary_layer = cls(
            linear_layer.in_features,
            linear_layer.out_features,
            bias=(linear_layer.bias is not None),
            threshold=threshold
        )
        
        # Ternarize weights
        weight = linear_layer.weight.data
        max_val = weight.abs().max()
        threshold_val = threshold * max_val
        
        mask = weight.abs() > threshold_val
        if mask.any():
            scale = weight[mask].abs().mean()
        else:
            scale = 1.0
        
        ternary_weight = torch.zeros_like(weight)
        ternary_weight[weight > threshold_val] = 1
        ternary_weight[weight < -threshold_val] = -1
        
        ternary_layer.weight.data = ternary_weight
        ternary_layer.weight_scale = scale.reshape(1, 1)
        
        if linear_layer.bias is not None:
            ternary_layer.bias.data = linear_layer.bias.data
        
        return ternary_layer
    
    def forward(self, x):
        scaled_weight = self.weight * self.weight_scale
        return F.linear(x, scaled_weight, self.bias)
```

## Experimental Protocol

### Phase 1: Baseline and 3-bit

1. Run baseline (BF16) experiments
2. Confirm 3-bit results match expectations
3. Establish baseline degradation curves

### Phase 2: 2-bit Exploration

1. **Uniform 2-bit (group size 128)**
   ```bash
   bash scripts/quantization/gptq_2bit.sh \
       ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0 128
   ```

2. **Uniform 2-bit (group size 64)**
   ```bash
   bash scripts/quantization/gptq_2bit.sh \
       ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0 64
   ```

3. **Uniform 2-bit (group size 32)**
   ```bash
   bash scripts/quantization/gptq_2bit.sh \
       ./modelzoo/DeepSeek-R1/DeepSeek-R1-Distill-Qwen-1.5B 1 0 32
   ```

4. **Mixed-precision 2-bit**
   - Implement mixed-precision configuration
   - Apply selective quantization

5. **Evaluation**
   - Run on all benchmarks
   - Compare group sizes
   - Analyze degradation patterns

### Phase 3: Ternary Quantization

1. **Ternary with threshold=0.05**
2. **Ternary with threshold=0.03**
3. **Ternary with threshold=0.07**
4. Compare with 2-bit and 1-bit

### Phase 4: 1-bit Binary

1. **Binary with 8-bit activations**
2. **Binary with 16-bit activations**
3. **Mixed-precision binary**
4. Evaluate feasibility

### Evaluation Metrics

For each configuration, measure:

1. **Accuracy**: On all benchmarks (AIME, MATH-500, GSM8K, etc.)
2. **Degradation**: Relative to baseline
3. **Memory**: Model size reduction
4. **Inference Speed**: If applicable
5. **Per-task Analysis**: Which tasks degrade most/least
6. **Layer-wise Impact**: Analyze which layers contribute most to degradation

## Expected Outcomes

### 2-bit Quantization

**Optimistic Scenario:**
- Uniform 2-bit with groupsize=32: 30-40% degradation
- Mixed-precision 2-bit: 20-30% degradation
- Still maintains basic reasoning capability

**Realistic Scenario:**
- Uniform 2-bit: 50-60% degradation
- Mixed-precision 2-bit: 35-45% degradation
- Significant but not catastrophic degradation

**Pessimistic Scenario:**
- Uniform 2-bit: >70% degradation
- Model barely functional for complex reasoning

### 1-bit Quantization

**Optimistic Scenario:**
- Extreme mixed-precision: 50-60% degradation
- Simple tasks (GSM8K) still partially functional

**Realistic Scenario:**
- Even with mixed-precision: >80% degradation
- Only simplest reasoning tasks partially work

**Pessimistic Scenario:**
- Complete failure on reasoning tasks
- Model produces incoherent outputs

## Recommendations

### For 2-bit Quantization

1. **Start with small group sizes** (32 or 64)
2. **Use mixed precision** to protect critical layers
3. **Fine-tune after quantization** on reasoning data
4. **Target specific use cases** where some degradation is acceptable

### For 1-bit Quantization

1. **Begin with ternary** as intermediate step
2. **Use extreme mixed precision** (only MLP layers binary)
3. **Consider quantization-aware training** from scratch
4. **Focus on simple reasoning tasks** initially
5. **May not be practical** for complex reasoning without major algorithmic innovations

## Future Research Directions

1. **Layer-wise sensitivity analysis**: Identify which layers can tolerate extreme quantization
2. **Task-specific quantization**: Different bit allocations for different task types
3. **Dynamic quantization**: Adjust bit-width based on input complexity
4. **Quantization-aware pre-training**: Train model with quantization from start
5. **Hybrid approaches**: Combine with pruning, distillation, or other compression techniques

## Conclusion

Ultra-low bit quantization (2-bit and 1-bit) represents an extreme compression regime that will likely require significant algorithmic innovations to maintain acceptable reasoning performance. The mixed-precision approach and careful selection of quantization targets will be critical for any chance of success.

This guide provides a starting point, but extensive experimentation and potentially new methods will be needed to achieve practical ultra-low bit quantization for reasoning models.
