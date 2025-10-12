#!/usr/bin/env python3
"""
Comprehensive analysis script for quantization experiments.
Generates detailed comparison tables and visualizations for different quantization approaches.
"""

import os
import json
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple
import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available, skipping visualizations")


def read_jsonl(file_path: str) -> List[Dict]:
    """Read JSONL file containing evaluation results."""
    with open(file_path, 'r') as f:
        return json.load(f)


def get_accuracy(data: List[Dict]) -> float:
    """Calculate accuracy from evaluation data."""
    if not data:
        return 0.0
    metric_name = list(data[0]["metrics"].keys())[0]
    correct = sum(1 for item in data if item["metrics"][metric_name])
    return (correct / len(data)) * 100


def analyze_results(output_dir: str, model_name: str, seeds: List[int]) -> Dict:
    """
    Analyze all quantization results for a specific model.
    
    Returns:
        Dictionary with structure: {method: {dataset: {seed: accuracy}}}
    """
    datasets = ["AIME-90", "AIME-2025", "MATH-500", "GSM8K", "GPQA-Diamond", "LiveCodeBench"]
    
    # Define quantization methods grouped by category
    methods_by_category = {
        "Baseline": [
            ("BF16", model_name)
        ],
        "Weight-Only": [
            ("AWQ-W4", f"{model_name}-awq-w4g128-tp1"),
            ("AWQ-W3", f"{model_name}-awq-w3g128-tp1"),
            ("GPTQ-W4", f"{model_name}-gptq-w4g128-tp1"),
            ("GPTQ-W3", f"{model_name}-gptq-w3g128-tp1"),
        ],
        "KV-Cache": [
            ("KVQuant*-KV4", f"{model_name}-kvquant_star-kv4-tp1"),
            ("KVQuant*-KV3", f"{model_name}-kvquant_star-kv3-tp1"),
            ("QuaRot-KV4", f"{model_name}-quarot-kv4-tp1"),
            ("QuaRot-KV3", f"{model_name}-quarot-kv3-tp1"),
        ],
        "Weight-Activation": [
            ("SmoothQuant-W8A8KV8", f"{model_name}-smoothquant-w8a8kv8-tp1"),
            ("QuaRot-W8A8KV8", f"{model_name}-quarot-w8a8kv8-tp1"),
            ("QuaRot-W4A4KV4", f"{model_name}-quarot-w4a4kv4-tp1"),
            ("FlatQuant-W8A8KV8", f"{model_name}-flatquant-w8a8kv8-tp1"),
            ("FlatQuant-W4A4KV4", f"{model_name}-flatquant-w4a4kv4-tp1"),
        ]
    }
    
    results = defaultdict(lambda: defaultdict(dict))
    
    for category, methods in methods_by_category.items():
        for method_name, model_path in methods:
            for seed in seeds:
                result_dir = os.path.join(output_dir, f"{model_path}-seed{seed}")
                
                for dataset in datasets:
                    file_path = os.path.join(result_dir, f"{dataset}.jsonl")
                    
                    if os.path.exists(file_path):
                        try:
                            data = read_jsonl(file_path)
                            acc = get_accuracy(data)
                            results[method_name][dataset][seed] = acc
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
                            results[method_name][dataset][seed] = None
                    else:
                        results[method_name][dataset][seed] = None
    
    return results


def compute_statistics(results: Dict) -> Tuple[Dict, Dict]:
    """Compute mean and std for each method and dataset."""
    stats_mean = defaultdict(dict)
    stats_std = defaultdict(dict)
    
    for method, datasets in results.items():
        for dataset, seeds_data in datasets.items():
            values = [v for v in seeds_data.values() if v is not None]
            
            if values:
                stats_mean[method][dataset] = np.mean(values)
                stats_std[method][dataset] = np.std(values, ddof=1) if len(values) > 1 else 0.0
            else:
                stats_mean[method][dataset] = None
                stats_std[method][dataset] = None
    
    return stats_mean, stats_std


def compute_relative_degradation(stats_mean: Dict, baseline_name: str = "BF16") -> Dict:
    """Compute relative degradation compared to baseline."""
    degradation = defaultdict(dict)
    baseline = stats_mean.get(baseline_name, {})
    
    for method, datasets in stats_mean.items():
        if method == baseline_name:
            continue
            
        for dataset, value in datasets.items():
            if value is not None and baseline.get(dataset) is not None:
                baseline_val = baseline[dataset]
                if baseline_val > 0:
                    degradation[method][dataset] = ((baseline_val - value) / baseline_val) * 100
                else:
                    degradation[method][dataset] = None
            else:
                degradation[method][dataset] = None
    
    return degradation


