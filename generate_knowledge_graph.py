#!/usr/bin/env python3
"""
Graphify Knowledge Graph Generator for Quantum Experiment Platform
Generates a comprehensive knowledge graph from the quantum codebase
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def gen_knowledge_graph():
    """Generate knowledge graph from codebase analysis"""
    
    project_root = Path("c:/Users/R/Desktop/Quantum Experiment")
    output_dir = project_root / "graphify-out"
    
    print("=" * 70)
    print("🔗 QUANTUM EXPERIMENT - KNOWLEDGE GRAPH GENERATION")
    print("=" * 70)
    print(f"\n📁 Project Root: {project_root}")
    print(f"📊 Output Dir: {output_dir}")
    print("\n🚀 Building knowledge graph...")
    print("-" * 70)
    
    # Create custom Quantum knowledge base
    create_quantum_knowledge_base(project_root, output_dir)

def create_quantum_knowledge_base(project_root, output_dir):
    """
    Create a custom knowledge base for the quantum experiment platform
    Since graphify's build command isn't easily accessible from CLI,
    we create a structured analysis manually.
    """
    
    import ast
    import os
    from collections import defaultdict
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("📊 Analyzing quantum experiment codebase...")
    
    modules = defaultdict(dict)
    classes = {}
    functions = {}
    relationships = defaultdict(list)
    
    # Parse all Python files
    python_files = list(project_root.glob("*.py"))
    test_files = list((project_root / "tests").glob("test_*.py")) if (project_root / "tests").exists() else []
    all_files = [f for f in python_files + test_files if f.exists()][:15]  # Limit to 15 files for processing
    
    print(f"   Found {len(all_files)} Python files to analyze")
    
    for py_file in all_files:
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read())
            
            filename = py_file.stem
            modules[filename] = {
                'file': str(py_file.relative_to(project_root)),
                'classes': [],
                'functions': [],
                'imports': []
            }
            
            # Extract classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    classes[f"{filename}.{class_name}"] = {
                        'module': filename,
                        'name': class_name,
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        'docstring': ast.get_docstring(node) or ''
                    }
                    modules[filename]['classes'].append(class_name)
                    
                    # Track relationships
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            relationships[class_name].append(('inherits', base.id))
                
                elif isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    functions[f"{filename}.{func_name}"] = {
                        'module': filename,
                        'name': func_name,
                        'docstring': ast.get_docstring(node) or '',
                        'args': [arg.arg for arg in node.args.args]
                    }
                    modules[filename]['functions'].append(func_name)
                
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            modules[filename]['imports'].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            modules[filename]['imports'].append(node.module)
        
        except Exception as e:
            print(f"   ⚠️  Error parsing {py_file.name}: {e}")
    
    # Create graph JSON structure
    graph_data = {
        'nodes': [],
        'edges': [],
        'metadata': {
            'title': 'Quantum Experiment Platform - Knowledge Graph',
            'description': 'Structural analysis of quantum computing modules',
            'generated': datetime.now().isoformat(),
            'corpus_size': len(all_files)
        }
    }
    
    # Add nodes
    node_ids = {}
    node_id = 0
    
    for module_name, module_info in modules.items():
        node_ids[('module', module_name)] = node_id
        graph_data['nodes'].append({
            'id': node_id,
            'label': module_name.replace('_', ' ').title(),
            'type': 'module',
            'file': module_info['file'],
            'category': 'code_module'
        })
        node_id += 1
        
        for cls_name in module_info['classes']:
            node_key = (f'{module_name}.{cls_name}', 'class')
            node_ids[node_key] = node_id
            graph_data['nodes'].append({
                'id': node_id,
                'label': cls_name,
                'type': 'class',
                'module': module_name,
                'category': 'quantum_class' if any(x in cls_name for x in ['Quantum', 'Circuit', 'Simulator']) else 'class'
            })
            node_id += 1
            
            # Add edge between module and class
            graph_data['edges'].append({
                'source': node_ids[('module', module_name)],
                'target': node_id - 1,
                'label': 'contains',
                'type': 'structural'
            })
        
        for func_name in module_info['functions']:
            node_key = (f'{module_name}.{func_name}', 'function')
            node_ids[node_key] = node_id
            graph_data['nodes'].append({
                'id': node_id,
                'label': func_name,
                'type': 'function',
                'module': module_name,
                'category': 'function'
            })
            node_id += 1
            
            # Add edge between module and function
            graph_data['edges'].append({
                'source': node_ids[('module', module_name)],
                'target': node_id - 1,
                'label': 'defines',
                'type': 'structural'
            })
    
    # Add relationship edges
    for source, rels in relationships.items():
        if (source, 'class') in node_ids:
            for rel_type, target in rels:
                if (target, 'class') in node_ids:
                    graph_data['edges'].append({
                        'source': node_ids[(source, 'class')],
                        'target': node_ids[(target, 'class')],
                        'label': rel_type,
                        'type': 'relationship'
                    })
    
    # Save graph JSON
    graph_json_path = output_dir / "graph.json"
    with open(graph_json_path, 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"✅ Generated graph.json: {len(graph_data['nodes'])} nodes, {len(graph_data['edges'])} edges")
    print(f"   📍 Saved to: {graph_json_path}")
    
    # Create report
    create_knowledge_report(output_dir, modules, classes, functions)
    
    print("\n" + "=" * 70)
    print("✨ Knowledge base generated successfully!")
    print("=" * 70)
    print(f"\n📁 Output files:")
    print(f"   ✓ {graph_json_path}")
    print(f"   ✓ {output_dir}/GRAPH_REPORT.md")

def create_knowledge_report(output_dir, modules, classes, functions):
    """Create a markdown report of the knowledge graph"""
    
    report_path = output_dir / "GRAPH_REPORT.md"
    
    with open(report_path, 'w') as f:
        f.write("# Quantum Experiment Platform - Knowledge Graph Report\n\n")
        f.write("## God Nodes (Most Connected)\n\n")
        
        # Find most connected modules
        connection_counts = {}
        for class_name, class_info in classes.items():
            module = class_info['module']
            connection_counts[module] = connection_counts.get(module, 0) + 1
        
        for module, count in sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            f.write(f"- **{module}**: {count} classes\n")
        
        f.write("\n## Modules\n\n")
        for module_name, module_info in sorted(modules.items()):
            f.write(f"### {module_name.replace('_', ' ').title()}\n")
            f.write(f"- **File**: `{module_info['file']}`\n")
            if module_info['classes']:
                f.write(f"- **Classes**: {', '.join(module_info['classes'][:5])}\n")
            if module_info['functions']:
                f.write(f"- **Functions**: {', '.join(module_info['functions'][:5])}\n")
            if module_info['imports']:
                f.write(f"- **Dependencies**: {', '.join(set(module_info['imports'][:3]))}\n")
            f.write("\n")
        
        f.write("## Key Classes\n\n")
        quantum_classes = [name for name in classes.keys() if any(x in name for x in ['Quantum', 'Circuit', 'Simulator', 'Analyzer'])]
        for cls_name in quantum_classes[:10]:
            if cls_name in classes:
                cls_info = classes[cls_name]
                f.write(f"### {cls_info['name']}\n")
                if cls_info['docstring']:
                    f.write(f"{cls_info['docstring']}\n\n")
                if cls_info['methods']:
                    f.write(f"**Methods**: {', '.join(cls_info['methods'][:5])}\n\n")
    
    print(f"✅ Generated GRAPH_REPORT.md")

if __name__ == "__main__":
    gen_knowledge_graph()
