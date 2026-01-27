from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from ..domain.rqaoa_core import RQAOAOptimizer

app = FastAPI(title="CascadeGuard R-QAOA Service")
optimizer = RQAOAOptimizer()

class NodeInput(BaseModel):
    id: str
    type: str # 'GEN_WIND', 'GEN_SOLAR', 'GEN_GAS', 'LOAD', 'STORAGE'
    capacity_mw: float
    weather_dependency: float # 0.0 - 1.0

class OptimizationRequest(BaseModel):
    nodes: List[NodeInput]
    total_demand_mw: float
    weather_factor: float # 0.0 - 1.0
    is_stress_event: bool

@app.get("/api/health")
async def health():
    return {"status": "healthy", "engine": "R-QAOA v2.1"}

@app.post("/api/optimize")
async def optimize(request: OptimizationRequest):
    # Convert Pydantic to Dict for Core
    nodes_dict = [n.dict() for n in request.nodes]
    
    result = optimizer.optimize(
        nodes=nodes_dict,
        demand=request.total_demand_mw,
        weather_factor=request.weather_factor,
        is_stress=request.is_stress_event
    )
    
    return {
        "status": "success",
        "result": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
