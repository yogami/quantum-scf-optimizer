"""FastAPI Main Application - Quantum SCF Risk Optimizer API."""
import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse

# Identify project root and backend directory
# Handle both local and Docker environments
current_file = Path(__file__).resolve()
# If main.py is in backend/api/main.py
root_path = current_file.parent.parent.parent
backend_path = root_path / "backend"

# Add to sys.path for absolute imports
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

app = FastAPI(
    title="Quantum SCF Risk Optimizer",
    description="Hybrid quantum/classical supply chain finance risk optimization API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# 1. Health Check (Immediate Priority)
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "quantum-scf-optimizer"}

# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. API Routes (Lazy Loading to prevent boot delays)
try:
    import backend.api.routes.optimize as optimize_routes
    app.include_router(optimize_routes.router, prefix="/api")
except ImportError as e:
    print(f"Warning: Could not load optimize routes: {e}")

# 4. Frontend Integration
frontend_dist = root_path / "frontend" / "dist"

# Debug endpoint to verify file structure in production
@app.get("/api/debug/paths")
async def debug_paths():
    return {
        "root": str(root_path),
        "frontend_dist": str(frontend_dist),
        "frontend_exists": frontend_dist.exists(),
        "frontend_contents": os.listdir(str(frontend_dist)) if frontend_dist.exists() else [],
        "cwd": os.getcwd()
    }

@app.get("/")
async def serve_index():
    index_file = frontend_dist / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "message": "Quantum SCF Backend Live. Frontend build not found.",
        "path_searched": str(index_file),
        "current_dir": os.getcwd()
    }

# Mount static files for assets (JS/CSS)
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    # Also mount root dist in case of other static files
    app.mount("/", StaticFiles(directory=str(frontend_dist)), name="root_static")

def custom_openapi():
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
