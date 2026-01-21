"""SCF Tier Entity - Core domain model for supply chain tiers."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SCFTier:
    """Represents a single tier/supplier in the supply chain."""
    supplier_id: str
    tier: int
    risk_score: float  # 0-100, higher = riskier
    yield_pct: float   # Expected yield percentage
    volatility: float  # Historical volatility
    esg_score: float   # ESG compliance score 0-100
    trade_volume: float  # Trade volume in EUR


@dataclass
class Allocation:
    """Represents an allocation decision for a tier."""
    supplier_id: str
    allocated_amount: float
    expected_return: float
    risk_contribution: float


@dataclass
class OptimizationResult:
    """Result from running optimization."""
    allocations: list[Allocation]
    total_yield: float
    total_risk: float
    solver_type: str  # "classical" or "quantum"
    solve_time_ms: float
    solver_logs: Optional[str] = None
