import os
import sys
import requests
import json

def run_neutral_o3_audit():
    # API Key
    api_key = "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"
    
    # Read the V9.0 Industrial Dossier
    dossier_path = "docs/SCF_AUDIT_DOSSIER.md"
    if not os.path.exists(dossier_path):
        print(f"❌ Error: {dossier_path} not found.")
        sys.exit(1)
        
    with open(dossier_path, "r") as f:
        dossier_content = f.read()

    print("🕵️ Running Neutral Venture Capital Audit (O3-Mini)...")
    
    # NEUTRAL SYSTEM PROMPT
    system_prompt = "You are a senior technical auditor and investment analyst at a top-tier venture capital firm. You are evaluating a Supply Chain Finance (SCF) optimization startup called CascadeGuard. Your task is to provide an objective, data-driven assessment of its technical feasibility, commercial potential, and sustainable competitive advantage (moat)."
    
    # NEUTRAL USER PROMPT
    user_prompt = f"""
    Please evaluate the following project dossier for CascadeGuard SCF V9.0.
    
    Specifically, analyze:
    1. Technical Maturity: Does the use of LOBPCG and Stochastic Validation represent a robust industrial implementation?
    2. Commercial Moat: In a landscape where large incumbents (Moody's, SAP) are moving towards multi-tier mapping, what is the 'Blue Ocean' differentiator here?
    3. Investment Verdict: Based on the provided performance metrics and scientific methodology, is this a viable standalone venture or a component set for acquisition?

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
                "X-Title": "Neutral VC Audit",
            },
            data=json.dumps({
                "model": "openai/o3-mini",
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
        output_path = "docs/NEUTRAL_O3_AUDIT_RESULTS.md"
        with open(output_path, "w") as f:
            f.write("# NEUTRAL VENTURE CAPITAL AUDIT RESULTS (O3-Mini)\n\n")
            f.write(audit_result)
            
        print(f"\n✅ Audit Complete. Results saved to {output_path}")
        print("\n--- NEUTRAL O3 AUDIT SUMMARY ---")
        print(audit_result[:1000] + "...")
        
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")

if __name__ == "__main__":
    run_neutral_o3_audit()
