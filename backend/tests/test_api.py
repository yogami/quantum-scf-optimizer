"""Integration Tests for FastAPI API endpoints."""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_csv():
    """Sample CSV content for testing."""
    return """supplier_id,tier,risk_score,yield_pct,volatility,esg_score,trade_volume
SUP_001,1,15.0,8.5,12.0,85.0,2500000
SUP_002,1,25.0,10.0,18.0,75.0,1800000
SUP_003,2,35.0,12.0,25.0,70.0,950000
SUP_004,3,45.0,15.0,32.0,65.0,450000"""


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_returns_200(self, client):
        """GIVEN API is running, WHEN /api/health called, THEN returns 200."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestOptimizeEndpoint:
    """Tests for optimization endpoint."""
    
    def test_optimize_with_valid_csv(self, client, sample_csv):
        """GIVEN valid CSV, WHEN /api/optimize called, THEN returns results."""
        response = client.post("/api/optimize", json={
            "csv_content": sample_csv,
            "budget": 1_000_000,
            "risk_tolerance": 50,
            "esg_min": 60
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert "classical" in data
        assert "quantum" in data
        assert "comparison" in data
    
    def test_optimize_returns_comparison_metrics(self, client, sample_csv):
        """GIVEN optimization run, WHEN complete, THEN comparison metrics exist."""
        response = client.post("/api/optimize", json={"csv_content": sample_csv})
        
        data = response.json()
        assert "yield_improvement_pct" in data["comparison"]
        assert "risk_reduction_pct" in data["comparison"]
        assert "speedup_factor" in data["comparison"]
    
    def test_optimize_classical_under_5s(self, client, sample_csv):
        """GIVEN CSV, WHEN classical runs, THEN completes <5000ms."""
        response = client.post("/api/optimize", json={"csv_content": sample_csv})
        
        data = response.json()
        assert data["classical"]["solve_time_ms"] < 5000
    
    def test_optimize_invalid_csv(self, client):
        """GIVEN invalid CSV, WHEN /api/optimize called, THEN returns 400."""
        response = client.post("/api/optimize", json={
            "csv_content": "invalid,csv,content"
        })
        assert response.status_code == 400
    
    def test_optimize_missing_columns(self, client):
        """GIVEN CSV missing columns, WHEN optimized, THEN returns 400."""
        response = client.post("/api/optimize", json={
            "csv_content": "supplier_id,wrong_column\nSUP_001,value"
        })
        assert response.status_code == 400


class TestReportEndpoint:
    """Tests for PDF report endpoint."""
    
    def test_report_for_completed_job(self, client, sample_csv):
        """GIVEN completed job, WHEN /api/report/{job_id} called, THEN returns PDF."""
        # First run optimization
        opt_response = client.post("/api/optimize", json={"csv_content": sample_csv})
        job_id = opt_response.json()["job_id"]
        
        # Then get report
        report_response = client.get(f"/api/report/{job_id}")
        
        assert report_response.status_code == 200
        assert report_response.headers["content-type"] == "application/pdf"
    
    def test_report_not_found(self, client):
        """GIVEN invalid job ID, WHEN /api/report called, THEN returns 404."""
        response = client.get("/api/report/invalid_id")
        assert response.status_code == 404


class TestOpenAPIEndpoint:
    """Tests for OpenAPI discovery endpoint."""
    
    def test_openapi_available(self, client):
        """GIVEN Agent-Ready API, WHEN /api/openapi.json called, THEN returns schema."""
        response = client.get("/api/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert data["info"]["x-agent-ready"] is True
