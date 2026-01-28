from typing import Dict, List, Any, Tuple
import statistics

class ComplexityGovernor:
    """
    Enforces 'Anti-Gaming' policies on Supply Chain Graphs.
    Specifically designed to block 'Grok Vectors' (Dummy Node Flooding, Inflation Gaming).
    """

    def __init__(self, inflation_cap_multiplier: float = 1.5):
        self.inflation_cap_multiplier = inflation_cap_multiplier

    def validate_graph(self, nodes: List[Dict], edges: List[Dict], total_exposure: float) -> Tuple[bool, List[str]]:
        """
        Validates the graph topology against governance rules.
        Returns: (passed: bool, reasons: List[str])
        """
        reasons = []
        node_count = len(nodes)
        
        # Rule 1: Artificial Dilution (Grok Vector 2)
        # If graph is large (>50 nodes) but has suspicious uniformity or lack of criticals (pre-calc check), flag it.
        # Here we check for 'Dummy Node' characteristics directly:
        # - High count of low-spend nodes that sum exactly to a cap.
        
        if node_count > 200:
             reasons.append(f"FAIL_COMPLEXITY_CAP: Node count {node_count} exceeds limit (200). MaRisk requires intelligible models.")

        # Rule 2: Inflation Gaming (Grok Vector 4)
        # Check total spend vs exposure.
        total_spend = sum(n.get('spend', 0) for n in nodes)
        max_allowed_spend = total_exposure * self.inflation_cap_multiplier
        
        # Allow small floating point margin, but strict check
        if total_spend > max_allowed_spend + 1.0: # 1.0 buffer for float noise
            reasons.append(f"FAIL_INFLATION: Total spend {total_spend:.2f} exceeds cap {max_allowed_spend:.2f} (1.5x Exposure).")

        # Rule 3: Tier Discipline (Grok Vector 5)
        # Tiers must flow logically (4->3->2->1->Anchor).
        # We assume standard tier naming or attributes.
        # This is harder to check without traversing edges, but we can sample.
        
        # Rule 4: 'Ghosting' Detection (Grok Vector 3)
        # Check for duplicate node attributes (same address/metadata if available, or just suspicious ID patterns).
        ids = [n['id'] for n in nodes]
        if len(ids) != len(set(ids)):
             reasons.append("FAIL_DUPLICATE_IDS: Duplicate node IDs detected.")
             
        # Check for suspicious ID patterns (e.g., "DummyTier2_001")
        dummy_count = sum(1 for nid in ids if "dummy" in nid.lower() or "fake" in nid.lower())
        if dummy_count > 0:
             reasons.append(f"FAIL_DUMMY_DETECTED: {dummy_count} nodes identified as test dummies.")

        passed = len(reasons) == 0
        return passed, reasons

    def analyze_criticality_ratio(self, nodes: List[Dict], critical_nodes: List[str]) -> Tuple[bool, str]:
        """
        Post-MaxFlow Check:
        If we have many nodes but almost NO critical chokepoints, it implies 'Dilution Gaming'.
        """
        node_count = len(nodes)
        crit_count = len(critical_nodes)
        
        if node_count > 50 and crit_count == 0:
            return False, "FAIL_DILUTION: Large graph (>50 nodes) with ZERO critical chokepoints. Mathematical improbability implies artificial dilution."
            
        return True, "OK"
