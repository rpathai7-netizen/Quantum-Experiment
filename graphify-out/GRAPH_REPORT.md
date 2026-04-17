# Quantum Experiment Platform - Knowledge Graph Report

## God Nodes (Most Connected)

- **cloud_integration**: 5 classes
- **measurement_analysis**: 2 classes
- **circuit_types**: 1 classes
- **integrated_platform**: 1 classes

## Modules

### Antimatter Engine
- **File**: `antimatter_engine.py`
- **Functions**: annihilation_reactor, teleportation_protocol, run_benchmark
- **Dependencies**: time, sys, numpy

### Circuit Types
- **File**: `circuit_types.py`
- **Classes**: QuantumCircuitFactory
- **Functions**: list_circuit_types, create_entangled_chain, create_ghz_state, create_random_circuit, create_qaoa_circuit
- **Dependencies**: typing, random, numpy

### Cloud Integration
- **File**: `cloud_integration.py`
- **Classes**: CloudQuantumProvider, IBMQuantumProvider, AWSBraketProvider, GoogleQuantumProvider, QuantumCloudManager
- **Functions**: __init__, authenticate, run_circuit, __init__, authenticate
- **Dependencies**: typing, os, qiskit_ibm_runtime

### Complete Publication
- **File**: `complete_publication.py`
- **Dependencies**: datetime, os, json

### Examples
- **File**: `examples.py`
- **Functions**: example_basic_entanglement, example_scaling, example_circuit_comparison, example_state_analysis, example_cloud_computing
- **Dependencies**: measurement_analysis, integrated_platform

### Final Benchmark
- **File**: `final_benchmark.py`
- **Functions**: main
- **Dependencies**: scalable_simulator, qiskit, qiskit_aer

### Finalize Publication
- **File**: `finalize_publication.py`
- **Dependencies**: requests, json

### Generate Knowledge Graph
- **File**: `generate_knowledge_graph.py`
- **Functions**: gen_knowledge_graph, create_quantum_knowledge_base, create_knowledge_report
- **Dependencies**: subprocess, sys, json

### Github Publish
- **File**: `github_publish.py`
- **Dependencies**: requests, os, json

### Integrated Platform
- **File**: `integrated_platform.py`
- **Classes**: QuantumExperimentPlatform
- **Functions**: demo_basic_workflow, demo_circuit_types, demo_scaling, __init__, create_circuit
- **Dependencies**: typing, os, circuit_types

### Measurement Analysis
- **File**: `measurement_analysis.py`
- **Classes**: QuantumMeasurementAnalyzer, QuantumCircuitBenchmark
- **Functions**: __init__, get_statistics, calculate_shannon_entropy, calculate_purity, calculate_coherence
- **Dependencies**: typing, collections, math

### Nuclear Pasta 3D
- **File**: `nuclear_pasta_3d.py`
- **Functions**: get_ram_usage_gb, create_nuclear_pasta_3d, run_simulation
- **Dependencies**: time, os, numpy

### Quantum Circuit
- **File**: `quantum_circuit.py`
- **Dependencies**: qiskit, qiskit_aer

### Quantum Solar Walk
- **File**: `quantum_solar_walk.py`
- **Functions**: get_ram_usage_gb, create_solar_graph, build_walk_circuit, run_simulation
- **Dependencies**: time, os, matplotlib.pyplot

### Quick Benchmark
- **File**: `quick_benchmark.py`
- **Functions**: log
- **Dependencies**: datetime, sys, io

## Key Classes

### QuantumCircuitFactory
Factory for creating different types of quantum circuits

**Methods**: create_entangled_chain, create_ghz_state, create_random_circuit, create_qaoa_circuit, create_grover_oracle

### CloudQuantumProvider
Base class for cloud quantum computing providers

**Methods**: __init__, authenticate, run_circuit

### IBMQuantumProvider
Integration with IBM Quantum Experience

**Methods**: __init__, authenticate, list_backends, run_circuit

### GoogleQuantumProvider
Integration with Google Quantum AI (Cirq)

**Methods**: __init__, authenticate, list_backends

### QuantumCloudManager
Manages multiple cloud quantum providers

**Methods**: __init__, initialize_provider, show_all_backends, run_on_provider

### QuantumExperimentPlatform
Main platform for quantum computing experiments

**Methods**: __init__, create_circuit, run_local, run_cloud, analyze_results

### QuantumMeasurementAnalyzer
Comprehensive analysis of quantum measurement results

**Methods**: __init__, get_statistics, calculate_shannon_entropy, calculate_purity, calculate_coherence

### QuantumCircuitBenchmark
Benchmark utilities for quantum circuits

**Methods**: gate_count, circuit_depth, circuit_size

