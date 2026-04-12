"""
Advanced Measurement Analysis for Quantum Circuits
Statistical analysis, entropy, correlations, and visualization
"""

import numpy as np
from typing import Dict, List, Tuple
from collections import Counter
import math


class QuantumMeasurementAnalyzer:
    """Comprehensive analysis of quantum measurement results"""
    
    def __init__(self, counts: Dict[str, int]):
        """
        Initialize with measurement counts.
        
        Args:
            counts: Dictionary mapping bitstrings to counts
                   e.g., {'00': 45, '11': 55}
        """
        self.counts = counts
        self.total_shots = sum(counts.values())
        self.probabilities = {
            bitstring: count / self.total_shots 
            for bitstring, count in counts.items()
        }
        self.num_qubits = len(list(counts.keys())[0])
    
    def get_statistics(self) -> Dict:
        """Calculate basic statistics"""
        probs = list(self.probabilities.values())
        
        return {
            "total_shots": self.total_shots,
            "num_unique_states": len(self.counts),
            "max_probability": max(probs),
            "min_probability": min(probs),
            "mean_probability": np.mean(probs),
            "std_probability": np.std(probs),
        }
    
    def calculate_shannon_entropy(self) -> float:
        """
        Calculate Shannon entropy of the measurement distribution.
        Measures uncertainty/mixedness of the state.
        
        Returns:
            Entropy value (0 = pure state, log2(N) = maximally mixed)
        """
        entropy = 0.0
        for prob in self.probabilities.values():
            if prob > 0:
                entropy -= prob * math.log2(prob)
        return entropy
    
    def calculate_purity(self) -> float:
        """
        Calculate purity of the quantum state.
        P = Tr(ρ²) = sum(p_i²)
        
        Returns:
            Purity value (1 = pure state, 1/N = maximally mixed)
        """
        purity = sum(p**2 for p in self.probabilities.values())
        return purity
    
    def calculate_coherence(self) -> float:
        """
        Measure coherence of the state.
        Based on off-diagonal elements of density matrix.
        """
        # Approximate coherence from entropy
        entropy = self.calculate_shannon_entropy()
        max_entropy = math.log2(len(self.probabilities))
        coherence = 1.0 - (entropy / max_entropy if max_entropy > 0 else 0)
        return max(0, coherence)
    
    def calculate_single_qubit_probabilities(self) -> Dict[int, Tuple[float, float]]:
        """
        Calculate probability of measuring 0 and 1 for each qubit.
        
        Returns:
            Dictionary mapping qubit index to (P(0), P(1))
        """
        qubit_probs = {}
        
        for qubit_idx in range(self.num_qubits):
            prob_0 = 0.0
            prob_1 = 0.0
            
            for bitstring, prob in self.probabilities.items():
                bit = int(bitstring[qubit_idx])
                if bit == 0:
                    prob_0 += prob
                else:
                    prob_1 += prob
            
            qubit_probs[qubit_idx] = (prob_0, prob_1)
        
        return qubit_probs
    
    def calculate_correlations(self) -> Dict[Tuple[int, int], float]:
        """
        Calculate correlation between pairs of qubits.
        Returns the correlation coefficient C_ij.
        """
        correlations = {}
        
        for i in range(self.num_qubits):
            for j in range(i + 1, self.num_qubits):
                # Calculate expectation values
                expect_0i_0j = 0.0  # P(both 0)
                expect_1i_1j = 0.0  # P(both 1)
                
                for bitstring, prob in self.probabilities.items():
                    bit_i = int(bitstring[i])
                    bit_j = int(bitstring[j])
                    
                    if bit_i == 0 and bit_j == 0:
                        expect_0i_0j += prob
                    elif bit_i == 1 and bit_j == 1:
                        expect_1i_1j += prob
                
                # Correlation: probability of same values
                correlation = expect_0i_0j + expect_1i_1j
                
                # Only store significant correlations
                if abs(correlation - 0.5) > 0.01:
                    correlations[(i, j)] = correlation
        
        return correlations
    
    def find_most_probable_states(self, top_n: int = 5) -> List[Tuple[str, float]]:
        """Get the most probable measurement outcomes"""
        sorted_states = sorted(
            self.probabilities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_states[:top_n]
    
    def analyze_hamming_distance_distribution(self) -> Dict[int, int]:
        """
        Analyze distribution of bitstrings by Hamming distance.
        Returns histogram of how many states have each distance.
        """
        if not self.counts:
            return {}
        
        # Get a reference state (could be all zeros)
        reference = '0' * self.num_qubits
        
        distance_dist = {}
        
        for bitstring, count in self.counts.items():
            # Calculate Hamming distance
            distance = sum(c1 != c2 for c1, c2 in zip(bitstring, reference))
            
            if distance not in distance_dist:
                distance_dist[distance] = 0
            distance_dist[distance] += count
        
        return distance_dist
    
    def detect_entanglement_pattern(self) -> str:
        """
        Detect potential entanglement patterns.
        """
        unique_states = len(self.counts)
        
        if unique_states == 1:
            return "PRODUCT STATE - No entanglement detected"
        elif unique_states == 2:
            states = list(self.counts.keys())
            # Check if states are complementary (Bell pair signature)
            hamming = sum(c1 != c2 for c1, c2 in zip(states[0], states[1]))
            if hamming == len(states[0]):
                return "BELL PAIR - Maximum entanglement (2-qubit)"
            else:
                return "PARTIAL ENTANGLEMENT - Multi-qubit correlated state"
        else:
            entropy = self.calculate_shannon_entropy()
            max_entropy = math.log2(len(self.counts))
            
            if entropy / max_entropy > 0.8:
                return "MIXED STATE - High entanglement/disorder"
            else:
                return "SUPERPOSITION - Partial coherence"
    
    def print_detailed_report(self):
        """Print comprehensive analysis report"""
        print("\n" + "="*70)
        print("QUANTUM MEASUREMENT ANALYSIS REPORT")
        print("="*70)
        
        # Basic statistics
        stats = self.get_statistics()
        print(f"\n[STATS] BASIC STATISTICS")
        print(f"   Total shots: {stats['total_shots']}")
        print(f"   Unique states observed: {stats['num_unique_states']}")
        print(f"   Max probability: {stats['max_probability']:.4f}")
        print(f"   Min probability: {stats['min_probability']:.4f}")
        print(f"   Mean probability: {stats['mean_probability']:.4f}")
        print(f"   Std deviation: {stats['std_probability']:.4f}")
        
        # Quantum state properties
        entropy = self.calculate_shannon_entropy()
        purity = self.calculate_purity()
        coherence = self.calculate_coherence()
        max_entropy = math.log2(len(self.probabilities))
        
        print(f"\n[STATE] QUANTUM STATE PROPERTIES")
        print(f"   Shannon entropy: {entropy:.4f} / {max_entropy:.4f}") 
        print(f"   Purity: {purity:.4f} (1.0 = pure)")
        print(f"   Coherence: {coherence:.4f} (1.0 = fully coherent)")
        
        # Single qubit analysis
        print(f"\n[QUBITS] SINGLE-QUBIT PROBABILITIES")
        qubit_probs = self.calculate_single_qubit_probabilities()
        for qubit, (p0, p1) in sorted(qubit_probs.items())[:5]:
            prob_dist = "*" * int(p0 * 20) + "-" * int((1-p0) * 20)
            print(f"   Q{qubit}: |0>={p0:.2%} |1>={p1:.2%} {prob_dist}")
        if self.num_qubits > 5:
            print(f"   ... and {self.num_qubits - 5} more qubits")
        
        # Correlations
        correlations = self.calculate_correlations()
        if correlations:
            print(f"\n[CORR] QUBIT CORRELATIONS (pairs with |C-0.5| > 0.01)")
            for (i, j), corr in sorted(correlations.items())[:5]:
                print(f"   Q{i}-Q{j}: {corr:.4f} {'(STRONG CORRELATION)' if abs(corr-1) < 0.1 else ''}")
        
        # Most probable states
        print(f"\n[STATES] MOST PROBABLE STATES")
        for state, prob in self.find_most_probable_states(5):
            bar = "*" * int(prob * 30)
            print(f"   {state}: {prob:.4f} ({int(prob*self.total_shots)} counts) {bar}")
        
        # Entanglement detection
        print(f"\n[ENT] ENTANGLEMENT ANALYSIS")
        print(f"   Status: {self.detect_entanglement_pattern()}")
        
        # Hamming distance
        hamming_dist = self.analyze_hamming_distance_distribution()
        if hamming_dist:
            print(f"\n[DIST] HAMMING DISTANCE DISTRIBUTION")
            for distance in sorted(hamming_dist.keys())[:8]:
                count = hamming_dist[distance]
                bar = "*" * int(count / max(hamming_dist.values()) * 20)
                print(f"   Distance {distance}: {count:4d} states {bar}")
        
        print("\n" + "="*70)


class QuantumCircuitBenchmark:
    """Benchmark utilities for quantum circuits"""
    
    @staticmethod
    def gate_count(circuit) -> Dict[str, int]:
        """Count gate operations in circuit"""
        gate_counts = {}
        
        for instruction, qargs, cargs in circuit.data:
            gate_name = instruction.name
            if gate_name not in gate_counts:
                gate_counts[gate_name] = 0
            gate_counts[gate_name] += 1
        
        return gate_counts
    
    @staticmethod
    def circuit_depth(circuit) -> int:
        """Get circuit depth"""
        return circuit.depth()
    
    @staticmethod
    def circuit_size(circuit) -> int:
        """Get circuit size (number of gates)"""
        return len(circuit)


if __name__ == "__main__":
    # Example analysis
    print("\n" + "="*70)
    print("QUANTUM MEASUREMENT ANALYSIS EXAMPLE")
    print("="*70)
    
    # Simulate some measurement results
    example_counts = {
        '00': 45,
        '01': 8,
        '10': 7,
        '11': 40,
    }
    
    analyzer = QuantumMeasurementAnalyzer(example_counts)
    analyzer.print_detailed_report()
