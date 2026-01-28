import os

def generate_grok_prompt():
    """
    Generates a BRUTAL, UNBIASED Audit Prompt for Grok 4.1.
    Ingests all 'Pillar V' evidence assets.
    """
    
    # Read Assets
    def read_file(path):
        try:
            with open(path, 'r') as f: return f.read()
        except: return "MISSING FILE"

    evidence_pack = read_file("EVIDENCE_PACK.md") # The "What"
    memo = read_file("STRATEGIC_MEMO_SCALE_FREE_SOLUTIONS.md") # The "Why"
    generator_code = read_file("scripts/fetch_real_world_proxy.py") # The "How" (Sustainability Proof)
    walkthrough = read_file("walkthrough.md") # The "Result"
    
    prompt = f"""
**OBJECTIVE:**
Conduct a rigorous **due diligence audit** of the attached Engineering & Financial Proposal ("CascadeGuard v36.1").
The User is requesting a Pilot Budget. Your task is to evaluate the proposal critically. 
**Do not accept marketing claims at face value.** Validate the Mathematical and Financial logic.
If the evidence is insufficient, recommend rejection. If the evidence is scientifically sound, recommend approval.

**THE CLAIMS:**
1.  **Fragility Thesis**: "Scale-Free Networks (Hub & Spoke) inherently fail contagion tests (~36% Resilience)."
2.  **Failed Fix**: "Dual Sourcing (Triadic Closure) only adds +0.9% resilience on Scale-Free nets."
3.  **The Fix**: "Only a Mesh Topology (>15 Gateways) achieves >85% Resilience."
4.  **The Money**: "Banks will reduce Pillar 2 Capital Add-ons for this resilience, worth ~€1.5M/year."

**THE EVIDENCE:**

=== CODE (Generator for Baseline) ===
{generator_code}

=== FINDINGS (Evidence Pack) ===
{evidence_pack}

=== COMMERCIAL LOGIC (Strategic Memo) ===
{memo}

=== AUDIT LOG (Walkthrough) ===
{walkthrough}

**YOUR TASK:**
Analyze this pack.
1.  **Network Science Check**: Does `nx.barabasi_albert_graph(300, 2)` accurately model the fragility of supply chain hubs?
2.  **Logic Check**: Is the finding that "Dual Sourcing fails on Hubs" consistent with Percolation Theory (i.e., hubs remain single points of failure)?
3.  **Financial Check**: Is the argument regarding "MaRisk Pillar 2 Capital Add-ons" a plausible mechanism for value creation?
4.  **Verdict**: Based *only* on the provided evidence, is the Pilot justified?

**OUTPUT FORMAT:**
*   **VERDICT**: [GREENLIGHT / REDLIGHT]
*   **SCIENTIFIC VALIDITY**: [Low/Medium/High]
*   **CRITICAL ANALYSIS**: 3 key strengths or weaknesses.
*   **DECISION**: "Proceed to Pilot" or "Reject".
"""
    
    filename = "GROK_UNBIASED_AUDIT_PROMPT.md"
    with open(filename, 'w') as f:
        f.write(prompt)
    
    print(f"SUCCESS: Generated Hostile Audit Prompt at {filename}")
    print("User: Please copy content of GROK_UNBIASED_AUDIT_PROMPT.md into Grok 4.1")

if __name__ == "__main__":
    generate_grok_prompt()
