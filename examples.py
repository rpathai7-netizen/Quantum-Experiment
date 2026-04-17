"""
Example Scripts for Quantum Experiment Platform
Copy and run these scripts for common quantum computing tasks
"""

# ============================================================================
# EXAMPLE 1: Basic 30-Qubit Entanglement Test
# ============================================================================


def example_basic_entanglement():
    """Test basic entanglement with 30 qubits"""
    from integrated_platform import QuantumExperimentPlatform

    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic 30-Qubit Entanglement Test")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    # Create circuit
    circuit = platform.create_circuit("entangled_chain", 30)

    # Run locally
    print("\nRunning 100 shots locally...")
    results = platform.run_local(circuit, 30, shots=100)

    # Analyze
    print("\nAnalyzing results...")
    platform.analyze_results()


# ============================================================================
# EXAMPLE 2: Scaling Test (30 to 6000 Qubits)
# ============================================================================


def example_scaling():
    """Test quantum circuit scaling"""
    from integrated_platform import QuantumExperimentPlatform
    from measurement_analysis import QuantumMeasurementAnalyzer

    print("\n" + "=" * 70)
    print("EXAMPLE 2: Quantum Scaling Test")
    print("=" * 70)

    platform = QuantumExperimentPlatform()
    sizes = [30, 100, 500, 1000, 6000]

    print(f"\n{'Qubits':<10} {'Entropy':<15} {'Pattern':<30}")
    print("-" * 70)

    for size in sizes:
        circuit = platform.create_circuit("entangled_chain", size)
        results = platform.run_local(circuit, size, shots=10)

        analyzer = QuantumMeasurementAnalyzer(results)
        entropy = analyzer.calculate_shannon_entropy()
        pattern = analyzer.detect_entanglement_pattern()

        print(f"{size:<10} {entropy:<15.4f} {pattern:<30}")


# ============================================================================
# EXAMPLE 3: Compare Different Circuit Types
# ============================================================================


def example_circuit_comparison():
    """Compare different quantum circuit types"""
    from integrated_platform import QuantumExperimentPlatform
    from measurement_analysis import QuantumMeasurementAnalyzer

    print("\n" + "=" * 70)
    print("EXAMPLE 3: Circuit Type Comparison")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    circuit_types = ["entangled_chain", "ghz_state", "random", "deutsch"]

    print(
        f"\n{'Circuit Type':<20} {'Unique States':<15} {'Entropy':<15} {'Purity':<15}"
    )
    print("-" * 70)

    for circuit_type in circuit_types:
        try:
            circuit = platform.create_circuit(circuit_type, 8)
            results = platform.run_local(circuit, 8, shots=100)

            analyzer = QuantumMeasurementAnalyzer(results)
            unique = analyzer.get_statistics()["num_unique_states"]
            entropy = analyzer.calculate_shannon_entropy()
            purity = analyzer.calculate_purity()

            print(f"{circuit_type:<20} {unique:<15} {entropy:<15.4f} {purity:<15.4f}")
        except Exception as e:
            print(f"{circuit_type:<20} ERROR: {str(e)[:30]}")


# ============================================================================
# EXAMPLE 4: Detailed State Analysis
# ============================================================================


def example_state_analysis():
    """Detailed analysis of quantum state"""
    from integrated_platform import QuantumExperimentPlatform
    from measurement_analysis import QuantumMeasurementAnalyzer

    print("\n" + "=" * 70)
    print("EXAMPLE 4: Detailed State Analysis")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    # Create and run circuit
    circuit = platform.create_circuit("ghz_state", 5)
    results = platform.run_local(circuit, 5, shots=1000)

    # Detailed analysis
    analyzer = QuantumMeasurementAnalyzer(results)

    print("\n1. PROBABILITY DISTRIBUTION")
    for state, prob in analyzer.find_most_probable_states(5):
        print(f"   {state}: {prob:.4f}")

    print("\n2. QUANTUM STATE METRICS")
    print(f"   Entropy: {analyzer.calculate_shannon_entropy():.4f}")
    print(f"   Purity: {analyzer.calculate_purity():.4f}")
    print(f"   Coherence: {analyzer.calculate_coherence():.4f}")

    print("\n3. SINGLE-QUBIT ANALYSIS")
    qubit_probs = analyzer.calculate_single_qubit_probabilities()
    for qubit, (p0, p1) in qubit_probs.items():
        print(f"   Q{qubit}: P(|0>) = {p0:.2%}, P(|1>) = {p1:.2%}")

    print("\n4. ENTANGLEMENT")
    correlations = analyzer.calculate_correlations()
    if correlations:
        for (i, j), corr in correlations.items():
            print(f"   Q{i}-Q{j}: {corr:.4f}")
    else:
        print("   No significant correlations detected")


