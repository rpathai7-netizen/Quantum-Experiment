"""
Tests for Quantum Circuit Types
Tests circuit creation and properties
"""

import pytest
from qiskit import QuantumCircuit

from circuit_types import QuantumCircuitFactory


class TestQuantumCircuitFactory:
    """Test suite for QuantumCircuitFactory"""

    def test_entangled_chain_creation(self):
        """Test entangled chain circuit creation"""
        qc = QuantumCircuitFactory.create_entangled_chain(10)
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 10
        assert qc.num_clbits == 10

    def test_entangled_chain_gates(self):
        """Test entangled chain contains correct gates"""
        qc = QuantumCircuitFactory.create_entangled_chain(5)
        # Check circuit depth is reasonable
        assert qc.depth() > 0
        # Should have hadamard and CNOT gates
        gate_names = [instr.operation.name for instr in qc.data]
        assert "h" in gate_names
        assert "cx" in gate_names

    def test_ghz_state_creation(self):
        """Test GHZ state circuit creation"""
        qc = QuantumCircuitFactory.create_ghz_state(15)
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 15
        assert qc.num_clbits == 15

    def test_ghz_state_properties(self):
        """Test GHZ state has correct structure"""
        qc = QuantumCircuitFactory.create_ghz_state(6)
        gate_names = [instr.operation.name for instr in qc.data]
        # GHZ uses central control qubit
        assert "h" in gate_names
        assert "cx" in gate_names

    def test_random_circuit_creation(self):
        """Test random circuit creation"""
        qc = QuantumCircuitFactory.create_random_circuit(8, depth=3)
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 8
        assert qc.depth() > 0

    def test_random_circuit_depth(self):
        """Test random circuit respects depth parameter"""
        qc_shallow = QuantumCircuitFactory.create_random_circuit(5, depth=1)
        qc_deep = QuantumCircuitFactory.create_random_circuit(5, depth=5)

        # Deeper circuit should have more gates
        shallow_gates = len(qc_shallow.data)
        deep_gates = len(qc_deep.data)
        assert deep_gates >= shallow_gates

    def test_circuit_scalability(self):
        """Test circuits can be created with varying qubit counts"""
        for num_qubits in [3, 10, 50, 100]:
            qc = QuantumCircuitFactory.create_entangled_chain(num_qubits)
            assert qc.num_qubits == num_qubits

    def test_circuit_measurement(self):
        """Test all circuits have measurement operations"""
        circuits = [
            QuantumCircuitFactory.create_entangled_chain(5),
            QuantumCircuitFactory.create_ghz_state(5),
            QuantumCircuitFactory.create_random_circuit(5, 2),
        ]

        for qc in circuits:
            gate_names = [instr.operation.name for instr in qc.data]
            assert "measure" in gate_names


class TestCircuitTypes:
    """Test different circuit properties"""

    def test_all_circuits_executable(self):
        """Test all circuit types can be created without errors"""
        circuit_creators = [
            QuantumCircuitFactory.create_entangled_chain,
            QuantumCircuitFactory.create_ghz_state,
        ]

        for creator in circuit_creators:
            try:
                qc = creator(8)
                assert qc is not None
                assert isinstance(qc, QuantumCircuit)
            except Exception as e:
                pytest.fail(f"Circuit creation failed: {e}")

    def test_circuit_validity(self):
        """Test circuits are valid Qiskit objects"""
        qc = QuantumCircuitFactory.create_entangled_chain(5)

        # Should be able to get circuit info
        assert qc.num_qubits > 0
        assert qc.num_clbits > 0
        assert qc.depth() >= 0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_single_qubit_circuit(self):
        """Test single qubit circuit"""
        qc = QuantumCircuitFactory.create_entangled_chain(1)
        assert qc.num_qubits == 1

    def test_zero_depth_random_circuit(self):
        """Test random circuit with zero depth"""
        qc = QuantumCircuitFactory.create_random_circuit(5, depth=0)
        assert isinstance(qc, QuantumCircuit)

    def test_large_circuit(self):
        """Test large circuit creation"""
        qc = QuantumCircuitFactory.create_entangled_chain(500)
        assert qc.num_qubits == 500
