import numpy as np
import pandas as pd
from domain.grid_entities import GridNode

class SimulationService:
    def __init__(self, data_fetcher, optimizer_adapter=None):
        self.data_fetcher = data_fetcher
        self.optimizer_adapter = optimizer_adapter

    def run_dunkelflaute_simulation(self):
        real_nodes_data = self.data_fetcher.get_topology_nodes()
        nodes = []
        for n in real_nodes_data:
            cost = 5 if 'WIND' in n['type'] or 'SOLAR' in n['type'] else 120
            if n['type'] == 'STORAGE': cost = 60
            dep = 1.0 if 'WIND' in n['type'] or 'SOLAR' in n['type'] else 0.0
            
            node = GridNode(node_id=n['id'], node_type=n['type'], capacity_mw=n['mw'], cost_per_mwh=cost, weather_dependency=dep)
            nodes.append(node)
        
        # Microservice-compatible node list
        nodes_input = [
            {"id": n.node_id, "type": n.node_type, "capacity_mw": n.capacity_mw, "weather_dependency": n.weather_dependency}
            for n in nodes
        ]
        
        total_demand = 80000
        days = 30
        results = []

        for day in range(1, days + 1):
            is_dunkelflaute = 10 <= day <= 13
            weather_factor = 0.05 if is_dunkelflaute else np.random.uniform(0.15, 0.40)
            weather_desc = "🌑 DUNKEL" if is_dunkelflaute else "☀ NORMAL"

            if self.optimizer_adapter:
                # DELEGATE TO MICROSERVICE
                opt = self.optimizer_adapter.get_resilient_dispatch(
                    nodes=nodes_input,
                    demand=total_demand,
                    weather_factor=weather_factor,
                    is_stress=is_dunkelflaute
                )
                classical_cost = opt["classical_cost"]
                resilient_cost = opt["resilient_cost"]
                gap = opt["gap_mw"]
            else:
                # Fallback to local logic (Legacy)
                total_gen_renew = sum([n.generate(weather_factor) for n in nodes if n.weather_dependency > 0])
                total_gen_dispatch = sum([n.generate(weather_factor) for n in nodes if n.weather_dependency == 0])
                gap = total_demand - (total_gen_renew + total_gen_dispatch)
                classical_cost = (total_gen_renew * 5) + (min(max(0, total_demand - total_gen_renew), total_gen_dispatch) * 120)
                if gap > 0: classical_cost += (gap * 3000)
                resilient_cost = classical_cost # Simplified fallback

            results.append({
                "day": day,
                "weather": weather_desc,
                "class_cost": classical_cost,
                "resil_cost": resilient_cost,
                "gap_mw": gap
            })

        df = pd.DataFrame(results)
        return {
            "status": "success",
            "total_classical_cost_eur": float(df['class_cost'].sum()),
            "total_resilient_cost_eur": float(df['resil_cost'].sum()),
            "resilience_alpha_eur": float(df['class_cost'].sum() - df['resil_cost'].sum()),
            "days_simulated": len(results),
            "engine": "CascadeGuard-Microservice" if self.optimizer_adapter else "Local-Fallback"
        }
