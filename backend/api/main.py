"""FastAPI Main Application - Quantum SCF Risk Optimizer API."""
import sys
import os
from pathlib import Path

# Identify project root and backend directory
root_path = Path(__file__).parent.parent.parent.resolve()
backend_path = root_path / "backend"

# Add to sys.path for absolute imports
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

try:
    import backend.api.routes.optimize as optimize_routes
except ImportError:
    optimize_routes = None

app = FastAPI(
    title="Quantum SCF Risk Optimizer",
    description="Hybrid quantum/classical supply chain finance risk optimization API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# 1. Health Check (Defined FIRST to avoid any shadowing/import delays)
@app.get("/api/health")
async def health_check():
    """Health check endpoint for Railway deployment verification."""
    return {"status": "healthy", "service": "quantum-scf-optimizer"}

# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. API Routes (Lazy Loading)
def include_routes():
    try:
        # Use absolute project import
        import backend.api.routes.optimize as optimize_routes
        app.include_router(optimize_routes.router, prefix="/api")
    except ImportError:
        try:
            import api.routes.optimize as optimize_routes
            app.include_router(optimize_routes.router, prefix="/api")
        except ImportError as e:
            print(f"CRITICAL: Could not load optimize routes: {e}")

include_routes()

# 4. Frontend Static Files (Catch-all root mount)
frontend_path = root_path / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    @app.get("/")
    async def root_fallback():
        return {
            "message": "Quantum SCF Backend Live. No frontend build found.",
            "searched_path": str(frontend_path),
            "cwd": os.getcwd(),
            "root_contents": os.listdir("/") if os.name != 'nt' else []
        }


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
