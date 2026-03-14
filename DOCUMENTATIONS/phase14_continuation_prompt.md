# Continue Table 1 Replication - Handoff Prompt

**Context:** Replicating Table 1 from "Quantized Reasoning Models" paper (COLM 2025) for DeepSeek-R1-Distill-Qwen-1.5B on machine iZbp1fax8vub5x0s6qvjqbZ.

**Background:** Use with `@/home/zane/.cursor/plans/complete_table_1_replication_b8aba935.plan.md`

---

## Current State (as of 2026-01-27 ~08:00 CST)

### Completed Phases:
- ✅ Phase 11: FlatQuant quantization (W4A4KV4, W8A8KV8)
- ✅ Phase 13: Baseline BF16 evaluation (all 3 seeds, 5/6 benchmarks each)
- ✅ GPTQ W4G128 & W3G128: All seeds complete (5/6 each)
- ✅ AWQ W4G128: All seeds complete (5/6 each)

### Currently Running (2 processes):
1. **phase14c** (GPU 2): AWQ-W3G128 - GSM8K @ ~89%
2. **phase14d** (GPU 3): AWQ-W3G128 - LiveCodeBench (slow due to KV preemption)

### Outstanding Work:
1. **AWQ W3G128**: Finish seeds 43, 44 (currently running)
2. **KV-Cache Models** (0/12 complete): KVQuant* KV3/KV4, QuaRot-KV KV3/KV4
3. **Weight-Activation Models** (0/15 complete): SmoothQuant, QuaRot W8A8/W4A4, FlatQuant W8A8/W4A4
4. **Phase 15**: Generate final Table 1 statistics

### GPU Availability:
- GPU 0: Free
- GPU 1: Free
- GPU 2: Active (phase14c)
- GPU 3: Active (phase14d)

---

## Step 1: Check Running Processes

```bash
# List tmux sessions
tmux list-sessions

# Check GPU status
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv

# Check each process
tmux capture-pane -t phase14c -p | tail -10
tmux capture-pane -t phase14d -p | tail -10

# Check inference outputs
find ./outputs/inference -type d -mindepth 1 -maxdepth 1 | sort | while read dir; do
  name=$(basename "$dir")
  count=$(ls "$dir"/*.jsonl 2>/dev/null | wc -l)
  echo "$name: $count/6"
done
```

---

## Step 2: Start New Processes with ntfy Notifications

### ntfy Setup:
- **Topic**: `qrm-inference-zane`
- **Subscribe**: ntfy.sh/qrm-inference-zane (or ntfy app on phone)
- **Test command**: `curl -s -d "Test message" ntfy.sh/qrm-inference-zane`

### Template for New tmux Session with Notifications:

```bash
TOPIC="qrm-inference-zane"
GPU=1  # or 0

tmux new-session -d -s phase14_kvcache -c /home/zane/Quantized-Reasoning-Models
tmux send-keys -t phase14_kvcache "source .venv/bin/activate && TOPIC=$TOPIC && \\
curl -s -d '🎬 Phase started: KV-Cache models on GPU $GPU' -H 'Title: Phase Started' -H 'Tags: clapper' ntfy.sh/\$TOPIC && \\
for model in kvquant_star-kv4 kvquant_star-kv3 quarot-kv4 quarot-kv3; do \\
  for seed in 42 43 44; do \\
    curl -s -d \"🚀 \$model seed\$seed starting\" -H 'Title: Starting' -H 'Tags: rocket' ntfy.sh/\$TOPIC && \\
    CUDA_VISIBLE_DEVICES=$GPU bash scripts/inference/inference.sh ./outputs/modelzoo/\${model%%-*}/DeepSeek-R1-Distill-Qwen-1.5B-\$model-tp1 $GPU \$seed && \\
    curl -s -d \"✅ \$model seed\$seed completed\" -H 'Title: Completed' -H 'Tags: white_check_mark' ntfy.sh/\$TOPIC; \\
  done; \\
done && \\
curl -s -d '🎉 KV-Cache models COMPLETE!' -H 'Title: Phase Done' -H 'Tags: tada' -H 'Priority: high' ntfy.sh/\$TOPIC" Enter
```

---

## Step 3: Priority Order for Remaining Work

### On GPU 0 - Start KV-Cache Models:

