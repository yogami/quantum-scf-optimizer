import numpy as np
import time
from domain.rqaoa_core import RQAOAOptimizer

def run_10k_node_benchmark():
    optimizer = RQAOAOptimizer()
    num_nodes = 10000
    
    print("🚀 Starting 10,000 Node Network Stress Test")
    print("Network Type: Global Interconnected Graph")
    
    # Generate 10k nodes
    nodes = []
    for i in range(num_nodes):
        is_renewable = i % 2 == 0
        nodes.append({
            "id": f"NODE_{i}",
            "type": "RENEWABLE" if is_renewable else "DISPATCHABLE",
            "capacity_mw": np.random.uniform(10, 500),
            "weather_dependency": 0.8 if is_renewable else 0.0
        })
    
    demand = 2000000 # 2 GW
    
    start_time = time.time()
    result = optimizer.optimize(
        nodes=nodes,
        demand=demand,
        weather_factor=0.05, # Dunkelflaute scenario
        is_stress=True
    )
    end_time = time.time()
    
    duration = (end_time - start_time) * 1000 # ms
    
    print("\n🏆 Scale Test Results")
    print(f"Total Nodes Processed: {num_nodes:,}")
    print(f"Execution Time:        {duration:.2f} ms")
    print(f"Classical Cost:        € {result['classical_cost']:,.0f}")
    print(f"Resilient Cost:        € {result['resilient_cost']:,.0f}")
    print(f"Cascade Alpha:         € {result['alpha']:,.0f}")
    print(f"System Status:         {result['status']}")
    
    # Write reproduction log
    with open("docs/REPRODUCTION_SCALE_10K.log", "w") as f:
        f.write(f"CASCADEGUARD SCALE AUDIT\n")
        f.write(f"Nodes: 10,000\n")
        f.write(f"Latency: {duration:.2f}ms\n")
        f.write(f"Alpha: €{result['alpha']:,.0f}\n")

if __name__ == "__main__":
    run_10k_node_benchmark()
