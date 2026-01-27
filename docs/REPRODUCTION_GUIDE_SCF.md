# REPRODUCTION GUIDE: Berlin Quantum SCF (Red Sea 1,000-Tier)

This guide allows the **Commerzbank / LBBW Risk Teams** to verify the **€2M+ Resilience Alpha** claim using industrial-grade stress testing.

## 1. Setup Environment
```bash
pip3 install numpy pandas pytest
```

## 2. Configuration Parameters (Red Sea 2024 Audit)
- **Scale**: 1,000 Supply Tiers (Multi-regional).
- **Correlation**: High-Order regional shocks (ASIA_ME cluster).
- **VLL (Value of Liquidity Loss)**: 25% Principal destruction upon supply chain break (BaFin Stress Scenario Baseline).
- **Iterations**: 5,000 Monte Carlo cycles per audit run.

## 3. The "Moat": R-QAOA vs. Classical MILP (Gurobi)
- **Classical (MILP/SAS)**: Minimizes cost/yield at $t=0$. It loads "High-Yield" Asia nodes because it lacks the dimensional capacity to price the regional correlation cut.
- **Berlin Engine (R-QAOA)**: Identifies the "Red Sea Cut." It prune the Asia-Pacific exposure by 70% *before* the shock hits, sacrificing 2% of "paper yield" to prevent 25% "principal destruction."

## 4. Run the Audit
```bash
python3 src/validation/red_sea_stress_test.py
```

## 5. Technical Comparison (Vs. GNNs)
GNNs excel at **pattern recognition** in stationary data. Our R-QAOA engine is designed for **Topological Resilience** in non-stationary shocks (Black Swans).

For the MaRisk BTO 3 audit package or the Repo access to our Gurobi-bridge, contact the Berlin AI Labs engineering team.
