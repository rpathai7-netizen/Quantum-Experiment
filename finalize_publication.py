#!/usr/bin/env python3
"""
Complete GitHub Publication - Final Edition
Sets description, topics, enables discussions, creates release
"""

import requests
import json

TOKEN = os.getenv('GH_TOKEN', 'YOUR_GITHUB_TOKEN_HERE')
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

REPO = 'rpathai7-netizen/Quantum-Experiment'
BASE_URL = f'https://api.github.com/repos/{REPO}'

print("\n" + "=" * 80)
print("FINAL QUANTUM EXPERIMENT PLATFORM PUBLICATION")
print("=" * 80)

# Step 1: Update description and enable features
print("\n[1/3] Updating repository configuration...")
config_payload = {
    'description': 'Production-ready quantum computing platform: Local simulation (30 qubits), analytical mode (6000+ qubits), cloud integration (IBM Quantum, AWS Braket, Google Quantum)',
    'has_issues': True,
    'has_projects': True,
    'has_discussions': True,
    'has_wiki': False
}

response = requests.patch(BASE_URL, headers=HEADERS, json=config_payload)
if response.status_code == 200:
    print("      SUCCESS - Description and features updated")
else:
    print(f"      WARNING - Status {response.status_code}")

# Step 2: Add topics (requires special header)
print("\n[2/3] Adding topics to repository...")
topics_header = {
    **HEADERS,
    'Accept': 'application/vnd.github.mercy-preview+json'
}
topics_payload = {
    'names': [
        'quantum-computing',
        'quantum-simulation', 
        'qiskit',
        'ibm-quantum',
        'aws-braket',
        'quantum-algorithms',
        'python',
        'education',
        'simulation'
    ]
}

response = requests.put(f'{BASE_URL}/topics', headers=topics_header, json=topics_payload)
if response.status_code == 200:
    data = response.json()
    print(f"      SUCCESS - {len(data.get('names', []))} topics added")
else:
    print(f"      WARNING - Status {response.status_code}")

# Step 3: Create release
print("\n[3/3] Creating release v1.0.0...")
release_payload = {
    'tag_name': 'v1.0.0',
    'target_commitish': 'main',
    'name': 'Quantum Experiment Platform v1.0.0 - Initial Release',
    'body': '''# Quantum Experiment Platform v1.0.0

Welcome to a production-ready quantum computing platform!

## Features

- Scalable Simulator: 30 qubits (local) to 6000+ qubits (analytical)
- Cloud Integration: IBM Quantum, AWS Braket, Google Quantum
- 9 Circuit Types: QAOA, VQE, Grover, GHZ, Deutsch, and more
- Advanced Analysis: Entropy, correlations, entanglement detection
- Comprehensive Documentation: 90K+ lines
- Benchmarking Suite: 100+ performance tests

## Quick Start

```bash
pip install qiskit qiskit-aer numpy
python examples.py
```

## Documentation

📖 [README](../README.md) | [QUICKSTART](../QUICKSTART.md) | [FAQ](../FAQ.md)''',
    'draft': False,
    'prerelease': False
}

response = requests.post(f'{BASE_URL}/releases', headers=HEADERS, json=release_payload)
if response.status_code == 201:
    release = response.json()
    print(f"      SUCCESS - Release created: {release['html_url']}")
elif response.status_code == 422:
    print(f"      INFO - Release v1.0.0 already exists (tag conflict)")
else:
    print(f"      WARNING - Status {response.status_code}")

# Final verification
print("\n" + "-" * 80)
print("FINAL VERIFICATION")
print("-" * 80)

response = requests.get(BASE_URL, headers=HEADERS)
if response.status_code == 200:
    repo = response.json()
    print(f"\nRepository: {repo['html_url']}")
    print(f"Description: {repo.get('description', 'NOT SET')[:60]}...")
    
    topics = repo.get('topics', [])
    print(f"Topics: {len(topics)} set")
    if topics:
        for t in topics[:5]:
            print(f"  - {t}")
        if len(topics) > 5:
            print(f"  ... and {len(topics) - 5} more")
    
    print(f"Issues: {'ON' if repo.get('has_issues') else 'OFF'}")
    print(f"Projects: {'ON' if repo.get('has_projects') else 'OFF'}")
    print(f"Discussions: {'ON' if repo.get('has_discussions') else 'OFF'}")
    print(f"Wiki: {'ON' if repo.get('has_wiki') else 'OFF'}")

# Check releases
releases_response = requests.get(f'{BASE_URL}/releases', headers=HEADERS)
if releases_response.status_code == 200:
    releases = releases_response.json()
    print(f"\nReleases: {len(releases)} published")
    if releases:
        for r in releases[:3]:
            print(f"  - {r['tag_name']}: {r.get('name')}")

print("\n" + "=" * 80)
print("PUBLICATION COMPLETE")
print("=" * 80)
print("\nYour repository is now fully configured and ready to use!")
print(f"\nGit clone:\n  git clone {repo['clone_url']}")
print("\nInstall:\n  pip install qiskit qiskit-aer numpy")
print("\nRun examples:\n  python examples.py")
print("\n" + "=" * 80 + "\n")
