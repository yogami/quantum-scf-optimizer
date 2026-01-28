import os
import json
import time
import requests
import concurrent.futures
from typing import Dict, List, Optional

class ConsensusEngine:
    """
    The 'Phoenix' Audit Engine.
    Consolidates the multi-role validation logic from the 'Idea Factory' into CascadeGuard.
    """
    
    AUDITORS = {
        "Regulator": {
            "model": "x-ai/grok-2-1212", # Primary
            "fallback": "anthropic/claude-3.5-sonnet",
            "role": "You are a cynical EU Regulator. Audit this supply chain finance model. Focus on MaRisk, BAIT, and Anti-Money Laundering (AML) compliance. Verdict: GREEN (Pass) or RED (Fail).",
            "deployment": "remote"
        },
        "CFO": {
            "model": "openai/gpt-4o",
            "role": "You are a Conservative CFO. Audit this risk model. Focus on Capital Efficiency, Default Rates, and 'Black Swan' resilience. Verdict: GREEN (Pass) or RED (Fail).",
            "deployment": "remote"
        },
        "Researcher": {
            "model": "perplexity/llama-3-sonar-large-32k-online", 
            "fallback": "openai/gpt-4o",
            "role": "You are a Market Researcher. Analysis the COMPETITIVE LANDSCAPE. Is this a 'Red Ocean' (Crowded/Commoditized) or 'Blue Ocean'? If crowded/low-margin, VERDICT: RED (Fail). If viable/defensible, VERDICT: GREEN (Pass).",
            "deployment": "remote"
        }
    }

    def __init__(self, openrouter_key: str):
        self.api_key = openrouter_key
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is required.")

    def _call_openrouter(self, model: str, system_prompt: str, user_prompt: str, persona: str, fallback_model: Optional[str] = None) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://berlin-ai.studio", 
            "X-Title": "CascadeGuard Consensus Engine"
        }
        
        models_to_try = [model]
        if fallback_model:
            models_to_try.append(fallback_model)
            
        for m in models_to_try:
            payload = {
                "model": m,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7
            }
            try:
                # print(f"  > [{persona}] Calling {m}...")
                resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                if 'error' in data:
                     print(f"API Error ({m}): {data['error']}")
                     continue 
                content = data['choices'][0]['message']['content']
                return {"persona": persona, "content": content, "model_used": m}
            except Exception as e:
                print(f"Request Failed ({m}): {e}")
                continue

        return {"persona": persona, "content": "AUDIT_FAILURE: All models failed.", "model_used": "None"}

    def run_audit(self, context_data: str) -> Dict:
        """
        Runs the multi-agent audit loop on the provided context (e.g. a Risk Report or Topology).
        """
        print(f"\n--- Starting Consensus Audit ---")
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_persona = {}
            for persona, config in self.AUDITORS.items():
                future = executor.submit(
                    self._call_openrouter, 
                    config["model"], 
                    config["role"], 
                    f"Audit this System State:\n{context_data}", 
                    persona,
                    config.get("fallback")
                )
                future_to_persona[future] = persona
            
            for future in concurrent.futures.as_completed(future_to_persona):
                data = future.result()
                results[data["persona"]] = data
                print(f"  > [{data['persona']}] Verdict Received (via {data['model_used']}).")

        # Synthesize Verdict
        green_votes = sum(1 for r in results.values() if "GREEN" in r["content"])
        consensus = "PASSED" if green_votes == len(self.AUDITORS) else "FAILED"
        
        return {
            "consensus": consensus,
            "details": results
        }
