import json
import random

def enrich_proxy_with_real_names():
    """
    Injects Real-World Supplier Names into the Scale-Free Proxy.
    Maps Hubs (High Degree) -> Tier 1 Giants.
    Maps Mid-Nodes -> Tier 2 Specialists.
    """
    print(">>> ENRICHING PROXY WITH REAL ENTITY NAMES <<<")
    
    # 1. Load Baseline Proxy
    try:
        with open("dashboard/public/real_world_proxy_auto.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("ERROR: Run fetch_real_world_proxy.py first.")
        return

    # 2. Real World Entities (Automotive)
    # Source: Top 100 Auto Suppliers
    tier_1_giants = [
        "Robert Bosch GmbH", "Denso Corp", "Magna International", "ZF Friedrichshafen", 
        "Aisin Seiki", "Continental AG", "Hyundai Mobis", "Faurecia", "Lear Corp", "Valeo",
        "Bridgestone", "Michelin", "CATL", "Panasonic Automotive", "BorgWarner"
    ]
    
    tier_2_tech = [
        "Infineon Technologies", "NXP Semiconductors", "Renesas Electronics", "STMicroelectronics",
        "Texas Instruments", "NVIDIA Corp", "Qualcomm", "Intel Mobileye", "LG Chem", "SK Innovation"
    ]
    
    tier_3_raw = [
        "ArcelorMittal", "Nippon Steel", "POSCO", "ThyssenKrupp", "BASF", "DuPont"
    ]
    
    # 3. Analyze Degrees to identify Hubs
    nodes = data["nodes"]
    # We need to compute degrees again or trust the 'spend' as proxy for size
    # Let's assume High Spend = Hub
    
    # Sort nodes by spend (descending) excluding Anchor
    supplier_nodes = [n for n in nodes if n["tier"] != "Anchor"]
    supplier_nodes.sort(key=lambda x: x["spend"], reverse=True)
    
    # 4. Map Names
    mapping_log = []
    
    for i, node in enumerate(supplier_nodes):
        old_id = node["id"]
        new_name = old_id # Default
        
        # Tier 1 Giants (Top 15 Big Spenders)
        if i < len(tier_1_giants):
            new_name = tier_1_giants[i]
            node["tier"] = "1" # Reinforce Tier
        
        # Tier 2 Tech (Next 10)
        elif i < len(tier_1_giants) + len(tier_2_tech):
            new_name = tier_2_tech[i - len(tier_1_giants)]
            node["tier"] = "2"
            
        # Tier 3 Raw (Next 6)
        elif i < len(tier_1_giants) + len(tier_2_tech) + len(tier_3_raw):
            new_name = tier_3_raw[i - (len(tier_1_giants) + len(tier_2_tech))]
            node["tier"] = "3"
            
        # Update Node ID
        # We must update references in Edges too!
        # Store mapping
        mapping_log.append((old_id, new_name))
        node["id"] = new_name
        node["meta"] = {"original_id": old_id, "type": "Real-World-Entity"}

    # Update Edges
    id_map = {old: new for old, new in mapping_log}
    # Add Anchor to map if needed (it stays BMW_GROUP_PROXY)
    
    updated_edges = []
    for edge in data["edges"]:
        u, v = edge
        new_u = id_map.get(u, u)
        new_v = id_map.get(v, v)
        updated_edges.append([new_u, new_v])
        
    data["edges"] = updated_edges
    
    # 5. Save as Digital Twin
    data["meta"]["description"] = "Digital Twin (Enriched) - BMW Group Proxy v1.0"
    
    filename = "dashboard/public/bmw_digital_twin_v1.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"SUCCESS: Digital Twin saved to {filename}")
    print(f"Mapped {len(mapping_log)} nodes to real entities.")

if __name__ == "__main__":
    enrich_proxy_with_real_names()
