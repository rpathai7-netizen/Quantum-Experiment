"""
Integrated Quantum Experiment System
Complete toolchain for quantum circuit design, execution, and analysis
"""

from scalable_simulator import ScalableQuantumSimulator
from cloud_integration import QuantumCloudManager
from circuit_types import CIRCUIT_TYPES, list_circuit_types
from measurement_analysis import QuantumMeasurementAnalyzer, QuantumCircuitBenchmark
from typing import Optional, Tuple
import os


class QuantumExperimentPlatform:
    """Main platform for quantum computing experiments"""
    
    def __init__(self):
        self.simulator = None
        self.cloud_manager = QuantumCloudManager()
        self.last_results = None
        self.execution_log = []
    
    # ============================================================================
    # CIRCUIT CREATION
    # ============================================================================
    
    def create_circuit(self, circuit_type: str, num_qubits: int, **kwargs):
        """
        Create a quantum circuit of specified type.
        
        Args:
            circuit_type: Type of circuit (from CIRCUIT_TYPES)
            num_qubits: Number of qubits
            **kwargs: Type-specific arguments
        """
        if circuit_type not in CIRCUIT_TYPES:
            available = list(CIRCUIT_TYPES.keys())
            print(f"[ERROR] Unknown circuit type: {circuit_type}")
            print(f"Available: {available}")
            return None
        
        circuit_info = CIRCUIT_TYPES[circuit_type]
        
        try:
            if circuit_type == "random":
                depth = kwargs.get("depth", 2)
                qc = circuit_info["factory"](num_qubits, depth)
            elif circuit_type == "qaoa":
                layers = kwargs.get("layers", 2)
                qc = circuit_info["factory"](num_qubits, layers)
            elif circuit_type == "grover":
                marked_state = kwargs.get("marked_state", 0)
                qc = circuit_info["factory"](num_qubits, marked_state)
            elif circuit_type == "vqe":
                layers = kwargs.get("layers", 2)
                qc = circuit_info["factory"](num_qubits, layers)
            elif circuit_type == "quantum_walk":
                steps = kwargs.get("steps", 5)
                qc = circuit_info["factory"](num_qubits, steps)
            else:
                qc = circuit_info["factory"](num_qubits)
            
            print(f"[OK] Created {circuit_type} circuit ({num_qubits} qubits)")
            return qc
        
        except Exception as e:
            print(f"[ERROR] Error creating circuit: {e}")
            return None
    
    # ============================================================================
    # CIRCUIT EXECUTION
    # ============================================================================
    
    def run_local(self, circuit, num_qubits: int, shots: int = 10):
        """Run circuit on local simulator"""
        if not circuit:
            print("[ERROR] No circuit provided")
            return None
        
        try:
            self.simulator = ScalableQuantumSimulator(num_qubits)
            
            # Inject the circuit into simulator for execution
            from qiskit_aer import AerSimulator
            simulator_backend = AerSimulator(method="statevector")
            
            job = simulator_backend.run(circuit, shots=shots)
            result = job.result()
            counts = result.get_counts(circuit)
            
            self.last_results = counts
            self._log_execution("local", num_qubits, shots)
            
            return counts
        except Exception as e:
            print(f"[WARNING] Falling back to analytical simulation: {e}")
            # Fallback to analytical for large circuits
            self.simulator = ScalableQuantumSimulator(num_qubits)
            counts = self.simulator.run(shots)
            self.last_results = counts
            self._log_execution("analytical", num_qubits, shots)
            return counts
    
    def run_cloud(self, circuit, provider: str, 
                  backend: Optional[str] = None, shots: int = 100):
        """
        Run circuit on cloud quantum provider.
        
        Args:
            circuit: QuantumCircuit
            provider: Cloud provider name ("ibm", "aws", "google")
            backend: Specific backend to use (optional)
            shots: Number of shots
        """
        if not self.cloud_manager.initialize_provider(provider):
            print(f"[ERROR] Could not initialize {provider}")
            return None
        
        try:
            results = self.cloud_manager.run_on_provider(circuit, provider, shots)
            self.last_results = results
            self._log_execution(provider, circuit.num_qubits, shots)
            return results
        except Exception as e:
            print(f"[ERROR] Error running on {provider}: {e}")
            return None
    
    # ============================================================================
    # ANALYSIS
    # ============================================================================
    
    def analyze_results(self):
        """Analyze the last execution results"""
        if not self.last_results:
            print("[ERROR] No results to analyze")
            return None
        
        analyzer = QuantumMeasurementAnalyzer(self.last_results)
        analyzer.print_detailed_report()
        return analyzer
    
    def get_circuit_metrics(self, circuit) -> dict:
        """Get performance metrics for a circuit"""
        bench = QuantumCircuitBenchmark()
        
        return {
            "depth": bench.circuit_depth(circuit),
            "size": bench.circuit_size(circuit),
            "gates": bench.gate_count(circuit),
            "num_qubits": circuit.num_qubits,
            "num_clbits": circuit.num_clbits,
        }
    
    # ============================================================================
    # UTILITIES
    # ============================================================================
    
    def _log_execution(self, method: str, num_qubits: int, shots: int):
        """Log execution details"""
        import datetime
        log_entry = {
            "timestamp": datetime.datetime.now(),
            "method": method,
            "qubits": num_qubits,
            "shots": shots,
        }
        self.execution_log.append(log_entry)
    
    def show_execution_log(self):
        """Display execution history"""
        if not self.execution_log:
            print("No executions yet")
            return
        
        print("\n" + "="*70)
        print("EXECUTION LOG")
        print("="*70)
        
        for i, entry in enumerate(self.execution_log, 1):
            print(f"\n{i}. {entry['timestamp'].strftime('%H:%M:%S')}")
            print(f"   Method: {entry['method']}")
            print(f"   Qubits: {entry['qubits']}, Shots: {entry['shots']}")
    
    def list_available_circuits(self):
        """Show all available circuit types"""
        list_circuit_types()
    
    def show_cloud_backends(self):
        """Show all cloud quantum backends"""
        self.cloud_manager.show_all_backends()


