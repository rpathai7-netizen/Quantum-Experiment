from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantum-experiment",
    version="1.0.0",
    author="rpathai7-netizen",
    description="Production-ready quantum computing platform with local simulation, cloud integration, and advanced analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rpathai7-netizen/Quantum-Experiment",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "qiskit>=0.41.0",
        "qiskit-aer>=0.12.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "cloud": [
            "qiskit-ibm-runtime>=0.13.0",
            "amazon-braket-sdk>=1.20.0",
            "cirq>=1.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/rpathai7-netizen/Quantum-Experiment/issues",
        "Documentation": "https://github.com/rpathai7-netizen/Quantum-Experiment/blob/main/README.md",
        "Source Code": "https://github.com/rpathai7-netizen/Quantum-Experiment",
    },
)
