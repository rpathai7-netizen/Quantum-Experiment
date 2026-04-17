# VS Code Copilot Chat Instructions for Quantum Experiment

You are assisting with the **Quantum Experiment Platform** - an advanced quantum computing simulation and analysis system. This project leverages cutting-edge quantum algorithms, benchmarking frameworks, and cloud integration.

## Project Context

The codebase consists of 15 Python modules implementing:
- **Quantum Circuit Management**: Building and manipulating quantum circuits
- **Scalable Simulation**: Classical simulation of quantum algorithms
- **Measurement Analysis**: Statistical analysis of quantum measurement outcomes
- **Cloud Integration**: Seamless cloud backend connectivity
- **Benchmarking**: Performance profiling and optimization

### Knowledge Graph Available

A machine-readable knowledge graph of the codebase is available in `graphify-out/graph.json`:
- **104 nodes** representing modules, classes, and functions
- **89 edges** representing relationships (contains, defines, inherits, connects)
- **Interactive visualization** at `graphify-out/graph-visualization.html`

## How to Use the Knowledge Graph

1. **Query the graph**: Run `python query_knowledge_graph.py` to find connections between components
2. **Visualize**: Open `graphify-out/graph-visualization.html` in a browser to explore interactively
3. **Reference in analysis**: When discussing code improvements, consider component relationships

## Key Components

### Most Connected Nodes (God Nodes)
- **QuantumCircuit**: Central class for circuit management
- **ScalableSimulator**: Quantum circuit simulator
- **MeasurementAnalyzer**: Quantum measurement analysis
- **CircuitTypes**: Type definitions for quantum circuits
- **CloudIntegration**: Cloud backend integration

### Code Organization

```
quantum_circuit.py       - Core QuantumCircuit implementation
scalable_simulator.py    - Quantum circuit simulator
circuit_types.py         - Type definitions and constants
measurement_analysis.py  - Quantum measurement analysis
cloud_integration.py     - Cloud backend integration
antimatter_engine.py     - Advanced quantum engine
superfluid_core.py       - Superfluid quantum computing
nuclear_pasta_3d.py      - 3D nuclear simulation
```

## Improvement Strategy

When suggesting improvements to this codebase:

1. **Consider the graph**: Reference how changes affect connected components
2. **Maintain relationships**: Keep dependencies between modules clear
3. **Test impact**: Changes to god nodes (highly connected) need broader testing
4. **Document connections**: Explain how your changes relate to other components

## Available Tools

- `python query_knowledge_graph.py` - Query node relationships
- `python generate_html_visualization.py` - Create interactive visualization
- `python generate_knowledge_graph.py` - Regenerate graph after code changes
- View: `graphify-out/GRAPH_REPORT.md` - Human-readable analysis

## Performance Optimization

When optimizing code, reference the knowledge graph to:
- Identify bottleneck components (high in, many components depending on them)
- Understand data flow through the system
- Plan refactoring to reduce coupling
- Design parallel improvements without conflicts

---

Generated: 2024 | Quantum Experiment Platform v1.0
