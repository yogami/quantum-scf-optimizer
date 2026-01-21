"""Solver Port - Interface for optimization solvers."""
from abc import ABC, abstractmethod
from domain.entities import SCFTier, OptimizationResult


class SolverPort(ABC):
    """Abstract interface for SCF optimization solvers."""
    
    @abstractmethod
    def optimize(
        self,
        tiers: list[SCFTier],
        budget: float,
        risk_tolerance: float,
        esg_min: float
    ) -> OptimizationResult:
        """
        Optimize allocation across supply chain tiers.
        
        Args:
            tiers: List of SCF tiers to allocate across
            budget: Total budget to allocate
            risk_tolerance: Maximum acceptable risk (0-100)
            esg_min: Minimum ESG score threshold
            
        Returns:
            OptimizationResult with allocations and metrics
        """
        pass
