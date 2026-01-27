import requests
from typing import List, Dict
import os

class CascadeGuardAdapter:
    """Infrastructure Adapter to call the external R-QAOA Microservice."""
    
    def __init__(self, endpoint_url: str = None):
        self.endpoint_url = endpoint_url or os.getenv(
            "CASCADE_GUARD_URL", 
            "https://cascade-guard-optimizer-production.up.railway.app/api/optimize"
        )

    def get_resilient_dispatch(self, nodes: List[Dict], demand: float, weather_factor: float, is_stress: bool):
        payload = {
            "nodes": nodes,
            "total_demand_mw": demand,
            "weather_factor": weather_factor,
            "is_stress_event": is_stress
        }
        
        try:
            response = requests.post(self.endpoint_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["result"]
        except Exception as e:
            print(f"⚠️ CascadeGuard Microservice Failure: {e}")
            # Fallback to local safety logic if needed, or raise
            raise
