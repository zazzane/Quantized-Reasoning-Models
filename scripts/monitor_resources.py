#!/usr/bin/env python3
"""
Resource Monitoring Script for Quantization Experiments

This script monitors GPU, CPU, memory, and disk usage during quantization experiments.
It logs metrics to a file for later analysis and inclusion in RESOURCE_BENCHMARKING.md.

Usage:
    # Start monitoring
    python scripts/monitor_resources.py --output logs/resource_monitor.log --interval 1
    
    # Monitor specific process
    python scripts/monitor_resources.py --output logs/resource_monitor.log --pid 12345
    
    # Generate summary report
    python scripts/monitor_resources.py --analyze logs/resource_monitor.log --report logs/resource_summary.md
"""

import argparse
import csv
import datetime
import os
import sys
import time
from pathlib import Path

try:
    import psutil
except ImportError:
    print("Error: psutil not installed. Install with: pip install psutil")
    sys.exit(1)

try:
    import pynvml
    NVIDIA_GPU_AVAILABLE = True
    pynvml.nvmlInit()
except (ImportError, pynvml.NVMLError):
    NVIDIA_GPU_AVAILABLE = False
    print("Warning: NVIDIA GPU monitoring not available")


class ResourceMonitor:
    """Monitor system resources during experiments."""
    
    def __init__(self, output_file, interval=1, pid=None):
        """
        Initialize resource monitor.
        
        Args:
            output_file: Path to output CSV file
            interval: Sampling interval in seconds
            pid: Process ID to monitor (optional)
        """
        self.output_file = output_file
        self.interval = interval
        self.pid = pid
        self.process = None
        
        if pid:
            try:
                self.process = psutil.Process(pid)
            except psutil.NoSuchProcess:
                print(f"Error: Process {pid} not found")
                sys.exit(1)
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        
        # Initialize CSV file with headers
        self._init_csv()
    
    def _init_csv(self):
        """Initialize CSV file with headers."""
        headers = [
            'timestamp',
            'cpu_percent',
            'cpu_count',
            'memory_used_gb',
            'memory_total_gb',
            'memory_percent',
            'disk_read_mb',
            'disk_write_mb',
        ]
        
        if self.process:
            headers.extend([
                'process_cpu_percent',
                'process_memory_gb',
                'process_memory_percent',
            ])
        
        if NVIDIA_GPU_AVAILABLE:
            device_count = pynvml.nvmlDeviceGetCount()
            for i in range(device_count):
                headers.extend([
                    f'gpu{i}_utilization',
                    f'gpu{i}_memory_used_gb',
                    f'gpu{i}_memory_total_gb',
                    f'gpu{i}_memory_percent',
                    f'gpu{i}_power_watts',
                    f'gpu{i}_temperature_c',
                ])
        
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    
    def _get_gpu_metrics(self):
        """Get GPU metrics from all available GPUs."""
        metrics = {}
        
        if not NVIDIA_GPU_AVAILABLE:
            return metrics
        
        try:
            device_count = pynvml.nvmlDeviceGetCount()
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                
                # Utilization
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                metrics[f'gpu{i}_utilization'] = util.gpu
                
                # Memory
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                metrics[f'gpu{i}_memory_used_gb'] = mem.used / (1024**3)
                metrics[f'gpu{i}_memory_total_gb'] = mem.total / (1024**3)
                metrics[f'gpu{i}_memory_percent'] = (mem.used / mem.total) * 100
                
                # Power
                try:
                    power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # mW to W
                    metrics[f'gpu{i}_power_watts'] = power
                except pynvml.NVMLError:
                    metrics[f'gpu{i}_power_watts'] = 0
                
                # Temperature
                try:
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    metrics[f'gpu{i}_temperature_c'] = temp
                except pynvml.NVMLError:
                    metrics[f'gpu{i}_temperature_c'] = 0
        
        except pynvml.NVMLError as e:
            print(f"Warning: Error reading GPU metrics: {e}")
        
        return metrics
    
    def _get_system_metrics(self):
        """Get system-wide metrics."""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_count = psutil.cpu_count()
        
        # Memory
        mem = psutil.virtual_memory()
        memory_used_gb = mem.used / (1024**3)
        memory_total_gb = mem.total / (1024**3)
        memory_percent = mem.percent
        
        # Disk I/O
        disk = psutil.disk_io_counters()
        disk_read_mb = disk.read_bytes / (1024**2) if disk else 0
        disk_write_mb = disk.write_bytes / (1024**2) if disk else 0
        
        return {
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'memory_used_gb': memory_used_gb,
            'memory_total_gb': memory_total_gb,
            'memory_percent': memory_percent,
            'disk_read_mb': disk_read_mb,
            'disk_write_mb': disk_write_mb,
        }
    
    def _get_process_metrics(self):
        """Get process-specific metrics."""
        if not self.process:
            return {}
        
        try:
            # CPU
            process_cpu_percent = self.process.cpu_percent(interval=None)
            
            # Memory
            mem = self.process.memory_info()
            process_memory_gb = mem.rss / (1024**3)
            
            # Memory percent
            process_memory_percent = self.process.memory_percent()
            
            return {
                'process_cpu_percent': process_cpu_percent,
                'process_memory_gb': process_memory_gb,
                'process_memory_percent': process_memory_percent,
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}
    
    def sample(self):
        """Sample all metrics once."""
        timestamp = datetime.datetime.now().isoformat()
        
        metrics = {'timestamp': timestamp}
        metrics.update(self._get_system_metrics())
        metrics.update(self._get_process_metrics())
        metrics.update(self._get_gpu_metrics())
        
        return metrics
    
    def monitor(self, duration=None):
        """
        Monitor resources continuously.
        
        Args:
            duration: Maximum duration in seconds (None for indefinite)
        """
        print(f"Monitoring resources every {self.interval}s...")
        print(f"Logging to: {self.output_file}")
        print("Press Ctrl+C to stop")
        
        start_time = time.time()
        sample_count = 0
        
        try:
            while True:
                metrics = self.sample()
                
                # Write to CSV
                with open(self.output_file, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=metrics.keys())
                    writer.writerow(metrics)
                
                sample_count += 1
                
                # Print summary every 10 samples
                if sample_count % 10 == 0:
                    elapsed = time.time() - start_time
                    print(f"[{elapsed:.1f}s] Samples: {sample_count}, "
                          f"CPU: {metrics['cpu_percent']:.1f}%, "
                          f"Mem: {metrics['memory_used_gb']:.1f}/{metrics['memory_total_gb']:.1f}GB", end='')
                    
                    if NVIDIA_GPU_AVAILABLE and 'gpu0_utilization' in metrics:
                        print(f", GPU: {metrics['gpu0_utilization']:.0f}% "
                              f"({metrics['gpu0_memory_used_gb']:.1f}/{metrics['gpu0_memory_total_gb']:.1f}GB)", end='')
                    print()
                
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                
                time.sleep(self.interval)
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        
        print(f"\nTotal samples collected: {sample_count}")
        print(f"Total duration: {time.time() - start_time:.1f}s")


