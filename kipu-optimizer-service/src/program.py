import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
import numpy as np
import neal

class SCFTierInput(BaseModel):
    supplier_id: str
    risk_score: float
    yield_pct: float
    esg_score: float

class InputData(BaseModel):
    tiers: List[SCFTierInput]
    budget: float = 1000000.0

class InputParams(BaseModel):
    risk_tolerance: float = 50.0
    esg_min: float = 60.0

class CalculationResult(BaseModel):
    selected_suppliers: List[str]
    sample: Dict[str, int]
    elapsed_time: float

def run(data: InputData, params: InputParams) -> CalculationResult:
    """
    Kipu-Native SCF Optimization.
    Using Simulated Annealing (Neal) inside the Kipu Managed Service as a first step.
    Can be upgraded to real QPU via Planqk Quantum Provider.
    """
    start_time = time.time()
    
    # 1. Build QUBO
    tiers = data.tiers
    n = len(tiers)
    Q = {}
    
    for i, tier in enumerate(tiers):
        # ESG-weighted objective
        esg_bonus = tier.esg_score / 100.0
        Q[(i, i)] = -tier.yield_pct + (0.5 * tier.risk_score) - esg_bonus
    
    # Penalty for over-concentration
    penalty = 800
    for i in range(n):
        for j in range(i + 1, n):
            Q[(i, j)] = penalty / n
            
    # 2. Solve using Neal (Simulated Annealing)
    sampler = neal.SimulatedAnnealingSampler()
    response = sampler.sample_qubo(Q, num_reads=50, seed=42)
    sample = response.first.sample
    
    # 3. Format Result
    selected_suppliers = [tiers[i].supplier_id for i, v in sample.items() if v == 1]
    
    # Cast keys to string for JSON serialization
    sample_json = {str(k): int(v) for k, v in sample.items()}
    
    elapsed_time = time.time() - start_time
    
    return CalculationResult(
        selected_suppliers=selected_suppliers,
        sample=sample_json,
        elapsed_time=elapsed_time
    )
