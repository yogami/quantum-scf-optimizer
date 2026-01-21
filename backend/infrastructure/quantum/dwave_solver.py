"""D-Wave Quantum Solver - Hybrid quantum annealing optimizer with lightweight fallback."""
import time
import os
from typing import Optional

from domain.entities import SCFTier, Allocation, OptimizationResult
from ports.secondary.solver_port import SolverPort


class DWaveSolver(SolverPort):
    """D-Wave Hybrid Solver with Lightweight Simulated Annealing Fallback."""
    
    def __init__(self):
        self.leap_token = os.environ.get("DWAVE_API_TOKEN")
        self._use_fallback = False
        
    def _build_qubo(self, tiers: list[SCFTier]) -> dict:
        """Build QUBO matrix for the optimization problem."""
        n = len(tiers)
        Q = {}
        # Simple max-yield min-risk formulation
        for i, tier in enumerate(tiers):
            Q[(i, i)] = -tier.yield_pct + 0.5 * tier.risk_score
        
        penalty = 500
        for i in range(n):
            for j in range(i + 1, n):
                Q[(i, j)] = penalty / n
        return Q
    
    def _try_dwave_solve(self, Q: dict):
        """Attempt to solve using real D-Wave hardware."""
        if not self.leap_token:
            return None, "No token provided"
        try:
            from dwave.system import LeapHybridSampler
            sampler = LeapHybridSampler(token=self.leap_token)
            response = sampler.sample_qubo(Q)
            return response.first.sample, "Real Quantum (D-Wave Leap)"
        except Exception as e:
            return None, str(e)
    
    def _simulated_fallback(self, Q: dict) -> tuple:
        """Fallback to local Simulated Annealing (Neal) - Lightweight & Faster."""
        try:
            import neal
            sampler = neal.SimulatedAnnealingSampler()
            response = sampler.sample_qubo(Q, num_reads=10)
            return response.first.sample, "Simulated Quantum (Neal Annealer)"
        except Exception as e:
            # Ultimate greedy fallback
            size = max(max(k) for k in Q.keys()) + 1
            sample = {i: 1 if Q.get((i, i), 0) < 0 else 0 for i in range(size)}
            return sample, f"Greedy fallback: {str(e)}"
    
    def optimize(
        self, tiers, budget, risk_tolerance, esg_min
    ) -> OptimizationResult:
        start_time = time.time()
        Q = self._build_qubo(tiers)
        
        # 1. Try real quantum first
        sample, method = self._try_dwave_solve(Q)
        
        # 2. Fallback if needed
        if not sample:
            self._use_fallback = True
            sample, method = self._simulated_fallback(Q)
        
        solve_time = (time.time() - start_time) * 1000
        selected_indices = [i for i, v in sample.items() if v == 1]
        
        # Guaranteed allocation even if solver returns empty
        if not selected_indices:
            selected_indices = [0] 

        alloc_per_selected = 1.0 / len(selected_indices)
        allocations = []
        total_yield = 0.0
        total_risk = 0.0
        
        for idx in selected_indices:
            if idx < len(tiers):
                tier = tiers[idx]
                amt = alloc_per_selected * budget
                allocations.append(Allocation(
                    supplier_id=tier.supplier_id,
                    allocated_amount=amt,
                    expected_return=amt * tier.yield_pct / 100,
                    risk_contribution=alloc_per_selected * tier.risk_score
                ))
                total_yield += amt * tier.yield_pct / 100
                total_risk += alloc_per_selected * tier.risk_score
        
        return OptimizationResult(
            allocations=allocations,
            total_yield=total_yield,
            total_risk=total_risk,
            solver_type="Quantum (Hardware)" if not self._use_fallback else "Quantum (Simulated)",
            solve_time_ms=solve_time,
            solver_logs=f"Method: {method}"
        )
