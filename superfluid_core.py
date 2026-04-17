import time

import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit.quantum_info import hellinger_fidelity
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (NoiseModel, depolarizing_error,
                              thermal_relaxation_error)


def setup_superfluid_backend():
    """Environment A: A mathematically perfect, frictionless vacuum."""
    return AerSimulator()


def setup_control_backend(qubits=12):
    """Environment B: A noisy simulator mimicking a standard IBM quantum chip."""
    noise_model = NoiseModel()

    # 1. High-Decoherence Surrogate (Depolarizing Noise)
    # Single-qubit errors (increased to show degradation clearly)
    error_1q = depolarizing_error(0.005, 1)
    noise_model.add_all_qubit_quantum_error(
        error_1q, ["h", "x", "y", "z", "p", "u1", "u2", "u3"]
    )

    # Two-qubit errors (CNOT / CP) - significantly higher error rate for deep circuits
    error_2q = depolarizing_error(0.02, 2)
    noise_model.add_all_qubit_quantum_error(error_2q, ["cx", "cp"])

    return AerSimulator(noise_model=noise_model)


def run_experiment():
    n_qubits = 12
    shots = 1024

    print("=" * 60)
    print("      SUPERFLUID CORE - DEEP CIRCUIT EXECUTION SIMULATOR")
    print("=" * 60)
    print(f"Algorithm: {n_qubits}-qubit Quantum Fourier Transform (QFT)")
    print(f"Complexity: Depth ~{n_qubits*(n_qubits+1)//2} gates")
    print("-" * 60)

    # 1. Initialize Deep QFT Circuit
    # We include measurements to obtain the probability distribution
    qft_circ = QFT(num_qubits=n_qubits, do_swaps=True).measure_all(inplace=False)

    # 2. Setup Environments
    superfluid = setup_superfluid_backend()
    control = setup_control_backend(n_qubits)

    # 3. Transpile and Execute - Environment A (Superfluid)
    print("Executing in Superfluid Core (Perfect Vacuum)... ", end="", flush=True)
    t_start = time.time()
    st_circ = transpile(qft_circ, superfluid)
    sf_job = superfluid.run(st_circ, shots=shots)
    sf_result = sf_job.result()
    sf_counts = sf_result.get_counts()
    print(f"Done ({time.time() - t_start:.2f}s)")

    # 4. Transpile and Execute - Environment B (Control)
    print("Executing in Control Environment (Noisy Chip)... ", end="", flush=True)
    t_start = time.time()
    ct_circ = transpile(qft_circ, control)
    ct_job = control.run(ct_circ, shots=shots)
    ct_result = ct_job.result()
    ct_counts = ct_result.get_counts()
    print(f"Done ({time.time() - t_start:.2f}s)")

    # 5. Extract Metrics & Plot
    fidelity = hellinger_fidelity(sf_counts, ct_counts)
    degradation = (1 - fidelity) * 100

    print("-" * 60)
    print(f"SIGNAL FIDELITY:      {fidelity:.4f}")
    print(f"DECOHERENCE PENALTY:  {degradation:.2f}%")
    print("=" * 60)

    # Visualization
    # For 20 qubits, we only show the top 10 recorded outcomes for clarity
    top_n = 10

    # Sort results
    sf_top = sorted(sf_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    ct_top = {
        k: ct_counts.get(k, 0) for k, v in sf_top
    }  # Get matching keys from control

    labels = [k for k, v in sf_top]
    sf_values = [v / shots for k, v in sf_top]
    ct_values = [ct_top[k] / shots for k in labels]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(
        x - width / 2, sf_values, width, label="Superfluid (Perfect)", color="#00d2ff"
    )
    rects2 = ax.bar(
        x + width / 2, ct_values, width, label="Control (Noisy)", color="#ff4b2b"
    )

    ax.set_ylabel("Probability")
    ax.set_title(f"QFT-20: Superfluid vs. Control Distribution (Top {top_n} States)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.legend()

    plt.tight_layout()
    plot_file = "qft_comparison_results.png"
    plt.savefig(plot_file)
    print(f"Comparison plot saved to: {plot_file}")
    plt.show()


if __name__ == "__main__":
    import sys

    import matplotlib

    matplotlib.use("Agg")  # Force non-interactive backend

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    run_experiment()