```bash
tmux new-session -d -s phase14_kv -c /home/zane/Quantized-Reasoning-Models
tmux send-keys -t phase14_kv 'source .venv/bin/activate && TOPIC=qrm-inference-zane && \
curl -s -d "🎬 KV-Cache inference started on GPU 0" -H "Title: Phase Started" -H "Tags: clapper" ntfy.sh/$TOPIC && \
for model in kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv4-tp1 \
             kvquant_star/DeepSeek-R1-Distill-Qwen-1.5B-kvquant_star-kv3-tp1 \
             quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv4-tp1 \
             quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-kv3-tp1; do \
  model_name=$(basename $model); \
  for seed in 42 43 44; do \
    curl -s -d "🚀 $model_name seed$seed starting on GPU 0" -H "Title: Starting" -H "Tags: rocket" ntfy.sh/$TOPIC && \
    CUDA_VISIBLE_DEVICES=0 bash scripts/inference/inference.sh ./outputs/modelzoo/$model 0 $seed && \
    curl -s -d "✅ $model_name seed$seed completed" -H "Title: Completed" -H "Tags: white_check_mark" ntfy.sh/$TOPIC; \
  done; \
done && \
curl -s -d "🎉 KV-Cache models COMPLETE on GPU 0!" -H "Title: Phase Done" -H "Tags: tada" -H "Priority: high" ntfy.sh/$TOPIC' Enter
```

### On GPU 1 - Start Weight-Activation Models:

```bash
tmux new-session -d -s phase14_wa -c /home/zane/Quantized-Reasoning-Models
tmux send-keys -t phase14_wa 'source .venv/bin/activate && TOPIC=qrm-inference-zane && \
curl -s -d "🎬 Weight-Activation inference started on GPU 1" -H "Title: Phase Started" -H "Tags: clapper" ntfy.sh/$TOPIC && \
for model in smoothquant/DeepSeek-R1-Distill-Qwen-1.5B-smoothquant-w8a8kv8-tp1 \
             quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w8a8kv8-tp1 \
             quarot/DeepSeek-R1-Distill-Qwen-1.5B-quarot-w4a4kv4-tp1 \
             flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w8a8kv8-tp1 \
             flatquant/DeepSeek-R1-Distill-Qwen-1.5B-flatquant-w4a4kv4-tp1; do \
  model_name=$(basename $model); \
  for seed in 42 43 44; do \
    curl -s -d "🚀 $model_name seed$seed starting on GPU 1" -H "Title: Starting" -H "Tags: rocket" ntfy.sh/$TOPIC && \
    CUDA_VISIBLE_DEVICES=1 bash scripts/inference/inference.sh ./outputs/modelzoo/$model 1 $seed && \
    curl -s -d "✅ $model_name seed$seed completed" -H "Title: Completed" -H "Tags: white_check_mark" ntfy.sh/$TOPIC; \
  done; \
done && \
curl -s -d "🎉 Weight-Activation models COMPLETE on GPU 1!" -H "Title: Phase Done" -H "Tags: tada" -H "Priority: high" ntfy.sh/$TOPIC' Enter
```

---

## Step 4: After All Inference Complete - Generate Table 1

```bash
# Verify all outputs exist (should show 14 models × 3 seeds = 42 directories, each with 5/6 files)
find ./outputs/inference -type d -mindepth 1 -maxdepth 1 | wc -l

# Generate accuracy table
python -m make_stats_table --stats acc --models DeepSeek-R1-Distill-Qwen-1.5B

# Generate response length table
python -m make_stats_table --stats length --models DeepSeek-R1-Distill-Qwen-1.5B
```

---

## Key Paths

| Resource | Path |
|----------|------|
| Workspace | `/home/zane/Quantized-Reasoning-Models` |
| Virtual env | `.venv/bin/activate` |
| Models | `./outputs/modelzoo/{awq,gptq,kvquant_star,quarot,smoothquant,flatquant}/` |
| Inference outputs | `./outputs/inference/` |
| Documentation | `./DOCUMENTATIONS/phase11/` |
| Plan file | `/home/zane/.cursor/plans/complete_table_1_replication_b8aba935.plan.md` |

---

## Reconnection Commands

```bash
# List all sessions
tmux list-sessions

# Attach to a session
tmux attach -t phase14c
tmux attach -t phase14d
tmux attach -t phase14_kv
tmux attach -t phase14_wa

# Quick status check for all
for s in phase14c phase14d phase14_kv phase14_wa; do 
  echo "=== $s ===" 
  tmux capture-pane -t $s -p 2>/dev/null | tail -3
done

# Detach from session: Ctrl+B, then D
```

---

## Important Notes

1. **GPQA-Diamond**: Benchmark skipped (requires HuggingFace approval) - all models show 5/6 benchmarks max

2. **KV Cache Preemption**: Some models (especially W3 variants) experience slower inference due to KV cache memory pressure - this is expected behavior

3. **Checkpointing**: Inference script automatically skips completed benchmarks - safe to restart interrupted runs

4. **ntfy Notifications**: Topic `qrm-inference-zane` - subscribe on phone app to receive completion alerts

5. **Estimated Time**: ~30-44 hours total for remaining work with 2 parallel GPUs

---

## Quick Start for New Chat

1. Check current process status
2. Verify GPU availability (0 and 1 should be free)
3. Start KV-Cache models on GPU 0 with ntfy
4. Start Weight-Activation models on GPU 1 with ntfy
5. Monitor progress via ntfy app
6. Generate Table 1 when all complete