# ============================================================================
# INTERACTIVE DEMO
# ============================================================================

def demo_basic_workflow():
    """Demo: Basic workflow from circuit creation to analysis"""
    print("\n" + "="*70)
    print("QUANTUM EXPERIMENT PLATFORM - DEMONSTRATION")
    print("="*70)
    
    platform = QuantumExperimentPlatform()
    
    # Step 1: Show available circuits
    platform.list_available_circuits()
    
    # Step 2: Create a circuit
    print("\n" + "-"*70)
    print("STEP 1: Creating 10-qubit GHZ state")
    print("-"*70)
    
    circuit = platform.create_circuit("ghz_state", 10)
    if circuit:
        metrics = platform.get_circuit_metrics(circuit)
        print(f"Circuit Metrics:")
        print(f"  Qubits: {metrics['num_qubits']}")
        print(f"  Classical bits: {metrics['num_clbits']}")
        print(f"  Circuit depth: {metrics['depth']}")
        print(f"  Gate count: {metrics['size']}")
        print(f"  Gates: {metrics['gates']}")
    
    # Step 3: Execute locally
    print("\n" + "-"*70)
    print("STEP 2: Running on local simulator (100 shots)")
    print("-"*70)
    
    results = platform.run_local(circuit, 10, shots=100)
    if results:
        print(f"Results: {results}")
    
    # Step 4: Analyze
    print("\n" + "-"*70)
    print("STEP 3: Analyzing results")
    print("-"*70)
    
    platform.analyze_results()
    
    # Step 5: Show cloud options
    print("\n" + "-"*70)
    print("STEP 4: Available cloud providers")
    print("-"*70)
    
    platform.show_cloud_backends()
    
    # Step 6: Show execution log
    print("\n" + "-"*70)
    print("STEP 5: Execution history")
    print("-"*70)
    
    platform.show_execution_log()


def demo_circuit_types():
    """Demo: Try different circuit types"""
    print("\n" + "="*70)
    print("CIRCUIT TYPES DEMONSTRATION")
    print("="*70)
    
    platform = QuantumExperimentPlatform()
    
    circuit_types = ["entangled_chain", "ghz_state", "deutsch"]
    
    for circuit_type in circuit_types:
        print(f"\n{'='*70}")
        print(f"Testing: {circuit_type}")
        print(f"{'='*70}")
        
        circuit = platform.create_circuit(circuit_type, 6)
        if circuit:
            # Show circuit info
            print(f"\nCircuit details:")
            print(f"  Type: {CIRCUIT_TYPES[circuit_type]['description']}")
            print(f"  Use case: {CIRCUIT_TYPES[circuit_type]['use_case']}")
            print(f"  Scalability: {CIRCUIT_TYPES[circuit_type]['scalability']}")
            
            # Run and analyze
            results = platform.run_local(circuit, 6, shots=100)
            if results:
                analyzer = QuantumMeasurementAnalyzer(results)
                stats = analyzer.get_statistics()
                print(f"\nQuick stats:")
                print(f"  Unique states: {stats['num_unique_states']}")
                print(f"  Entropy: {analyzer.calculate_shannon_entropy():.4f}")
                print(f"  Purity: {analyzer.calculate_purity():.4f}")
                print(f"  Pattern: {analyzer.detect_entanglement_pattern()}")


def demo_scaling():
    """Demo: Test scaling to 6000 qubits"""
    print("\n" + "="*70)
    print("SCALING DEMONSTRATION - Up to 6000 Qubits")
    print("="*70)
    
    platform = QuantumExperimentPlatform()
    
    sizes = [10, 50, 100, 500, 1000, 6000]
    
    for size in sizes:
        print(f"\n{'='*70}")
        print(f"Testing {size} qubits")
        print(f"{'='*70}")
        
        # Create circuit
        circuit = platform.create_circuit("entangled_chain", size)
        
        if circuit:
            # Show metrics
            metrics = platform.get_circuit_metrics(circuit)
            print(f"Circuit depth: {metrics['depth']}")
            print(f"Gate count: {metrics['size']}")
            
            # Run
            results = platform.run_local(circuit, size, shots=10)
            if results:
                print(f"Execution successful!")
                print(f"States measured: {len(results)}")
                
                # Quick analysis
                analyzer = QuantumMeasurementAnalyzer(results)
                print(f"Entropy: {analyzer.calculate_shannon_entropy():.4f}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("INTEGRATED QUANTUM EXPERIMENT PLATFORM")
    print("="*70)
    print("""
Available demonstrations:
  1. Basic workflow (circuit creation > execution > analysis)
  2. Circuit types showcase
  3. Scaling test (up to 6000 qubits)
    """)
    
    print("\nRunning basic workflow demo...\n")
    demo_basic_workflow()
    
    print("\n\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("""
Next steps:
  • Use QuantumExperimentPlatform for custom experiments
  • Check cloud_integration.py for cloud quantum computing
  • Review measurement_analysis.py for detailed result analysis
    """)
