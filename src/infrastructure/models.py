from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from uuid import UUID

class NodeModel(BaseModel):
    id: str
    tier: str
    spend: float = 0.0
    meta: Optional[Dict[str, Any]] = {}

class EdgeModel(BaseModel):
    source: str
    target: str

class GraphCreate(BaseModel):
    name: str
    description: Optional[str] = None
    nodes: List[Dict[str, Any]]
    edges: List[List[str]]
    meta: Optional[Dict[str, Any]] = {}

class GraphRead(GraphCreate):
    id: str
    resilience_score: float
    created_at: Optional[datetime] = None

class AuditRunCreate(BaseModel):
    graph_id: str
    status: str
    resilience_score: float
    rwa_saving_estimate: float
    details: Dict[str, Any]
