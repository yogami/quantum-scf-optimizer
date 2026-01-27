import os
import sys
from openai import OpenAI

def run_scientific_audit():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment.")
        print("Please run: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    
    # Read the dossier
    dossier_path = "docs/SCIENTIFIC_AUDIT_DOSSIER.md"
    if not os.path.exists(dossier_path):
        print(f"❌ Error: {dossier_path} not found.")
        sys.exit(1)
        
    with open(dossier_path, "r") as f:
        dossier_content = f.read()

    print("🧠 Sending CascadeGuard Dossier to OpenAI o1 for Deep Scientific Audit...")
    
    prompt = f"""
    I am the Lead Scientist for a Deep Tech startup. I am submitting this Technical Dossier for a ruthless scientific audit. 
    I need you to find the 'Hidden Triviality.' Is there a classical Graph Laplacian or Spectral Clustering method that achieves these same results for 10% of the complexity? 
    If not, help me harden the Recursive QAOA argument for a patent filing.

    DOSSIER:
    {dossier_content}
    """

    try:
        # Using o1-preview for the deepest reasoning
        response = client.chat.completions.create(
            model="o1-preview",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        audit_result = response.choices[0].message.content
        
        # Save the result
        output_path = "docs/O1_SCIENTIFIC_AUDIT_RESULTS.md"
        with open(output_path, "w") as f:
            f.write("# OpenAI o1 Scientific Audit Results\n\n")
            f.write(audit_result)
            
        print(f"\n✅ Audit Complete. Results saved to {output_path}")
        print("\n--- AUDIT SUMMARY ---")
        print(audit_result[:500] + "...")
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        if "o1-preview" in str(e):
            print("Retrying with gpt-4o...")
            # Fallback to 4o if o1-preview is not available
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a professional scientific auditor and quantum physicist."},
                    {"role": "user", "content": prompt}
                ]
            )
            audit_result = response.choices[0].message.content
            with open("docs/GPT4O_SCIENTIFIC_AUDIT_RESULTS.md", "w") as f:
                f.write(audit_result)
            print(f"✅ Audit Complete with GPT-4o. Results saved to docs/GPT4O_SCIENTIFIC_AUDIT_RESULTS.md")

if __name__ == "__main__":
    run_scientific_audit()
