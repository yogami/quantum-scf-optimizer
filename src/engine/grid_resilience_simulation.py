import sys
import os

# Jenkins-Hardy Path Management
# Add current directory and src to sys.path
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(base_dir, '../../')))
sys.path.append(os.path.abspath(os.path.join(base_dir, '../')))

from src.application.simulation_service import SimulationService
from src.infrastructure.entsoe_adapter import EntsoeAdapter

def main():
    print("🚀 INITIALIZING BERLIN QUANTUM GRID SIMULATION (PRODUCTION v2)")
    print("-" * 60)
    
    # Dependency Injection
    adapter = EntsoeAdapter()
    service = SimulationService(adapter)
    
    result = service.run_dunkelflaute_simulation()
    
    print("\n🏆 SIMULATION COMPLETE")
    print(f"Classical Cost:   € {result['total_classical_cost_eur']:,.0f}")
    print(f"Resilient Cost:   € {result['total_resilient_cost_eur']:,.0f}")
    print(f"🛡️ VALIDATED ALPHA: € {result['resilience_alpha_eur']:,.0f}")
    
    return result

if __name__ == "__main__":
    main()
