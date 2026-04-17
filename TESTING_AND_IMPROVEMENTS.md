# Testing and Improvement Infrastructure

This directory contains automated testing and improvement systems for the Quantum Experiment Platform.

## Structure

```
tests/
├── __init__.py
├── conftest.py                      # Pytest configuration
├── test_measurement_analysis.py      # Measurement analysis tests
├── test_circuit_types.py             # Circuit type tests
└── test_scalable_simulator.py        # Simulator tests

scripts/
├── run_improvements.py               # Main improvement orchestrator
├── analyze_code_quality.py           # Code quality analyzer
└── performance_profiler.py           # Performance profiler

.github/workflows/
├── tests.yml                         # Automated testing workflow
├── benchmarks.yml                    # Performance benchmarking
├── auto-improve.yml                  # Automatic code improvements
└── docs.yml                          # Documentation generation
```

## Running Tests Locally

### Install Test Dependencies
```bash
pip install -e ".[test,dev]"
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_measurement_analysis.py -v
```

### Run Tests Matching Pattern
```bash
pytest tests/ -k "entropy" -v
```

## Running Improvements

### Run All Improvements
```bash
python scripts/run_improvements.py
```

### Analyze Code Quality
```bash
python scripts/analyze_code_quality.py
```

### Profile Performance
```bash
python scripts/performance_profiler.py
```

## Automated Workflows

### Tests Workflow (tests.yml)
- **Trigger**: Every push and pull request
- **Schedule**: Daily at 2 AM UTC
- **Tests**: Runs on Python 3.8, 3.9, 3.10, 3.11
- **Checks**: 
  - Unit tests with pytest
  - Code formatting with black
  - Linting with flake8
  - Type checking with mypy
  - Security checks with bandit

### Benchmarks Workflow (benchmarks.yml)
- **Trigger**: Daily at 3 AM UTC
- **Measures**: Performance of:
  - Circuit creation
  - Simulator initialization
  - Measurement analysis

### Auto-Improve Workflow (auto-improve.yml)
- **Trigger**: Daily at 4 AM UTC
- **Improvements**:
  - Code formatting with black
  - Import organization with isort
  - PEP8 fixes with autopep8
- **Actions**: Auto-commits improvements or creates pull requests

### Documentation Workflow (docs.yml)
- **Trigger**: Every push and daily at 5 AM UTC
- **Generates**: API documentation and module summaries

## Test Coverage

We aim for >80% code coverage. Current status:

- `measurement_analysis.py`: Core analysis functions
- `circuit_types.py`: Circuit factory patterns
- `scalable_simulator.py`: Simulation methods
- `cloud_integration.py`: Cloud provider integration
- `integrated_platform.py`: Platform coordination

## Adding New Tests

1. Create test file: `tests/test_module_name.py`
2. Use pytest fixtures for setup
3. Follow naming convention: `test_function_name()`
4. Document test intent in docstring

Example:
```python
import pytest
from measurement_analysis import QuantumMeasurementAnalyzer

def test_shannon_entropy_pure_state():
    """Shannon entropy of pure state should be 0"""
    pure_state = {'00': 100}
    analyzer = QuantumMeasurementAnalyzer(pure_state)
    entropy = analyzer.calculate_shannon_entropy()
    assert abs(entropy - 0.0) < 1e-10
```

## Continuous Improvement

The automation system runs continuously to:

1. **Maintain Code Quality**
   - Format code consistently
   - Organize imports
   - Fix style issues

2. **Ensure Functionality**
   - Run test suite
   - Check type hints
   - Verify logic

3. **Monitor Performance**
   - Profile circuit operations
   - Track benchmarks
   - Identify bottlenecks

4. **Document Changes**
   - Generate API docs
   - Track improvements
   - Update reports

## Best Practices

### Writing Tests
- ✅ One assertion per test (or related assertions)
- ✅ Descriptive test names
- ✅ Use fixtures for shared setup
- ✅ Test edge cases and error conditions
- ❌ Don't test implementation details

### Code Quality
- ✅ Follow PEP 8
- ✅ Add docstrings to functions
- ✅ Use type hints
- ✅ Keep functions small (<50 lines)
- ❌ No commented-out code

## Troubleshooting

### Tests Fail Locally but Pass in CI
- Check Python version: `python --version`
- Verify dependencies: `pip install -e ".[test]"`
- Clear cache: `pytest --cache-clear`

### Import Errors in Tests
- Ensure project root is in PYTHONPATH
- Check `conftest.py` is in tests directory
- Verify module names match file names

### Performance Tests Slow
- Some tests may timeout on slow machines
- Use `-m "not slow"` to skip slow tests
- Adjust timeout in conftest.py if needed

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Quantum Computing with Qiskit](https://qiskit.org/learn/)
