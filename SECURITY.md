# Security Policy

## Reporting Security Vulnerabilities

**Do not** open public GitHub issues for security vulnerabilities.

If you discover a security vulnerability, please email the maintainers directly. We take security seriously and will respond promptly to security reports.

### Reporting format:
1. **Vulnerability Title**: Brief description
2. **Description**: Detailed explanation
3. **Affected Component**: Which file/function is affected
4. **Reproduction Steps**: How to reproduce (if applicable)
5. **Impact**: What does this affect (confidentiality, integrity, availability)
6. **Suggested Fix** (optional): Your proposed solution

## Security Best Practices

### When Using This Library

1. **API Keys & Credentials**
   - Never hardcode API keys in code
   - Use environment variables
   - Rotate keys regularly
   - Never commit credentials to git

   ```python
   # ✅ Good
   import os
   api_key = os.getenv('QISKIT_IBM_API_KEY')
   
   # ❌ Bad
   api_key = "ghp_xxxxxxxxxxxxxxxxxxxx"  # Never do this!
   ```

2. **Circuit Validation**
   - Validate circuit parameters before execution
   - Check qubit count against backend limits
   - Verify gate compatibility

3. **Result Handling**
   - Don't log sensitive measurements
   - Sanitize results before storage
   - Use secure channels for transmission

4. **Dependency Management**
   - Keep dependencies updated
   - Check for security advisories
   - Use trusted sources only

### Known Limitations

- **Qiskit Security**: Follow [Qiskit security guidelines](https://qiskit.org/)
- **Cloud Provider Limits**: Respect rate limiting
- **Network Security**: Use HTTPS only
- **Local Execution**: No special security measures needed for simulation

## Security Scanning

This project is scanned for:
- ✅ Dependency vulnerabilities
- ✅ Code vulnerabilities
- ✅ Secret detection
- ✅ License compliance

## Third-Party Dependencies

Core dependencies:
- **qiskit**: Quantum computing framework
- **numpy**: Numerical computing
- **qiskit-aer**: Quantum simulator
- **qiskit-ibm-runtime** (optional): IBM Quantum
- **amazon-braket-sdk** (optional): AWS Braket

All dependencies are maintained by reputable organizations and regularly updated.

## Compliance

This project follows:
- ✅ OWASP Top 10 guidelines
- ✅ PEP 8 for Python code security
- ✅ MIT License terms
- ✅ Code of Conduct standards

## Security Updates

- Security updates will be released as patches
- Critical vulnerabilities get priority
- Users are notified via GitHub security alerts
- Updates are documented in release notes

## Contact

For security issues, please contact through GitHub's security advisory feature or open a private security report.

---

**Thank you for helping keep Quantum Experiment Platform secure!** 🔒
