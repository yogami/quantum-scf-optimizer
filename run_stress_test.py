import os
import requests
import json
import sys

# Constants
API_KEY = os.getenv("OPENROUTER_API_KEY")
PROMPT_FILE = "/Users/user1000/.gemini/antigravity/brain/3546fa56-fd0a-4fcd-9a9a-c83dcb95b043/gpt5_2_stress_test_prompt.md"
MODEL = "openai/gpt-5" # User requested real GPT-5

if not API_KEY:
    print("Error: OPENROUTER_API_KEY environment variable not set.")
    sys.exit(1)

def run_audit():
    try:
        with open(PROMPT_FILE, "r") as f:
            prompt_content = f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found at {PROMPT_FILE}")
        sys.exit(1)

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are GPT-5.2, the world's most advanced MaRisk and Supply Chain Risk Auditor. You are cynical, mathematical, and technically precise."},
            {"role": "user", "content": prompt_content}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"--- Sending Request to OpenRouter ({MODEL}) ---")
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        print("\n--- GPT-5.2 AUDIT VERDICT ---\n")
        print(content)
        
        # Save raw result
        with open("gpt5_2_raw_verdict.txt", "w") as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error during API call: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")

if __name__ == "__main__":
    run_audit()
