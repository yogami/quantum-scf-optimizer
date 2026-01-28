import networkx as nx
import json
import random
import numpy as np

def generate_hardened_proxy():
    """
    Generates the 'Optimized' State of the Auto Supply Chain.
    Baseline: Scale-Free (Resilience 36%).
    Hardened: Scale-Free + Mesh Redundancy (Target >80%).
    """
    print(">>> GENERATING HARDENED PROXY (Triadic Mesh) <<<")
    
    # 1. Same Backbone (Barabasi-Albert)
    N = 300 
    m = 2   
    G_base = nx.barabasi_albert_graph(N, m, seed=42) # Fixed seed for direct comparison
    
    # 2. HARDENING: Triadic Closure (Mesh Redundancy)
    # in real life, this means "Dual Sourcing" critical paths.
    
    # Identify Hubs
    degrees = dict(G_base.degree())
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    tier_1_hubs = sorted_nodes[:5]
    
    # Strategy: For every neighbor of a Hub, add a link to ANOTHER Hub (Cross-Linking)
    # This prevents a single Hub failure from cutting off the supply.
    edges_added = 0
    
    # 3. Assign Tiers (Breadth-First Search from 'Anchor')
    # Use the highest degree node as the 'Main Tier 1 Aggregator' feeding the Anchor
    degrees = dict(G_base.degree())
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    
    # Anchor is external, we connect the Hubs to it.
    anchor_id = "BMW_GROUP_PROXY"
    
    # BFS to assign tiers FIRST (so we can enforce DAG on new edges)
    tier_1_hubs = sorted_nodes[:5]
    node_tiers = {}
    for n in G_base.nodes(): node_tiers[n] = 4
    for n in tier_1_hubs: node_tiers[n] = 1
    
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
                    
    # NOW Add Redundancy (Respecting Tiers)
    # We want to connect Tier 2/3 nodes to Alternative Hubs (Tier 1)
    for hub in tier_1_hubs:
        neighbors = list(G_base.neighbors(hub)) # These are mostly Tier 2
        for n in neighbors:
            # Connect this neighbor to a BACKUP Hub (different from current hub)
            backup = random.choice([h for h in tier_1_hubs if h != hub])
            
            # Check edge existence
            if not G_base.has_edge(n, backup) and not G_base.has_edge(backup, n):
                 # Direction must be: n (Tier >1) -> backup (Tier 1). But in undirected base it's just an edge.
                 # The final Directed conversion handles direction based on Tiers.
                 # Since backup is Tier 1, and n is Tier >=2, the flow will naturally be n -> backup. (High Tier Num -> Low Tier Num).
                 # This is valid.
                 G_base.add_edge(n, backup)
                 edges_added += 1

    print(f"   ... Added {edges_added} Triadic Closure Edges (Dual Sourcing).")

    # 4. Assign Financials (Same Spend Logic)
    formatted_nodes = []
    for n in G_base.nodes():
        tier = str(node_tiers.get(n, 4))
        degree = degrees[n] # Use ORIGINAL degree for basic size, or NEW degree?
        # Let's use new degree to reflect that redundancy costs money/capacity? 
        # Or keep base spend to show pure topological gain? 
        # Let's keep base spend logic but update degree count.
        current_degree = G_base.degree(n)
        
        base_spend = np.random.lognormal(mean=2.0, sigma=1.0) * 10.0
        spend = base_spend * current_degree
        
        formatted_nodes.append({
            "id": f"SUPPLIER_{n}",
            "tier": tier,
            "spend": round(spend, 2)
        })
    
    formatted_nodes.append({ "id": anchor_id, "tier": "Anchor", "spend": 500000.0 })
    
    # 5. Directed Edges & Final Formatting (STRICT DAG ENFORCEMENT)
    final_edges = []
    
    # 5. Directed Edges & Final Formatting (GUARANTEED DAG)
    final_edges = []
    
    # helper: convert node to integer ID for tie-breaking
    def get_node_id(node_val):
        return int(node_val)
        
    for u, v in G_base.edges():
        tier_u = node_tiers[u]
        tier_v = node_tiers[v]
        
        # Rule: Flow goes High Tier -> Low Tier (Supplier -> Buyer)
        # We strictly ENFORCE this. If Tiers are equal, we DELETE the edge (for this proxy visualizer).
        # This is the "Hardening" step - simplifying the complexity.
        
        source, target = None, None
        
        if tier_u > tier_v:
            source, target = u, v
        elif tier_v > tier_u:
            source, target = v, u
        else:
            # Same Tier: We REMOVE lateral dependencies in the 'Hardened' model.
            # This represents "Streamlining Supply Lines" to explicit upstream sources.
            continue 
             
        final_edges.append([f"SUPPLIER_{source}", f"SUPPLIER_{target}"])
        
    for hub in tier_1_hubs:
         # Hubs feed Anchor
         final_edges.append([f"SUPPLIER_{hub}", anchor_id])

    dataset = {
        "nodes": formatted_nodes,
        "edges": final_edges,
        "meta": {
            "source": "Hardened Proxy (Scale-Free + Mesh Redundancy)",
            "description": "Optimized Topology (No Lateral Dependencies, Dual Sourcing)",
            "node_count": len(formatted_nodes),
            "edge_count": len(final_edges)
        }
    }
    
    filename = "dashboard/public/hardened_proxy_auto.json"
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)
        
    print(f"SUCCESS: Hardened Proxy saved to {filename}")

if __name__ == "__main__":
    generate_hardened_proxy()
