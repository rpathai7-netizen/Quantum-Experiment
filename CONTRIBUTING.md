# Contributing to Quantum Experiment Platform

Thank you for your interest in contributing! We welcome improvements, bug reports, and feature suggestions.

## 🐛 Found a Bug?

1. **Check existing issues** - Search [Issues](../../issues) first
2. **Create a new issue** with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS)

## 🤔 Have a Feature Idea?

1. **Discuss first** - Open an issue with `[FEATURE REQUEST]` tag
2. **Describe the use case** - Why is this feature needed?
3. **Suggest implementation** - Any ideas on how to implement it?

## 📝 Submitting Code Changes

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/rpathai7-netizen/Quantum-Experiment.git
cd Quantum-Experiment

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install qiskit qiskit-aer numpy qiskit-ibm-runtime amazon-braket-sdk
```

### Code Style Guidelines

- **Python**: Follow PEP 8
- **Documentation**: Use docstrings for all functions
- **Comments**: Explain "why", not "what"
- **Naming**: Use clear, descriptive names

Example function:
```python
def calculate_entanglement_entropy(quantum_state: np.ndarray) -> float:
    """
    Calculate von Neumann entropy of a quantum state.
    
    Args:
        quantum_state: Density matrix or state vector
        
    Returns:
        Entropy value (0.0 to log(N))
        
    Example:
        >>> entropy = calculate_entanglement_entropy(state)
        >>> print(f"Entropy: {entropy:.4f}")
    """
```

### Testing

- Write tests for new features
- Run existing tests before submitting
- Ensure no regressions

```bash
python -m pytest tests/ -v
```

### Commit Guidelines

```
[SHORT TYPE] Clear description of changes

[FEATURE] Add entanglement visualization
[BUG] Fix cloud provider authentication error
[DOCS] Improve installation documentation
```

Types:
- `[FEATURE]` - New feature
- `[BUG]` - Bug fix
- `[DOCS]` - Documentation improvement
- `[REFACTOR]` - Code refactoring
- `[PERF]` - Performance improvement

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** with clear commits
4. **Test thoroughly** - Run all tests and benchmarks
5. **Update documentation** - Add docstrings and update README if needed
6. **Submit a PR** with:
   - Clear description of changes
   - Link to related issue(s)
   - Any breaking changes noted
7. **Respond to review comments** promptly

## 📚 Documentation Standards

All code should include:

1. **Docstrings**: Explain what the function/class does
2. **Type hints**: Use Python type annotations
3. **Examples**: Show typical usage
4. **Error handling**: Document exceptions

```python
def run_quantum_circuit(
    circuit: QuantumCircuit,
    backend: str = "local",
    shots: int = 1000
) -> Dict[str, int]:
    """
    Execute a quantum circuit and return measurements.
    
    Args:
        circuit: Qiskit QuantumCircuit object
        backend: "local", "ibm", "aws", or "google"
        shots: Number of measurement repetitions
        
    Returns:
        Dictionary of measurement results {state: count}
        
    Raises:
        ValueError: If circuit is invalid
        ConnectionError: If cloud provider unreachable
        
    Example:
        >>> circuit = create_entangled_circuit(5)
        >>> results = run_quantum_circuit(circuit, shots=100)
        >>> print(results)
        {'00000': 50, '11111': 50}
    """
```

## 🔍 Code Review Process

All submissions require review. Reviewers look for:

- **Correctness**: Does the code work correctly?
- **Quality**: Is it maintainable and well-documented?
- **Tests**: Are there appropriate tests?
- **Performance**: Does it impact performance negatively?
- **Consistency**: Does it follow project standards?

## 📦 Adding Dependencies

Before adding a new package:

1. **Justify necessity** - Is it really needed?
2. **Check alternatives** - Is there a built-in or existing solution?
3. **Consider maintenance** - Will this require ongoing updates?
4. **Update documentation** - Add to installation instructions

## 🏆 Recognition

Contributors will be:
- Listed in the README
- Credited in release notes
- Added to the contributors page

## Questions?

- Check [README.md](README.md) for documentation
- Review [QUICKSTART.md](QUICKSTART.md) for examples
- Open an issue for clarification

Thank you for contributing! 🎉

---

By contributing to this project, you agree that your contributions will be licensed under its MIT License.
