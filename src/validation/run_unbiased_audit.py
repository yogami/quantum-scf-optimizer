import os
import sys
import requests
import json

def run_unbiased_o3_audit():
    # Use the OpenRouter key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found.")
        sys.exit(1)

    # Read the unbiased dossier
    dossier_path = "docs/UNBIASED_AUDIT_DOSSIER.md"
    if not os.path.exists(dossier_path):
        print(f"❌ Error: {dossier_path} not found.")
        sys.exit(1)
        
    with open(dossier_path, "r") as f:
        dossier_content = f.read()

    print("🏛️ Convening Nobel-Level PhD Panel for Blind Scientific Audit...")
    print("Instruction: Identify every flaw, bias, and 'magic number' in our work.")
    
    # The Nobel Panel Prompt
    system_prompt = "You are a panel of Nobel-prize winning PhD professors in Quantum Physics, Network Science, and Mathematical Finance. You are reviewing a submission for the journal Nature. You are notoriously skeptical. You must find the flaws in the methodology, detect any 'lab manipulation' or bias, and evaluate the authenticity of the results across different domains."
    
    user_prompt = f"""
    Please provide a ruthless, unbiased audit of the following submission. We are particularly concerned about 'magic numbers' in our simulation and the validity of mapping Energy physics to Finance. 

    SUBMISSION:
    {dossier_content}
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://berlinailabs.de",
                "X-Title": "Unbiased Nobel Audit",
            },
            data=json.dumps({
                "model": "openai/o3", # Peak 2026 reasoning
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
        output_path = "docs/UNBIASED_NOBEL_AUDIT_RESULTS.md"
        with open(output_path, "w") as f:
            f.write("# NOBEL-LEVEL UNBIASED SCIENTIFIC AUDIT RESULTS\n\n")
            f.write(audit_result)
            
        print(f"\n✅ Audit Complete. Results saved to {output_path}")
        print("\n--- NOBEL AUDIT SUMMARY ---")
        print(audit_result[:1000] + "...")
        
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Details: {e.response.text}")

if __name__ == "__main__":
    run_unbiased_o3_audit()
