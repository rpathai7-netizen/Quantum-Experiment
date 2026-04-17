#!/usr/bin/env python3
"""
Code Quality Analyzer and Improver
Analyzes the codebase for issues and suggests/applies improvements
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


class CodeAnalyzer:
    """Analyze Python code for quality issues"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.python_files = list(self.project_root.rglob("*.py"))
        self.issues = []
        self.stats = {
            "files": len(self.python_files),
            "total_lines": 0,
            "docstrings": 0,
            "type_hints": 0,
            "issues": 0,
        }

    def analyze_all(self):
        """Analyze all Python files in the project"""
        print("\n" + "=" * 70)
        print("CODE QUALITY ANALYSIS REPORT")
        print("=" * 70)

        for py_file in self.python_files:
            if self._should_skip(py_file):
                continue

            print(f"\n📄 Analyzing: {py_file.relative_to(self.project_root)}")
            self._analyze_file(py_file)

        self._print_summary()

    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_patterns = [
            "__pycache__",
            ".venv",
            "venv",
            "build",
            "dist",
            ".git",
            "tests",
        ]
        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            self.stats["total_lines"] += len(lines)

            # Check for docstrings
            docstring_count = self._count_docstrings(content)
            self.stats["docstrings"] += docstring_count

            # Check for type hints
            type_hint_count = self._count_type_hints(content)
            self.stats["type_hints"] += type_hint_count

            # Parse AST for issues
            try:
                tree = ast.parse(content)
                self._check_functions(tree, file_path, lines)
            except SyntaxError as e:
                print(f"  ⚠️  Syntax Error: {e}")
                self.stats["issues"] += 1

            # Check line length
            long_lines = [
                (i + 1, len(line)) for i, line in enumerate(lines) if len(line) > 120
            ]
            if long_lines:
                print(f"  ⚠️  Long lines (>120 chars): {len(long_lines)}")
                self.stats["issues"] += len(long_lines)

            # Check for missing docstrings
            if docstring_count == 0 and len(lines) > 10:
                print(f"  ⚠️  No module docstring")
                self.stats["issues"] += 1

        except Exception as e:
            print(f"  ❌ Error analyzing: {e}")

    def _count_docstrings(self, content: str) -> int:
        """Count docstrings in content"""
        pattern = r'""".*?"""'
        return len(re.findall(pattern, content, re.DOTALL))

    def _count_type_hints(self, content: str) -> int:
        """Count type hints in content"""
        pattern = r":\s*[A-Za-z_][A-Za-z0-9_\[\], ]*\s*(?:=|,|\))"
        return len(re.findall(pattern, content))

    def _check_functions(self, tree: ast.AST, file_path: Path, lines: List[str]):
        """Check functions for documentation and type hints"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for docstring
                has_docstring = ast.get_docstring(node) is not None

                # Check for type hints
                has_return_type = node.returns is not None
                has_arg_types = any(arg.annotation for arg in node.args.args)

                if not has_docstring and len(lines) > 10:
                    print(f"  ℹ️  Function '{node.name}' lacks docstring")

    def _print_summary(self):
        """Print analysis summary"""
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Files analyzed:        {self.stats['files']}")
        print(f"Total lines:           {self.stats['total_lines']}")
        print(f"Issues found:          {self.stats['issues']}")
        print(f"Docstrings:            {self.stats['docstrings']}")
        print(f"Type hints found:      {self.stats['type_hints']}")

        if self.stats["files"] > 0:
            docs_per_file = self.stats["docstrings"] / self.stats["files"]
            print(f"Avg docstrings/file:   {docs_per_file:.1f}")

        print("\n✅ Analysis complete!")


class CodeQualityReporter:
    """Generate detailed quality reports"""

    @staticmethod
    def generate_report(project_root: str = "."):
        """Generate comprehensive quality report"""
        analyzer = CodeAnalyzer(project_root)
        analyzer.analyze_all()

        # Generate recommendations
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS FOR IMPROVEMENT")
        print("=" * 70)

        recommendations = [
            "✓ Add type hints to all functions for better IDE support",
            "✓ Add docstrings to all modules and classes",
            "✓ Reduce line length to <100 characters where possible",
            "✓ Add more unit tests for edge cases",
            "✓ Consider using dataclasses for data structures",
            "✓ Add error handling with try-except blocks",
            "✓ Use logging instead of print statements",
            "✓ Add input validation to public functions",
        ]

        for rec in recommendations:
            print(f"  {rec}")

        print("\n" + "=" * 70)
        print("To auto-fix issues, run:")
        print("  black .")
        print("  isort .")
        print("  autopep8 --in-place --aggressive --aggressive .")
        print("=" * 70)


if __name__ == "__main__":
    CodeQualityReporter.generate_report()