class ResourceAnalyzer:
    """Analyze resource monitoring logs and generate reports."""
    
    def __init__(self, log_file):
        """Initialize analyzer with log file."""
        self.log_file = log_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from CSV log file."""
        data = []
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for key, value in row.items():
                    if key != 'timestamp':
                        try:
                            row[key] = float(value)
                        except ValueError:
                            pass
                data.append(row)
        return data
    
    def get_summary_stats(self, metric):
        """Get summary statistics for a metric."""
        values = [row[metric] for row in self.data if metric in row and row[metric] != '']
        
        if not values:
            return None
        
        return {
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / len(values),
            'samples': len(values),
        }
    
    def generate_report(self, output_file):
        """Generate markdown report with summary statistics."""
        print(f"Generating report: {output_file}")
        
        with open(output_file, 'w') as f:
            f.write("# Resource Monitoring Report\n\n")
            f.write(f"**Log File**: {self.log_file}\n")
            f.write(f"**Total Samples**: {len(self.data)}\n")
            
            if self.data:
                start_time = self.data[0]['timestamp']
                end_time = self.data[-1]['timestamp']
                f.write(f"**Start Time**: {start_time}\n")
                f.write(f"**End Time**: {end_time}\n")
            
            f.write("\n## System Metrics\n\n")
            
            # CPU
            cpu_stats = self.get_summary_stats('cpu_percent')
            if cpu_stats:
                f.write("### CPU\n\n")
                f.write(f"- Average: {cpu_stats['mean']:.1f}%\n")
                f.write(f"- Peak: {cpu_stats['max']:.1f}%\n")
                f.write(f"- Minimum: {cpu_stats['min']:.1f}%\n\n")
            
            # Memory
            mem_stats = self.get_summary_stats('memory_used_gb')
            if mem_stats:
                f.write("### Memory\n\n")
                f.write(f"- Average Used: {mem_stats['mean']:.2f} GB\n")
                f.write(f"- Peak Used: {mem_stats['max']:.2f} GB\n")
                f.write(f"- Minimum Used: {mem_stats['min']:.2f} GB\n\n")
            
            # GPU
            if any('gpu0_utilization' in row for row in self.data):
                f.write("## GPU Metrics\n\n")
                
                gpu_util_stats = self.get_summary_stats('gpu0_utilization')
                if gpu_util_stats:
                    f.write("### GPU Utilization\n\n")
                    f.write(f"- Average: {gpu_util_stats['mean']:.1f}%\n")
                    f.write(f"- Peak: {gpu_util_stats['max']:.1f}%\n")
                    f.write(f"- Minimum: {gpu_util_stats['min']:.1f}%\n\n")
                
                gpu_mem_stats = self.get_summary_stats('gpu0_memory_used_gb')
                if gpu_mem_stats:
                    f.write("### GPU Memory\n\n")
                    f.write(f"- Average Used: {gpu_mem_stats['mean']:.2f} GB\n")
                    f.write(f"- Peak Used: {gpu_mem_stats['max']:.2f} GB\n")
                    f.write(f"- Minimum Used: {gpu_mem_stats['min']:.2f} GB\n\n")
                
                gpu_power_stats = self.get_summary_stats('gpu0_power_watts')
                if gpu_power_stats:
                    f.write("### GPU Power\n\n")
                    f.write(f"- Average: {gpu_power_stats['mean']:.1f} W\n")
                    f.write(f"- Peak: {gpu_power_stats['max']:.1f} W\n")
                    f.write(f"- Minimum: {gpu_power_stats['min']:.1f} W\n\n")
        
        print(f"Report saved to: {output_file}")
    
    def print_summary(self):
        """Print summary to console."""
        print("\n=== Resource Monitoring Summary ===\n")
        print(f"Log File: {self.log_file}")
        print(f"Total Samples: {len(self.data)}")
        
        if self.data:
            print(f"Start Time: {self.data[0]['timestamp']}")
            print(f"End Time: {self.data[-1]['timestamp']}")
        
        print("\n--- System Metrics ---")
        
        cpu_stats = self.get_summary_stats('cpu_percent')
        if cpu_stats:
            print(f"\nCPU Utilization:")
            print(f"  Average: {cpu_stats['mean']:.1f}%")
            print(f"  Peak: {cpu_stats['max']:.1f}%")
        
        mem_stats = self.get_summary_stats('memory_used_gb')
        mem_total_stats = self.get_summary_stats('memory_total_gb')
        if mem_stats and mem_total_stats:
            print(f"\nMemory:")
            print(f"  Total: {mem_total_stats['mean']:.1f} GB")
            print(f"  Average Used: {mem_stats['mean']:.2f} GB ({(mem_stats['mean']/mem_total_stats['mean']*100):.1f}%)")
            print(f"  Peak Used: {mem_stats['max']:.2f} GB ({(mem_stats['max']/mem_total_stats['mean']*100):.1f}%)")
        
        if any('gpu0_utilization' in row for row in self.data):
            print("\n--- GPU Metrics ---")
            
            gpu_util_stats = self.get_summary_stats('gpu0_utilization')
            if gpu_util_stats:
                print(f"\nGPU Utilization:")
                print(f"  Average: {gpu_util_stats['mean']:.1f}%")
                print(f"  Peak: {gpu_util_stats['max']:.1f}%")
            
            gpu_mem_stats = self.get_summary_stats('gpu0_memory_used_gb')
            gpu_mem_total_stats = self.get_summary_stats('gpu0_memory_total_gb')
            if gpu_mem_stats and gpu_mem_total_stats:
                print(f"\nGPU Memory:")
                print(f"  Total: {gpu_mem_total_stats['mean']:.1f} GB")
                print(f"  Average Used: {gpu_mem_stats['mean']:.2f} GB ({(gpu_mem_stats['mean']/gpu_mem_total_stats['mean']*100):.1f}%)")
                print(f"  Peak Used: {gpu_mem_stats['max']:.2f} GB ({(gpu_mem_stats['max']/gpu_mem_total_stats['mean']*100):.1f}%)")
            
            gpu_power_stats = self.get_summary_stats('gpu0_power_watts')
            if gpu_power_stats:
                print(f"\nGPU Power:")
                print(f"  Average: {gpu_power_stats['mean']:.1f} W")
                print(f"  Peak: {gpu_power_stats['max']:.1f} W")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor system resources during quantization experiments"
    )
    
    parser.add_argument(
        '--output', '-o',
        default='logs/resource_monitor.log',
        help='Output CSV file for monitoring data'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=1.0,
        help='Sampling interval in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--duration', '-d',
        type=float,
        default=None,
        help='Monitoring duration in seconds (default: indefinite)'
    )
    
    parser.add_argument(
        '--pid', '-p',
        type=int,
        default=None,
        help='Process ID to monitor (optional)'
    )
    
    parser.add_argument(
        '--analyze', '-a',
        metavar='LOG_FILE',
        help='Analyze existing log file instead of monitoring'
    )
    
    parser.add_argument(
        '--report', '-r',
        metavar='REPORT_FILE',
        help='Generate markdown report (use with --analyze)'
    )
    
    args = parser.parse_args()
    
    if args.analyze:
        # Analyze mode
        analyzer = ResourceAnalyzer(args.analyze)
        analyzer.print_summary()
        
        if args.report:
            analyzer.generate_report(args.report)
    else:
        # Monitor mode
        monitor = ResourceMonitor(args.output, args.interval, args.pid)
        monitor.monitor(args.duration)


if __name__ == '__main__':
    main()
