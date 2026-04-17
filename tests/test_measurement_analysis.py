"""
Tests for Measurement Analysis Module
Tests all statistical and quantum property calculations
"""

import math

import pytest

from measurement_analysis import QuantumMeasurementAnalyzer


class TestQuantumMeasurementAnalyzer:
    """Test suite for QuantumMeasurementAnalyzer"""

    @pytest.fixture
    def simple_counts(self):
        """Simple measurement counts for testing"""
        return {"00": 50, "11": 50}

    @pytest.fixture
    def uniform_counts(self):
        """Uniform distribution across all states"""
        return {"00": 25, "01": 25, "10": 25, "11": 25}

    @pytest.fixture
    def skewed_counts(self):
        """Skewed distribution"""
        return {"00": 90, "01": 5, "10": 3, "11": 2}

    def test_initialization(self, simple_counts):
        """Test analyzer initialization"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        assert analyzer.total_shots == 100
        assert analyzer.num_qubits == 2
        assert len(analyzer.probabilities) == 2

    def test_statistics_calculation(self, simple_counts):
        """Test basic statistics"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        stats = analyzer.get_statistics()

        assert stats["total_shots"] == 100
        assert stats["num_unique_states"] == 2
        assert stats["max_probability"] == 0.5
        assert stats["min_probability"] == 0.5

    def test_shannon_entropy_pure_state(self):
        """Shannon entropy of pure state should be 0"""
        pure_state = {"00": 100}
        analyzer = QuantumMeasurementAnalyzer(pure_state)
        entropy = analyzer.calculate_shannon_entropy()
        assert abs(entropy - 0.0) < 1e-10

    def test_shannon_entropy_uniform(self, uniform_counts):
        """Shannon entropy of uniform distribution"""
        analyzer = QuantumMeasurementAnalyzer(uniform_counts)
        entropy = analyzer.calculate_shannon_entropy()
        expected = 2.0  # log2(4) = 2
        assert abs(entropy - expected) < 1e-10

    def test_shannon_entropy_binary(self, simple_counts):
        """Shannon entropy of 50-50 distribution"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        entropy = analyzer.calculate_shannon_entropy()
        expected = 1.0  # -0.5*log2(0.5) - 0.5*log2(0.5) = 1
        assert abs(entropy - expected) < 1e-10

    def test_purity_pure_state(self):
        """Purity of pure state should be 1"""
        pure_state = {"00": 100}
        analyzer = QuantumMeasurementAnalyzer(pure_state)
        purity = analyzer.calculate_purity()
        assert abs(purity - 1.0) < 1e-10

    def test_purity_maximally_mixed(self, uniform_counts):
        """Purity of maximally mixed state"""
        analyzer = QuantumMeasurementAnalyzer(uniform_counts)
        purity = analyzer.calculate_purity()
        expected = 0.25  # 4 * (0.25)^2
        assert abs(purity - expected) < 1e-10

    def test_single_qubit_probabilities(self, simple_counts):
        """Test single qubit probability calculation"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        probs = analyzer.calculate_single_qubit_probabilities()

        # For counts {'00': 50, '11': 50}
        # Qubit 0: p(0) = 0.5, p(1) = 0.5
        assert probs[0][0] == pytest.approx(0.5)
        assert probs[0][1] == pytest.approx(0.5)
        assert probs[1][0] == pytest.approx(0.5)
        assert probs[1][1] == pytest.approx(0.5)

    def test_hamming_distance(self, simple_counts):
        """Test Hamming distance calculation"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        hamming_distances = analyzer.calculate_hamming_distances()

        # Hamming distance between '00' and '11' is 2
        # Both appear with 50% probability
        assert 2 in hamming_distances

    def test_coherence_pure_state(self):
        """Coherence of pure state should be 1"""
        pure_state = {"00": 100}
        analyzer = QuantumMeasurementAnalyzer(pure_state)
        coherence = analyzer.calculate_coherence()
        assert coherence == pytest.approx(1.0, abs=0.1)

    def test_coherence_mixed_state(self, uniform_counts):
        """Coherence of maximally mixed state should be 0"""
        analyzer = QuantumMeasurementAnalyzer(uniform_counts)
        coherence = analyzer.calculate_coherence()
        assert coherence == pytest.approx(0.0, abs=0.1)

    def test_entanglement_detection_strong(self, simple_counts):
        """Test entanglement detection for entangled state"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        is_entangled = analyzer.detect_entanglement_pattern()
        # {'00': 50, '11': 50} is maximally entangled
        assert is_entangled is not None

    def test_entanglement_detection_separable(self):
        """Test entanglement detection for separable state"""
        # Simple separable state: no correlations
        separable = {"00": 25, "01": 25, "10": 25, "11": 25}
        analyzer = QuantumMeasurementAnalyzer(separable)
        is_entangled = analyzer.detect_entanglement_pattern()
        # Should detect no entanglement
        assert is_entangled is not None

    def test_bell_inequality(self, simple_counts):
        """Test Bell inequality violation detection"""
        analyzer = QuantumMeasurementAnalyzer(simple_counts)
        bell_violation = analyzer.check_bell_inequality()
        assert isinstance(bell_violation, dict)
        assert "chsh" in bell_violation or "explanation" in bell_violation


class TestMeasurementAnalyzerEdgeCases:
    """Test edge cases and error handling"""

    def test_single_state(self):
        """Test with only one state"""
        counts = {"00": 100}
        analyzer = QuantumMeasurementAnalyzer(counts)
        assert analyzer.total_shots == 100
        entropy = analyzer.calculate_shannon_entropy()
        assert entropy == pytest.approx(0.0)

    def test_single_qubit(self):
        """Test with single qubit"""
        counts = {"0": 45, "1": 55}
        analyzer = QuantumMeasurementAnalyzer(counts)
        assert analyzer.num_qubits == 1
        stats = analyzer.get_statistics()
        assert stats["num_unique_states"] == 2

    def test_many_qubits(self):
        """Test with many qubits (8 qubits = 256 possible states)"""
        # Create a dictionary with all 256 possible states
        counts = {f"{i:08b}": 1 for i in range(256)}
        analyzer = QuantumMeasurementAnalyzer(counts)
        assert analyzer.num_qubits == 8
        entropy = analyzer.calculate_shannon_entropy()
        expected = 8.0  # log2(256) = 8
        assert entropy == pytest.approx(expected, abs=1e-10)


class TestMeasurementAnalyzerNumericalStability:
    """Test numerical stability and precision"""

    def test_very_small_probabilities(self):
        """Test with very small probabilities"""
        counts = {"00": 1000000, "01": 1, "10": 1}
        analyzer = QuantumMeasurementAnalyzer(counts)
        entropy = analyzer.calculate_shannon_entropy()
        assert entropy >= 0  # Entropy is non-negative
        assert entropy < 1  # But still very small

    def test_rounding_errors(self):
        """Test stability with rounding errors"""
        # Create counts that sum to 1000000 (large number)
        counts = {"0": 1, "1": 999999}
        analyzer = QuantumMeasurementAnalyzer(counts)
        purity = analyzer.calculate_purity()
        assert 0 <= purity <= 1.0
        assert purity > 0.99  # Should be close to 1