def print_results_table(stats_mean: Dict, stats_std: Dict, datasets: List[str]):
    """Print results as a formatted markdown table."""
    print("\n" + "="*100)
    print("QUANTIZATION RESULTS - ACCURACY (%)")
    print("="*100 + "\n")
    
    # Header
    header = "| Method | " + " | ".join(datasets) + " | Avg |"
    separator = "|" + "|".join([":---:"] * (len(datasets) + 2)) + "|"
    
    print(header)
    print(separator)
    
    # Data rows
    for method in stats_mean.keys():
        row = [method]
        
        dataset_values = []
        for dataset in datasets:
            mean_val = stats_mean[method].get(dataset)
            std_val = stats_std[method].get(dataset)
            
            if mean_val is not None:
                if std_val is not None and std_val > 0:
                    row.append(f"{mean_val:.2f}±{std_val:.2f}")
                else:
                    row.append(f"{mean_val:.2f}")
                dataset_values.append(mean_val)
            else:
                row.append("-")
        
        # Calculate average
        if dataset_values:
            avg = np.mean(dataset_values)
            row.append(f"{avg:.2f}")
        else:
            row.append("-")
        
        print("| " + " | ".join(row) + " |")
    
    print()


def print_degradation_table(degradation: Dict, datasets: List[str]):
    """Print relative degradation table."""
    print("\n" + "="*100)
    print("RELATIVE DEGRADATION vs BASELINE (%)")
    print("="*100 + "\n")
    
    # Header
    header = "| Method | " + " | ".join(datasets) + " | Avg |"
    separator = "|" + "|".join([":---:"] * (len(datasets) + 2)) + "|"
    
    print(header)
    print(separator)
    
    # Data rows
    for method in degradation.keys():
        row = [method]
        
        dataset_values = []
        for dataset in datasets:
            deg_val = degradation[method].get(dataset)
            
            if deg_val is not None:
                row.append(f"{deg_val:.2f}")
                dataset_values.append(deg_val)
            else:
                row.append("-")
        
        # Calculate average degradation
        if dataset_values:
            avg_deg = np.mean(dataset_values)
            row.append(f"{avg_deg:.2f}")
        else:
            row.append("-")
        
        print("| " + " | ".join(row) + " |")
    
    print()


