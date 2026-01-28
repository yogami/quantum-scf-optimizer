import json
import random
import networkx as nx

def generate_bmw_topology(n=500):
    """
    Generates a synthetic "BMW-Style" Supply Chain Network.
    Structure:
    - Tier 1: Major Module Integrators (Engine, Chassis, Electronics...) - High Capacity (100)
    - Tier 2: Sub-System Suppliers - Med Capacity (75)
    - Tier 3: Component Manufacturers - Low Capacity (50)
    - Tier 4: Raw Material/Commodity - Min Capacity (25) - "Silent Killers"
    """
    random.seed(42) # Determinism
    
    nodes = []
    edges = []
    
    # 1. ANCHOR
    anchor = {"id": "BMW_GROUP", "tier": "Anchor", "capacity": 1000.0}
    nodes.append(anchor)
    
    # 2. TIER DISTRIBUTION
    # Pyramid structure
    t1_count = 10
    t2_count = 40
    t3_count = 100
    t4_count = n - t1_count - t2_count - t3_count - 1 # ~350
    
    # Generate Nodes
    t1_nodes = [f"T1_{i}" for i in range(t1_count)]
    t2_nodes = [f"T2_{i}" for i in range(t2_count)]
    t3_nodes = [f"T3_{i}" for i in range(t3_count)]
    t4_nodes = [f"T4_{i}" for i in range(t4_count)]
    
    for nid in t1_nodes: nodes.append({"id": nid, "tier": "1", "capacity": 100.0})
    for nid in t2_nodes: nodes.append({"id": nid, "tier": "2", "capacity": 75.0})
    for nid in t3_nodes: nodes.append({"id": nid, "tier": "3", "capacity": 50.0})
    for nid in t4_nodes: nodes.append({"id": nid, "tier": "4", "capacity": 25.0})
    
    # 3. EDGES (Flow: T4 -> T3 -> T2 -> T1 -> Anchor)
    # T1 -> Anchor
    for t1 in t1_nodes:
        edges.append((t1, "BMW_GROUP"))
        
    # T2 -> T1 (Clustered: Each T1 has ~3-5 T2s)
    for t2 in t2_nodes:
        target = random.choice(t1_nodes)
        edges.append((t2, target))
        # 10% Cross-Link (Redundancy)
        if random.random() < 0.1:
            edges.append((t2, random.choice(t1_nodes)))

    # T3 -> T2
    for t3 in t3_nodes:
        target = random.choice(t2_nodes)
        edges.append((t3, target))
        if random.random() < 0.1: edges.append((t3, random.choice(t2_nodes)))

    # T4 -> T3
    for t4 in t4_nodes:
        target = random.choice(t3_nodes)
        edges.append((t4, target))
        # Higher redundancy at bottom? Or severe bottlenecks?
        # "Silent Killers" often supply MANY T3s (e.g., specialized screw).
        # Let's create some T4 Hubs (High Betweenness, Low Degree? No, High Degree if they supply many)
        # To make them "Silent Killers" (v32 logic), they should link clusters.
        if random.random() < 0.05:
            # Critical raw material supplier feeding multiple clusters
            extra_target = random.choice(t3_nodes)
            if extra_target != target:
                edges.append((t4, extra_target))

    topology = {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "name": "Synthetic BMW Supply Chain",
            "N": n,
            "description": "Clustered Pyramid: T4(Raw)->T3->T2->T1->Anchor"
        }
    }
    
    with open("bmw_synthetic_scf.json", "w") as f:
        json.dump(topology, f, indent=2)
        
    print(f"Generated BMW Topology with {len(nodes)} nodes and {len(edges)} edges.")

if __name__ == "__main__":
    generate_bmw_topology()
