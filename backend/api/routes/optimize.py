"""Optimize Routes - API endpoints for SCF optimization."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional

from application import OptimizeSCFUseCase


router = APIRouter()
use_case = OptimizeSCFUseCase()

# In-memory storage for job results (POC - use Supabase for prod)
job_store: dict = {}


class OptimizeRequest(BaseModel):
    """Request body for optimization with inline CSV."""
    csv_content: str
    budget: float = 1_000_000
    risk_tolerance: float = 50
    esg_min: float = 60


class OptimizeResponse(BaseModel):
    """Response from optimization run."""
    job_id: str
    classical: dict
    quantum: dict
    comparison: dict


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_scf(request: OptimizeRequest):
    """
    Run classical and quantum optimization on SCF tiers.
    
    Accepts CSV content with columns:
    supplier_id, tier, risk_score, yield_pct, volatility, esg_score, trade_volume
    """
    try:
        tiers = use_case.parse_csv(request.csv_content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    
    if len(tiers) == 0:
        raise HTTPException(status_code=400, detail="CSV must contain at least one tier")
    
    result = use_case.run_optimization(
        tiers,
        budget=request.budget,
        risk_tolerance=request.risk_tolerance,
        esg_min=request.esg_min
    )
    
    # Store for PDF generation
    job_store[result["job_id"]] = result
    
    return result


@router.post("/optimize/upload", response_model=OptimizeResponse)
async def optimize_scf_upload(
    file: UploadFile = File(...),
    budget: float = 1_000_000,
    risk_tolerance: float = 50,
    esg_min: float = 60
):
    """
    Upload CSV file and run optimization.
    
    CSV must have columns:
    supplier_id, tier, risk_score, yield_pct, volatility, esg_score, trade_volume
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = content.decode('utf-8')
    
    try:
        tiers = use_case.parse_csv(csv_content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    
    if len(tiers) == 0:
        raise HTTPException(status_code=400, detail="CSV must contain at least one tier")
    
    result = use_case.run_optimization(
        tiers,
        budget=budget,
        risk_tolerance=risk_tolerance,
        esg_min=esg_min
    )
    
    job_store[result["job_id"]] = result
    
    return result


@router.get("/report/{job_id}")
async def get_report(job_id: str):
    """Download PDF report for a completed job."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_store[job_id]
    
    # Reconstruct OptimizationResult objects for PDF
    from domain.entities import Allocation, OptimizationResult
    
    classical_allocs = [
        Allocation(**a) for a in job["classical"]["allocations"]
    ]
    quantum_allocs = [
        Allocation(**a) for a in job["quantum"]["allocations"]
    ]
    
    classical_result = OptimizationResult(
        allocations=classical_allocs,
        total_yield=job["classical"]["total_yield"],
        total_risk=job["classical"]["total_risk"],
        solver_type="classical",
        solve_time_ms=job["classical"]["solve_time_ms"],
        solver_logs=job["classical"]["solver_logs"]
    )
    
    quantum_result = OptimizationResult(
        allocations=quantum_allocs,
        total_yield=job["quantum"]["total_yield"],
        total_risk=job["quantum"]["total_risk"],
        solver_type="quantum",
        solve_time_ms=job["quantum"]["solve_time_ms"],
        solver_logs=job["quantum"]["solver_logs"]
    )
    
    pdf_bytes = use_case.generate_report(classical_result, quantum_result, job_id)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=scf_report_{job_id}.pdf"}
    )


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Get stored job results."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_store[job_id]