# ============================================================================
# EXAMPLE 5: Cloud Quantum Computing
# ============================================================================


def example_cloud_computing():
    """Run on cloud quantum backend (requires API key)"""
    import os

    from integrated_platform import QuantumExperimentPlatform

    print("\n" + "=" * 70)
    print("EXAMPLE 5: Cloud Quantum Computing")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    # Show available backends
    print("\nAvailable Cloud Backends:")
    platform.show_cloud_backends()

    # Example: IBM Quantum
    print("\n" + "-" * 70)
    print("Example: Running on IBM Quantum")
    print("-" * 70)
    print("""
To run on IBM Quantum:
    1. Create account: https://quantum-computing.ibm.com/
    2. Copy API key from dashboard
    3. Use in code:

        api_key = "your-api-key-here"
        platform = QuantumExperimentPlatform()
        circuit = platform.create_circuit("ghz_state", 10)
        
        results = platform.run_cloud(circuit, "ibm", shots=100)
        platform.analyze_results()
    """)


# ============================================================================
# EXAMPLE 6: Circuit Gate Analysis
# ============================================================================


def example_circuit_metrics():
    """Analyze circuit gate composition and depth"""
    from integrated_platform import QuantumExperimentPlatform

    print("\n" + "=" * 70)
    print("EXAMPLE 6: Circuit Metrics & Gate Analysis")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    circuit_types = ["entangled_chain", "ghz_state", "qaoa"]

    print(f"\n{'Circuit':<20} {'Depth':<10} {'Size':<10} {'Main Gates':<30}")
    print("-" * 70)

    for circuit_type in circuit_types:
        try:
            circuit = platform.create_circuit(circuit_type, 10)
            metrics = platform.get_circuit_metrics(circuit)

            gates = metrics["gates"]
            gate_str = ", ".join([f"{g}:{c}" for g, c in list(gates.items())[:3]])

            print(
                f"{circuit_type:<20} {metrics['depth']:<10} {metrics['size']:<10} {gate_str:<30}"
            )
        except Exception as e:
            print(f"{circuit_type:<20} ERROR")


# ============================================================================
# EXAMPLE 7: Entanglement Pattern Detection
# ============================================================================


def example_entanglement_detection():
    """Detect and classify entanglement patterns"""
    from integrated_platform import QuantumExperimentPlatform
    from measurement_analysis import QuantumMeasurementAnalyzer

    print("\n" + "=" * 70)
    print("EXAMPLE 7: Entanglement Pattern Detection")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    circuit_types = ["entangled_chain", "ghz_state", "random", "deutsch"]

    print(f"\n{'Circuit Type':<20} {'Entanglement Pattern':<50}")
    print("-" * 70)

    for circuit_type in circuit_types:
        try:
            circuit = platform.create_circuit(circuit_type, 6)
            results = platform.run_local(circuit, 6, shots=100)

            analyzer = QuantumMeasurementAnalyzer(results)
            pattern = analyzer.detect_entanglement_pattern()

            print(f"{circuit_type:<20} {pattern:<50}")
        except Exception as e:
            print(f"{circuit_type:<20} ERROR: {str(e)[:40]}")


# ============================================================================
# EXAMPLE 8: Batch Processing
# ============================================================================


