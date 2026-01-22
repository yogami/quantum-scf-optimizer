"""SCF Optimization Use Case - Application layer orchestrator."""
import uuid
import pandas as pd
from io import StringIO
from typing import Optional

from domain.entities import SCFTier, OptimizationResult
from infrastructure.quantum import ClassicalSolver, DWaveSolver, PlanQKSolver
from infrastructure.pdf import PDFReportGenerator


class OptimizeSCFUseCase:
    """Orchestrates the SCF optimization workflow."""
    
    def __init__(self):
        self.classical_solver = ClassicalSolver()
        self.dwave_solver = DWaveSolver()
        self.planqk_solver = PlanQKSolver()
        self.pdf_generator = PDFReportGenerator()
    
    def parse_csv(self, csv_content: str) -> list[SCFTier]:
        """Parse CSV content into SCFTier entities."""
        df = pd.read_csv(StringIO(csv_content))
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()
        
        required = ['supplier_id', 'tier', 'risk_score', 'yield_pct', 'volatility', 'esg_score', 'trade_volume']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        tiers = []
        for _, row in df.iterrows():
            tiers.append(SCFTier(
                supplier_id=str(row['supplier_id']),
                tier=int(row['tier']),
                risk_score=float(row['risk_score']),
                yield_pct=float(row['yield_pct']),
                volatility=float(row['volatility']),
                esg_score=float(row['esg_score']),
                trade_volume=float(row['trade_volume'])
            ))
        
        return tiers
    
    def run_optimization(
        self,
        tiers: list[SCFTier],
        budget: float = 1_000_000,
        risk_tolerance: float = 50,
        esg_min: float = 60,
        quantum_provider: str = "planqk"
    ) -> dict:
        """Run both classical and quantum optimization."""
        classical_result = self.classical_solver.optimize(
            tiers, budget, risk_tolerance, esg_min
        )
        
        # Select quantum solver
        if quantum_provider.lower() == "dwave":
            quantum_solver = self.dwave_solver
        else:
            quantum_solver = self.planqk_solver

        quantum_result = quantum_solver.optimize(
            tiers, budget, risk_tolerance, esg_min
        )
        
        job_id = str(uuid.uuid4())[:8]
        
        # Calculate improvements
        yield_improvement = 0
        if classical_result.total_yield > 0:
            yield_improvement = (
                (quantum_result.total_yield - classical_result.total_yield)
                / classical_result.total_yield * 100
            )
        
        risk_improvement = 0
        if classical_result.total_risk > 0:
            risk_improvement = (
                (classical_result.total_risk - quantum_result.total_risk)
                / classical_result.total_risk * 100
            )
        
        return {
            "job_id": job_id,
            "classical": {
                "allocations": [
                    {
                        "supplier_id": a.supplier_id,
                        "allocated_amount": a.allocated_amount,
                        "expected_return": a.expected_return,
                        "risk_contribution": a.risk_contribution
                    }
                    for a in classical_result.allocations
                ],
                "total_yield": classical_result.total_yield,
                "total_risk": classical_result.total_risk,
                "solve_time_ms": classical_result.solve_time_ms,
                "solver_logs": classical_result.solver_logs
            },
            "quantum": {
                "allocations": [
                    {
                        "supplier_id": a.supplier_id,
                        "allocated_amount": a.allocated_amount,
                        "expected_return": a.expected_return,
                        "risk_contribution": a.risk_contribution
                    }
                    for a in quantum_result.allocations
                ],
                "total_yield": quantum_result.total_yield,
                "total_risk": quantum_result.total_risk,
                "solve_time_ms": quantum_result.solve_time_ms,
                "solver_logs": quantum_result.solver_logs
            },
            "comparison": {
                "yield_improvement_pct": yield_improvement,
                "risk_reduction_pct": risk_improvement,
                "speedup_factor": (
                    classical_result.solve_time_ms / quantum_result.solve_time_ms
                    if quantum_result.solve_time_ms > 0 else 1
                )
            }
        }
    
    def generate_report(
        self,
        classical_result: OptimizationResult,
        quantum_result: OptimizationResult,
        job_id: str
    ) -> bytes:
        """Generate PDF report."""
        return self.pdf_generator.generate(classical_result, quantum_result, job_id)