def plot_comparison_chart(stats_mean: Dict, output_file: str = "quantization_comparison.png"):
    """Generate a comparison chart of different quantization methods."""
    if not HAS_MATPLOTLIB:
        print("Skipping visualization (matplotlib not available)")
        return
    
    datasets = ["AIME-90", "MATH-500", "GSM8K", "GPQA-Diamond"]
    methods = list(stats_mean.keys())
    
    # Prepare data
    data = []
    labels = []
    
    for method in methods:
        method_data = []
        for dataset in datasets:
            val = stats_mean[method].get(dataset)
            method_data.append(val if val is not None else 0)
        data.append(method_data)
        labels.append(method)
    
    # Create grouped bar chart
    x = np.arange(len(datasets))
    width = 0.8 / len(methods)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for i, (method_data, label) in enumerate(zip(data, labels)):
        offset = width * i - (width * len(methods) / 2)
        ax.bar(x + offset, method_data, width, label=label)
    
    ax.set_xlabel('Dataset', fontsize=12)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('Quantization Method Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Comparison chart saved to: {output_file}")


def generate_summary_report(stats_mean: Dict, stats_std: Dict, degradation: Dict, 
                           model_name: str, output_file: str = "quantization_report.md"):
    """Generate a comprehensive markdown report."""
    with open(output_file, 'w') as f:
        f.write(f"# Quantization Analysis Report: {model_name}\n\n")
        f.write(f"Generated: {os.popen('date').read()}\n\n")
        
        f.write("## Overview\n\n")
        f.write("This report summarizes the impact of different quantization approaches on ")
        f.write(f"the {model_name} model across various reasoning benchmarks.\n\n")
        
        f.write("### Quantization Categories\n\n")
        f.write("1. **Weight-Only Quantization**: AWQ, GPTQ (3-bit, 4-bit)\n")
        f.write("2. **KV-Cache Quantization**: KVQuant*, QuaRot-KV (3-bit, 4-bit)\n")
        f.write("3. **Weight-Activation Quantization**: SmoothQuant, QuaRot, FlatQuant (4-bit, 8-bit)\n\n")
        
        # Accuracy table
        f.write("## Accuracy Results\n\n")
        datasets = ["AIME-90", "AIME-2025", "MATH-500", "GSM8K", "GPQA-Diamond", "LiveCodeBench"]
        
        f.write("| Method | " + " | ".join(datasets) + " | Avg |\n")
        f.write("|" + "|".join([":---:"] * (len(datasets) + 2)) + "|\n")
        
        for method in stats_mean.keys():
            row = [method]
            dataset_values = []
            
            for dataset in datasets:
                mean_val = stats_mean[method].get(dataset)
                std_val = stats_std[method].get(dataset)
                
                if mean_val is not None:
                    if std_val is not None and std_val > 0:
                        row.append(f"{mean_val:.2f}±{std_val:.2f}")
                    else:
                        row.append(f"{mean_val:.2f}")
                    dataset_values.append(mean_val)
                else:
                    row.append("-")
            
            if dataset_values:
                avg = np.mean(dataset_values)
                row.append(f"{avg:.2f}")
            else:
                row.append("-")
            
            f.write("| " + " | ".join(row) + " |\n")
        
        # Degradation analysis
        f.write("\n## Relative Degradation vs Baseline\n\n")
        f.write("| Method | " + " | ".join(datasets) + " | Avg |\n")
        f.write("|" + "|".join([":---:"] * (len(datasets) + 2)) + "|\n")
        
        for method in degradation.keys():
            row = [method]
            dataset_values = []
            
            for dataset in datasets:
                deg_val = degradation[method].get(dataset)
                if deg_val is not None:
                    row.append(f"{deg_val:.2f}%")
                    dataset_values.append(deg_val)
                else:
                    row.append("-")
            
            if dataset_values:
                avg_deg = np.mean(dataset_values)
                row.append(f"{avg_deg:.2f}%")
            else:
                row.append("-")
            
            f.write("| " + " | ".join(row) + " |\n")
        
        # Key findings
        f.write("\n## Key Findings\n\n")
        
        # Find best performing methods per category
        categories = {
            "Weight-Only (4-bit)": ["AWQ-W4", "GPTQ-W4"],
            "Weight-Only (3-bit)": ["AWQ-W3", "GPTQ-W3"],
            "KV-Cache (4-bit)": ["KVQuant*-KV4", "QuaRot-KV4"],
            "KV-Cache (3-bit)": ["KVQuant*-KV3", "QuaRot-KV3"],
            "Weight-Activation (8-bit)": ["SmoothQuant-W8A8KV8", "QuaRot-W8A8KV8", "FlatQuant-W8A8KV8"],
            "Weight-Activation (4-bit)": ["QuaRot-W4A4KV4", "FlatQuant-W4A4KV4"]
        }
        
        for cat_name, methods in categories.items():
            best_method = None
            best_avg = -float('inf')
            
            for method in methods:
                if method in stats_mean:
                    values = [v for v in stats_mean[method].values() if v is not None]
                    if values:
                        avg = np.mean(values)
                        if avg > best_avg:
                            best_avg = avg
                            best_method = method
            
            if best_method:
                f.write(f"- **{cat_name}**: {best_method} achieves {best_avg:.2f}% average accuracy\n")
        
        f.write("\n## Recommendations\n\n")
        f.write("Based on the analysis:\n\n")
        f.write("1. **For minimal accuracy loss**: Use weight-only quantization (AWQ/GPTQ 4-bit)\n")
        f.write("2. **For memory efficiency**: Consider KV-cache quantization\n")
        f.write("3. **For maximum compression**: Weight-activation quantization, but expect significant degradation\n")
        f.write("4. **For production use**: 4-bit weight-only quantization offers best accuracy-efficiency trade-off\n\n")
        
        f.write("## Future Work\n\n")
        f.write("To explore 2-bit and 1-bit quantization:\n\n")
        f.write("1. Implement mixed-precision strategies (keep critical layers at higher precision)\n")
        f.write("2. Use smaller group sizes for extreme quantization\n")
        f.write("3. Consider task-specific fine-tuning after quantization\n")
        f.write("4. Investigate ternary quantization as stepping stone to binary\n")
        f.write("5. Analyze per-layer sensitivity to guide mixed-precision decisions\n")
    
    print(f"Comprehensive report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze quantization experiment results")
    parser.add_argument("--output_dir", type=str, default="./outputs/inference",
                       help="Directory containing inference results")
    parser.add_argument("--model_name", type=str, default="DeepSeek-R1-Distill-Qwen-1.5B",
                       help="Model name to analyze")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44],
                       help="Seeds used for evaluation")
    parser.add_argument("--save_report", action="store_true",
                       help="Save comprehensive markdown report")
    parser.add_argument("--plot", action="store_true",
                       help="Generate comparison plots")
    
    args = parser.parse_args()
    
    print(f"Analyzing results for {args.model_name}...")
    print(f"Output directory: {args.output_dir}")
    print(f"Seeds: {args.seeds}\n")
    
    # Analyze results
    results = analyze_results(args.output_dir, args.model_name, args.seeds)
    
    if not results:
        print("No results found! Please run experiments first.")
        return
    
    # Compute statistics
    stats_mean, stats_std = compute_statistics(results)
    degradation = compute_relative_degradation(stats_mean)
    
    # Print tables
    datasets = ["AIME-90", "AIME-2025", "MATH-500", "GSM8K", "GPQA-Diamond", "LiveCodeBench"]
    print_results_table(stats_mean, stats_std, datasets)
    print_degradation_table(degradation, datasets)
    
    # Generate visualizations
    if args.plot:
        plot_comparison_chart(stats_mean, f"quantization_comparison_{args.model_name}.png")
    
    # Save comprehensive report
    if args.save_report:
        generate_summary_report(stats_mean, stats_std, degradation, args.model_name,
                               f"quantization_report_{args.model_name}.md")
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
