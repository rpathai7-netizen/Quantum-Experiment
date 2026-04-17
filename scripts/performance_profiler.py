#!/usr/bin/env python3
"""
Performance Profiler for Quantum Platform
Measures and reports on performance metrics
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class PerformanceProfiler:
    """Profile performance of quantum components"""

    def __init__(self):
        self.results = {}
        self.start_time = None

    def profile_circuit_creation(self):
        """Profile circuit creation performance"""
        print("\n" + "=" * 70)
        print("[1] CIRCUIT CREATION PERFORMANCE")
        print("=" * 70)

        try:
            from circuit_types import QuantumCircuitFactory

            sizes = [5, 10, 20, 50, 100]
            print(f"\n{'Qubits':<10} {'Time (ms)':<15} {'Status':<20}")
            print("-" * 70)

            for size in sizes:
                start = time.time()
                qc = QuantumCircuitFactory.create_entangled_chain(size)
                elapsed = (time.time() - start) * 1000  # Convert to ms

                status = "✓" if elapsed < 100 else "⚠" if elapsed < 1000 else "⚠ SLOW"
                print(f"{size:<10} {elapsed:<15.3f} {status:<20}")

                self.results[f"circuit_creation_{size}"] = elapsed

        except ImportError as e:
            print(f"⚠️  Could not import circuit_types: {e}")

    def profile_simulator_init(self):
        """Profile simulator initialization performance"""
        print("\n" + "=" * 70)
        print("[2] SIMULATOR INITIALIZATION PERFORMANCE")
        print("=" * 70)

        try:
            from scalable_simulator import ScalableQuantumSimulator

            sizes = [10, 50, 100, 500, 1000]
            print(f"\n{'Qubits':<10} {'Time (ms)':<15} {'Method':<20}")
            print("-" * 70)

            for size in sizes:
                start = time.time()
                sim = ScalableQuantumSimulator(size)
                elapsed = (time.time() - start) * 1000

                print(f"{size:<10} {elapsed:<15.3f} {sim.method:<20}")
                self.results[f"simulator_init_{size}"] = elapsed

        except ImportError as e:
            print(f"⚠️  Could not import scalable_simulator: {e}")

    def profile_analysis(self):
        """Profile measurement analysis performance"""
        print("\n" + "=" * 70)
        print("[3] MEASUREMENT ANALYSIS PERFORMANCE")
        print("=" * 70)

        try:
            from measurement_analysis import QuantumMeasurementAnalyzer

            # Create test data
            test_counts = {
                "small": {"00": 500, "11": 500},
                "medium": {f"{i:04b}": 100 for i in range(16)},
                "large": {f"{i:08b}": 10 for i in range(256)},
            }

            print(f"\n{'Dataset':<15} {'States':<10} {'Time (ms)':<15} {'Status':<20}")
            print("-" * 70)

            for name, counts in test_counts.items():
                start = time.time()
                analyzer = QuantumMeasurementAnalyzer(counts)

                # Run all calculations
                stats = analyzer.get_statistics()
                entropy = analyzer.calculate_shannon_entropy()
                purity = analyzer.calculate_purity()

                elapsed = (time.time() - start) * 1000
                status = "✓"

                print(f"{name:<15} {len(counts):<10} {elapsed:<15.3f} {status:<20}")
                self.results[f"analysis_{name}"] = elapsed

        except ImportError as e:
            print(f"⚠️  Could not import measurement_analysis: {e}")

    def generate_report(self):
        """Generate performance report"""
        print("\n" + "=" * 70)
        print("PERFORMANCE SUMMARY")
        print("=" * 70)

        if not self.results:
            print("⚠️  No performance data collected")
            return

        avg_time = sum(self.results.values()) / len(self.results)
        min_time = min(self.results.values())
        max_time = max(self.results.values())

        print(f"\nTotal operations:      {len(self.results)}")
        print(f"Average time:          {avg_time:.3f} ms")
        print(f"Min time:              {min_time:.3f} ms")
        print(f"Max time:              {max_time:.3f} ms")

        print("\n" + "=" * 70)
        print("✅ Performance profiling complete!")
        print("=" * 70)

    def run_all(self):
        """Run all performance profiling"""
        print("\n" + "=" * 70)
        print("QUANTUM PLATFORM PERFORMANCE PROFILING")
        print("=" * 70)

        try:
            self.profile_circuit_creation()
            self.profile_simulator_init()
            self.profile_analysis()
            self.generate_report()
        except Exception as e:
            print(f"\n❌ Error during profiling: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    profiler = PerformanceProfiler()
    profiler.run_all()
