# Documentation Structure for Quantization Replication

This document provides a visual overview of the documentation structure and how different components relate to each other.

## 📚 Documentation Hierarchy

```
Quantized-Reasoning-Models/
│
├── 🎯 QUICK REFERENCES
│   ├── REPLICATION_QUICKSTART.md         ⭐ START HERE
│   │   └── Overview of all docs and quick commands
│   └── QUICK_START_1.5B.md
│       └── Condensed command reference
│
├── 📖 MAIN GUIDES
│   ├── README.md                          ⭐ MAIN ENTRY
│   │   ├── Project overview
│   │   ├── Installation instructions
│   │   └── Links to all other docs
│   │
│   ├── REPLICATION_GUIDE_1.5B.md         ⭐ STEP-BY-STEP
│   │   ├── Detailed replication instructions
│   │   ├── Prerequisites
│   │   ├── All quantization methods
│   │   └── Evaluation procedures
│   │
│   └── IMPLEMENTATION_SUMMARY.md
│       ├── Technical implementation details
│       ├── Code structure
│       └── Design decisions
│
├── 📋 OUTPUT TEMPLATES
│   ├── REPLICATION_OUTPUTS.md            ⭐ RESULTS
│   │   ├── Accuracy tables (all methods)
│   │   ├── Performance metrics
│   │   ├── Degradation analysis
│   │   └── Model size comparisons
│   │
│   └── RESOURCE_BENCHMARKING.md          ⭐ RESOURCES
│       ├── Hardware specifications
│       ├── Runtime metrics
│       ├── Memory usage
│       └── Power consumption
│
├── 🔬 RESEARCH GUIDE
│   └── ULTRA_LOW_BIT_QUANTIZATION.md
│       ├── 2-bit quantization approaches
│       ├── 1-bit quantization strategies
│       ├── Implementation roadmap
│       └── Expected outcomes
│
└── 🛠️ TOOLS DOCUMENTATION
    └── scripts/README_REPLICATION.md      ⭐ SCRIPTS
        ├── Tool usage instructions
        ├── Complete workflow
        ├── Troubleshooting
        └── Hardware recommendations
```

---

## 🔄 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    REPLICATION WORKFLOW                      │
└─────────────────────────────────────────────────────────────┘

PHASE 1: PREPARATION
┌──────────────────┐
│ Read Documentation│
│ - README.md      │
│ - REPLICATION_   │
│   QUICKSTART.md  │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Setup Environment│
│ - Install deps   │
│ - Download model │
│ - Get datasets   │
└────────┬─────────┘
         │
         v
PHASE 2: EXECUTION
┌──────────────────┐
│ Start Monitoring │◄─────────────┐
│ monitor_         │              │
│ resources.py     │              │
└────────┬─────────┘              │
         │                        │
         v                        │
┌──────────────────┐              │
│ Run Experiments  │              │
│ run_all_         │              │
│ quantization_    │              │
│ 1.5b.sh          │              │
└────────┬─────────┘              │
         │                        │
         v                        │
┌──────────────────┐              │
│ Quantization     │              │
│ (4-8 hours)      │──────────────┤
│ - AWQ            │              │
│ - GPTQ           │              │
│ - KVQuant*       │   Resource   │
│ - QuaRot-KV      │   Monitoring │
│ - SmoothQuant    │   (Parallel) │
│ - QuaRot         │              │
│ - FlatQuant      │              │
└────────┬─────────┘              │
         │                        │
         v                        │
┌──────────────────┐              │
│ Evaluation       │              │
│ (22-33 hours)    │──────────────┤
│ - Baseline       │              │
│ - 13 Methods     │              │
│ - 6 Benchmarks   │              │
│ - 3 Seeds each   │              │
└────────┬─────────┘              │
         │                        │
         └────────────────────────┘
         │
         v
PHASE 3: ANALYSIS
┌──────────────────┐
│ Stop Monitoring  │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Analyze Resources│
│ monitor_         │
│ resources.py     │
│ --analyze        │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Analyze Results  │
│ analyze_         │
│ quantization_    │
│ results.py       │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Extract Metrics  │
│ extract_metrics_ │
│ to_docs.py       │
└────────┬─────────┘
         │
         v
PHASE 4: DOCUMENTATION
┌──────────────────┐
│ Fill Templates   │
│ - REPLICATION_   │
│   OUTPUTS.md     │
│ - RESOURCE_      │
│   BENCHMARKING.md│
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Review & Validate│
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Publish Results  │
└──────────────────┘
```

---

## 🎯 Document Usage Map

### When to Use Each Document

```
Starting Out?
  └─> REPLICATION_QUICKSTART.md
        ├─> Need details? ─> REPLICATION_GUIDE_1.5B.md
        ├─> Need commands? ─> QUICK_START_1.5B.md
        └─> Need overview? ─> README.md

