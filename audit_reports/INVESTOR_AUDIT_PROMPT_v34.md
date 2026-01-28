# INVESTOR/CFO AUDIT PROMPT (v34.0)

**INSTRUCTIONS:**
Copy and paste the entire block below into **Grok 2 (fun mode)** or **Perplexity (Pro)**.

---

**ROLE:**
Act as the **Chief Risk Officer (CRO)** and **Head of Quantitative Analysis** for a Tier 1 Global Bank (e.g., Deutsche Bank, JP Morgan). You are strict, skeptical, and terrified of regulatory fines (MaRisk, Basel III).

**CONTEXT:**
We are considering acquiring a startup called **CascadeGuard**.
They claim their "Flow Sentinel" engine (v34.0) is a MaRisk-compliant solution for identifying "Hidden Chokepoints" in our Multi-Tier Supply Chain.
Previous versions were rejected for "math-washing" and "gameability" (e.g., Dilution Floods).
They claim v34.0 is "Pilot Ready" and has solved these issues with "Financial Integrity" checks.

**INPUT DATA:**

### 1. The Code (v34.0 Flow Sentinel)
```python
import networkx as nx

class SupplyChainContagionAuditor:
    def audit_contagion_risk(self, suppliers, total_exposure, policy_tier="bafin_standard", dependencies=None, run_adversarial_test=False):
        # [HARDENING v33.8] FINANCIAL VALIDATION & SPEND-BASED CAPACITIES
        total_supplier_spend = sum(float(s.get('spend', 0.0)) for s in suppliers)
        inflation_ratio = total_supplier_spend / total_exposure if total_exposure > 0 else 0.0

        # Heuristic Capacity Mapping
        supplier_map = {s['id']: s for s in suppliers}
        for s in suppliers: 
            tier = str(s.get('tier', '4')).replace("Tier ", "")
            if tier.lower() == 'anchor': 
                 cap = total_exposure * 1.5 
            else:
                 # v33.9: spend=0 -> cap=0.01 (No Free Capacity)
                 spend = float(s.get('spend', 0.0))
                 cap = spend if spend > 0 else 0.01 
            
            G.add_node(s['id'], **s, capacity=cap)
            
        # [HARDENING v33.7] TOPOLOGY VALIDATION
        if dependencies:
            valid_edges = []
            for u, v in dependencies:
                # Tier 3/4 CANNOT connect directly to Anchor.
                u_tier = str(supplier_map.get(u, {'tier':'4'}).get('tier','4')).replace("Tier ", "")
                v_tier = str(supplier_map.get(v, {'tier':'4'}).get('tier','4')).replace("Tier ", "")
                is_deep = u_tier in ['3','4']
                is_anchor = (v == "BMW_GROUP" or v_tier.lower()=='anchor')
                if is_deep and is_anchor: continue 
                valid_edges.append((u, v))
            G.add_edges_from(valid_edges)

        # BASELINE FLOW
        G_split = self._build_node_split(G, "BMW_GROUP")
        base_flow = nx.maximum_flow_value(G_split, "SUPER_SOURCE", "BMW_GROUP_OUT")

        # ADVERSARIAL TEST
        if run_adversarial_test and base_flow > 0:
            # v34.0: Mandatory Inflation Check (No "Aggressive" Bypass)
            if inflation_ratio > 1.5:
                 return {"status": "FAILED_INFLATION", "resilience": 0.0}
            
            # Simulation...
            drop_percent = self._simulate_shock(G, "BMW_GROUP", base_flow)
            
            # Complexity Cap (v33.5)
            if drop_percent == -1.0: # >50 Criticals
                 return {"status": "FAILED_COMPLEXITY_CAP", "resilience": 0.0}
                 
            return {"status": "PASSED" if (1-drop_percent)>0.8 else "FAILED", "resilience": 1-drop_percent}
```

### 2. The Release Notes (v34.0)
*   **Anti-Dilution**: Checks `Total Spend / Exposure < 1.5`. Fails if breached.
*   **Zero-Cost**: `spend=0` now gives `cap=0.01` (negligible).
*   **Result**: Attackers must inject spend to get capacity, but injecting spend triggers the Inflation Cap.
*   **Catch-22**: "To dilute the risk, you must reveal the fraud."

### 3. The Latest Audit (Iteration 10)
*   **Grok's Critique**: "I can't flood dummies because they have no capacity. I can't add capacity because I hit the Inflation Cap. The only way is to lie about 'Total Spend' (Data Fraud)."
*   **Perplexity**: "Max-Flow Min-Cut is a valid screening tool, but relies on Data Integrity (Spend=Capacity)."

---

**YOUR TASK:**
As the **CRO**, make a definitive decision: **BUY** or **NO-BUY**?

1.  **Gameability Check**: Is there ANY way a trader can bypass the `inflation_ratio > 1.5` check to hide a massive single-point-of-failure? (Assume they cannot change the code, only the `suppliers.json`).
    *   *Can they use 'Circular Dependencies'?*
    *   *Can they use 'Negative Spend'?*
2.  **MaRisk Compliance**: Does the "Failed Inflation" error satisfy the requirement for "Data Consistency Checks"?
3.  **Verdict**: Is this "Snake Oil" or "Industrial Grade"?

**Output Format:**
*   **Executive Summary**: (2 lines).
*   **The "Kill Shot" Analysis**: Try to break it one last time.
*   **Final Decision**: BUY / NO-BUY.
