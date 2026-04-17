import os
import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import psutil
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def get_ram_usage_gb():
    """Returns current RAM usage of the process in GB."""
    return psutil.Process(os.getpid()).memory_info().rss / (1024**3)


def create_solar_graph(n_nodes):
    """
    Generates a Watts-Strogatz small-world graph representing
    a highly interconnected photovoltaic capture grid.
    """
    # k=4 neighbors, p=0.1 rewiring for small-world properties
    return nx.watts_strogatz_graph(n_nodes, k=4, p=0.1)


def build_walk_circuit(n_nodes, graph, steps=3):
    """
    Constructs a Discrete-Time Quantum Walk (DTQW) using strictly Clifford gates.
    Initial exciton starts at Node 0. Reaction Center is Node N-1.
    """
    qc = QuantumCircuit(n_nodes)

    # 1. Photon Impact (Initial State)
    qc.x(0)

    # 2. Iterative Walk Steps
    # A Clifford walk uses H (coin) and SWAP (shift) operators
    edges = list(graph.edges())

    for _ in range(steps):
        # Coin operator (Superposition)
        # We apply Hadamard to all current sites to induce coherence
        qc.h(range(n_nodes))

        # Shift operator (Graph connectivity)
        # We apply swaps based on the graph edges
        # To maintain Clifford properties and avoid non-Clifford control gates,
        # we treat the walk as a series of stochastic transmissions along edges.
        for u, v in edges:
            qc.swap(u, v)

        # S-gate can be added for phase complexity (still Clifford)
        qc.s(range(n_nodes))

    qc.measure_all()
    return qc


def run_simulation():
    RAM_LIMIT_GB = 84.0
    nodes_milestones = [50, 100, 500, 1000, 3000, 6000]
    steps = 2  # Small steps for large-scale stability

    results_efficiency = []
    results_ram = []

    print("=" * 60)
    print("      QUANTUM SOLAR WALK - MACROSCOPIC COHERENCE MONITOR")
    print("=" * 60)
    print(f"Safety Threshold: {RAM_LIMIT_GB} GB RAM")
    print(f"Algorithm: Clifford-Only Discrete Random Walk")
    print("-" * 60)

    # Initialize Stabilizer Simulator (Essential for huge qubit counts)
    simulator = AerSimulator(method="stabilizer")

    try:
        for n in nodes_milestones:
            current_ram = get_ram_usage_gb()
            if current_ram > RAM_LIMIT_GB:
                print(f"\n[!!!] SAFETY HALT: RAM Limit Reached ({current_ram:.2f} GB)")
                break

            print(
                f"Scale: {n:4d} Nodes | Current RAM: {current_ram:6.4f} GB ... ",
                end="",
                flush=True,
            )

            # 1. Graph and Circuit
            graph = create_solar_graph(n)
            qc = build_walk_circuit(n, graph, steps=steps)

            # 2. Transpile and Execute
            start_time = time.time()
            # Fast transpile for simple Clifford circuits
            t_qc = transpile(qc, simulator, optimization_level=0)

            # Shots=1024 to estimate probability at the Reaction Center (Sink)
            job = simulator.run(t_qc, shots=512)
            result = job.result()
            counts = result.get_counts()

            duration = time.time() - start_time

            # 3. Calculate Efficiency
            # Probability of being at the reaction center (the binary representation of N-1)
            sink_id = format(n - 1, f"0{n}b")
            # In Qiskit's counts, the string represents the whole state.
            # We look for states where only the N-1 bit is 1?
            # No, in this one-hot walk, the state is a string of bits.
            # We look for counts where the (N-1)-th bit is '1'.
            sink_hits = 0
            for state, count in counts.items():
                # Qiskit bit ordering: bit 0 is at the end (right)
                # Sink is node N-1, so it's the leftmost bit in the state string
                if state[0] == "1":
                    sink_hits += count

            efficiency = sink_hits / 512
            post_ram = get_ram_usage_gb()

            print(
                f"Efficiency: {efficiency:.4f} | RAM: {post_ram:6.4f} GB ({duration:5.2f}s)"
            )

            results_efficiency.append(efficiency)
            results_ram.append(post_ram)

    except Exception as e:
        print(f"\n[Error] Simulation failed at scale {n}: {e}")

    print("-" * 60)
    print("SIMULATION COMPLETE.")

    # Visualization
    if results_efficiency:
        plt.figure(figsize=(10, 6))
        plt.plot(
            nodes_milestones[: len(results_efficiency)],
            results_efficiency,
            "o-",
            color="#ffaa00",
            label="Transfer Efficiency",
        )
        plt.title("Quantum Exciton Transfer Efficiency vs. Grid Scale")
        plt.xlabel("Node Count (N)")
        plt.ylabel("Probability at Reaction Center (Sink)")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()

        plot_file = "solar_walk_efficiency.png"
        plt.savefig(plot_file)
        print(f"Efficiency curve saved to: {plot_file}")


if __name__ == "__main__":
    import sys

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    run_simulation()
