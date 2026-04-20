"""
Quantum Experiment Platform - Application Launcher
Simple entry point for users
"""

import os
import sys
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent))

print("""
╔════════════════════════════════════════════════════════════════════════╗
║        Quantum Experiment Platform - Launching Application             ║
╚════════════════════════════════════════════════════════════════════════╝
""")

# Check if dependencies are installed
print("Checking dependencies...")
missing_packages = []

required = {"qiskit": "Qiskit", "numpy": "NumPy", "tkinter": "tkinter"}

for module, name in required.items():
    try:
        if module == "tkinter":
            import tkinter
        else:
            __import__(module)
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ❌ {name} - NOT FOUND")
        missing_packages.append(module)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print("Installing missing packages...")
    os.system(f"pip install {' '.join(missing_packages)}")

print("\n🚀 Launching application...\n")

try:
    from gui_application import main

    main()
except Exception as e:
    print(f"❌ Error launching application: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure all packages are installed: pip install -r requirements.txt")
    print("2. Check that Python 3.8+ is installed")
    print("3. Try running from Command Prompt to see full error")
    input("\nPress Enter to exit...")
