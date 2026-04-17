#!/usr/bin/env python3
import json
import re
from pathlib import Path

def parse_installation_md(file_path):
    """
    Parses INSTALLATION.md to extract sections, steps, and code blocks.
    Returns a list of nodes and edges for the graph.
    """
    content = Path(file_path).read_text(encoding='utf-8')
    
    nodes = []
    edges = []
    
    # Define sections to extract
    sections = [
        {"id": "pre", "label": "Prerequisites", "type": "start", "pattern": r"## 📋 Prerequisites(.*?)(?=##|$)", "color": "#00d2ff"},
        {"id": "quick", "label": "Quick Installation", "type": "step", "pattern": r"## 🚀 Quick Installation(.*?)(?=##|$)", "color": "#3a7bd5"},
        {"id": "full", "label": "Full Installation", "type": "step", "pattern": r"## 📦 Full Installation(.*?)(?=##|$)", "color": "#6a11cb"},
        {"id": "cloud", "label": "Cloud Provider Setup", "type": "config", "pattern": r"## ☁️ Optional: Cloud Provider Setup(.*?)(?=##|$)", "color": "#2575fc"},
        {"id": "verify", "label": "Verify Installation", "type": "verify", "pattern": r"## ✅ Verify Installation(.*?)(?=##|$)", "color": "#11998e"},
        {"id": "trouble", "label": "Troubleshooting", "type": "help", "pattern": r"## 🔧 Troubleshooting(.*?)(?=##|$)", "color": "#f85032"},
        {"id": "next", "label": "Next Steps", "type": "end", "pattern": r"## 📚 Next Steps(.*?)(?=##|$)", "color": "#b21f1f"}
    ]
    
    node_id = 0
    section_nodes = {}
    
    for sec in sections:
        match = re.search(sec["pattern"], content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Extract code blocks
            codes = re.findall(r"```(?:bash|cmd|powershell|python|)\n(.*?)\n```", text, re.DOTALL)
            
            node = {
                "id": node_id,
                "label": sec["label"],
                "type": sec["type"],
                "content": text,
                "codes": codes,
                "color": sec["color"]
            }
            nodes.append(node)
            section_nodes[sec["id"]] = node_id
            node_id += 1

    # Define edges based on typical installation flow
    flow = [("pre", "quick"), ("quick", "full"), ("quick", "verify"), ("full", "cloud"), ("cloud", "verify"), ("verify", "next"), ("trouble", "verify")]
    
    for start_id, end_id in flow:
        if start_id in section_nodes and end_id in section_nodes:
            edges.append({
                "from": section_nodes[start_id],
                "to": section_nodes[end_id],
                "label": "Next Step"
            })
            
    return nodes, edges

def generate_html(nodes, edges, output_path):
    """
    Generates a premium HTML visualization.
    """
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antigravity - Installation Graph</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Outfit', sans-serif; 
            background: var(--bg-color); 
            color: var(--text-main);
            overflow: hidden;
            height: 100vh;
            width: 100vw;
        }

        #app {
            display: flex;
            height: 100vh;
            width: 100vw;
            position: relative;
        }

        #network {
            flex: 1;
            background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        }

        .sidebar {
            width: 450px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-left: 1px solid var(--glass-border);
            padding: 40px;
            overflow-y: auto;
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            gap: 20px;
            box-shadow: -10px 0 30px rgba(0,0,0,0.5);
        }

        .header {
            margin-bottom: 20px;
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 600;
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }

        .header p {
            color: var(--text-dim);
            font-size: 1.1rem;
            margin-top: 8px;
        }

        .detail-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            transition: transform 0.3s ease, background 0.3s ease;
            display: none;
        }

        .detail-card.active {
            display: block;
            animation: slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        @keyframes slideIn {
            from { transform: translateX(30px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .detail-card h2 {
            font-size: 1.8rem;
            margin-bottom: 15px;
            color: var(--accent-primary);
        }

        .detail-content {
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-main);
            white-space: pre-wrap;
        }

        .code-block {
            background: #000;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 0.9rem;
            color: #10b981;
            position: relative;
            border: 1px solid #333;
            overflow-x: auto;
        }

        .code-block::before {
            content: 'Terminal';
            position: absolute;
            top: 5px;
            right: 10px;
            font-size: 0.7rem;
            color: #555;
            text-transform: uppercase;
        }

        #empty-state {
            text-align: center;
            margin-top: 50px;
            color: var(--text-dim);
        }

        .footer {
            margin-top: auto;
            padding-top: 20px;
            font-size: 0.8rem;
            color: var(--text-dim);
            opacity: 0.7;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

        .btn {
            background: var(--accent-primary);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
        }
    </style>
</head>
<body>
    <div id="app">
        <div id="network"></div>
        
        <div class="sidebar">
            <div class="header">
                <h1>Antigravity</h1>
                <p>Interactive Installation Graph</p>
            </div>

            <div id="empty-state">
                <p>Select a node on the graph to view details</p>
            </div>

            <div id="detail-pane">
                <!-- Content injected here -->
            </div>

            <div class="footer">
                <p>&copy; 2026 Antigravity System - Quantum Experiment Platform</p>
            </div>
        </div>
    </div>

    <script>
        const nodesData = __NODES_JSON__;
        const edgesData = __EDGES_JSON__;

        const visNodes = new vis.DataSet(nodesData.map(n => ({
            id: n.id,
            label: n.label,
            color: {
                background: n.color,
                border: n.color,
                highlight: { background: '#fff', border: n.color }
            },
            font: { color: '#fff', size: 16, face: 'Outfit' },
            shape: 'dot',
            size: 25,
            borderWidth: 2,
            shadow: { enabled: true, color: 'rgba(0,0,0,0.5)', size: 10 }
        })));

        const visEdges = new vis.DataSet(edgesData.map(e => ({
            from: e.from,
            to: e.to,
            label: e.label,
            arrows: 'to',
            color: { color: '#475569', highlight: '#3b82f6' },
            font: { color: '#94a3b8', size: 12, face: 'Outfit', align: 'top' },
            width: 2,
            smooth: { type: 'curvedCW', roundness: 0.2 }
        })));

        const container = document.getElementById('network');
        const data = { nodes: visNodes, edges: visEdges };
        const options = {
            physics: {
                enabled: true,
                stabilization: { iterations: 150 },
                barnesHut: {
                    gravitationalConstant: -20000,
                    centralGravity: 0.3,
                    springLength: 250,
                    springConstant: 0.05
                }
            },
            interaction: {
                hover: true,
                navigationButtons: true,
                keyboard: true,
                tooltipDelay: 200
            }
        };

        const network = new vis.Network(container, data, options);

        network.on("selectNode", function (params) {
            const nodeId = params.nodes[0];
            const node = nodesData.find(n => n.id === nodeId);
            displayDetail(node);
        });

        function displayDetail(node) {
            const emptyState = document.getElementById('empty-state');
            const detailPane = document.getElementById('detail-pane');
            
            emptyState.style.display = 'none';
            
            let codesHtml = '';
            if (node.codes && node.codes.length > 0) {
                codesHtml = node.codes.map(code => `<div class="code-block">${code}</div>`).join('');
            }

            detailPane.innerHTML = `
                <div class="detail-card active">
                    <h2>${node.label}</h2>
                    <div class="detail-content">${node.content.replace(/```.*?```/gs, '').trim()}</div>
                    ${codesHtml}
                    <button class="btn" onclick="network.unselectAll()">Dismiss</button>
                </div>
            `;
        }
    </script>
</body>
</html>
"""
    # Replace placeholders with actual JSON
    html_content = html_template.replace("__NODES_JSON__", json.dumps(nodes))
    html_content = html_content.replace("__EDGES_JSON__", json.dumps(edges))
    
    Path(output_path).write_text(html_content, encoding='utf-8')
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    project_root = Path("c:/Users/R/Desktop/Quantum Experiment")
    install_md = project_root / "INSTALLATION.md"
    output_html = project_root / "antigravity_install_graph.html"
    
    nodes, edges = parse_installation_md(install_md)
    generate_html(nodes, edges, output_html)
