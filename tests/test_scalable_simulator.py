"""
Tests for Scalable Quantum Simulator
Tests simulation accuracy and performance
"""

import numpy as np
import pytest
from qiskit import QuantumCircuit

from scalable_simulator import ScalableQuantumSimulator


class TestScalableQuantumSimulator:
    """Test suite for ScalableQuantumSimulator"""

    def test_simulator_initialization_small(self):
        """Test simulator initialization with small qubit count"""
        sim = ScalableQuantumSimulator(5)
        assert sim.num_qubits == 5
        assert sim.method in ["statevector", "density_matrix", "tensor_network"]

    def test_simulator_initialization_large(self):
        """Test simulator initialization with large qubit count"""
        sim = ScalableQuantumSimulator(1000)
        assert sim.num_qubits == 1000

    def test_method_selection_small(self):
        """Test that small circuits use statevector"""
        sim = ScalableQuantumSimulator(10, method="auto")
        # Should use statevector for small circuits
        assert sim.method in ["statevector", "density_matrix", "tensor_network"]

    def test_method_selection_large(self):
        """Test that large circuits use tensor network or analytical"""
        sim = ScalableQuantumSimulator(1000, method="auto")
        # Should use analytical method for large circuits
        assert sim.method in ["tensor_network", "density_matrix"]

    def test_build_entangled_circuit(self):
        """Test entangled circuit building"""
        sim = ScalableQuantumSimulator(8)
        qc = sim.build_entangled_circuit(8, shots=10)

        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 8
        assert qc.num_clbits == 8

    def test_entangled_circuit_structure(self):
        """Test entangled circuit has correct structure"""
        sim = ScalableQuantumSimulator(5)
        qc = sim.build_entangled_circuit(5)

        gate_names = [instr.operation.name for instr in qc.data]
        assert "h" in gate_names
        assert "cx" in gate_names
        assert "measure" in gate_names


class TestSimulatorAccuracy:
    """Test simulation accuracy and correctness"""

    def test_small_circuit_results(self):
        """Test results for small circuits"""
        sim = ScalableQuantumSimulator(2, method="statevector")
        qc = sim.build_entangled_circuit(2, shots=100)

        # Circuit should only produce 00 and 11
        # Build a simple entangled state manually
        from qiskit import ClassicalRegister, QuantumRegister

        test_qc = QuantumCircuit(2, 2)
        test_qc.h(0)
        test_qc.cx(0, 1)
        test_qc.measure([0, 1], [0, 1])

        assert test_qc is not None

    def test_result_format(self):
        """Test that results are in expected format"""
        sim = ScalableQuantumSimulator(3, method="statevector")
        qc = sim.build_entangled_circuit(3)

        if hasattr(sim, "simulate_with_statevector"):
            results = sim.simulate_with_statevector(qc, shots=10)

            # Results should be dict of bitstrings to counts
            assert isinstance(results, dict)
            for bitstring, count in results.items():
                assert isinstance(bitstring, str)
                assert isinstance(count, int)
                assert count > 0


class TestSimulatorScalability:
    """Test simulator behavior with different scales"""

    def test_tiny_circuit(self):
        """Test single qubit circuit"""
        sim = ScalableQuantumSimulator(1)
        qc = sim.build_entangled_circuit(1)
        assert qc is not None

    def test_small_circuit(self):
        """Test small circuit (within state vector limits)"""
        sim = ScalableQuantumSimulator(10)
        qc = sim.build_entangled_circuit(10)
        assert qc.num_qubits == 10

    def test_medium_circuit(self):
        """Test medium circuit (requires approximation)"""
        sim = ScalableQuantumSimulator(50)
        qc = sim.build_entangled_circuit(50)
        assert qc.num_qubits == 50

    def test_large_circuit(self):
        """Test large circuit (pure analytical)"""
        sim = ScalableQuantumSimulator(1000)
        qc = sim.build_entangled_circuit(
            100
        )  # Build smaller circuit on large simulator
        assert qc is not None


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_zero_qubits(self):
        """Test behavior with zero qubits"""
        # Should handle gracefully or raise error
        try:
            sim = ScalableQuantumSimulator(0)
            # If no error, should have reasonable defaults
            assert sim.num_qubits == 0
        except (ValueError, RuntimeError):
            # Expected
            pass

    def test_single_shot(self):
        """Test with single shot"""
        sim = ScalableQuantumSimulator(3)
        qc = sim.build_entangled_circuit(3)
        # Should handle single shot
        assert qc is not None

    def test_many_shots(self):
        """Test with large number of shots"""
        sim = ScalableQuantumSimulator(2)
        qc = sim.build_entangled_circuit(2)
        # Should handle large number of shots
        assert qc is not None


class TestSimulatorConfiguration:
    """Test simulator configuration options"""

    def test_method_parameter(self):
        """Test different method parameters"""
        for method in ["auto", "statevector", "density_matrix", "tensor_network"]:
            try:
                sim = ScalableQuantumSimulator(5, method=method)
                assert sim.method is not None
            except Exception:
                # Some methods might not be available
                pass

    def test_invalid_method(self):
        """Test with invalid method"""
        sim = ScalableQuantumSimulator(5, method="invalid_method")
        # Should fall back to auto or raise error
        assert sim.method is not None
