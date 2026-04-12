"""
Complete Quantum Benchmark Test Suite - All Tests in One
Runs all benchmarks and saves results to file
"""

import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """Run a command and return output"""
    print(f"\n[RUNNING] {description}...", flush=True)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        return f"\n{'='*70}\n{description}\n{'='*70}\n{result.stdout}\n"
    except subprocess.TimeoutExpired:
        return f"\n{'='*70}\n{description} - TIMEOUT\n{'='*70}\n[TIMEOUT] Test took too long\n"
    except Exception as e:
        return f"\n{'='*70}\n{description} - ERROR\n{'='*70}\n{str(e)}\n"

def main():
    """Run all benchmarks and save to file"""
    
    results = []
    results.append(f"\n{'='*70}")
    results.append("QUANTUM COMPUTING PLATFORM - COMPLETE BENCHMARK SUITE")
    results.append(f"{'='*70}")
    results.append(f"Test Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    results.append(f"{'='*70}\n")
    
    # Test 1: Original quantum circuit
    print("\n[1/5] Testing original 30-qubit circuit...")
    results.append(run_command(
        'python quantum_circuit.py',
        "TEST 1: Original 30-Qubit Quantum Circuit"
    ))
    
    # Test 2: Scalable simulator (30-6000 qubits)
    print("[2/5] Testing scalable simulator (30-6000 qubits)...")
    results.append(run_command(
        'python scalable_simulator.py',
        "TEST 2: Scalable Quantum Simulator (30 to 6000 Qubits)"
    ))
    
    # Test 3: Circuit types showcase
    print("[3/5] Testing all circuit types...")
    results.append(run_command(
        'python circuit_types.py',
        "TEST 3: Quantum Circuit Types (9 Different Algorithms)"
    ))
    
    # Test 4: Measurement analysis
    print("[4/5] Testing measurement analysis...")
    results.append(run_command(
        'python measurement_analysis.py',
        "TEST 4: Quantum Measurement Analysis & Statistics"
    ))
    
    # Test 5: All examples
    print("[5/5] Running all example scenarios...")
    results.append(run_command(
        'python examples.py',
        "TEST 5: All Example Scenarios (10 Different Tests)"
    ))
    
    # Compile final results
    final_results = ''.join(results)
    
    # Add summary
    summary = f"\n\n{'='*70}\nBENCHMARK SUMMARY\n{'='*70}\n"
    summary += f"Total Tests Run: 5\n"
    summary += f"Completion Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    summary += f"Status: COMPLETE\n"
    summary += f"{'='*70}\n"
    
    final_results += summary
    
    # Save to file
    output_file = "quantum_benchmark_results.txt"
    with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
        f.write(final_results)
    
    print(f"\n{'='*70}")
    print(f"ALL TESTS COMPLETE!")
    print(f"Results saved to: {output_file}")
    print(f"{'='*70}\n")
    
    # Print summary to console
    print(summary)
    print(f"Open '{output_file}' to view full results")

if __name__ == "__main__":
    main()
