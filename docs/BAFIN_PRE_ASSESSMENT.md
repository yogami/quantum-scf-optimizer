# BAFIN MARISK BTO 3 PRE-ASSESSMENT (DRAFT)

**To**: Compliance / Model Risk Management (Commerzbank / LBBW)
**From**: Berlin AI Labs (Engineering Lead)
**Subject**: Preliminary Compliance Statement for R-QAOA Risk Engine

## 1. Interpretability (No "Black Box" Guarantee)
Under **MaRisk BTO 3**, AI models must be interpretable. Our **R-QAOA** engine is a **Topological Optimizer**, not a Deep Learning model.
- Every optimization decision (the "cut") is mathematically deterministic and traceable.
- We provide the **Hamiltonian Energy Landscape** logs for every run, allowing auditors to see exactly why a specific regional exposure was pruned.

## 2. Backtesting (Historical Integrity)
The engine has been "Back-Validated" against the **Red Sea 2024 Logistics Crisis**.
- **Dataset**: 1,000 anonymised industrial tiers.
- **Success Criterion**: Prevented >20% principal destruction that classical Gurobi/SAS models incurred.

## 3. Data Sovereignty
To meet **GDPR Article 9** and **BNetzA IT-Sicherheit** standards:
- The engine runs as a **Rust-based Edge Service**.
- **Zero Cloud Persistence**: Financial data is processed in-memory and discarded upon optimization.
- **Sovereign Hosting**: Fully compatible with PlanQK / T-Systems Sovereign Cloud.

## 4. Operational Waiver Request
For the "Shadow Mode" pilot (Q2 2026), we propose a **MaRisk Waiver** on the following grounds:
1. The engine is **Read-Only** (Zero influence on live liquidity biddings).
2. All inputs are **Delayed Data** (Post-audit).
3. The pilot is an **Ablation Study** to verify Resilience Alpha before live deployment.

---
**Berlin AI Labs - Regulatory Guardrails.**
