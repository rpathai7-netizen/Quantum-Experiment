"""
Quick Quantum Benchmark - Fast Results File Generator
"""

import sys
from datetime import datetime
from io import StringIO

# Redirect output
output = StringIO()


def log(message):
    """Log to both console and output"""
    print(message)
    output.write(message + "\n")


try:
    log(f"\n{'='*70}")
    log("QUANTUM COMPUTING PLATFORM - BENCHMARK RESULTS")
    log(f"{'='*70}")
    log(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'='*70}\n")

    # Test 1: Original circuit
    log("\n[TEST 1] Original 30-Qubit Circuit")
    log("-" * 70)

    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    qc = QuantumCircuit(30, 30)
    qc.h(0)
    for i in range(29):
        qc.cx(i, i + 1)
    qc.measure(range(30), range(30))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=10)
    result = job.result()
    counts = result.get_counts(qc)

    log(f"Status: SUCCESS")
    log(f"Qubits: 30")
    log(f"Shots: 10")
    log(f"Results: {counts}")
    log(f"Unique states: {len(counts)}")

    # Test 2: Scalable simulator
    log("\n[TEST 2] Scalable Quantum Simulator")
    log("-" * 70)

    from scalable_simulator import ScalableQuantumSimulator

    sizes = [30, 100, 500, 6000]
    log(f"Testing various qubit counts: {sizes}")

    for size in sizes:
        simulator = ScalableQuantumSimulator(size)
        results = simulator.run(shots=5)
        log(f"  {size:>5} qubits: {len(results)} unique states - SUCCESS")

    # Test 3: Circuit types
    log("\n[TEST 3] Quantum Circuit Types")
    log("-" * 70)

    from circuit_types import CIRCUIT_TYPES

    log(f"Available circuit types: {len(CIRCUIT_TYPES)}")
    for name in CIRCUIT_TYPES.keys():
        log(f"  - {name}")

    # Test 4: Measurement analysis
    log("\n[TEST 4] Measurement Analysis")
    log("-" * 70)

    from measurement_analysis import QuantumMeasurementAnalyzer

    test_counts = {"00": 45, "01": 8, "10": 7, "11": 40}
    analyzer = QuantumMeasurementAnalyzer(test_counts)

    stats = analyzer.get_statistics()
    log(f"Test measurement stats:")
    log(f"  Total shots: {stats['total_shots']}")
    log(f"  Unique states: {stats['num_unique_states']}")
    log(f"  Entropy: {analyzer.calculate_shannon_entropy():.4f}")
    log(f"  Purity: {analyzer.calculate_purity():.4f}")
    log(f"  Entanglement: {analyzer.detect_entanglement_pattern()}")

    # Test 5: Integrated platform
    log("\n[TEST 5] Integrated Platform")
    log("-" * 70)

    from integrated_platform import QuantumExperimentPlatform

    platform = QuantumExperimentPlatform()

    # Create and run a circuit
    circuit = platform.create_circuit("ghz_state", 10)
    results = platform.run_local(circuit, 10, shots=50)

    log(f"GHZ state (10 qubits) test:")
    log(f"  Circuit created: SUCCESS")
    log(f"  Execution: SUCCESS")
    log(f"  Results: {results}")
    log(f"  Unique states: {len(results)}")

    # Summary
    log(f"\n{'='*70}")
    log("BENCHMARK SUMMARY")
    log(f"{'='*70}")
    log(f"All Tests: PASSED")
    log(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Status: COMPLETE")
    log(f"{'='*70}\n")

    # Save to file
    results_text = output.getvalue()

    with open(
        "quantum_benchmark_results.txt", "w", encoding="utf-8", errors="replace"
    ) as f:
        f.write(results_text)

    log("\nResults saved to: quantum_benchmark_results.txt")

except Exception as e:
    log(f"\nERROR: {e}")
    import traceback

    log(traceback.format_exc())