Running Experiments?
  └─> scripts/README_REPLICATION.md
        ├─> Using tools? ─> Scripts documentation
        ├─> Debugging? ─> Troubleshooting section
        └─> Questions? ─> FAQ section

Analyzing Results?
  └─> scripts/README_REPLICATION.md
        ├─> Resource logs ─> monitor_resources.py --analyze
        ├─> Accuracy data ─> analyze_quantization_results.py
        └─> Fill templates ─> extract_metrics_to_docs.py

Documenting Outputs?
  └─> REPLICATION_OUTPUTS.md
        ├─> Quantization details per method
        ├─> Accuracy tables per benchmark
        └─> Summary and recommendations

Documenting Resources?
  └─> RESOURCE_BENCHMARKING.md
        ├─> Hardware specs
        ├─> Runtime metrics
        └─> Cost analysis

Planning Future Work?
  └─> ULTRA_LOW_BIT_QUANTIZATION.md
        ├─> 2-bit approaches
        ├─> 1-bit strategies
        └─> Implementation guide

Understanding Implementation?
  └─> IMPLEMENTATION_SUMMARY.md
        ├─> Code structure
        ├─> Design decisions
        └─> Technical details
```

---

## 📊 Data Flow Diagram

```
INPUT DATA
┌─────────────────────────────────────┐
│ Model: DeepSeek-R1-Distill-Qwen-1.5B│
│ Size: ~3GB                           │
└──────────────┬──────────────────────┘
               │
               v
┌─────────────────────────────────────┐
│ Datasets                             │
│ - AIME (2024, 2025, 90)             │
│ - MATH-500                           │
│ - GSM8K                              │
│ - GPQA-Diamond                       │
│ Size: ~10-15GB                       │
└──────────────┬──────────────────────┘
               │
               v
         QUANTIZATION
               │
    ┌──────────┼──────────┐
    │          │          │
    v          v          v
┌────────┐ ┌───────┐ ┌──────────┐
│Weight  │ │KV     │ │Weight-   │
│Only    │ │Cache  │ │Activation│
│- AWQ   │ │-KVQ*  │ │-Smooth   │
│- GPTQ  │ │-QRot  │ │-QuaRot   │
│        │ │-KV    │ │-Flat     │
└───┬────┘ └───┬───┘ └────┬─────┘
    │          │          │
    └──────────┼──────────┘
               │
               v
      QUANTIZED MODELS
      (outputs/modelzoo/)
      Size: ~10-15GB
               │
               v
         EVALUATION
         (6 benchmarks)
         (3 seeds each)
               │
    ┌──────────┼──────────┐
    │          │          │
    v          v          v
┌────────┐ ┌───────┐ ┌──────────┐
│Accuracy│ │Speed  │ │Quality   │
│Results │ │Metrics│ │Analysis  │
└───┬────┘ └───┬───┘ └────┬─────┘
    │          │          │
    └──────────┼──────────┘
               │
               v
      OUTPUT DATA
      ┌─────────────────────────┐
      │ outputs/inference/      │
      │ - JSON results          │
      │ - Accuracy scores       │
      │ - Response lengths      │
      └───────────┬─────────────┘
                  │
                  v
      ┌─────────────────────────┐
      │ logs/                   │
      │ - resource_monitor.log  │
      │ - GPU/CPU metrics       │
      │ - Memory usage          │
      │ - Power consumption     │
      └───────────┬─────────────┘
                  │
                  v
           ANALYSIS
      ┌─────────────────────────┐
      │ - Statistical analysis  │
      │ - Degradation calc      │
      │ - Comparison tables     │
      │ - Visualization plots   │
      └───────────┬─────────────┘
                  │
                  v
        DOCUMENTATION
      ┌─────────────────────────┐
      │ REPLICATION_OUTPUTS.md  │
      │ - Filled tables         │
      │ - Analysis results      │
      │ - Recommendations       │
      └─────────────────────────┘
      ┌─────────────────────────┐
      │ RESOURCE_BENCHMARKING.md│
      │ - Hardware specs        │
      │ - Runtime data          │
      │ - Cost analysis         │
      └─────────────────────────┘
```

---

## 🔧 Tools and Their Outputs

```
┌─────────────────────────────────────────────────────────┐
│                    TOOL ECOSYSTEM                        │
└─────────────────────────────────────────────────────────┘

Tool: monitor_resources.py
├─ Input: None (monitors system)
├─ Output:
│  ├─ logs/resource_monitor.log (CSV)
│  └─ logs/resource_summary.md (Markdown)
└─ Used: During experiments (parallel)

Tool: run_all_quantization_1.5b.sh
├─ Input: Model path, GPU device
├─ Output:
│  ├─ outputs/modelzoo/ (quantized models)
│  ├─ outputs/inference/ (evaluation results)
│  └─ logs/ (execution logs)
└─ Used: Main experiment execution