def example_batch_processing():
    """Run multiple circuits in batch and compare results"""
    from integrated_platform import QuantumExperimentPlatform
    from measurement_analysis import QuantumMeasurementAnalyzer

    print("\n" + "=" * 70)
    print("EXAMPLE 8: Batch Processing & Comparison")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    # Define batch
    batch = [
        ("entangled_chain", 5, 100),
        ("entangled_chain", 10, 100),
        ("ghz_state", 5, 100),
        ("ghz_state", 10, 100),
    ]

    print(f"\n{'Circuit':<20} {'Qubits':<10} {'States':<10} {'Entropy':<15}")
    print("-" * 70)

    for circuit_type, qubits, shots in batch:
        circuit = platform.create_circuit(circuit_type, qubits)
        results = platform.run_local(circuit, qubits, shots=shots)

        analyzer = QuantumMeasurementAnalyzer(results)
        states = len(results)
        entropy = analyzer.calculate_shannon_entropy()

        print(f"{circuit_type:<20} {qubits:<10} {states:<10} {entropy:<15.4f}")


# ============================================================================
# EXAMPLE 9: Performance Benchmark
# ============================================================================


def example_performance_benchmark():
    """Benchmark circuit execution performance"""
    import time

    from integrated_platform import QuantumExperimentPlatform

    print("\n" + "=" * 70)
    print("EXAMPLE 9: Performance Benchmark")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    sizes = [10, 50, 100, 500, 1000]

    print(f"\n{'Qubits':<10} {'Time (sec)':<15} {'Shots':<10} {'Throughput':<20}")
    print("-" * 70)

    for size in sizes:
        circuit = platform.create_circuit("entangled_chain", size)

        start = time.time()
        results = platform.run_local(circuit, size, shots=10)
        elapsed = time.time() - start

        throughput = 10 / elapsed if elapsed > 0 else float("inf")

        print(f"{size:<10} {elapsed:<15.4f} {10:<10} {throughput:<20.1f} shots/sec")


# ============================================================================
# EXAMPLE 10: Full Experiment Workflow
# ============================================================================


def example_full_workflow():
    """Complete quantum experiment workflow"""
    from integrated_platform import QuantumExperimentPlatform

    print("\n" + "=" * 70)
    print("EXAMPLE 10: Full Experiment Workflow")
    print("=" * 70)

    platform = QuantumExperimentPlatform()

    print("\n[STEP 1] Circuit Design")
    circuit = platform.create_circuit("ghz_state", 15)
    metrics = platform.get_circuit_metrics(circuit)
    print(
        f"  Created circuit with {metrics['num_qubits']} qubits, depth {metrics['depth']}"
    )

    print("\n[STEP 2] Execution")
    results = platform.run_local(circuit, 15, shots=500)
    print(f"  Results collected: {len(results)} unique states")

    print("\n[STEP 3] Analysis")
    analyzer = platform.analyze_results()

    print("\n[STEP 4] Logging")
    platform.show_execution_log()

    print("\n[COMPLETE] Workflow execution successful!")


# ============================================================================
# MAIN - Run All Examples
# ============================================================================

if __name__ == "__main__":
    import sys

    examples = {
        "1": ("Basic Entanglement (30 qubits)", example_basic_entanglement),
        "2": ("Scaling Test (30-6000 qubits)", example_scaling),
        "3": ("Circuit Type Comparison", example_circuit_comparison),
        "4": ("Detailed State Analysis", example_state_analysis),
        "5": ("Cloud Quantum Info", example_cloud_computing),
        "6": ("Circuit Gate Analysis", example_circuit_metrics),
        "7": ("Entanglement Detection", example_entanglement_detection),
        "8": ("Batch Processing", example_batch_processing),
        "9": ("Performance Benchmark", example_performance_benchmark),
        "10": ("Full Workflow", example_full_workflow),
    }

    print("\n" + "=" * 70)
    print("QUANTUM EXPERIMENT EXAMPLES")
    print("=" * 70)
    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")

    print("\n" + "=" * 70)
    print("Running all examples...\n")

    for key in sorted(examples.keys()):
        name, func = examples[key]
        try:
            func()
        except Exception as e:
            print(f"\n⚠️  Example {key} error: {e}")

    print("\n" + "=" * 70)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 70)
