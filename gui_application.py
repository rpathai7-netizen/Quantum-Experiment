"""
Quantum Experiment Platform - GUI Application
User-friendly graphical interface for quantum computing simulations
"""

import os
import sys
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    print("ERROR: tkinter is required. On Linux, run: sudo apt-get install python3-tk")
    sys.exit(1)

import json
import threading
from datetime import datetime

from integrated_platform import QuantumExperimentPlatform
from measurement_analysis import QuantumMeasurementAnalyzer


class QuantumGUI:
    """Main GUI Application for Quantum Experiment Platform"""

    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Experiment Platform")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize platform
        self.platform = QuantumExperimentPlatform()
        self.results = None
        self.is_running = False

        # Configure styles
        self.setup_styles()

        # Create main UI
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

    def setup_styles(self):
        """Configure TTK styles"""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Title.TLabel", font=("Helvetica", 16, "bold"), background="#f0f0f0"
        )
        style.configure(
            "Header.TLabel", font=("Helvetica", 12, "bold"), background="#f0f0f0"
        )
        style.configure("Normal.TLabel", font=("Helvetica", 10), background="#f0f0f0")

    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(
            label="Real-World Applications", command=self.show_applications
        )

    def create_main_frame(self):
        """Create main application frame"""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill="x", padx=20, pady=15)

        ttk.Label(
            title_frame,
            text="🔬 Quantum Experiment Platform",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            title_frame,
            text="Learn and simulate quantum computing without expertise",
            style="Normal.TLabel",
            foreground="#666",
        ).pack(anchor="w")

        # Main notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Tabs
        self.tab_simple = ttk.Frame(notebook)
        self.tab_advanced = ttk.Frame(notebook)
        self.tab_usecases = ttk.Frame(notebook)

        notebook.add(self.tab_simple, text="🚀 Simple Start")
        notebook.add(self.tab_advanced, text="⚙️ Advanced Options")
        notebook.add(self.tab_usecases, text="💼 Real-World Uses")

        self.create_simple_tab()
        self.create_advanced_tab()
        self.create_usecases_tab()

    def create_simple_tab(self):
        """Create simple starter tab"""
        frame = ttk.Frame(self.tab_simple, padding=20)
        frame.pack(fill="both", expand=True)

        # Welcome section
        ttk.Label(
            frame, text="Welcome to Quantum Computing!", style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        welcome_text = (
            "This platform lets you:\n"
            "✓ Create and run quantum circuits\n"
            "✓ Learn quantum computing concepts\n"
            "✓ Analyze quantum measurements\n"
            "✓ Scale up to 6000+ qubits"
        )
        ttk.Label(frame, text=welcome_text, style="Normal.TLabel", justify="left").pack(
            anchor="w", pady=10
        )

        # Simple circuit selection
        ttk.Label(frame, text="Choose a Circuit Type:", style="Header.TLabel").pack(
            anchor="w", pady=(20, 10)
        )

        circuit_desc = {
            "ghz_state": "✨ GHZ State (Best for beginners - Maximum entanglement)",
            "entangled_chain": "🔗 Entangled Chain (Create connected qubits)",
            "deutsch": "📚 Deutsch Algorithm (Educational classic)",
            "random": "🎲 Random Circuit (Stress test the system)",
        }

        self.simple_circuit = tk.StringVar(value="ghz_state")

        for circuit_type, description in circuit_desc.items():
            ttk.Radiobutton(
                frame,
                text=description,
                variable=self.simple_circuit,
                value=circuit_type,
            ).pack(anchor="w", pady=5)

        # Qubit count
        ttk.Label(frame, text="Number of Qubits:", style="Header.TLabel").pack(
            anchor="w", pady=(20, 5)
        )

        qubit_frame = ttk.Frame(frame)
        qubit_frame.pack(anchor="w", fill="x", pady=5)

        ttk.Label(qubit_frame, text="Use slider (5-30 qubits):").pack(
            side="left", padx=(0, 10)
        )

        self.simple_qubit_slider = ttk.Scale(
            qubit_frame,
            from_=5,
            to=30,
            orient="horizontal",
            command=self.update_qubit_label,
        )
        self.simple_qubit_slider.set(10)
        self.simple_qubit_slider.pack(side="left", fill="x", expand=True)

        self.simple_qubit_label = ttk.Label(qubit_frame, text="10", width=3)
        self.simple_qubit_label.pack(side="left", padx=10)

        # Or enter manually
        manual_frame = ttk.Frame(frame)
        manual_frame.pack(anchor="w", fill="x", pady=5)

        ttk.Label(manual_frame, text="Or enter manually (5-6000):").pack(
            side="left", padx=(0, 10)
        )
        self.simple_qubit_entry = ttk.Entry(manual_frame, width=10)
        self.simple_qubit_entry.pack(side="left")
        self.simple_qubit_entry.insert(0, "10")

        # Shots
        ttk.Label(frame, text="Number of Shots (runs):", style="Header.TLabel").pack(
            anchor="w", pady=(20, 5)
        )

        shots_frame = ttk.Frame(frame)
        shots_frame.pack(anchor="w", fill="x", pady=5)

        self.simple_shots = ttk.Scale(
            shots_frame, from_=10, to=1000, orient="horizontal"
        )
        self.simple_shots.set(100)
        self.simple_shots.pack(side="left", fill="x", expand=True)

        self.simple_shots_label = ttk.Label(shots_frame, text="100", width=5)
        self.simple_shots_label.pack(side="left", padx=10)
        self.simple_shots.config(command=self.update_shots_label)

        # Run button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(30, 0))

        self.simple_run_btn = ttk.Button(
            button_frame, text="▶️ Run Simulation", command=self.run_simple_simulation
        )
        self.simple_run_btn.pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="📊 View Results", command=self.show_results
        ).pack(side="left", padx=5)

        # Results display
        ttk.Label(frame, text="Results:", style="Header.TLabel").pack(
            anchor="w", pady=(20, 5)
        )

        self.simple_results_text = tk.Text(frame, height=10, width=60, bg="white")
        self.simple_results_text.pack(fill="both", expand=True, pady=5)

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.simple_results_text.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.simple_results_text.config(yscrollcommand=scrollbar.set)

    def create_advanced_tab(self):
        """Create advanced options tab"""
        frame = ttk.Frame(self.tab_advanced, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Advanced Configuration", style="Header.TLabel").pack(
            anchor="w", pady=(0, 20)
        )

        # Circuit type selection
        ttk.Label(frame, text="Circuit Type:", style="Header.TLabel").pack(
            anchor="w", pady=(10, 5)
        )

        circuit_types = [
            "entangled_chain",
            "ghz_state",
            "random",
            "qaoa",
            "grover",
            "vqe",
            "quantum_walk",
            "deutsch",
            "phase_estimation",
        ]

        self.adv_circuit = tk.StringVar(value="entangled_chain")
        circuit_combo = ttk.Combobox(
            frame, textvariable=self.adv_circuit, values=circuit_types, state="readonly"
        )
        circuit_combo.pack(anchor="w", fill="x", pady=(0, 20))

        # Qubit configuration
        ttk.Label(
            frame, text="Advanced Qubit Configuration:", style="Header.TLabel"
        ).pack(anchor="w", pady=(10, 5))

        adv_qubit_frame = ttk.LabelFrame(frame, text="Qubit Count", padding=10)
        adv_qubit_frame.pack(fill="x", pady=10)

        ttk.Label(
            adv_qubit_frame, text="For large circuits (>30 qubits), analytical"
        ).pack(anchor="w")
        ttk.Label(adv_qubit_frame, text="methods are used automatically.").pack(
            anchor="w"
        )

        ttk.Label(adv_qubit_frame, text="Enter qubits (5-6000):").pack(
            anchor="w", pady=(10, 5)
        )
        self.adv_qubits = ttk.Entry(adv_qubit_frame)
        self.adv_qubits.insert(0, "20")
        self.adv_qubits.pack(fill="x")

        # Shots configuration
        ttk.Label(frame, text="Execution Configuration:", style="Header.TLabel").pack(
            anchor="w", pady=(10, 5)
        )

        shots_frame = ttk.LabelFrame(frame, text="Number of Shots", padding=10)
        shots_frame.pack(fill="x", pady=10)

        ttk.Label(shots_frame, text="How many times to run the circuit:").pack(
            anchor="w"
        )
        self.adv_shots = ttk.Scale(shots_frame, from_=10, to=10000, orient="horizontal")
        self.adv_shots.set(1000)
        self.adv_shots.pack(fill="x", pady=5)

        self.adv_shots_label = ttk.Label(shots_frame, text="1000")
        self.adv_shots_label.pack(anchor="w")
        self.adv_shots.config(
            command=lambda x: self.adv_shots_label.config(text=str(int(float(x))))
        )

        # Run buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(30, 0))

        ttk.Button(
            button_frame, text="▶️ Run Advanced", command=self.run_advanced_simulation
        ).pack(side="left", padx=5)

        # Results
        ttk.Label(frame, text="Advanced Results:", style="Header.TLabel").pack(
            anchor="w", pady=(20, 5)
        )

        self.adv_results_text = tk.Text(frame, height=8, width=60, bg="white")
        self.adv_results_text.pack(fill="both", expand=True, pady=5)

    def create_usecases_tab(self):
        """Create real-world use cases tab"""
        frame = ttk.Frame(self.tab_usecases, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Real-World Applications for Quantum Computing",
            style="Header.TLabel",
        ).pack(anchor="w", pady=(0, 20))

        usecases = [
            {
                "name": "🔐 Quantum Key Distribution",
                "desc": "Learn quantum-secure encryption\nSetup: Uses Deutsch algorithm",
            },
            {
                "name": "💰 Financial Portfolio Optimization",
                "desc": "Optimize investment portfolios\nSetup: Uses QAOA algorithm",
            },
            {
                "name": "💊 Drug Discovery Simulation",
                "desc": "Simulate molecular properties\nSetup: Uses VQE algorithm",
            },
            {
                "name": "🎲 Quantum Random Number Generation",
                "desc": "Generate certified random numbers\nSetup: Uses entangled_chain",
            },
            {
                "name": "🚗 Route Optimization",
                "desc": "Find optimal delivery routes\nSetup: Uses QAOA algorithm",
            },
            {
                "name": "🧠 Machine Learning Fundamentals",
                "desc": "Quantum ML algorithm basics\nSetup: Uses VQE and QAOA",
            },
        ]

        # Create usecase buttons in grid
        usecases_frame = ttk.Frame(frame)
        usecases_frame.pack(fill="both", expand=True, pady=10)

        for i, usecase in enumerate(usecases):
            col = i % 2
            row = i // 2

            btn = tk.Button(
                usecases_frame,
                text=usecase["name"],
                bg="#4CAF50",
                fg="white",
                font=("Helvetica", 11, "bold"),
                padx=20,
                pady=15,
                relief="raised",
                cursor="hand2",
                command=lambda u=usecase: self.show_usecase_details(u),
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew", ipady=10)

        usecases_frame.columnconfigure(0, weight=1)
        usecases_frame.columnconfigure(1, weight=1)
        usecases_frame.rowconfigure(0, weight=1)
        usecases_frame.rowconfigure(1, weight=1)
        usecases_frame.rowconfigure(2, weight=1)

        # Info display
        ttk.Label(frame, text="Learn More:", style="Header.TLabel").pack(
            anchor="w", pady=(10, 5)
        )

        self.usecase_text = tk.Text(frame, height=6, width=60, bg="white")
        self.usecase_text.pack(fill="both", expand=True, pady=5)

    def run_simple_simulation(self):
        """Run a simple simulation"""
        if self.is_running:
            messagebox.showwarning("Running", "A simulation is already running!")
            return

        try:
            circuit_type = self.simple_circuit.get()

            # Get qubits from manual entry if provided, otherwise use slider
            try:
                qubits = int(self.simple_qubit_entry.get())
            except:
                qubits = int(float(self.simple_qubit_slider.get()))

            shots = int(float(self.simple_shots.get()))

            if qubits < 5 or qubits > 6000:
                messagebox.showerror(
                    "Invalid Input", "Qubits must be between 5 and 6000"
                )
                return

            if shots < 10 or shots > 10000:
                messagebox.showerror(
                    "Invalid Input", "Shots must be between 10 and 10000"
                )
                return

            self.is_running = True
            self.simple_run_btn.config(state="disabled")

            # Run in thread
            thread = threading.Thread(
                target=self._run_simple_thread, args=(circuit_type, qubits, shots)
            )
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            self.is_running = False
            self.simple_run_btn.config(state="normal")

    def _run_simple_thread(self, circuit_type, qubits, shots):
        """Run simple simulation in background thread"""
        try:
            self.simple_results_text.config(state="normal")
            self.simple_results_text.delete("1.0", "end")
            self.simple_results_text.insert(
                "end", f"Running {circuit_type} with {qubits} qubits...\n\n"
            )
            self.simple_results_text.update()

            # Create and run circuit
            circuit = self.platform.create_circuit(circuit_type, qubits)
            self.results = self.platform.run_local(circuit, qubits, shots=shots)

            # Display basic results
            output = f"✅ Simulation Complete!\n\n"
            output += f"Circuit Type: {circuit_type}\n"
            output += f"Qubits: {qubits}\n"
            output += f"Shots: {shots}\n"
            output += f"\n{'─' * 40}\n"
            output += f"Measurement Outcomes (top 10):\n"
            output += f"{'─' * 40}\n"

            # Get counts
            counts = self.results.get("counts", {})
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)[
                :10
            ]

            for state, count in sorted_counts:
                percentage = (count / shots) * 100
                output += f"{state}: {count:4d} times ({percentage:5.1f}%)\n"

            self.simple_results_text.config(state="normal")
            self.simple_results_text.delete("1.0", "end")
            self.simple_results_text.insert("end", output)

        except Exception as e:
            self.simple_results_text.config(state="normal")
            self.simple_results_text.delete("1.0", "end")
            self.simple_results_text.insert(
                "end", f"❌ Error: {str(e)}\n\nTip: Try with fewer qubits (10-15)"
            )

        finally:
            self.is_running = False
            self.simple_run_btn.config(state="normal")

    def run_advanced_simulation(self):
        """Run advanced simulation"""
        if self.is_running:
            messagebox.showwarning("Running", "A simulation is already running!")
            return

        try:
            circuit_type = self.adv_circuit.get()
            qubits = int(self.adv_qubits.get())
            shots = int(float(self.adv_shots.get()))

            if qubits < 5 or qubits > 6000:
                messagebox.showerror(
                    "Invalid Input", "Qubits must be between 5 and 6000"
                )
                return

            self.is_running = True

            thread = threading.Thread(
                target=self._run_advanced_thread, args=(circuit_type, qubits, shots)
            )
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def _run_advanced_thread(self, circuit_type, qubits, shots):
        """Run advanced simulation in background"""
        try:
            self.adv_results_text.config(state="normal")
            self.adv_results_text.delete("1.0", "end")
            self.adv_results_text.insert("end", f"Running {circuit_type}...\n")
            self.adv_results_text.update()

            circuit = self.platform.create_circuit(circuit_type, qubits)
            results = self.platform.run_local(circuit, qubits, shots=shots)

            # Create analysis
            analyzer = QuantumMeasurementAnalyzer(results)
            entropy = analyzer.calculate_shannon_entropy()
            stats = analyzer.get_statistics()

            output = f"Advanced Results for {circuit_type}\n"
            output += f"{'─' * 50}\n"
            output += f"Configuration:\n"
            output += f"  Qubits: {qubits}\n"
            output += f"  Shots: {shots}\n\n"
            output += f"Analysis:\n"
            output += f"  Shannon Entropy: {entropy:.4f}\n"
            output += f"  Unique States: {stats.get('num_unique_states', 'N/A')}\n"
            output += f"  Purity: {analyzer.calculate_purity():.4f}\n"

            self.adv_results_text.config(state="normal")
            self.adv_results_text.delete("1.0", "end")
            self.adv_results_text.insert("end", output)

        except Exception as e:
            self.adv_results_text.config(state="normal")
            self.adv_results_text.delete("1.0", "end")
            self.adv_results_text.insert("end", f"❌ Error: {str(e)}")

        finally:
            self.is_running = False

    def show_usecase_details(self, usecase):
        """Show details for a use case"""
        details = f"""
{usecase['name']}

{usecase['desc']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESCRIPTION:
This real-world application demonstrates quantum computing's
practical benefits. The quantum algorithm can solve problems
faster than classical computers.

HOW TO GET STARTED:
1. Use the Simple Start tab to run the recommended circuit
2. Observe the measurement patterns
3. Try different qubit counts to see scaling
4. Use Advanced Options for detailed analysis

QUANTUM ADVANTAGE:
- Exponential speedup for certain problems
- Better optimization than brute force
- Quantum properties enable new solutions
"""
        self.usecase_text.config(state="normal")
        self.usecase_text.delete("1.0", "end")
        self.usecase_text.insert("end", details)

    def show_results(self):
        """Show detailed results"""
        if not self.results:
            messagebox.showinfo("No Results", "Run a simulation first!")
            return

        try:
            analyzer = QuantumMeasurementAnalyzer(self.results)
            detail_window = tk.Toplevel(self.root)
            detail_window.title("Detailed Results Analysis")
            detail_window.geometry("600x500")

            text = tk.Text(detail_window, bg="white", font=("Courier", 9))
            text.pack(fill="both", expand=True, padx=10, pady=10)

            output = analyzer.print_detailed_report()
            text.insert("end", str(output))
            text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def update_qubit_label(self, value):
        """Update qubit label"""
        self.simple_qubit_label.config(text=str(int(float(value))))

    def update_shots_label(self, value):
        """Update shots label"""
        self.simple_shots_label.config(text=str(int(float(value))))

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Quantum Experiment Platform\n\n"
            "A complete quantum computing simulation system\n"
            "with cloud integration and analysis tools.\n\n"
            "Version 2.0 (GUI Edition)\n"
            "Made accessible for everyone!",
        )

    def show_documentation(self):
        """Show documentation"""
        messagebox.showinfo(
            "Documentation",
            "Quick Tips:\n\n"
            "1. Start with Simple Start tab\n"
            "2. GHZ State is best for beginners\n"
            "3. Try 10-30 qubits first\n"
            "4. Use Advanced tab for detailed analysis\n"
            "5. Check Real-World Uses for applications",
        )

    def show_applications(self):
        """Show real-world applications"""
        msg = """
Real-World Quantum Computing Applications:

🔐 CRYPTOGRAPHY
  - Quantum Key Distribution (QKD)
  - Secure communication protocols
  - Post-quantum cryptography

💰 FINANCE
  - Portfolio optimization
  - Risk analysis
  - Derivatives pricing
  - Fraud detection

💊 DRUG DISCOVERY
  - Molecular simulation
  - Protein folding
  - Chemical reactions
  - Compound screening

🚗 OPTIMIZATION
  - Route planning
  - Supply chain management
  - Task scheduling
  - Traffic management

🧠 MACHINE LEARNING
  - Quantum neural networks
  - Pattern recognition
  - Feature extraction
  - Classification

⚛️ PHYSICS & CHEMISTRY
  - Quantum material simulation
  - Battery design
  - Catalyst discovery
  - Weather prediction

🎲 RANDOM NUMBERS
  - Certified randomness
  - Gaming and lotteries
  - Statistical sampling

This platform lets you explore all these domains!
"""
        messagebox.showinfo("Real-World Applications", msg)

    def create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken")
        status_bar.pack(fill="x", side="bottom")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = QuantumGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