Tool: analyze_quantization_results.py
├─ Input: outputs/inference/
├─ Output:
│  ├─ Console tables
│  ├─ outputs/analysis/quantization_analysis.md
│  └─ outputs/analysis/plots/ (PNG)
└─ Used: After experiments

Tool: extract_metrics_to_docs.py
├─ Input:
│  ├─ outputs/inference/
│  ├─ outputs/modelzoo/
│  └─ logs/
├─ Output:
│  ├─ filled_docs/REPLICATION_OUTPUTS_FILLED.md
│  └─ filled_docs/RESOURCE_BENCHMARKING_FILLED.md
└─ Used: After analysis

Templates:
├─ REPLICATION_OUTPUTS.md
│  └─ Filled by: extract_metrics_to_docs.py + manual
└─ RESOURCE_BENCHMARKING.md
   └─ Filled by: monitor_resources.py + manual
```

---

## 📈 Quantization Methods Coverage

```
┌─────────────────────────────────────────────────────────┐
│              13 QUANTIZATION METHODS                     │
└─────────────────────────────────────────────────────────┘

1. Baseline (BF16)
   └─ No quantization, reference point

2-5. Weight-Only (4 methods)
   ├─ AWQ W3A16KV16
   ├─ AWQ W4A16KV16
   ├─ GPTQ W3A16KV16
   └─ GPTQ W4A16KV16

6-9. KV-Cache (4 methods)
   ├─ KVQuant* W16A16KV3
   ├─ KVQuant* W16A16KV4
   ├─ QuaRot-KV W16A16KV3
   └─ QuaRot-KV W16A16KV4

10-13. Weight-Activation (4 methods)
   ├─ SmoothQuant W8A8KV8
   ├─ QuaRot W4A4KV4
   ├─ QuaRot W8A8KV8
   ├─ FlatQuant W4A4KV4
   └─ FlatQuant W8A8KV8

Each method evaluated on:
├─ 6 benchmarks
│  ├─ AIME-2024 (30 questions)
│  ├─ AIME-2025 (30 questions)
│  ├─ AIME-90 (90 questions)
│  ├─ MATH-500 (500 problems)
│  ├─ GSM8K (1,319 questions)
│  └─ GPQA-Diamond (198 questions)
└─ 3 seeds (42, 43, 44)

Total evaluations: 14 models × 6 benchmarks × 3 seeds = 252 runs
```

---

## 🎓 Reading Path by User Type

### For Researchers (Understanding Methods)
1. README.md - Project overview
2. Paper (arXiv:2504.04823) - Theoretical background
3. IMPLEMENTATION_SUMMARY.md - Technical details
4. REPLICATION_GUIDE_1.5B.md - Experimental setup
5. ULTRA_LOW_BIT_QUANTIZATION.md - Future directions

### For Practitioners (Running Experiments)
1. REPLICATION_QUICKSTART.md - Quick overview
2. scripts/README_REPLICATION.md - Tool documentation
3. REPLICATION_GUIDE_1.5B.md - Step-by-step instructions
4. QUICK_START_1.5B.md - Command reference

### For Documenters (Recording Results)
1. REPLICATION_QUICKSTART.md - Overview
2. REPLICATION_OUTPUTS.md - Output template
3. RESOURCE_BENCHMARKING.md - Resource template
4. scripts/README_REPLICATION.md - Tool usage

### For Beginners (First Time)
1. REPLICATION_QUICKSTART.md - Start here!
2. README.md - Installation and basics
3. QUICK_START_1.5B.md - Quick commands
4. scripts/README_REPLICATION.md - Full workflow

---

## 🎯 Key Takeaways

### Documentation is Complete ✅
- All templates created
- All tools implemented
- All workflows documented
- Ready for immediate use

### Clear Structure ✅
- Logical hierarchy
- Clear usage paths
- Cross-references
- No ambiguity

### Comprehensive Coverage ✅
- 13 quantization methods
- 6 evaluation benchmarks
- Hardware specifications
- Resource tracking
- Cost analysis

### Production Ready ✅
- Executable scripts
- Error handling
- Monitoring tools
- Analysis automation

---

## 📞 Quick Help Reference

```
Need                          → See Document
───────────────────────────────────────────────
Quick overview               → REPLICATION_QUICKSTART.md
Installation guide           → README.md
Step-by-step instructions    → REPLICATION_GUIDE_1.5B.md
Quick commands               → QUICK_START_1.5B.md
Tool usage                   → scripts/README_REPLICATION.md
Output template              → REPLICATION_OUTPUTS.md
Resource template            → RESOURCE_BENCHMARKING.md
Future research              → ULTRA_LOW_BIT_QUANTIZATION.md
Technical details            → IMPLEMENTATION_SUMMARY.md
```

---

*This documentation structure ensures comprehensive coverage while maintaining clarity and accessibility.*
