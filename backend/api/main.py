"""FastAPI Main Application - Quantum SCF Risk Optimizer API."""
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from api.routes import optimize

app = FastAPI(
    title="Quantum SCF Risk Optimizer",
    description="Hybrid quantum/classical supply chain finance risk optimization API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS for external dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. API Routes (Router)
app.include_router(optimize.router, prefix="/api")

# 2. Health Check (Crucial to be before root mount)
@app.get("/api/health")
async def health_check():
    """Health check endpoint for Railway deployment verification."""
    return {"status": "healthy", "service": "quantum-scf-optimizer"}

# 3. Frontend Static Files (Catch-all root mount)
# Note: Ensure frontend/dist exists (run npm build)
frontend_path = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    @app.get("/")
    async def root_fallback():
        return {"message": "Quantum SCF Backend Live. Frontend build not detected. Please run 'npm run build' in /frontend."}


def custom_openapi():
    """Custom OpenAPI schema for Agent-Ready discovery."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Quantum SCF Risk Optimizer API",
        version="1.0.0",
        description="Berlin AI Labs - Hybrid quantum/classical SCF optimization",
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-agent-ready"] = True
    openapi_schema["info"]["x-capability"] = "quantum-scf-optimization"
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
