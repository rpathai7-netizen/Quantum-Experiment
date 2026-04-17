"""
Advanced Quantum Circuit Types
Different circuit architectures for various applications
"""

import random
from typing import List, Tuple

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister


class QuantumCircuitFactory:
    """Factory for creating different types of quantum circuits"""

    @staticmethod
    def create_entangled_chain(num_qubits: int) -> QuantumCircuit:
        """
        CNOT chain entanglement.
        Qubit 0 in superposition, all others entangled.
        Result: always all-0s or all-1s.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.h(0)
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_ghz_state(num_qubits: int) -> QuantumCircuit:
        """
        GHZ (Greenberger–Horne–Zeilinger) state.
        Similar to CNOT chain but optimized structure.
        Maximum entanglement across all qubits.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.h(0)
        for i in range(num_qubits - 1):
            qc.cx(0, i + 1)
        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_random_circuit(num_qubits: int, depth: int) -> QuantumCircuit:
        """
        Random circuit with parametrized gates.
        Good for testing circuit depth and complexity.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Hadamard layer
        for i in range(num_qubits):
            qc.h(i)

        # Random depth layers of 2-qubit gates
        for _ in range(depth):
            # Random pairs of qubits
            for i in range(0, num_qubits - 1, 2):
                angle = random.uniform(0, 2 * np.pi)
                qc.cx(i, i + 1)
                qc.rz(angle, i)
                qc.rz(angle, i + 1)

        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_qaoa_circuit(num_qubits: int, layers: int = 2) -> QuantumCircuit:
        """
        QAOA (Quantum Approximate Optimization Algorithm) circuit.
        Used for combinatorial optimization problems.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Initial superposition
        for i in range(num_qubits):
            qc.h(i)

        # QAOA layers (simplified)
        for layer in range(layers):
            # Problem Hamiltonian
            gamma = 0.5
            for i in range(num_qubits - 1):
                qc.cx(i, i + 1)
                qc.rz(gamma, i + 1)
                qc.cx(i, i + 1)

            # Mixer Hamiltonian
            beta = 0.5
            for i in range(num_qubits):
                qc.rx(2 * beta, i)

        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_grover_oracle(num_qubits: int, marked_state: int) -> QuantumCircuit:
        """
        Grover's algorithm circuit.
        Searches for a marked state in unsorted database.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Initial superposition
        for i in range(num_qubits):
            qc.h(i)

        # Grover iterations (simplified)
        for iteration in range(int(np.pi / 4 * np.sqrt(2**num_qubits))):
            # Oracle: mark the target state
            marked_bits = format(marked_state, f"0{num_qubits}b")
            for i, bit in enumerate(marked_bits):
                if bit == "0":
                    qc.x(i)

            # Multi-controlled Z gate (simplified as phase flip)
            qc.z(0)

            for i, bit in enumerate(marked_bits):
                if bit == "0":
                    qc.x(i)

            # Diffusion operator
            for i in range(num_qubits):
                qc.h(i)
            for i in range(num_qubits):
                qc.x(i)

            qc.h(num_qubits - 1)
            for i in range(num_qubits - 1):
                qc.cx(i, num_qubits - 1)
            qc.h(num_qubits - 1)

            for i in range(num_qubits):
                qc.x(i)
            for i in range(num_qubits):
                qc.h(i)

            if iteration >= 1:  # Limit iterations for larger circuits
                break

        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_vqe_ansatz(num_qubits: int, layers: int = 2) -> QuantumCircuit:
        """
        VQE (Variational Quantum Eigensolver) ansatz circuit.
        Used for finding ground states of quantum systems.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Variational layers
        for layer in range(layers):
            # Single-qubit rotations
            for i in range(num_qubits):
                angle = np.pi / (layer + 1)
                qc.ry(angle, i)
                qc.rz(angle, i)

            # Entangling layer
            for i in range(num_qubits - 1):
                qc.cx(i, i + 1)

        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_quantum_walk(num_qubits: int, steps: int = 5) -> QuantumCircuit:
        """
        Quantum walk circuit.
        Simulates random walk on a graph using quantum mechanics.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Initialize to equal superposition
        for i in range(num_qubits):
            qc.h(i)

        # Walk steps
        for step in range(min(steps, 3)):  # Limit steps for larger circuits
            for i in range(num_qubits - 1):
                qc.cx(i, i + 1)
                qc.rx(np.pi / 8, i)

        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_deutsch_algorithm(num_qubits: int = 2) -> QuantumCircuit:
        """
        Deutsch algorithm circuit.
        Determines if a function is balanced or constant.
        Classic quantum algorithm example.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Initialize
        qc.x(num_qubits - 1)
        for i in range(num_qubits):
            qc.h(i)

        # Oracle (identity function for demo)
        qc.id(0)

        # Final Hadamard
        for i in range(num_qubits - 1):
            qc.h(i)

        qc.measure(range(num_qubits), range(num_qubits))
        return qc

    @staticmethod
    def create_phase_estimation(num_qubits: int = 4) -> QuantumCircuit:
        """
        Quantum Phase Estimation circuit.
        Estimates eigenvalues of quantum gates.
        """
        qc = QuantumCircuit(num_qubits, num_qubits)

        # Initialize counting qubits
        for i in range(num_qubits - 1):
            qc.h(i)

        # Eigenstate preparation
        qc.x(num_qubits - 1)

        # Controlled unitary operations (simplified)
        for i in range(num_qubits - 1):
            qc.cp(2 * np.pi / (2 ** (i + 1)), i, num_qubits - 1)

        # Inverse QFT (simplified)
        for i in range(num_qubits - 1):
            qc.h(i)

        qc.measure(range(num_qubits), range(num_qubits))
        return qc


