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
async def get_live_scenario(scenario: str = "baseline"):
    """
    Returns the REAL calculated risk profile for various Supply Chain scenarios.
    """
    try:
        # 1. DEFINE SCENARIOS
        if scenario == "red-sea":
            # Red Sea Blockade: High lead times for Asian Semi-conductors
            suppliers = [
                {"id": "BMW Group", "tier": 0, "revenue": 50000.0},
                {"id": "Bosch", "tier": 1, "revenue": 15000.0},
                {"id": "TSMC", "tier": 2, "revenue": 60000.0},
                {"id": "GlobalFoundries", "tier": 2, "revenue": 8000.0}
            ]
            dependencies = [
                ("BMW Group", "Bosch"),
                ("Bosch", "TSMC"),
                ("Bosch", "GlobalFoundries")
            ]
            total_exposure = 2400.0 # Doubled risk exposure
            threshold = 0.3 # Lower threshold for panic
        
        elif scenario == "energy-crisis":
            # Energy Crisis: EU Manufacturing under stress
            suppliers = [
                {"id": "Volkswagen", "tier": 0, "revenue": 65000.0},
                {"id": "Continental", "tier": 1, "revenue": 12000.0},
                {"id": "BASF", "tier": 2, "revenue": 18000.0},
                {"id": "ThyssenKrupp", "tier": 2, "revenue": 9000.0}
            ]
            dependencies = [
                ("Volkswagen", "Continental"),
                ("Continental", "BASF"),
                ("Continental", "ThyssenKrupp")
            ]
            total_exposure = 1800.0
            threshold = 0.4
            
        elif scenario == "port-strike":
            # Global Logistics Strike: Logistics hubs become single points of failure
            suppliers = [
                {"id": "Mercedes-Benz", "tier": 0, "revenue": 45000.0},
                {"id": "ZF Group", "tier": 1, "revenue": 14000.0},
                {"id": "Maersk Logistics", "tier": 2, "revenue": 25000.0}, # The critical node
                {"id": "Kuhne+Nagel", "tier": 2, "revenue": 12000.0}
            ]
            dependencies = [
                ("Mercedes-Benz", "ZF Group"),
                ("ZF Group", "Maersk Logistics"),
                ("ZF Group", "Kuhne+Nagel")
            ]
            total_exposure = 3200.0
            threshold = 0.2
            
        else: # baseline
            suppliers = [
                {"id": "BMW Group", "tier": 0, "revenue": 50000.0},
                {"id": "Bosch", "tier": 1, "revenue": 15000.0},
                {"id": "ZF", "tier": 1, "revenue": 12000.0},
                {"id": "NXP", "tier": 2, "revenue": 8000.0},
                {"id": "Infineon", "tier": 2, "revenue": 7500.0},
                {"id": "TSMC", "tier": 3, "revenue": 60000.0}
            ]
            dependencies = [
                ("BMW Group", "Bosch"),
                ("BMW Group", "ZF"),
                ("Bosch", "NXP"),
                ("Bosch", "Infineon"),
                ("ZF", "NXP"),
                ("NXP", "TSMC"),
                ("Infineon", "TSMC")
            ]
            total_exposure = 1200.0
            threshold = 0.5

        # 2. CALCULATE REAL RISK
        result = auditor.audit_contagion_risk(
            suppliers=suppliers,
            total_exposure=total_exposure, 
            risk_threshold=threshold,
            dependencies=dependencies
        )
        
        # 3. FORMAT FOR FRONTEND
        response = {
            "scenario": scenario,
            "spectral_radius": result.get("systemic_vulnerability_score", 0) * 100,
            "max_eigenvalue": result.get("stochastic_confirmation", 0),
            "risk_score": result.get("systemic_vulnerability_score", 0),
            "potential_loss": {
                "amount": result.get("expected_contagion_loss_eur", 0) * 1000000,
                "currency": "EUR"
            },
            "topology": {
                "nodes": [{"id": s["id"], "tier": s["tier"], "isCritical": s["id"] in ["TSMC", "Maersk Logistics", "BASF"]} for s in suppliers],
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
