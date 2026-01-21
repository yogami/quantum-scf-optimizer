"""Classical Solver - PuLP-based QUBO optimizer for baseline comparison."""
import time
from typing import Optional
import pulp

from domain.entities import SCFTier, Allocation, OptimizationResult
from ports.secondary.solver_port import SolverPort


class ClassicalSolver(SolverPort):
    """PuLP-based classical linear programming solver."""
    
    def optimize(
        self,
        tiers: list[SCFTier],
        budget: float,
        risk_tolerance: float,
        esg_min: float
    ) -> OptimizationResult:
        """Optimize using PuLP linear programming."""
        start_time = time.time()
        
        # Create problem
        prob = pulp.LpProblem("SCF_Optimization", pulp.LpMaximize)
        
        # Decision variables: allocation percentage for each tier
        alloc_vars = {
            tier.supplier_id: pulp.LpVariable(
                f"alloc_{tier.supplier_id}",
                lowBound=0,
                upBound=1
            )
            for tier in tiers
        }
        
        # Objective: Maximize yield-weighted allocations, penalize risk
        risk_penalty = 0.5
        prob += pulp.lpSum([
            alloc_vars[t.supplier_id] * (t.yield_pct - risk_penalty * t.risk_score / 100)
            for t in tiers
        ]), "Maximize_Risk_Adjusted_Yield"
        
        # Constraint 1: Total allocation = 100%
        prob += pulp.lpSum([alloc_vars[t.supplier_id] for t in tiers]) == 1, "Total_Allocation"
        
        # Constraint 2: Weighted risk <= tolerance
        prob += pulp.lpSum([
            alloc_vars[t.supplier_id] * t.risk_score for t in tiers
        ]) <= risk_tolerance, "Risk_Tolerance"
        
        # Constraint 3: Weighted ESG >= minimum
        prob += pulp.lpSum([
            alloc_vars[t.supplier_id] * t.esg_score for t in tiers
        ]) >= esg_min, "ESG_Minimum"
        
        # Solve
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        solve_time = (time.time() - start_time) * 1000
        
        # Build allocations
        allocations = []
        total_yield = 0.0
        total_risk = 0.0
        
        for tier in tiers:
            alloc_pct = pulp.value(alloc_vars[tier.supplier_id]) or 0.0
            if alloc_pct > 0.001:  # Skip negligible allocations
                allocated_amount = alloc_pct * budget
                expected_return = allocated_amount * tier.yield_pct / 100
                risk_contribution = alloc_pct * tier.risk_score
                
                allocations.append(Allocation(
                    supplier_id=tier.supplier_id,
                    allocated_amount=allocated_amount,
                    expected_return=expected_return,
                    risk_contribution=risk_contribution
                ))
                
                total_yield += expected_return
                total_risk += risk_contribution
        
        return OptimizationResult(
            allocations=allocations,
            total_yield=total_yield,
            total_risk=total_risk,
            solver_type="classical",
            solve_time_ms=solve_time,
            solver_logs=f"Status: {pulp.LpStatus[prob.status]}"
        )
