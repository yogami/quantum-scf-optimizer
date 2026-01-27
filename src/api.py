from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import networkx as nx
import os
from domain.topological_core import SupplyChainContagionAuditor

app = FastAPI(title="CascadeGuard SCF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auditor = SupplyChainContagionAuditor()

class Supplier(BaseModel):
    id: str
    tier: int
    revenue: Optional[float] = 1000.0

class TradeDependency(BaseModel):
    source: str
    target: str

class AuditRequest(BaseModel):
    suppliers: List[Supplier]
    exposure: float
    dependencies: Optional[List[TradeDependency]] = None

@app.get("/health")
def read_root():
    return {"status": "CascadeGuard Engine Online", "version": "9.0-Industrial"}

@app.post("/api/audit")
async def run_audit(request: AuditRequest):
    try:
        suppliers_data = [s.dict() for s in request.suppliers]
        dependencies = [(d.source, d.target) for d in request.dependencies] if request.dependencies else None
        
        result = auditor.audit_contagion_risk(
            suppliers=suppliers_data,
            total_exposure=request.exposure,
            risk_threshold=0.5,
            dependencies=dependencies
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/demo-topology")
async def get_demo_topology():
    G = nx.disjoint_union(nx.complete_graph(20), nx.complete_graph(20))
    G.add_edge(10, 30)
    
    nodes = []
    for n in G.nodes():
        tier = 1 if n < 20 else (2 if n < 40 else 3)
        nodes.append({
            "id": f"Supplier_{n}",
            "tier": tier,
            "isCritical": n in [10, 30]
        })
    
    links = [{"source": f"Supplier_{u}", "target": f"Supplier_{v}", "value": 1} for u, v in G.edges()]
    
    return {"nodes": nodes, "links": links}

@app.get("/api/live-scenario")
async def get_live_scenario():
    """
    Returns the REAL calculated risk profile for the Automotive Supply Chain scenario.
    """
    try:
        # Define the Real-World Scenario (Figures in Millions EUR)
        suppliers = [
            {"id": "BMW Group", "tier": 0, "revenue": 50000.0}, # €50B
            {"id": "Bosch", "tier": 1, "revenue": 15000.0},     # €15B
            {"id": "ZF", "tier": 1, "revenue": 12000.0},        # €12B
            {"id": "NXP", "tier": 2, "revenue": 8000.0},        # €8B
            {"id": "Infineon", "tier": 2, "revenue": 7500.0},   # €7.5B
            {"id": "TSMC", "tier": 3, "revenue": 60000.0}       # €60B
        ]
        
        # Define Dependencies (The Real Graph)
        dependencies = [
            ("BMW Group", "Bosch"),
            ("BMW Group", "ZF"),
            ("Bosch", "NXP"),
            ("Bosch", "Infineon"),
            ("ZF", "NXP"),
            ("NXP", "TSMC"),     # Critical Single Point
            ("Infineon", "TSMC") # Critical Single Point
        ]

        # CALCULATE REAL RISK
        # Total Exposure = €1.2B (1200M)
        result = auditor.audit_contagion_risk(
            suppliers=suppliers,
            total_exposure=1200.0, 
            risk_threshold=0.5,
            dependencies=dependencies
        )
        
        # Format for Frontend (match App.tsx expectations)
        response = {
            "spectral_radius": result.get("systemic_vulnerability_score", 0) * 100, # Scale for display (0.18 -> 18.0)
            "max_eigenvalue": result.get("stochastic_confirmation", 0),
            "risk_score": result.get("systemic_vulnerability_score", 0),
            "potential_loss": {
                "amount": result.get("expected_contagion_loss_eur", 0) * 1000000, # Convert to absolute units if needed, or keep as M
                "currency": "EUR"
            },
            "topology": {
                "nodes": [{"id": s["id"], "tier": s["tier"], "isCritical": s["id"] == "TSMC"} for s in suppliers],
                "links": [{"source": s, "target": t} for s, t in dependencies]
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve the Stunning Frontend
static_dir = os.path.join(os.getcwd(), "dashboard/dist")
if os.path.exists(static_dir):
    app.mount("/dashboard", StaticFiles(directory=static_dir, html=True), name="dashboard")
    
    @app.get("/")
    @app.get("/{path:path}")
    async def serve_dashboard(path: Optional[str] = None):
        # Serve index.html for any unknown route (SPA support)
        return FileResponse(os.path.join(static_dir, "index.html"))
