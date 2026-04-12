from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# 1. Initialize the Hardware Map
# We are creating 30 qubits and 30 classical bits (to store the final measurements)
print("Building the 30-qubit circuit...")
qc = QuantumCircuit(30, 30)

# 2. Add the Quantum "Magic" (Superposition)
# The 'h' gate (Hadamard) puts Qubit 0 into a perfect 50/50 state of 1 and 0
qc.h(0)

# 3. Build the Entanglement Web
# We loop through and connect every qubit to the one next to it using 'cx' (CNOT) gates.
# If Qubit 0 changes, it instantly forces Qubits 1 through 29 to change as well.
for i in range(29):
    qc.cx(i, i+1)

# 4. Measure the Qubits
# This forces the quantum superposition to collapse into a classical binary answer (0s and 1s)
qc.measure(range(30), range(30))

# 5. Boot up the CPU Simulator
print("Allocating memory and launching local Aer Simulator...")
simulator = AerSimulator()

# 6. Execute the Simulation
# We will run this entanglement experiment 10 separate times (shots)
job = simulator.run(qc, shots=10)
result = job.result()

# 7. Output the Results
counts = result.get_counts(qc)
print("Simulation complete! Results:")
print(counts)
