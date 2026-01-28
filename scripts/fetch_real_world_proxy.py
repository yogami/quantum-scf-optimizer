import networkx as nx
import json
import random
import numpy as np

def generate_real_world_proxy():
    """
    Generates a 'Real-World Proxy' Supply Chain relying on Network Science.
    Real supply chains are Scale-Free (Power Law), not Random.
    We use Barabási-Albert model to simulate 'Preferential Attachment' (Big Suppliers get Bigger).
    """
    print(">>> GENERATING REAL-WORLD PROXY TOPOLOGY (Scale-Free) <<<")
    
    # Parameters for a "Tier 1 Auto" sized slice
    N = 300 # Number of suppliers
    m = 2   # Number of edges to attach from a new node to existing nodes
    
    # 1. Topology: Scale-Free Network (Hub & Spoke)
    G_base = nx.barabasi_albert_graph(N, m, seed=42)
    
    # 2. Assign Tiers (Breadth-First Search from 'Anchor')
    # Use the highest degree node as the 'Main Tier 1 Aggregator' feeding the Anchor
    degrees = dict(G_base.degree())
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    
    # Anchor is external, we connect the Hubs to it.
    anchor_id = "BMW_GROUP_PROXY"
    
    formatted_nodes = []
    formatted_edges = []
    
    # Map graph nodes to Tiers based on distance from Hubs
    # We treat the Top 5 Hubs as Tier 1.
    tier_1_hubs = sorted_nodes[:5]
    
    # BFS to assign tiers
    node_tiers = {}
    for n in G_base.nodes():
        node_tiers[n] = 4 # Default deep tier
        
    # Set Tier 1
    for n in tier_1_hubs:
        node_tiers[n] = 1
        
    # Propagate Tiers (If connected to Tier 1, you are Tier 2, etc.)
    # Simple simulation: 
    # Tier 1 = Hubs
    # Tier 2 = Neighbors of Tier 1
    # Tier 3 = Neighbors of Tier 2
    # Tier 4 = Rest
    
    # Build explicit Tier Map
    visited = set(tier_1_hubs)
    queue = [(n, 1) for n in tier_1_hubs]
    
    while queue:
        node, current_tier = queue.pop(0)
        node_tiers[node] = current_tier
        
        if current_tier < 4:
            neighbors = list(G_base.neighbors(node))
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, current_tier + 1))
    
    # 3. Assign Financials (Spend) - Log-Normal Distribution (Real world wealth distribution)
    # Hubs get massive spend, tail gets tiny spend.
    for n in G_base.nodes():
        tier = str(node_tiers.get(n, 4))
        # Spend correlates with Degree (Connectivity)
        degree = degrees[n]
        base_spend = np.random.lognormal(mean=2.0, sigma=1.0) * 10.0
        spend = base_spend * degree # Hubs have high spend
        
        formatted_nodes.append({
            "id": f"SUPPLIER_{n}",
            "tier": tier,
            "spend": round(spend, 2)
        })
    
    # Add Anchor
    formatted_nodes.append({
        "id": anchor_id,
        "tier": "Anchor",
        "spend": 500000.0 # Massive capacity
    })
    
    # 4. Create Directed Flow (Tier N -> Tier N-1 -> ... -> Tier 1 -> Anchor)
    # In BA graph, edges are undirected. We direct them towards the Hubs.
    for u, v in G_base.edges():
        tier_u = node_tiers[u]
        tier_v = node_tiers[v]
        
        # Flow goes High Tier Number -> Low Tier Number
        source, target = (u, v) if tier_u > tier_v else (v, u)
        
        # If same tier, random direction or bidirectional? Let's say flow towards higher degree
        if tier_u == tier_v:
            source, target = (u, v) if degrees[u] < degrees[v] else (v, u)
            
        formatted_edges.append([f"SUPPLIER_{source}", f"SUPPLIER_{target}"])
        
    # Connect Tier 1 to Anchor
    for hub in tier_1_hubs:
         formatted_edges.append([f"SUPPLIER_{hub}", anchor_id])
         
    dataset = {
        "nodes": formatted_nodes,
        "edges": formatted_edges,
        "meta": {
            "source": "Generated via Barabasi-Albert Scale-Free Model (Network Science Standard)",
            "description": "Proxy for Automotive Supply Chain (Hub & Spoke Topology)",
            "node_count": len(formatted_nodes),
            "edge_count": len(formatted_edges)
        }
    }
    
    filename = "dashboard/public/real_world_proxy_auto.json"
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"SUCCESS: Real-World Proxy saved to {filename}")
    print(f"Nodes: {len(formatted_nodes)}, Edges: {len(formatted_edges)}")

if __name__ == "__main__":
    generate_real_world_proxy()
