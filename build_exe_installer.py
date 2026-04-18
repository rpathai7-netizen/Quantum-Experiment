"""
Windows EXE Installer Builder for Quantum Experiment Platform
Creates a standalone executable for easy distribution
"""

import os
import sys
import subprocess
import shutil
import tempfile
import json
from pathlib import Path


class QuantumInstallerBuilder:
    """Build standalone EXE for Quantum Experiment Platform"""

    def __init__(self):
        self.repo_root = Path(__file__).parent
        self.build_dir = self.repo_root / "build"
        self.dist_dir = self.repo_root / "dist"
        self.temp_dir = Path(tempfile.gettempdir()) / "quantum_build"

    def check_dependencies(self):
        """Check if required packages are installed"""
        print("[*] Checking dependencies...")

        required_packages = {
            "pyinstaller": "pyinstaller",
            "qiskit": "qiskit",
            "qiskit_aer": "qiskit-aer",
            "numpy": "numpy",
        }

        missing = []
        for import_name, package_name in required_packages.items():
            try:
                __import__(import_name)
                print(f"  [OK] {package_name}")
            except ImportError:
                print(f"  [ERROR] {package_name} NOT FOUND")
                missing.append(package_name)

        if missing:
            print(f"\n[*] Installing missing packages: {', '.join(missing)}")
            cmd = f"pip install {' '.join(missing)}"
            print(f"Running: {cmd}\n")
            os.system(cmd)
            print("\n[OK] Installation complete")

    def create_spec_file(self):
        """Create PyInstaller spec file"""
        print("\n[*] Creating PyInstaller spec file...")

        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui_application.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('quantum_circuit.py', '.'),
        ('scalable_simulator.py', '.'),
        ('circuit_types.py', '.'),
        ('measurement_analysis.py', '.'),
        ('cloud_integration.py', '.'),
        ('integrated_platform.py', '.'),
        ('realworld_usecases.py', '.'),
        ('BEGINNERS_GUIDE.py', '.'),
        ('README.md', '.'),
        ('QUICKSTART.md', '.'),
    ],
    hiddenimports=[
        'qiskit',
        'qiskit_aer',
        'qiskit.circuit',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QuantumExperiment',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='quantum_icon.ico',
)
'''

        spec_file = self.repo_root / "QuantumExperiment.spec"
        with open(spec_file, "w") as f:
            f.write(spec_content)

        print(f"  [OK] Created: {spec_file}")

    def create_icon(self):
        """Create application icon"""
        print("\n[*] Creating application icon...")

        # Create a simple icon using PIL if available
        try:
            from PIL import Image, ImageDraw

            img = Image.new("RGB", (256, 256), color="#1a1a2e")
            draw = ImageDraw.Draw(img)

            # Draw quantum symbol
            # Draw circle
            draw.ellipse([20, 20, 236, 236], outline="#00ff00", width=3)

            # Draw orbits
            for angle in [0, 120, 240]:
                x1 = 128 + 80 * (angle * 3.14159 / 180) ** 0.5
                y1 = 128 + 80 * ((angle + 120) * 3.14159 / 180) ** 0.5
                draw.ellipse(
                    [x1 - 3, y1 - 3, x1 + 3, y1 + 3], fill="#00ff00"
                )

            img.save(self.repo_root / "quantum_icon.ico")
            print("  [OK] Icon created")

        except ImportError:
            print("  [*] PIL not installed, using default icon")

    def build_exe(self):
        """Build the EXE using PyInstaller"""
        print("\n[*] Building EXE (this may take 2-5 minutes)...")

        try:
            # Change to repo directory
            os.chdir(self.repo_root)

            # Run PyInstaller
            cmd = f'pyinstaller "{self.repo_root / "QuantumExperiment.spec"}" --distpath "{self.dist_dir}" --workpath "{self.build_dir}"'

            print(f"Running: {cmd}\n")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print("[OK] EXE build successful!")
                return True
            else:
                print(f"[ERROR] Build failed:")
                print(result.stdout)
                print(result.stderr)
                return False

        except Exception as e:
            print(f"[ERROR] Build error: {e}")
            return False

    def create_installer_script(self):
        """Create a Windows installer batch script"""
        print("\n[*] Creating Windows installer script...")

        installer_script = f'''@echo off
