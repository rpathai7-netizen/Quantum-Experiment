#!/usr/bin/env python3
"""
Cross-Platform Executable Builder for Quantum Experiment Platform
Creates Windows EXE, macOS app, and Linux executable

Usage:
    python cross_platform_builder.py          # Build all platforms
    python cross_platform_builder.py --windows # Windows only
    python cross_platform_builder.py --macos   # macOS only
    python cross_platform_builder.py --linux   # Linux only
"""

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


class CrossPlatformBuilder:
    """Build executables for Windows, macOS, and Linux"""
    
    def __init__(self):
        self.current_platform = platform.system()
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.spec_dir = self.project_root / "specs"
        
        self.spec_dir.mkdir(exist_ok=True)
        self.log("Cross-Platform Builder initialized")
        self.log(f"Current Platform: {self.current_platform}")
        self.log(f"Project Root: {self.project_root}")
    
    def log(self, message, status="[*]"):
        """Print formatted log message"""
        print(f"{status} {message}")
    
    def check_dependencies(self):
        """Verify required packages"""
        self.log("Checking dependencies...", "[CHECKING]")
        
        required = ["pyinstaller", "qiskit", "numpy"]
        missing = []
        
        for package in required:
            try:
                __import__(package.replace("-", "_"))
                self.log(f"✓ {package} found", "[OK]")
            except ImportError:
                self.log(f"✗ {package} NOT found", "[ERROR]")
                missing.append(package)
        
        if missing:
            self.log(f"Installing missing packages: {', '.join(missing)}", "[INSTALL]")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing)
        
        return len(missing) == 0
    
    def create_windows_spec(self):
        """Create PyInstaller spec for Windows"""
        spec_content = """# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Windows

a = Analysis(
    ['gui_application.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['qiskit', 'qiskit_aer', 'numpy', 'tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
        spec_file = self.spec_dir / "QuantumExperiment_Windows.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        return spec_file
    
    def create_macos_spec(self):
        """Create PyInstaller spec for macOS"""
        spec_content = """# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for macOS

a = Analysis(
    ['gui_application.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['qiskit', 'qiskit_aer', 'numpy', 'tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

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
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='QuantumExperiment.app',
    icon=None,
    bundle_identifier='com.quantumexperiment.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
    },
)
"""
        spec_file = self.spec_dir / "QuantumExperiment_macOS.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        return spec_file
    
    def create_linux_spec(self):
        """Create PyInstaller spec for Linux"""
        spec_content = """# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Linux

a = Analysis(
    ['gui_application.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['qiskit', 'qiskit_aer', 'numpy', 'tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='quantumexperiment',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
"""
        spec_file = self.spec_dir / "QuantumExperiment_Linux.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        return spec_file
    
    def build_windows(self):
        """Build Windows executable"""
        if self.current_platform != "Windows":
            self.log("Skipping Windows build (not on Windows platform)", "[SKIP]")
            self.log("Note: Windows EXE can only be built on Windows", "[INFO]")
            return False
        
        self.log("Building Windows executable...", "[BUILD]")
        spec_file = self.create_windows_spec()
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "PyInstaller", str(spec_file),
                 "--distpath", str(self.dist_dir),
                 "--buildpath", str(self.build_dir),
                 "--workpath", str(self.build_dir)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                exe_path = self.dist_dir / "QuantumExperiment" / "QuantumExperiment.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    self.log(f"✓ Windows EXE created: {exe_path} ({size_mb:.1f} MB)", "[SUCCESS]")
                    return True
            
            self.log(f"Windows build failed: {result.stderr}", "[ERROR]")
            return False
            
        except Exception as e:
            self.log(f"Error building Windows: {e}", "[ERROR]")
            return False
    
    def build_macos(self):
        """Build macOS app"""
        if self.current_platform != "Darwin":
            self.log("Skipping macOS build (not on macOS platform)", "[SKIP]")
            self.log("Note: macOS app can only be built on macOS", "[INFO]")
            return False
        
        self.log("Building macOS application...", "[BUILD]")
        spec_file = self.create_macos_spec()
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "PyInstaller", str(spec_file),
                 "--distpath", str(self.dist_dir),
                 "--buildpath", str(self.build_dir)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                app_path = self.dist_dir / "QuantumExperiment.app"
                if app_path.exists():
                    self.log(f"✓ macOS app created: {app_path}", "[SUCCESS]")
                    
                    # Create DMG for distribution
                    self.log("Creating DMG for distribution...", "[DMG]")
                    dmg_path = self.dist_dir / "QuantumExperiment.dmg"
                    os.system(f'hdiutil create -volname "QuantumExperiment" -srcfolder "{app_path}" -ov -format UDZO "{dmg_path}"')
                    
                    if dmg_path.exists():
                        size_mb = dmg_path.stat().st_size / (1024 * 1024)
                        self.log(f"✓ macOS DMG created: {dmg_path} ({size_mb:.1f} MB)", "[SUCCESS]")
                    
                    return True
            
            self.log(f"macOS build failed: {result.stderr}", "[ERROR]")
            return False
            
        except Exception as e:
            self.log(f"Error building macOS: {e}", "[ERROR]")
            return False
    
    def build_linux(self):
        """Build Linux executable"""
        if self.current_platform != "Linux":
            self.log("Skipping Linux build (not on Linux platform)", "[SKIP]")
            self.log("Note: Linux executable can only be built on Linux", "[INFO]")
            return False
        
        self.log("Building Linux executable...", "[BUILD]")
        spec_file = self.create_linux_spec()
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "PyInstaller", str(spec_file),
                 "--distpath", str(self.dist_dir),
                 "--buildpath", str(self.build_dir)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                exe_path = self.dist_dir / "quantumexperiment"
                if exe_path.exists():
                    # Make executable
                    os.chmod(exe_path, 0o755)
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    self.log(f"✓ Linux executable created: {exe_path} ({size_mb:.1f} MB)", "[SUCCESS]")
                    return True
            
            self.log(f"Linux build failed: {result.stderr}", "[ERROR]")
            return False
            
        except Exception as e:
            self.log(f"Error building Linux: {e}", "[ERROR]")
            return False
    
    def build_all(self):
        """Build for all available platforms"""
        self.log("Starting cross-platform build...", "[START]")
        
        if not self.check_dependencies():
            self.log("Missing dependencies. Please install required packages.", "[ERROR]")
            return False
        
        results = {}
        
        # Build for current platform
        if self.current_platform == "Windows":
            results["Windows"] = self.build_windows()
        elif self.current_platform == "Darwin":
            results["macOS"] = self.build_macos()
        elif self.current_platform == "Linux":
            results["Linux"] = self.build_linux()
        
        self.print_summary(results)
        return all(results.values())
    
    def print_summary(self, results):
        """Print build summary"""
        self.log("=" * 60, "[SUMMARY]")
        self.log("Build Summary", "[SUMMARY]")
        self.log("=" * 60, "[SUMMARY]")
        
        for platform_name, success in results.items():
            status = "[SUCCESS]" if success else "[FAILED]"
            result = "✓ BUILT" if success else "✗ FAILED"
            self.log(f"{platform_name}: {result}", status)
        
        self.log("=" * 60, "[SUMMARY]")
        self.log("Note: Cross-platform builds must be done on target platform", "[INFO]")
        self.log("- Windows EXE: Build on Windows", "[INFO]")
        self.log("- macOS app: Build on macOS", "[INFO]")
        self.log("- Linux binary: Build on Linux", "[INFO]")

def main():
    """Main entry point"""
    builder = CrossPlatformBuilder()
    builder.build_all()

if __name__ == "__main__":
    main()
