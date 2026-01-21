"""Unit Tests for Quantum Solver (D-Wave with fallback)."""
import pytest
import os
from domain.entities import SCFTier
from infrastructure.quantum.dwave_solver import DWaveSolver


@pytest.fixture
def sample_tiers():
    """Create sample SCF tiers for testing."""
    return [
        SCFTier("SUP_001", 1, 15.0, 8.5, 12.0, 85.0, 2500000),
        SCFTier("SUP_002", 1, 25.0, 10.0, 18.0, 75.0, 1800000),
        SCFTier("SUP_003", 2, 35.0, 12.0, 25.0, 70.0, 950000),
        SCFTier("SUP_004", 3, 45.0, 15.0, 32.0, 65.0, 450000),
    ]


@pytest.fixture
def solver():
    """Create D-Wave solver instance (will use fallback without token)."""
    return DWaveSolver()


class TestDWaveSolver:
    """Tests for DWaveSolver with automatic fallback."""
    
    def test_optimize_returns_valid_result_with_fallback(self, solver, sample_tiers):
        """GIVEN no D-Wave token, WHEN optimize runs, THEN uses fallback."""
        result = solver.optimize(
            tiers=sample_tiers,
            budget=1_000_000,
            risk_tolerance=50,
            esg_min=60
        )
        
        assert result is not None
        assert "quantum" in result.solver_type
        assert result.solve_time_ms > 0
        assert len(result.allocations) > 0
    
    def test_fallback_logs_correctly(self, solver, sample_tiers):
        """GIVEN no token, WHEN optimized, THEN logs fallback info."""
        result = solver.optimize(sample_tiers, 1_000_000, 50, 60)
        
        assert result.solver_logs is not None
        assert "fallback" in result.solver_logs.lower() or "qiskit" in result.solver_logs.lower()
    
    def test_qubo_build_succeeds(self, solver, sample_tiers):
        """GIVEN sample tiers, WHEN QUBO built, THEN valid matrix."""
        Q = solver._build_qubo(sample_tiers, 1_000_000, 50, 60)
        
        assert isinstance(Q, dict)
        assert len(Q) > 0
    
    def test_optimize_produces_allocations(self, solver, sample_tiers):
        """GIVEN sample tiers, WHEN optimized, THEN produces allocations."""
        result = solver.optimize(sample_tiers, 1_000_000, 50, 60)
        
        assert len(result.allocations) > 0
        for alloc in result.allocations:
            assert alloc.allocated_amount >= 0
    
    def test_solver_logs_contain_info(self, solver, sample_tiers):
        """GIVEN optimization run, WHEN complete, THEN logs available."""
        result = solver.optimize(sample_tiers, 1_000_000, 50, 60)
        assert result.solver_logs is not None
        assert len(result.solver_logs) > 0