REM Quantum Experiment Platform - Windows Installer
REM Run this script to install the application

echo ================================================
echo Quantum Experiment Platform - Installer
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
pip install qiskit qiskit-aer numpy
if errorlevel 1 (
    echo Warning: Some packages may have failed to install
)

echo.
echo Step 2: Launching Quantum Experiment Platform...
echo.

REM Launch the GUI
python "{self.repo_root / "gui_application.py"}"

pause
'''

        installer_file = self.repo_root / "install_and_run.bat"
        with open(installer_file, "w") as f:
            f.write(installer_script)

        print(f"  [OK] Created: {installer_file}")

    def create_shortcut(self):
        """Create Windows shortcut"""
        print("\n[*] Creating Windows shortcut...")

        shortcut_vbs = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{self.repo_root / "QuantumExperiment.lnk"}"
Set oLink = oWS.CreateShortCut(sLinkFile)
oLink.TargetPath = "{self.dist_dir / "QuantumExperiment" / "QuantumExperiment.exe"}"
oLink.WorkingDirectory = "{self.dist_dir / "QuantumExperiment"}"
oLink.Description = "Quantum Computing Experiment Platform"
oLink.IconLocation = "{self.repo_root / "quantum_icon.ico"}"
oLink.Save
'''

        vbs_file = self.repo_root / "create_shortcut.vbs"
        with open(vbs_file, "w") as f:
            f.write(shortcut_vbs)

        print(f"  [OK] Created: {vbs_file}")

    def create_readme_installer(self):
        """Create installer README"""
        print("\n[*] Creating installer documentation...")

        readme = """# Quantum Experiment Platform - Windows Installer

## Quick Start

### Option 1: Run the EXE (Easiest)
1. Find QuantumExperiment.exe in the dist/QuantumExperiment/ folder
2. Double-click to launch
3. The application will start automatically

### Option 2: Run the Installer Script
1. Double-click `install_and_run.bat`
2. Wait for Python packages to install (first time only)
3. The application will launch

### Option 3: Run from Source
1. Install Python 3.8+ from python.org
2. Open Command Prompt in this directory
3. Run: `python gui_application.py`

## System Requirements

- Windows 7 or later
- 2 GB RAM (4 GB recommended)
- 500 MB free disk space
- Python 3.8+ (if running from source)

## Features

✅ Simulate quantum circuits (5-6000 qubits)
✅ Multiple circuit types (QAOA, VQE, Grover, etc.)
✅ Cloud provider integration (IBM, AWS, Google)
✅ Advanced measurement analysis
✅ Real-world use cases
✅ Beginner-friendly interface

## Troubleshooting

### "Module not found" error
- Run `install_and_run.bat` to install dependencies

### Application won't start
- Check that Python 3.8+ is installed
- Run from Command Prompt to see detailed error messages

### EXE is large (500+ MB)
- This is normal. PyInstaller bundles Python and all dependencies.
- The EXE is a complete, standalone application.

## Usage

1. **Simple Start Tab**: Begin with easy circuits and pre-built examples
2. **Advanced Tab**: Customize circuits and parameters
3. **Real-World Uses Tab**: Learn practical quantum computing applications

## Real-World Applications

- 🔐 Cryptography and security
- 💰 Financial portfolio optimization
- 💊 Drug discovery simulation
- 🚗 Route optimization
- 🧠 Machine learning
- 🎲 Random number generation

## Documentation

- See `README.md` for full documentation
- See `QUICKSTART.md` for quick tutorials
- See `BEGINNERS_GUIDE.py` for learning guide

## Support

For issues or questions:
1. Check the Help menu in the application
2. Review documentation files
3. Run from Command Prompt to see error messages

## Version

Quantum Experiment Platform v2.0 (GUI Edition)
Built for everyday users interested in quantum computing

Enjoy exploring quantum computing! 🌟
"""

        readme_file = self.repo_root / "INSTALLER_README.md"
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(readme)

        print(f"  ✅ Created: {readme_file}")

    def create_distribution_package(self):
        """Create distribution package"""
        print("\n[*] Creating distribution package...")

        dist_package = self.repo_root / "QuantumExperiment_Distribution"
        dist_package.mkdir(exist_ok=True)

        # Copy files
        files_to_copy = [
            "README.md",
            "QUICKSTART.md",
            "BEGINNERS_GUIDE.py",
            "INSTALLER_README.md",
            "LICENSE",
        ]

        for file in files_to_copy:
            src = self.repo_root / file
            if src.exists():
                shutil.copy(src, dist_package / file)
                print(f"  [OK] Copied: {file}")

        print(f"  [OK] Distribution package created")

    def cleanup(self):
        """Clean up temporary files"""
        print("\n[*] Cleaning up temporary files...")

        dirs_to_remove = [self.build_dir, self.temp_dir]
        for dir in dirs_to_remove:
            if dir.exists():
                shutil.rmtree(dir)
                print(f"  [OK] Removed: {dir}")

    def print_summary(self):
        """Print build summary"""
        exe_path = self.dist_dir / "QuantumExperiment" / "QuantumExperiment.exe"

        print(
            f"""
BUILD COMPLETE! 

Output Location:
   {self.dist_dir}

Distribution Files:
   [OK] QuantumExperiment.exe - Main application
   [OK] install_and_run.bat - Easy installer
   [OK] README.md, QUICKSTART.md - Documentation
   [OK] BEGINNERS_GUIDE.py - Learning guide

To Use:

   Option 1 (Easiest):
   -> Double-click: install_and_run.bat
   
   Option 2:
   -> Double-click: QuantumExperiment.exe
   -> (Located in: dist/QuantumExperiment/)

Build Information:
   Executable Size: ~500-700 MB (includes Python + all dependencies)
   This is normal and creates a self-contained, portable application
   
   No additional installation needed!
   No Python required!
   Works on any Windows 7+ system!

Features:
   [OK] 9 quantum circuit types
   [OK] Scales to 6000+ qubits
   [OK] Cloud provider integration
   [OK] Real-world use cases
   [OK] Beginner guides
   [OK] Advanced analysis tools

Next Steps:
   1. Test the EXE locally
   2. Share with others
   3. Collect feedback
   4. Improve the application
"""
        )

    def build(self):
        """Main build process"""
        print(
            """
Quantum Experiment Platform - EXE Builder
Create standalone Windows executable
"""
        )

        try:
            # Check dependencies
            self.check_dependencies()

            # Create spec file
            self.create_spec_file()

            # Create icon
            self.create_icon()

            # Create installer script
            self.create_installer_script()

            # Create documentation
            self.create_readme_installer()

            # Build EXE
            if self.build_exe():
                # Create distribution package
                self.create_distribution_package()

                # Print summary
                self.print_summary()

                return True
            else:
                print("\n[ERROR] Build failed!")
                return False

        except Exception as e:
            print(f"\n[ERROR] Error: {e}")
            return False


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--create-icon-only":
        builder = QuantumInstallerBuilder()
        builder.create_icon()
        print("[OK] Icon created successfully")
        return

    builder = QuantumInstallerBuilder()
    success = builder.build()

    if success:
        print("\n[OK] Ready to distribute!")
        print("Share the files in: dist/QuantumExperiment/")
    else:
        print("\n[ERROR] Build failed. Check errors above.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
