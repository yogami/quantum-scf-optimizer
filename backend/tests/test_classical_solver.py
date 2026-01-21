"""Unit Tests for Classical Solver."""
import pytest
from domain.entities import SCFTier
from infrastructure.quantum.classical_solver import ClassicalSolver


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
    """Create classical solver instance."""
    return ClassicalSolver()


class TestClassicalSolver:
    """Tests for ClassicalSolver."""
    
    def test_optimize_returns_valid_result(self, solver, sample_tiers):
        """GIVEN sample tiers, WHEN optimize runs, THEN returns valid result."""
        result = solver.optimize(
            tiers=sample_tiers,
            budget=1_000_000,
            risk_tolerance=50,
            esg_min=60
        )
        
        assert result is not None
        assert result.solver_type == "classical"
        assert result.solve_time_ms > 0
        assert len(result.allocations) > 0
    
    def test_optimize_respects_budget(self, solver, sample_tiers):
        """GIVEN budget, WHEN optimized, THEN total allocation <= budget."""
        budget = 1_000_000
        result = solver.optimize(sample_tiers, budget, 50, 60)
        
        total_allocated = sum(a.allocated_amount for a in result.allocations)
        assert total_allocated <= budget * 1.01  # 1% tolerance
    
    def test_optimize_completes_under_5_seconds(self, solver, sample_tiers):
        """GIVEN 10 tiers, WHEN optimize runs, THEN completes in <5000ms."""
        result = solver.optimize(sample_tiers, 1_000_000, 50, 60)
        assert result.solve_time_ms < 5000
    
    def test_optimize_produces_positive_yield(self, solver, sample_tiers):
        """GIVEN sample tiers, WHEN optimized, THEN total yield > 0."""
        result = solver.optimize(sample_tiers, 1_000_000, 50, 60)
        assert result.total_yield > 0
    
    def test_optimize_single_tier(self, solver):
        """GIVEN single tier, WHEN optimized, THEN allocates 100%."""
        single_tier = [SCFTier("SINGLE", 1, 10.0, 10.0, 5.0, 90.0, 1000000)]
        result = solver.optimize(single_tier, 1_000_000, 50, 60)
        
        assert len(result.allocations) == 1
        assert result.allocations[0].allocated_amount == pytest.approx(1_000_000, rel=0.01)
