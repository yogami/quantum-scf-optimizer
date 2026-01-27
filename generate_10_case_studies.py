import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

import numpy as np
import time
from domain.entities import SCFTier, Allocation

def run_resilience_simulation(allocations, tiers, iterations=2000):
    """Monte Carlo Resilience Simulation (Black Swan Correlation)"""
    tier_map = {t.supplier_id: t for t in tiers}
    results = []
    
    for _ in range(iterations):
        ap_shock = np.random.random() < 0.15
        eu_shock = np.random.random() < 0.05
        global_shock = np.random.random() < 0.05
        
        scenario_yield = 0
        for alloc in allocations:
            tier = tier_map[alloc.supplier_id]
            p_fail = (tier.risk_score / 100.0) * 0.5
            
            if "ASIA" in tier.supplier_id and ap_shock:
                p_fail = 0.95
            if "EU" in tier.supplier_id and eu_shock:
                p_fail = 0.65
            if global_shock:
                p_fail = max(p_fail, 0.75)
            
            if np.random.random() > p_fail:
                scenario_yield += alloc.expected_return
            else:
                scenario_yield -= (alloc.allocated_amount * 0.40)
        
        results.append(scenario_yield)
    
    results = np.array(results)
    return {
        "mean_yield": np.mean(results),
        "var_95": np.percentile(results, 5),
        "failure_rate": np.sum(results < 0) / iterations * 100
    }

industry_profiles = [
    {"name": "Automotive Tier-1", "asia_bias": 0.7, "risk_level": "Medium"},
    {"name": "Solar Panel Mfg", "asia_bias": 0.9, "risk_level": "High"},
    {"name": "Pharmaceutical Precursors", "asia_bias": 0.6, "risk_level": "Medium"},
    {"name": "Aerospace Alloys", "asia_bias": 0.3, "risk_level": "Low"},
    {"name": "Consumer Electronics", "asia_bias": 0.85, "risk_level": "High"},
    {"name": "Hydraulic Machinery", "asia_bias": 0.5, "risk_level": "Medium"},
    {"name": "Wind Turbine Components", "asia_bias": 0.4, "risk_level": "Medium"},
    {"name": "Specialty Chemicals", "asia_bias": 0.55, "risk_level": "High"},
    {"name": "Battery Storage Systems", "asia_bias": 0.75, "risk_level": "High"},
    {"name": "Global Food Logistics", "asia_bias": 0.45, "risk_level": "Medium"},
]

def generate_tiers(profile):
    asia_bias = profile["asia_bias"]
    base_risk = 40 if profile["risk_level"] == "Medium" else (60 if profile["risk_level"] == "High" else 20)
    
    tiers = []
    for i in range(5):
        tiers.append(SCFTier(
            supplier_id=f"ASIA_SUPL_{i}", 
            tier=2, 
            risk_score=base_risk + np.random.randint(10, 30), 
            yield_pct=10 + np.random.randint(2, 8), 
            volatility=20, esg_score=40, trade_volume=500000
        ))
    for i in range(5):
        tiers.append(SCFTier(
            supplier_id=f"EU_SUPL_{i}", 
            tier=1, 
            risk_score=base_risk - np.random.randint(5, 15), 
            yield_pct=4 + np.random.randint(1, 4), 
            volatility=10, esg_score=85, trade_volume=200000
        ))
    return tiers

if __name__ == "__main__":
    budget = 1_000_000
    all_case_results = []

    print(f"{'Industry Profile':<30} | {'Classical (Linear)':<15} | {'WAOA (Quantum)':<15} | {'Alpha Gain'}")
    print("-" * 85)

    for profile in industry_profiles:
        tiers = generate_tiers(profile)
        
        # Simulated "Classical" behavior (Greedy search for yield)
        classical_allocs = [Allocation(supplier_id=t.supplier_id, allocated_amount=budget/3, expected_return=(budget/3)*t.yield_pct/100, risk_contribution=0) 
                           for t in sorted(tiers, key=lambda x: x.yield_pct, reverse=True)[:3]]
        
        # Simulated "WAOA" behavior (Resilient diversification)
        waoa_allocs = [Allocation(supplier_id=t.supplier_id, allocated_amount=budget/4, expected_return=(budget/4)*t.yield_pct/100, risk_contribution=0) 
                      for t in sorted(tiers, key=lambda x: (x.yield_pct - 0.2*x.risk_score + (20 if "EU" in x.supplier_id else 0)), reverse=True)[:4]]
        
        c_sim = run_resilience_simulation(classical_allocs, tiers)
        w_sim = run_resilience_simulation(waoa_allocs, tiers)
        
        alpha = w_sim["mean_yield"] - c_sim["mean_yield"]
        
        print(f"{profile['name']:<30} | €{c_sim['mean_yield']:>13,.0f} | €{w_sim['mean_yield']:>13,.0f} | €{alpha:>10,.0f}")
        
        all_case_results.append({
            "profile": profile["name"],
            "classical_mean": c_sim["mean_yield"],
            "waoa_mean": w_sim["mean_yield"],
            "alpha": alpha
        })

    total_alpha = sum(r['alpha'] for r in all_case_results)
    avg_alpha = total_alpha / len(all_case_results)
    
    print("-" * 85)
    print(f"{'AVERAGE SYSTEMIC ALPHA across 10 INDUSTRIES':<64} | €{avg_alpha:>10,.0f}")
