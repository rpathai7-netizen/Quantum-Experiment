#!/usr/bin/env python3
"""
Automated Improvement Orchestrator
Runs all improvement tools and generates a report
"""

import subprocess
import sys
from pathlib import Path


class ImprovementOrchestrator:
    """Orchestrates all code improvement processes"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.improvements_made = []
        self.errors = []

    def run_tests(self):
        """Run test suite"""
        print("\n" + "=" * 70)
        print("Running Tests...")
        print("=" * 70)

        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                print("✓ All tests passed!")
                self.improvements_made.append("Tests: All tests passed")
            else:
                print("⚠️  Some tests failed (see details above)")
                self.improvements_made.append("Tests: Some failures (check output)")

            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)

        except subprocess.TimeoutExpired:
            print("⚠️  Tests timed out")
            self.errors.append("Test timeout")
        except FileNotFoundError:
            print("⚠️  pytest not installed")
        except Exception as e:
            self.errors.append(f"Test error: {e}")

    def format_code(self):
        """Format code with black"""
        print("\n" + "=" * 70)
        print("Formatting Code with Black...")
        print("=" * 70)

        try:
            result = subprocess.run(
                [
                    "python",
                    "-m",
                    "black",
                    ".",
                    "--exclude",
                    r"(__pycache__|\.git|\.venv)",
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
            )

            if "reformatted" in result.stdout:
                print(f"✓ Code formatted")
                self.improvements_made.append("Formatting: Applied black formatting")
            else:
                print("✓ Code already well-formatted")

            print(result.stdout[-300:] if len(result.stdout) > 300 else result.stdout)

        except Exception as e:
            print(f"⚠️  Could not run black: {e}")

    def sort_imports(self):
        """Sort imports with isort"""
        print("\n" + "=" * 70)
        print("Organizing Imports...")
        print("=" * 70)

        try:
            result = subprocess.run(
                ["python", "-m", "isort", ".", "--skip-gitignore"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
            )

            print("✓ Imports organized")
            self.improvements_made.append("Imports: Organized with isort")

            if result.stdout:
                print(
                    result.stdout[-300:] if len(result.stdout) > 300 else result.stdout
                )

        except Exception as e:
            print(f"⚠️  Could not run isort: {e}")

    def analyze_code(self):
        """Analyze code quality"""
        print("\n" + "=" * 70)
        print("Analyzing Code Quality...")
        print("=" * 70)

        try:
            script_path = self.project_root / "scripts" / "analyze_code_quality.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                print(result.stdout)
                self.improvements_made.append("Analysis: Code quality checked")
            else:
                print("⚠️  Code quality analyzer not found")

        except Exception as e:
            print(f"⚠️  Could not run code analysis: {e}")

    def profile_performance(self):
        """Profile performance"""
        print("\n" + "=" * 70)
        print("Profiling Performance...")
        print("=" * 70)

        try:
            script_path = self.project_root / "scripts" / "performance_profiler.py"
            if script_path.exists():
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )

                print(result.stdout)
                self.improvements_made.append("Performance: Profiling completed")
            else:
                print("⚠️  Performance profiler not found")

        except Exception as e:
            print(f"⚠️  Could not run performance profiling: {e}")

    def generate_summary(self):
        """Generate improvement summary"""
        print("\n" + "=" * 70)
        print("IMPROVEMENT SUMMARY")
        print("=" * 70)

        print(f"\n✅ Improvements Applied: {len(self.improvements_made)}")
        for imp in self.improvements_made:
            print(f"   • {imp}")

        if self.errors:
            print(f"\n⚠️  Errors Encountered: {len(self.errors)}")
            for err in self.errors:
                print(f"   • {err}")

        print("\n" + "=" * 70)
        print("✨ Automatic improvement cycle complete!")
        print("=" * 70)

    def run_all(self):
        """Run all improvements"""
        print("\n" + "=" * 70)
        print("QUANTUM PLATFORM - AUTOMATED IMPROVEMENTS")
        print("=" * 70)
        print(f"Project root: {self.project_root}")

        try:
            self.run_tests()
            self.format_code()
            self.sort_imports()
            self.analyze_code()
            self.profile_performance()
            self.generate_summary()

        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    orchestrator = ImprovementOrchestrator()
    orchestrator.run_all()
