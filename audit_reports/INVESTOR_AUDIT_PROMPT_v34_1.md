# INVESTOR/CFO AUDIT PROMPT (v34.1)

**INSTRUCTIONS:**
Copy and paste the entire block below into **Grok 2 (fun mode)** or **Perplexity (Pro)**.

---

**ROLE:**
Act as the **Chief Risk Officer (CRO)** and **Head of Quantitative Analysis** for a Tier 1 Global Bank.
You previously rejected "CascadeGuard" for Code Bugs and Gameability.
They have submitted **v34.1** for re-evaluation.

**CONTEXT:**
CascadeGuard claims to have fixed the "Negative Spend" and "Circular Dependency" exploits you identified.
They also fixed the "broken code" snippet where the Graph `G` was not initialized.

**INPUT DATA:**

### 1. The Code (v34.1 Flow Sentinel - Corrected)
```python
import networkx as nx

class SupplyChainContagionAuditor:
    def audit_contagion_risk(self, suppliers, total_exposure, policy_tier="bafin_standard", dependencies=None, run_adversarial_test=False):
        G = nx.DiGraph() # Initialized correctly

        # [HARDENING v33.8] FINANCIAL VALIDATION
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
        
        try:
            base_flow = nx.maximum_flow_value(G_split, "SUPER_SOURCE", "BMW_GROUP_OUT")
        except: base_flow = 0.0

        # ADVERSARIAL TEST
        if run_adversarial_test and base_flow > 0:
            # [HARDENING v34.1] Data Integrity Checks (Perplexity Fixes)
            
            # 1. Negative Spend: Block -1000 spend exploits.
            if any(float(s.get('spend', 0.0)) < 0 for s in suppliers):
                 return {"status": "FAILED_NEGATIVE_SPEND", "resilience": 0.0}

            # 2. Cycles: Block Circular Dependencies (A->B->A).
            if not nx.is_directed_acyclic_graph(G):
                 return {"status": "FAILED_CYCLES", "resilience": 0.0}

            # 3. Inflation: Mandatory Check (>1.5x Exposure).
            if inflation_ratio > 1.5:
                 return {"status": "FAILED_INFLATION", "resilience": 0.0}
            
            # Simulation...
            drop_percent = self._simulate_shock(G, "BMW_GROUP", base_flow)
            
            # Complexity Cap (v33.5)
            if drop_percent == -1.0: # >50 Criticals
                 return {"status": "FAILED_COMPLEXITY_CAP", "resilience": 0.0}
                 
            return {"status": "PASSED" if (1-drop_percent)>0.8 else "FAILED", "resilience": 1-drop_percent}
```

### 2. The Release Notes (v34.1)
*   **Fixed Negative Spend**: Code now scans all suppliers for `spend < 0` and Fails immediately.
*   **Fixed Cycles**: Code now runs `nx.is_directed_acyclic_graph(G)` and Fails on cycles.
*   **Fixed Code Snippet**: `G` is correctly initialized.

---

**YOUR TASK:**
As the **CRO**, make a definitive decision: **BUY** or **NO-BUY**?

1.  **Re-Verify**: Did v34.1 actually fix the specific exploits you found?
2.  **Kill Shot**: Is there *still* a way to lie? (e.g. "Duplicate Supplier Names"? "Unicode Homoglyphs"?)
3.  **Verdict**: Is this Pilot Ready for testing with *Verified Data*?
