from src.domain.topological_core import SupplyChainContagionAuditor

def test_grok_patch():
    auditor = SupplyChainContagionAuditor()
    
    # 1. Create a "Grok Vector" Attack (Artificial Dilution)
    # 201 Nodes (Limit is 200) to trigger FAIL_COMPLEXITY_CAP
    attack_nodes = [{"id": f"Dummy_{i}", "tier": "4", "spend": 10.0} for i in range(201)]
    # Add an anchor
    attack_nodes.append({"id": "Anchor_BMW", "tier": "Anchor", "spend": 1000.0})
    
    total_exposure = 50000.0 # High exposure
    
    print("--- Running Adversarial Audit (Grok Patch) ---")
    result = auditor.audit_contagion_risk(
        suppliers=attack_nodes,
        total_exposure=total_exposure,
        run_adversarial_test=True
    )
    
    print(f"Status: {result['status']}")
    print(f"Description: {result.get('description', 'N/A')}")
    
    if result["status"] == "FAILED_GOVERNANCE_CHECK":
        print("\n*** SUCCESS: Grok Patch BLOCKED the attack. ***")
        return True
    else:
        print("\n*** FAIL: Attack bypassed the governor. ***")
        return False

if __name__ == "__main__":
    test_grok_patch()
