import sys
import time

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import (DensityMatrix, Statevector, partial_trace,
                                 random_statevector, state_fidelity)
from qiskit_aer import AerSimulator


def annihilation_reactor(qc, node_a_qubit, node_b_qubit):
    """
    Simulates the generation of an EPR pair (Bell state) representing
    entangled gamma-ray photons from matter-antimatter annihilation.
    """
    qc.h(node_a_qubit)
    qc.cx(node_a_qubit, node_b_qubit)


def teleportation_protocol(qc, msg_qubit, node_a_qubit, node_b_qubit, clbits):
    """
    Standard Quantum Teleportation protocol.
    """
    # 1. Bell measurement on Node A's side
    qc.cx(msg_qubit, node_a_qubit)
    qc.h(msg_qubit)

    # Measure and store in classical bits
    qc.measure(msg_qubit, clbits[0])
    qc.measure(node_a_qubit, clbits[1])

    # 2. Conditioned corrections at Node B
    # Z-correction if clbits[0] (msg) is 1
    with qc.if_test((clbits[0], 1)):
        qc.z(node_b_qubit)
    # X-correction if clbits[1] (node_a) is 1
    with qc.if_test((clbits[1], 1)):
        qc.x(node_b_qubit)


def run_benchmark(iterations=1000):
    print(
        f"🚀 Initializing Antimatter Engine Benchmarking ({iterations} cycles)...",
        flush=True,
    )

    # Initialize simulator once
    simulator = AerSimulator()
    fidelities = []
    start_time = time.time()

    for i in range(iterations):
        qc = QuantumCircuit(3, 2)
        initial_state = random_statevector(2)
        qc.prepare_state(initial_state, 0)

        annihilation_reactor(qc, 1, 2)
        teleportation_protocol(qc, 0, 1, 2, qc.clbits)

        # Save statevector to measure fidelity at the end
        qc.save_statevector()

        # Decompose state_preparation gates for Aer
        t_qc = transpile(qc, simulator, optimization_level=1)

        # Execute (shots=1 since we want the statevector result of a single branch)
        job = simulator.run(t_qc, shots=1)
        result = job.result()

        final_sv = result.get_statevector()
        dm = DensityMatrix(final_sv)

        # Trace out qubits 0 and 1 to get the state of node B (qubit 2)
        rho_target = partial_trace(dm, [0, 1])

        fid = state_fidelity(initial_state, rho_target)
        fidelities.append(fid)

        if (i + 1) % 10 == 0:
            elapsed = time.time() - start_time
            print(
                f"  [Cycle {i+1:4d}] Avg Fidelity: {np.mean(fidelities):.6f} | Elapsed: {elapsed:.2f}s",
                flush=True,
            )

    total_time = time.time() - start_time
    avg_fidelity = np.mean(fidelities)
    throughput = iterations / total_time

    print("\n" + "=" * 50, flush=True)
    print("      ANTIMATTER ENGINE PERFORMANCE REPORT", flush=True)
    print("=" * 50, flush=True)
    print(f"Total Teleportations:  {iterations}", flush=True)
    print(f"Total Execution Time:  {total_time:.4f} seconds", flush=True)
    print(f"Average Fidelity:      {avg_fidelity:.6f}", flush=True)
    print(f"Throughput Rate:       {throughput:.2f} cycles/sec", flush=True)
    print(
        f"Network Latency:       {(total_time/iterations)*1000:.4f} ms/teleport",
        flush=True,
    )
    print("=" * 50, flush=True)


if __name__ == "__main__":
    # Handle Windows encoding issues
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    print("Visualizing Circuit for First Photon Entanglement Event...", flush=True)
    test_qc = QuantumCircuit(3, 2)
    annihilation_reactor(test_qc, 1, 2)
    teleportation_protocol(test_qc, 0, 1, 2, test_qc.clbits)
    try:
        print(test_qc.draw(output="text"), flush=True)
    except Exception as e:
        print(f"[Warn] Could not render circuit drawing: {e}", flush=True)

    # Run with 1,000 iterations for final benchmark
    run_benchmark(1000)
