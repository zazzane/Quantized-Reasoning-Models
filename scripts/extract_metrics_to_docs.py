#!/usr/bin/env python3
"""
Extract Metrics to Documentation

This script helps populate the REPLICATION_OUTPUTS.md and RESOURCE_BENCHMARKING.md
templates with actual experimental results.

It reads:
1. Inference results from outputs/inference/
2. Resource monitoring logs from logs/
3. Model size information from outputs/modelzoo/

And generates filled templates with actual data.

Usage:
    python scripts/extract_metrics_to_docs.py \
        --model DeepSeek-R1-Distill-Qwen-1.5B \
        --output-dir ./filled_docs
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path


class MetricsExtractor:
    """Extract metrics from experiment outputs and populate documentation."""
    
    def __init__(self, model_name, inference_dir="outputs/inference", 
                 resource_dir="logs", output_dir="filled_docs"):
        """
        Initialize metrics extractor.
        
        Args:
            model_name: Name of the model (e.g., "DeepSeek-R1-Distill-Qwen-1.5B")
            inference_dir: Directory containing inference results
            resource_dir: Directory containing resource monitoring logs
            output_dir: Directory to save filled documentation
        """
        self.model_name = model_name
        self.inference_dir = Path(inference_dir)
        self.resource_dir = Path(resource_dir)
        self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.benchmarks = [
            "aime:2024",
            "aime:2025", 
            "aime:90",
            "math:500",
            "gsm8k",
            "gpqa:diamond"
        ]
        
        self.methods = {
            "baseline": "Baseline (BF16)",
            "awq-w4g128": "AWQ W4A16KV16",
            "awq-w3g128": "AWQ W3A16KV16",
            "gptq-w4g128": "GPTQ W4A16KV16",
            "gptq-w3g128": "GPTQ W3A16KV16",
            "kvquant_star-kv4": "KVQuant* W16A16KV4",
            "kvquant_star-kv3": "KVQuant* W16A16KV3",
            "quarot-kv4": "QuaRot-KV W16A16KV4",
            "quarot-kv3": "QuaRot-KV W16A16KV3",
            "smoothquant-w8a8kv8": "SmoothQuant W8A8KV8",
            "quarot-w8a8kv8": "QuaRot W8A8KV8",
            "quarot-w4a4kv4": "QuaRot W4A4KV4",
            "flatquant-w8a8kv8": "FlatQuant W8A8KV8",
            "flatquant-w4a4kv4": "FlatQuant W4A4KV4",
        }
    
    def extract_inference_results(self):
        """
        Extract accuracy results from inference outputs.
        
        Returns:
            dict: Nested dict of {method: {benchmark: {seed: accuracy}}}
        """
        results = defaultdict(lambda: defaultdict(dict))
        
        if not self.inference_dir.exists():
            print(f"Warning: Inference directory not found: {self.inference_dir}")
            return results
        
        # Look for JSON result files
        for json_file in self.inference_dir.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Extract method, benchmark, seed from filename or data
                # This is a simplified parser - adjust based on actual file structure
                filename = json_file.stem
                
                # Parse filename (e.g., "results_baseline_aime2024_seed42.json")
                parts = filename.split('_')
                
                # Extract accuracy from data
                if 'accuracy' in data:
                    accuracy = data['accuracy']
                elif 'results' in data:
                    accuracy = data['results'].get('accuracy', 0.0)
                else:
                    continue
                
                # Store result
                # results[method][benchmark][seed] = accuracy
                
            except Exception as e:
                print(f"Warning: Error reading {json_file}: {e}")
        
        return results
    
    def calculate_statistics(self, values):
        """Calculate mean and std dev from list of values."""
        if not values:
            return None, None
        
        mean = sum(values) / len(values)
        
        if len(values) > 1:
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std = variance ** 0.5
        else:
            std = 0.0
        
        return mean, std
    
    def extract_model_sizes(self):
        """
        Extract model sizes from outputs/modelzoo/.
        
        Returns:
            dict: {method: size_in_gb}
        """
        sizes = {}
        modelzoo_dir = Path("outputs/modelzoo")
        
        if not modelzoo_dir.exists():
            print(f"Warning: Modelzoo directory not found: {modelzoo_dir}")
            return sizes
        
        for method_dir in modelzoo_dir.iterdir():
            if method_dir.is_dir():
                # Calculate directory size
                total_size = sum(f.stat().st_size for f in method_dir.rglob('*') if f.is_file())
                size_gb = total_size / (1024**3)
                
                method_name = method_dir.name
                sizes[method_name] = size_gb
        
        return sizes
    
    def generate_outputs_doc(self, results, sizes):
        """
        Generate filled REPLICATION_OUTPUTS.md.
        
        Args:
            results: Inference results
            sizes: Model sizes
        """
        output_file = self.output_dir / "REPLICATION_OUTPUTS_FILLED.md"
        
        print(f"Generating outputs documentation: {output_file}")
        
        # Read template
        template_file = Path("REPLICATION_OUTPUTS.md")
        if not template_file.exists():
            print(f"Error: Template not found: {template_file}")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Fill in results
        # This is a simplified example - you would need to parse the template
        # and fill in tables programmatically
        
        # For now, just add a summary section at the end
        summary = "\n\n---\n\n## Auto-Generated Summary\n\n"
        summary += f"**Model**: {self.model_name}\n\n"
        summary += "### Extracted Results\n\n"
        
        if results:
            summary += "| Method | Benchmark | Mean Accuracy | Std Dev |\n"
            summary += "|--------|-----------|---------------|----------|\n"
            
            for method, benchmarks in results.items():
                for benchmark, seeds in benchmarks.items():
                    values = list(seeds.values())
                    mean, std = self.calculate_statistics(values)
                    if mean is not None:
                        summary += f"| {method} | {benchmark} | {mean:.2f}% | ±{std:.2f}% |\n"
        else:
            summary += "*No inference results found. Run experiments first.*\n"
        
        summary += "\n### Model Sizes\n\n"
        if sizes:
            summary += "| Method | Size (GB) |\n"
            summary += "|--------|-----------|\n"
            for method, size in sorted(sizes.items()):
                summary += f"| {method} | {size:.2f} |\n"
        else:
            summary += "*No model size information found.*\n"
        
        # Append summary to template
        with open(output_file, 'w') as f:
            f.write(content)
            f.write(summary)
        
        print(f"Documentation saved to: {output_file}")
    
    def generate_resource_doc(self):
        """Generate filled RESOURCE_BENCHMARKING.md."""
        output_file = self.output_dir / "RESOURCE_BENCHMARKING_FILLED.md"
        
        print(f"Generating resource documentation: {output_file}")
        
        # Read template
        template_file = Path("RESOURCE_BENCHMARKING.md")
        if not template_file.exists():
            print(f"Error: Template not found: {template_file}")
            return
        
        with open(template_file, 'r') as f:
            content = f.read()
        
        # Look for resource monitoring logs
        summary = "\n\n---\n\n## Auto-Generated Summary\n\n"
        
        resource_logs = list(self.resource_dir.glob("resource_monitor*.log"))
        if resource_logs:
            summary += f"**Resource Logs Found**: {len(resource_logs)}\n\n"
            for log in resource_logs:
                summary += f"- {log.name}\n"
        else:
            summary += "*No resource monitoring logs found. Use `python scripts/monitor_resources.py` during experiments.*\n"
        
        # Append to template
        with open(output_file, 'w') as f:
            f.write(content)
            f.write(summary)
        
        print(f"Documentation saved to: {output_file}")
    
    def run(self):
        """Run the extraction and documentation generation."""
        print("=" * 60)
        print("Extracting Metrics for Documentation")
        print("=" * 60)
        print(f"Model: {self.model_name}")
        print(f"Inference Dir: {self.inference_dir}")
        print(f"Resource Dir: {self.resource_dir}")
        print(f"Output Dir: {self.output_dir}")
        print()
        
        # Extract data
        print("Extracting inference results...")
        results = self.extract_inference_results()
        
        print("Extracting model sizes...")
        sizes = self.extract_model_sizes()
        
        # Generate documentation
        print("\nGenerating documentation...")
        self.generate_outputs_doc(results, sizes)
        self.generate_resource_doc()
        
        print("\n" + "=" * 60)
        print("Documentation generation complete!")
        print("=" * 60)
        print(f"\nFilled templates are in: {self.output_dir}/")
        print("\nNext steps:")
        print("1. Review the auto-generated summaries")
        print("2. Manually fill in remaining details in the templates")
        print("3. Copy filled templates to the main documentation")


def main():
    parser = argparse.ArgumentParser(
        description="Extract metrics and populate documentation templates"
    )
    
    parser.add_argument(
        '--model',
        default='DeepSeek-R1-Distill-Qwen-1.5B',
        help='Model name'
    )
    
    parser.add_argument(
        '--inference-dir',
        default='outputs/inference',
        help='Directory containing inference results'
    )
    
    parser.add_argument(
        '--resource-dir',
        default='logs',
        help='Directory containing resource monitoring logs'
    )
    
    parser.add_argument(
        '--output-dir',
        default='filled_docs',
        help='Directory to save filled documentation'
    )
    
    args = parser.parse_args()
    
    extractor = MetricsExtractor(
        model_name=args.model,
        inference_dir=args.inference_dir,
        resource_dir=args.resource_dir,
        output_dir=args.output_dir
    )
    
    extractor.run()


if __name__ == '__main__':
    main()
