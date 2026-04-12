# Installation Guide

Complete installation instructions for Quantum Experiment Platform.

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Latest version (run `pip install --upgrade pip`)
- **Virtual Environment** (recommended): venv or conda

## 🚀 Quick Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/rpathai7-netizen/Quantum-Experiment.git
cd Quantum-Experiment
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Core Dependencies

```bash
pip install qiskit qiskit-aer numpy
```

**Expected installation time**: 2-5 minutes

## 📦 Full Installation (With Cloud Support)

For cloud provider support, install additional packages:

```bash
# All dependencies including cloud providers
pip install qiskit qiskit-aer numpy qiskit-ibm-runtime amazon-braket-sdk
```

## ☁️ Optional: Cloud Provider Setup

### IBM Quantum

1. **Create Account**: https://quantum-computing.ibm.com/

2. **Get API Key**:
   - Log in to your IBM Quantum account
   - Go to Dashboard → API tokens
   - Copy your API token

3. **Configure Environment**:

   **Windows (Command Prompt):**
   ```cmd
   set QISKIT_IBM_API_KEY=your_api_key_here
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:QISKIT_IBM_API_KEY="your_api_key_here"
   ```

   **macOS/Linux:**
   ```bash
   export QISKIT_IBM_API_KEY=your_api_key_here
   ```

4. **Test Connection**:
   ```python
   from qiskit_ibm_runtime import QiskitRuntimeService
   
   service = QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_TOKEN")
   print("IBM Quantum configured successfully!")
   ```

### AWS Braket

1. **Create AWS Account**: https://aws.amazon.com/

2. **Configure AWS Credentials**:
   ```bash
   aws configure
   ```
   
   Provide:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., `us-east-1`)

3. **Install AWS SDK**:
   ```bash
   pip install amazon-braket-sdk
   ```

4. **Test Connection**:
   ```python
   from braket.aws import AwsDevice
   
   device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
   print("AWS Braket configured successfully!")
   ```

### Google Quantum (Cirq)

1. **Install Cirq**:
   ```bash
   pip install cirq
   ```

2. **Note**: Google Quantum hardware requires research collaboration. Use Cirq simulator for learning.

## ✅ Verify Installation

Test your installation:

```bash
python -c "import qiskit; import numpy; print('Core installation successful!')"
```

For cloud access:
```bash
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print('IBM Quantum ready!')"
```

## 🔧 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'qiskit'`

**Solution**: Ensure virtual environment is activated
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Then reinstall:
```bash
pip install qiskit qiskit-aer
```

### Issue: `ImportError: libopenblas... cannot open shared object`

**Solution** (Linux):
```bash
sudo apt-get install libopenblas-dev liblapack-dev
```

### Issue: `Connection refused` when connecting to cloud provider

**Solutions**:
1. Check internet connection
2. Verify API key is correct
3. Check if cloud service is up (check status page)
4. Ensure API key has not expired

### Issue: `Illegal instruction (core dumped)`

**Solution** (Linux): Install a compatibility version
```bash
pip install numpy==1.21.0
```

## 📊 Installation Verification Checklist

After installation, verify:

- [ ] Python version: `python --version` (should be 3.8+)
- [ ] Core packages: `pip list | grep qiskit`
- [ ] NumPy: `python -c "import numpy; print(numpy.__version__)"`
- [ ] Qiskit: `python -c "import qiskit; print(qiskit.__version__)"`
- [ ] Cloud (optional): Run cloud provider test scripts

## 🐛 Still Having Issues?

1. **Check Environment**: `pip list` - shows all installed packages
2. **Upgrade pip**: `pip install --upgrade pip setuptools wheel`
3. **Clean Install**: 
   ```bash
   pip uninstall qiskit qiskit-aer -y
   pip install --upgrade qiskit qiskit-aer
   ```
4. **Create Fresh Virtual Environment**:
   ```bash
   # Remove old one
   rm -r venv  # or rmdir venv /s on Windows
   
   # Create new one
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install qiskit qiskit-aer numpy
   ```

## 📚 Next Steps

After successful installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for 5-minute introduction
2. Check [examples.py](examples.py) for code samples
3. Review [README.md](README.md) for full documentation
4. Run benchmark: `python run_all_benchmarks.py`

## 💡 Recommended: IDE Setup

### VS Code

1. Install Python extension
2. Select interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose the venv interpreter

### PyCharm

1. Open project settings
2. Go to Project → Python Interpreter
3. Click gear icon → Add → Existing Environment
4. Navigate to `venv/Scripts/python.exe`

## 📖 Additional Resources

- [Qiskit Installation Guide](https://qiskit.org/documentation/getting_started.html)
- [IBM Quantum Documentation](https://quantum-computing.ibm.com/docs/)
- [AWS Braket Getting Started](https://docs.aws.amazon.com/braket/)
- [Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

---

**Installation Complete?** Head over to [QUICKSTART.md](QUICKSTART.md) to start quantum computing! 🚀
