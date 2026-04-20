#!/usr/bin/env python3
"""
Graphify Integration for VS Code Copilot Chat
Query the quantum knowledge graph from the Copilot Chat interface
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


class QuantumGraphQuery:
    """Query the Quantum Experiment knowledge graph"""

    def __init__(self, graph_path: str = "graphify-out/graph.json"):
        self.graph_path = Path(graph_path)
        self.graph = self._load_graph()
        self.nodes = {n["id"]: n for n in self.graph["nodes"]}
        self.edges = self.graph["edges"]

    def _load_graph(self) -> Dict:
        """Load the knowledge graph"""
        if not self.graph_path.exists():
            return {"nodes": [], "edges": []}

        with open(self.graph_path, "r") as f:
            return json.load(f)

    def find_node(self, label: str) -> List[Dict]:
        """Find nodes by label or partial match"""
        return [n for n in self.graph["nodes"] if label.lower() in n["label"].lower()]

    def get_node_connections(self, node_id: int) -> Dict[str, List]:
        """Get all connections for a node"""
        incoming = []
        outgoing = []

        for edge in self.edges:
            if edge["source"] == node_id:
                outgoing.append(
                    {
                        "target": self.nodes.get(edge["target"], {}).get("label", "?"),
                        "type": edge.get("label", "?"),
                    }
                )
            elif edge["target"] == node_id:
                incoming.append(
                    {
                        "source": self.nodes.get(edge["source"], {}).get("label", "?"),
                        "type": edge.get("label", "?"),
                    }
                )

        return {"incoming": incoming, "outgoing": outgoing}

    def query(self, question: str) -> str:
        """Query the knowledge graph with a natural language question"""

        # Keyword extraction from question
        keywords = question.lower().split()

        # Search for relevant nodes
        relevant_nodes = []
        for node in self.graph["nodes"]:
            label_words = node["label"].lower().split()
            if any(k in label_words for k in keywords):
                relevant_nodes.append(node)

        if not relevant_nodes:
            return f"No nodes found matching: {question}"

        # Build response
        response = f"📊 Found {len(relevant_nodes)} relevant nodes:\n\n"
        for node in relevant_nodes[:5]:
            connections = self.get_node_connections(node["id"])
            response += f"**{node['label']}** ({node.get('type', 'node')})\n"

            if connections["outgoing"]:
                response += f"  → Connects to: {', '.join([c['target'] for c in connections['outgoing'][:3]])}\n"
            if connections["incoming"]:
                response += f"  ← Connected from: {', '.join([c['source'] for c in connections['incoming'][:3]])}\n"
            response += "\n"

        return response

    def get_god_nodes(self, top_n: int = 5) -> List[Dict]:
        """Find most connected nodes (god nodes)"""
        connectivity = {}

        for node in self.graph["nodes"]:
            connections = len(
                [
                    e
                    for e in self.edges
                    if e["source"] == node["id"] or e["target"] == node["id"]
                ]
            )
            connectivity[node["id"]] = {
                "label": node["label"],
                "type": node.get("type", "unknown"),
                "connections": connections,
            }

        return sorted(
            connectivity.items(), key=lambda x: x[1]["connections"], reverse=True
        )[:top_n]


def main():
    """Demo usage of QuantumGraphQuery"""

    print("=" * 70)
    print("🔗 QUANTUM EXPERIMENT PLATFORM - KNOWLEDGE GRAPH QUERY DEMO")
    print("=" * 70)

    query_engine = QuantumGraphQuery()

    print(
        f"\n📊 Graph Loaded: {len(query_engine.graph['nodes'])} nodes, {len(query_engine.edges)} edges"
    )

    # Find god nodes
    print("\n🎯 Most Connected Nodes (God Nodes):")
    god_nodes = query_engine.get_god_nodes()
    for node_id, info in god_nodes:
        print(f"   • {info['label']}: {info['connections']} connections")

    # Example queries
    queries = [
        "What is a quantum circuit?",
        "How does the simulator work?",
        "Show measurement analysis",
        "What connects scalable simulator to cloud integration?",
    ]

    print("\n📝 Example Queries:")
    for q in queries:
        print(f"\n❓ Query: {q}")
        result = query_engine.query(q)
        print(result[:200] + "..." if len(result) > 200 else result)


if __name__ == "__main__":
    main()
