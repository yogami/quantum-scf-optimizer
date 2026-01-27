# Data Disclosure: SCF Industry Profiles (RWD)
**Dataset Reference: v2026.01**

The Quantum SCF Risk Optimizer utilizes a reference dataset of 15+ supplier profiles reconstructed from public industrial filings, industry resilience reports (McKinsey/BCG 2024-25), and historical failure signatures.

## 📂 1. Profile Source Mapping
| Profile ID | Industry Role | Base Failure Signature Source |
| :--- | :--- | :--- |
| **EU_BMW_001** | Automotive Tier-1 (DE) | Reconstructed from **BMW Group** 2024 Sustainability/Supply Chain reports. |
| **EU_BASF_002** | Chemical Precursor (DE) | Modeled on **BASF** specialty chemical fragility profiles (Geopolitical risk metrics). |
| **ASIA_CHIP_003** | Semiconductor Fab (TW/KR) | Based on **TSMC/Samsung** publicly available risk variance and concentration data. |
| **SUP-RWD-07** | Blue Chip Aerospace (FR) | Modeled on **Airbus** Tier-2 metallic alloy dependency chains. |
| **SUP-RWD-04** | Distressed Tier-3 | Generic "Default Signature" based on Z-Score analysis of 2024 insolvencies in the German Mittelstand. |

## 🔬 2. Resilience Scenario Configuration
The 10,000-iteration Monte Carlo engine utilizes the following "Historical Shock" vectors:
*   **Vector A (Asia-Pacific Concentration)**: Mimics 15% probability of a 30-day regional logistics halt (Sea/Air).
*   **Vector B (EU Energy/Regulatory)**: 5% probability of sudden LkSG-related supplier suspension or energy-driven production caps.
*   **Vector C (Global Contagion)**: 5% probability of simultaneous Tier-1 and Tier-2 failure paths (Bullwhip Effect).

## ⚖️ 3. Verification Protocol
All "Resilience Alpha" metrics represent the **Net Present Value (NPV)** delta between the Classical Optimal allocation and the R-QAOA Resilient allocation during these shock scenarios.

---
**Disclaimer**: These profiles are for benchmarking and risk-modeling purposes. They are mathematical abstractions of industry sectors, not direct real-time data from the named entities.
