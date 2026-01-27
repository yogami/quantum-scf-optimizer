import os
import sys
import requests
import json

def run_o3_scf_audit():
    # API Key - Hardcoded for this environment as seen in previous logs
    api_key = "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"
    
    # Read the Scf dossier
    dossier_path = "docs/SCF_AUDIT_DOSSIER.md"
    if not os.path.exists(dossier_path):
        print(f"❌ Error: {dossier_path} not found.")
        sys.exit(1)
        
    with open(dossier_path, "r") as f:
        dossier_content = f.read()

    print("🏛️ Convening O3 Reasoning Panel for Brutally Honest SCF Audit...")
    
    system_prompt = "You are a ruthless auditor specializing in Supply Chain Finance (SCF) and Network Science. You do not care about marketing hype. Your job is to destroy the 'Blue Ocean' narrative if it lacks mathematical or industrial substance. You are auditing CascadeGuard SCF."
    
    user_prompt = f"""
    Please perform a BRUTALLY HONEST audit of the provided dossier. 
    Evaluate:
    1. Problem Authenticity: Is 'Multi-Tier Contagion' a real pain point for banks, or is this a solution searching for a problem?
    2. Mathematical Rigor: Is the use of Spectral Radius (lambda_1) for contagion identification legitimate, or is it trivial compared to standard degree-based hub analysis?
    3. 'Blue Ocean' Reality: Does this actually provide a differentiator that Commerzbank or LBBW would pay €25K for, or is this just 'GraphViz for Tier-1s'?
    4. Honesty Check: Does the pivot from Quantum to Classical show maturity, or is the engine still essentially a placeholder?

    DOSSIER:
    {dossier_content}
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://berlinailabs.de",
                "X-Title": "Brutally Honest SCF Audit",
            },
            data=json.dumps({
                "model": "openai/o3-mini", # Using the latest O3 mini for sharp reasoning
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            })
        )
        
        response.raise_for_status()
        result_json = response.json()
        audit_result = result_json['choices'][0]['message']['content']
        
        # Save the result
        output_path = "docs/O3_SCF_AUDIT_RESULTS.md"
        with open(output_path, "w") as f:
            f.write("# O3 BRUTALLY HONEST SCF AUDIT RESULTS\n\n")
            f.write(audit_result)
            
        print(f"\n✅ Audit Complete. Results saved to {output_path}")
        print("\n--- O3 AUDIT SUMMARY ---")
        print(audit_result[:1000] + "...")
        
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Details: {e.response.text}")

if __name__ == "__main__":
    run_o3_scf_audit()
