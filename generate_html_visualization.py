#!/usr/bin/env python3
"""
Generate interactive HTML visualization of Quantum Knowledge Graph using Vis.js
"""

import json
import subprocess
from pathlib import Path
from typing import Optional


def generate_visualization(
    graph_path: str = "graphify-out/graph.json",
    output_path: str = "graphify-out/graph-visualization.html",
) -> bool:
    """Generate interactive HTML visualization of the knowledge graph"""

    graph_file = Path(graph_path)
    if not graph_file.exists():
        print(f"❌ Graph file not found: {graph_path}")
        return False

    with open(graph_file, "r") as f:
        graph_data = json.load(f)

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    # Create Vis.js nodes and edges arrays
    vis_nodes = []
    for node in nodes:
        vis_nodes.append(
            {
                "id": node["id"],
                "label": node["label"],
                "title": f"{node['type']}: {node['label']}",
                "color": get_node_color(node.get("type", "unknown")),
                "size": min(30, 15 + len(node.get("label", "")) / 4),
                "font": {"size": 12},
            }
        )

    vis_edges = []
    for edge in edges:
        vis_edges.append(
            {
                "from": edge["source"],
                "to": edge["target"],
                "label": edge.get("label", ""),
                "title": f"{edge.get('label', 'unknown')} relationship",
                "arrows": "to",
                "color": {"color": "#ccc", "highlight": "#ff0000"},
                "smooth": {"type": "continuous"},
            }
        )

    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Quantum Experiment - Knowledge Graph</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }}
        
        .container {{ display: flex; height: 100vh; }}
        
        #network {{
            flex: 1;
            background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
            border-right: 2px solid #333;
        }}
        
        .sidebar {{
            width: 300px;
            background: white;
            padding: 20px;
            overflow-y: auto;
            box-shadow: -2px 0 10px rgba(0,0,0,0.1);
        }}
        
        .sidebar h2 {{ color: #333; margin-bottom: 20px; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
        
        .sidebar h3 {{ color: #666; font-size: 14px; margin-top: 15px; margin-bottom: 10px; text-transform: uppercase; }}
        
        .stats {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 13px;
        }}
        
        .stats div {{ margin: 8px 0; }}
        
        .stats strong {{ color: #0066cc; }}
        
        .node-list {{
            list-style: none;
        }}
        
        .node-list li {{
            padding: 8px;
            margin: 5px 0;
            background: #f0f0f0;
            border-left: 3px solid #0066cc;
            cursor: pointer;
            border-radius: 3px;
            font-size: 12px;
            transition: background 0.2s;
        }}
        
        .node-list li:hover {{
            background: #e0e7ff;
        }}
        
        .legend {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #ccc;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 8px 0;
            font-size: 12px;
        }}
        
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 2px;
            margin-right: 8px;
        }}
        
        .controls {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
        }}
        
        .controls input {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-size: 12px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
            color: white;
            padding: 15px;
            margin: -20px -20px 20px -20px;
            border-radius: 0;
        }}
        
        .header h1 {{ font-size: 16px; margin: 0; }}
        .header p {{ font-size: 12px; margin: 5px 0 0 0; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="container">
        <div id="network"></div>
        
        <div class="sidebar">
            <div class="header">
                <h1>🔗 Knowledge Graph</h1>
                <p>Quantum Experiment Platform</p>
            </div>
            
            <div class="controls">
                <input type="text" id="searchBox" placeholder="Search nodes..." />
            </div>
            
            <div class="stats">
                <div><strong>Nodes:</strong> {len(nodes)}</div>
                <div><strong>Edges:</strong> {len(edges)}</div>
                <div><strong>Types:</strong> {len(set(n.get('type', 'unknown') for n in nodes))}</div>
            </div>
            
            <h3>🎯 God Nodes</h3>
            <ul class="node-list" id="godNodes"></ul>
            
            <h3>All Nodes</h3>
            <ul class="node-list" id="nodeList"></ul>
            
            <div class="legend">
                <h3>Legend</h3>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FF6B6B;"></div>
                    <span>Module</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #4ECDC4;"></div>
                    <span>Class</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #45B7D1;"></div>
                    <span>Function</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FFA07A;"></div>
                    <span>Other</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Vis.js initialization
        const nodes = new vis.DataSet({nodes});
        const edges = new vis.DataSet({edges});
        
        const container = document.getElementById('network');
        const data = {{ nodes: nodes, edges: edges }};
        
        const options = {{
            physics: {{
                enabled: true,
                stabilization: {{ iterations: 200 }},
                barnesHut: {{
                    gravitationalConstant: -15000,
                    centralGravity: 0.3,
                    springLength: 200,
                    damping: 0.4
                }}
            }},
            interaction: {{
                hideEdgesOnDrag: true,
                navigationButtons: true,
                keyboard: true
            }},
            nodes: {{
                borderWidth: 2,
                borderWidthSelected: 3,
                font: {{ color: '#fff', size: 13, face: 'Segoe UI' }}
            }},
            edges: {{
                width: 1.5,
                font: {{ size: 10, color: '#999' }}
            }}
        }};
        
        const network = new vis.Network(container, data, options);
        
        // Calculate god nodes
        function getGodNodes() {{
            const connectivity = {{}};
            edges.forEach(edge => {{
                connectivity[edge.from] = (connectivity[edge.from] || 0) + 1;
                connectivity[edge.to] = (connectivity[edge.to] || 0) + 1;
            }});
            
            return Object.entries(connectivity)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5);
        }}
        
        // Populate god nodes
        const godNodesList = document.getElementById('godNodes');
        getGodNodes().forEach(([nodeId, count]) => {{
            const node = nodes.get(parseInt(nodeId));
            const li = document.createElement('li');
            li.textContent = node.label + ' (' + count + ')';
            li.onclick = () => network.selectNodes([node.id]);
            godNodesList.appendChild(li);
        }});
        
        // Populate all nodes
        const nodeList = document.getElementById('nodeList');
        nodes.forEach(node => {{
            const li = document.createElement('li');
            li.textContent = node.label;
            li.onclick = () => network.selectNodes([node.id]);
            nodeList.appendChild(li);
        }});
        
        // Search functionality
        document.getElementById('searchBox').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const filtered = nodes.get({{
                filter: node => node.label.toLowerCase().includes(query)
            }});
            
            nodeList.innerHTML = '';
            filtered.forEach(node => {{
                const li = document.createElement('li');
                li.textContent = node.label;
                li.onclick = () => network.selectNodes([node.id]);
                nodeList.appendChild(li);
            }});
        }});
    </script>
</body>
</html>"""

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Generated visualization: {output_path}")
    return True


def get_node_color(node_type: str) -> str:
    """Get color for node type"""
    colors = {
        "module": "#FF6B6B",
        "class": "#4ECDC4",
        "function": "#45B7D1",
        "method": "#96CEB4",
        "variable": "#FFEAA7",
    }
    return colors.get(node_type, "#FFA07A")


if __name__ == "__main__":
    success = generate_visualization()
    if success:
        output_path = Path("graphify-out/graph-visualization.html").resolve()
        print(f"\n📊 Open in browser: {output_path}")
