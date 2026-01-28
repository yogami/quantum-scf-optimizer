import os
import requests

def run_grok_unbiased():
    """
    Executes the 'Hostile Audit' Prompt against Grok/Perplexity via OpenRouter.
    """
    
    # Configuration
    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    # MODEL = "x-ai/grok-beta" # 404
    MODEL = "perplexity/sonar-reasoning-pro" # Deep Reasoning Fallback
    
    if not OPENROUTER_KEY:
        print("ERROR: OPENROUTER_API_KEY not set.")
        return

    # Load Prompt
    try:
        with open("GROK_UNBIASED_AUDIT_PROMPT.md", "r") as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print("ERROR: GROK_UNBIASED_AUDIT_PROMPT.md not found.")
        return

    print(f">>> SENDING UNBIASED PROMPT TO {MODEL} <<<")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://cascadeguard.ai", 
        "X-Title": "CascadeGuard Grok Audit"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt_content}
        ],
        "temperature": 0.4 # Slightly creative to allow 'Brutality' and 'Thinking'
    }
    
    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json()['choices'][0]['message']['content']
        
        print("\n=== VERDICT ===\n")
        print(result)
        
        # Save to file
        with open("GROK_VERDICT_FINAL.md", "w") as f:
            f.write(result)
            
    except Exception as e:
        print(f"API ERROR: {e}")
        try:
            print(resp.text)
        except: pass

if __name__ == "__main__":
    run_grok_unbiased()
