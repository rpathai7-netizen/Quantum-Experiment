# Quantum Computing Experiment Platform

[![GitHub Release](https://img.shields.io/github/v/release/rpathai7-netizen/Quantum-Experiment?include_prereleases&label=version)](https://github.com/rpathai7-netizen/Quantum-Experiment/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-v0.41%2B-green)](https://qiskit.org/)
[![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baadc.svg)](CODE_OF_CONDUCT.md)

A complete, production-ready quantum computing system supporting local simulation, cloud integration, and advanced analysis. **Scales from 30 qubits to 6000+ qubits** using analytical methods.

**Quick Links:** [📖 Docs](#-system-overview) | [⚡ Quick Start](QUICKSTART.md) | [📦 Installation](INSTALLATION.md) | [🚀 Features](FEATURES.md) | [❓ FAQ](FAQ.md) | [⭐ Star us](#-support)

## 📋 System Overview

```
┌─────────────────────────────────────────────────────┐
│        Quantum Experiment Platform                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │  Local Simulator │  │ Cloud Providers  │       │
│  │  (Qiskit Aer)    │  │ (IBM, AWS, Goog)│       │
│  └──────────────────┘  └──────────────────┘       │
│           │                    │                    │
│           └────────┬───────────┘                    │
│                    ▼                                 │
│  ┌─────────────────────────────────────┐           │
│  │   Circuit Execution Engine           │           │
│  │   (Local/Analytical/Cloud)          │           │
│  └─────────────────────────────────────┘           │
│           │                                          │
│           ▼                                          │
│  ┌─────────────────────────────────────┐           │
│  │   Measurement Analysis Module        │           │
│  │   (Entropy, Correlations, Metrics)  │           │
│  └─────────────────────────────────────┘           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🚀 Features

### 1. **Scalable Simulator** (`scalable_simulator.py`)
- **30 qubits**: Full state vector simulation (Qiskit Aer)
- **100-500 qubits**: Analytical simulation (no state vector)
- **6000+ qubits**: Mathematical approximation (memory-free)

```python
simulator = ScalableQuantumSimulator(6000)
results = simulator.run(shots=10)
# Output: {'1111...1111': 5, '0000...0000': 5}
```

### 2. **Cloud Integration** (`cloud_integration.py`)
Connect to quantum cloud providers:
- **IBM Quantum** (up to 433 qubits)
- **AWS Braket** (SV1, DM1 simulators + IonQ, Rigetti)
- **Google Quantum** (Cirq framework, Sycamore access)

```python
manager = QuantumCloudManager()
manager.initialize_provider("ibm", api_key="your-key")
results = manager.run_on_provider(circuit, "ibm", shots=100)
```

### 3. **Circuit Types** (`circuit_types.py`)
9 different quantum circuit architectures:

| Circuit Type | Description | Scalability | Use Case |
|---|---|---|---|
| `entangled_chain` | CNOT chain entanglement | ⭐⭐⭐⭐⭐ | Testing entanglement |
| `ghz_state` | Central control qubit | ⭐⭐⭐⭐⭐ | Maximum entanglement |
| `random` | Random gates | ⭐⭐⭐ | Stress testing |
| `qaoa` | Optimization algorithm | ⭐⭐⭐ | Combinatorial problems |
| `grover` | Database search | ⭐ | Quantum search |
| `vqe` | Variational eigensolver | ⭐⭐⭐ | Ground state energy |
| `quantum_walk` | Graph random walk | ⭐⭐ | Graph algorithms |
| `deutsch` | Function testing | ⭐⭐⭐⭐⭐ | Educational |
| `phase_estimation` | Eigenvalue estimation | ⭐ | Eigenvalue problems |

### 4. **Measurement Analysis** (`measurement_analysis.py`)
Comprehensive quantum state analysis:

- **Statistical analysis**: Shot distribution, probability statistics
- **Entropy**: Shannon entropy & purity measurement
- **Correlations**: Qubit-to-qubit correlation detection
- **Entanglement detection**: Identifies entanglement patterns
- **Hamming distance**: State space distribution analysis
- **Single qubit probabilities**: P(|0⟩) and P(|1⟩) per qubit

```python
analyzer = QuantumMeasurementAnalyzer(results)
analyzer.print_detailed_report()
```

### 5. **Integrated Platform** (`integrated_platform.py`)
Unified interface combining all components:

```python
platform = QuantumExperimentPlatform()

# Create circuit
circuit = platform.create_circuit("ghz_state", 30)

# Run locally
results = platform.run_local(circuit, 30, shots=100)

# Analyze
analyzer = platform.analyze_results()

# Or run on cloud
results = platform.run_cloud(circuit, "ibm", shots=100)
```

## 📊 Quick Start Examples

### Example 1: Simple Entanglement Test
```python
from integrated_platform import QuantumExperimentPlatform

platform = QuantumExperimentPlatform()

# Create 30-qubit entangled circuit
circuit = platform.create_circuit("entangled_chain", 30)

# Run 100 shots
results = platform.run_local(circuit, 30, shots=100)
# Results: {'0000...0000': 48, '1111...1111': 52}

# Analyze
platform.analyze_results()
```

### Example 2: Scaling to 6000 Qubits
```python
# Analytical simulation (instant, no memory overhead)
simulator = ScalableQuantumSimulator(6000)
results = simulator.run(shots=10)

simulator.print_results(results)
```

### Example 3: Cloud Quantum Computing
```python
from cloud_integration import QuantumCloudManager

manager = QuantumCloudManager()

# Show available backends
manager.show_all_backends()

# Initialize IBM Quantum
if manager.initialize_provider("ibm", api_key="your_api_key"):
    results = manager.run_on_provider(circuit, "ibm", shots=100)
```

## 🔧 Installation & Setup

### Prerequisites
```bash
pip install qiskit qiskit-aer numpy
```

### Optional: Cloud Provider Setup

**IBM Quantum:**
1. Create account: https://quantum-computing.ibm.com/
2. Get API key from dashboard
3. Set environment: `set QISKIT_IBM_API_KEY=your-key` (Windows)
4. Install: `pip install qiskit-ibm-runtime`

**AWS Braket:**
1. Create AWS account
2. Configure: `aws configure`
3. Install: `pip install amazon-braket-sdk`

**Google Quantum (Cirq):**
1. Install: `pip install cirq`
2. Research collaboration required for hardware

## 📁 File Structure

```
Quantum Experiment/
├── quantum_circuit.py          # Original 30-qubit circuit
├── scalable_simulator.py       # 30-6000 qubit simulator
├── cloud_integration.py        # Cloud provider connectors
├── circuit_types.py            # 9 circuit architectures
├── measurement_analysis.py     # Analysis & statistics
├── integrated_platform.py      # Main unified interface
└── README.md                   # This file
```

## 🧪 Available Circuit Types

### Entangled Chain (CNOT)
- Full linear entanglement
- Analytical solution: always all-0s or all-1s
- Perfect for testing up to 6000 qubits

### GHZ State
- Central qubit controls all others
- Maximum entanglement demonstration
- Great for testing correlations

### QAOA
- Quantum Approximate Optimization Algorithm
- For combinatorial optimization
- Parameterized variational circuit

### Grover's Algorithm
- Unsorted database search
- Quadratic speedup over classical
- Educational quantum algorithm

### VQE
- Variational Quantum Eigensolver
- Ground state energy estimation
- Hybrid classical-quantum

### More...
See `circuit_types.py` for all 9 types

## 📈 Analysis Capabilities

```python
analyzer = QuantumMeasurementAnalyzer(results)

# Get statistics
stats = analyzer.get_statistics()
print(f"Unique states: {stats['num_unique_states']}")

# Calculate properties
entropy = analyzer.calculate_shannon_entropy()
purity = analyzer.calculate_purity()
coherence = analyzer.calculate_coherence()

# Find correlations
correlations = analyzer.calculate_correlations()

# Detect entanglement
pattern = analyzer.detect_entanglement_pattern()

# Print comprehensive report
analyzer.print_detailed_report()
```

## 🎯 Use Cases

| Use Case | Circuit Type | Scale | Time |
|---|---|---|---|
| Entanglement testing | `entangled_chain` | 6000 qubits | Instant |
| State correlation analysis | `ghz_state` | 100 qubits | <1 sec |
| Optimization demo | `qaoa` | 30 qubits | <10 sec |
| Algorithm education | `deutsch` | 6 qubits | Instant |
| Cloud computing test | Any | 20 qubits | Depends on queue |
| Quantum walk simulation | `quantum_walk` | 30 qubits | <5 sec |

## ⚠️ Limitations

| Size | Method | Memory | Time | Practical? |
|---|---|---|---|---|
| 1-22 qubits | State vector | 2^n MB | Seconds | ✅ |
| 23-500 qubits | Analytical | Negligible | Instant | ✅ |
| 501-6000 qubits | Analytical* | Negligible | Instant | ✅ |
| 6000+ qubits | Tensor network | Variable | Varies | ⚠️ |

*For CNOT chain and similar structured circuits only

## 🔗 Cloud Provider Features

### IBM Quantum
- Up to 433 physical qubits
- Free tier available
- Noisy simulators
- Quantum processors

### AWS Braket
- Multiple backends (SV1, DM1)
- IonQ trapped ions (11 qubits)
- Rigetti superconducting
- Pay-per-use pricing

### Google Quantum
- Sycamore processor (54 qubits)
- Cirq framework
- Research collaboration required

## 📊 Example Output

```
QUANTUM MEASUREMENT ANALYSIS REPORT
==============================

BASIC STATISTICS
  Total shots: 100
  Unique states: 2
  Max probability: 0.5400
  Min probability: 0.4600

QUANTUM STATE PROPERTIES
  Shannon entropy: 0.9954 / 1.0000
  Purity: 0.5032 (1.0 = pure)
  Coherence: 0.0046 (1.0 = fully coherent)

SINGLE-QUBIT PROBABILITIES
  Q0: |0⟩=46.00% |1⟩=54.00%
  Q1: |0⟩=46.00% |1⟩=54.00%
  ... (all qubits fully correlated)

QUBIT CORRELATIONS
  Q0-Q1: 1.0000 (STRONG CORRELATION)
  Q0-Q2: 1.0000 (STRONG CORRELATION)
  ... (all pairs perfectly correlated)

MOST PROBABLE STATES
  1111...1111: 54.00% (54 counts)
  0000...0000: 46.00% (46 counts)

ENTANGLEMENT ANALYSIS
  Status: BELL PAIR - Maximum entanglement
```

## 🧑‍💻 Advanced Usage

### Custom Circuit Execution
```python
from qiskit import QuantumCircuit
from integrated_platform import QuantumExperimentPlatform

# Create custom circuit
qc = QuantumCircuit(5, 5)
qc.h([0, 1, 2])  # Superposition
qc.measure([0,1,2], [0,1,2])

# Run through platform
platform = QuantumExperimentPlatform()
results = platform.run_local(qc, 5, shots=1000)
analyzer = platform.analyze_results()
```

### Multi-Provider Testing
```python
platform = QuantumExperimentPlatform()
circuit = platform.create_circuit("ghz_state", 10)

# Test locally
local_results = platform.run_local(circuit, 10, shots=100)

# Test on cloud
if platform.cloud_manager.initialize_provider("ibm", api_key="key"):
    cloud_results = platform.run_cloud(circuit, "ibm", shots=100)
    
# Compare results
print("Local entropy:", QuantumMeasurementAnalyzer(local_results).calculate_shannon_entropy())
print("Cloud entropy:", QuantumMeasurementAnalyzer(cloud_results).calculate_shannon_entropy())
```

## 🐛 Troubleshooting

**"Insufficient memory" error:**
- Use analytical simulator for >22 qubits
- Platform auto-selects method based on qubit count

**Cloud connection failed:**
- Verify API key/credentials
- Install provider package: `pip install qiskit-ibm-runtime`
- Check network connection

**Unicode encoding error:**
- Set environment: `chcp 65001` (Windows PowerShell)

## 📚 References

- **Qiskit**: https://qiskit.org/
- **IBM Quantum**: https://quantum-computing.ibm.com/
- **AWS Braket**: https://aws.amazon.com/braket/
- **Google Cirq**: https://quantumai.google/cirq

## 📄 License

This system is provided as-is for quantum computing experimentation.

## ✨ Key Achievements

✅ **30 to 6000 qubit simulation** - Analytical methods for large-scale testing  
✅ **Cloud provider integration** - IBM, AWS, Google quantum systems  
✅ **9 circuit types** - From basic gates to advanced algorithms  
✅ **Comprehensive analysis** - Entropy, purity, correlations, entanglement  
✅ **Production ready** - Error handling, type hints, documentation  

---

**Built with Qiskit | Supports IBM Quantum, AWS Braket, Google Cirq**

---

## 💬 Support

Having trouble? Here's how to get help:

- 📖 **Documentation**: Check [QUICKSTART.md](QUICKSTART.md), [INSTALLATION.md](INSTALLATION.md), or [FAQ.md](FAQ.md)
- 🐛 **Bug Reports**: [Open an issue](../../issues) with details
- 💡 **Feature Requests**: [Suggest features](../../issues/new) with use cases
- 📚 **Learning**: Review [examples.py](examples.py) for code samples
- 🤝 **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## ⭐ Support the Project

If you find this useful, please:

- ⭐ **Star this repository** - Helps others discover it
- 🐦 **Share on social media** - Spread the word
- 📢 **Cite in your work** - Give credit
- 🤝 **Contribute** - Submit PRs or issues
- 📧 **Feedback** - Tell us what you think!

---

## 📞 Contact & Community

- **Author**: rpathai7-netizen
- **Repository**: [Quantum-Experiment](https://github.com/rpathai7-netizen/Quantum-Experiment)
- **Issues**: [GitHub Issues](../../issues)
- **License**: MIT - See [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

Built with:
- [Qiskit](https://qiskit.org/) - Quantum computing framework
- [IBM Quantum](https://quantum-computing.ibm.com/) - Cloud quantum hardware
- [AWS Braket](https://aws.amazon.com/braket/) - Quantum services
- Open-source community

---

**Ready to start?** ⚡ Jump to [QUICKSTART.md](QUICKSTART.md) now!