# ============================================================================
# CIRCUIT REGISTRY
# ============================================================================

CIRCUIT_TYPES = {
    "entangled_chain": {
        "factory": QuantumCircuitFactory.create_entangled_chain,
        "description": "CNOT chain - qubits fully entangled in sequence",
        "use_case": "Testing entanglement",
        "scalability": "Excellent (>6000 qubits analytical)",
    },
    "ghz_state": {
        "factory": QuantumCircuitFactory.create_ghz_state,
        "description": "GHZ state - central control qubit entangles all others",
        "use_case": "Testing maximum entanglement",
        "scalability": "Excellent (>1000 qubits)",
    },
    "random": {
        "factory": QuantumCircuitFactory.create_random_circuit,
        "description": "Random gates at variable depth",
        "use_case": "Stress testing, random benchmarks",
        "scalability": "Moderate (depth-dependent)",
    },
    "qaoa": {
        "factory": QuantumCircuitFactory.create_qaoa_circuit,
        "description": "QAOA - optimization algorithm",
        "use_case": "Combinatorial optimization problems",
        "scalability": "Moderate (max ~100 qubits practical)",
    },
    "grover": {
        "factory": QuantumCircuitFactory.create_grover_oracle,
        "description": "Grover's algorithm - unsorted database search",
        "use_case": "Quantum search",
        "scalability": "Low (exponential iterations, max ~20 qubits)",
    },
    "vqe": {
        "factory": QuantumCircuitFactory.create_vqe_ansatz,
        "description": "VQE - variational quantum eigensolver",
        "use_case": "Ground state energy estimation",
        "scalability": "Moderate (max ~50 qubits practical)",
    },
    "quantum_walk": {
        "factory": QuantumCircuitFactory.create_quantum_walk,
        "description": "Quantum walk on graph",
        "use_case": "Graph algorithms, simulation",
        "scalability": "Moderate (max ~30 qubits)",
    },
    "deutsch": {
        "factory": QuantumCircuitFactory.create_deutsch_algorithm,
        "description": "Deutsch algorithm - function property testing",
        "use_case": "Educational, function analysis",
        "scalability": "Excellent (simple circuit)",
    },
    "phase_estimation": {
        "factory": QuantumCircuitFactory.create_phase_estimation,
        "description": "Phase estimation - eigenvalue estimation",
        "use_case": "Eigenvalue problems",
        "scalability": "Low (exponential resources)",
    },
}


def list_circuit_types():
    """Display all available circuit types"""
    print("\n" + "=" * 80)
    print("AVAILABLE QUANTUM CIRCUIT TYPES")
    print("=" * 80)

    for circuit_type, info in CIRCUIT_TYPES.items():
        print(f"\n📊 {circuit_type.upper()}")
        print(f"   Description: {info['description']}")
        print(f"   Use Case: {info['use_case']}")
        print(f"   Scalability: {info['scalability']}")


if __name__ == "__main__":
    list_circuit_types()

    # Example: Create and show different circuit types
    print("\n" + "=" * 80)
    print("CIRCUIT EXAMPLES")
    print("=" * 80)

    for circuit_name in ["entangled_chain", "ghz_state", "deutsch"]:
        circuit_info = CIRCUIT_TYPES[circuit_name]
        circuit = circuit_info["factory"](6)
        print(f"\n{circuit_name}:")
        print(circuit)
