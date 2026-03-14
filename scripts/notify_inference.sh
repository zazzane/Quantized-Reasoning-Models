#!/bin/bash
# Inference script with ntfy notifications
# Usage: ./notify_inference.sh <model_path> <gpu_id> <seed> <topic>

MODEL_PATH=$1
GPU_ID=$2
SEED=$3
TOPIC=${4:-qrm-inference-zane}

MODEL_NAME=$(basename $MODEL_PATH)

# Send start notification
curl -s -d "🚀 Started: $MODEL_NAME seed$SEED on GPU $GPU_ID" \
  -H "Title: Inference Started" \
  -H "Tags: rocket" \
  ntfy.sh/$TOPIC > /dev/null

# Run inference
CUDA_VISIBLE_DEVICES=$GPU_ID bash scripts/inference/inference.sh $MODEL_PATH $GPU_ID $SEED
EXIT_CODE=$?

# Send completion notification
if [ $EXIT_CODE -eq 0 ]; then
  curl -s -d "✅ Completed: $MODEL_NAME seed$SEED on GPU $GPU_ID" \
    -H "Title: Inference Complete" \
    -H "Tags: white_check_mark" \
    ntfy.sh/$TOPIC > /dev/null
else
  curl -s -d "❌ FAILED: $MODEL_NAME seed$SEED on GPU $GPU_ID (exit code: $EXIT_CODE)" \
    -H "Title: Inference Failed" \
    -H "Priority: high" \
    -H "Tags: x" \
    ntfy.sh/$TOPIC > /dev/null
fi

exit $EXIT_CODE
