import os
import json
from typing import List, Optional, Dict, Any
from databases import Database
from pydantic import BaseModel
import asyncio
from contextlib import asynccontextmanager

# Load from ENV or Default to Local/Mock if missing
DATABASE_URL = os.getenv("DATABASE_URL") 
# Example: postgresql://user:pass@db.supabase.co:5432/postgres

class DatabaseService:
    def __init__(self):
        self.database = None
        if DATABASE_URL:
            self.database = Database(DATABASE_URL)
            
    async def connect(self):
        if self.database:
            await self.database.connect()
            print(">>> DB CONNECTED")
            
    async def disconnect(self):
        if self.database:
            await self.database.disconnect()
            print(">>> DB DISCONNECTED")
            
    async def save_graph(self, name: str, description: str, nodes: List[Dict], edges: List[List], meta: Dict) -> str:
        if not self.database:
            return "MOCK_DB_ID_123"
            
        try:
            query = """
                INSERT INTO scf_graphs (name, description, nodes_json, edges_json, meta_json)
                VALUES (:name, :description, :nodes, :edges, :meta)
                RETURNING id
            """
            values = {
                "name": name,
                "description": description,
                "nodes": json.dumps(nodes),
                "edges": json.dumps(edges),
                "meta": json.dumps(meta)
            }
            graph_id = await self.database.execute(query=query, values=values)
            return str(graph_id)
        except Exception as e:
            print(f"DB ERROR [save_graph]: {e}")
            return None

    async def log_audit(self, graph_id: str, status: str, score: float, rwa_est: float, details: Dict):
        if not self.database: # Fallback Log
            print(f"[MOCK DB] Audit Logged: {status} Score={score} RWA={rwa_est}")
            return
            
        try:
            # First update the graph score
            update_query = "UPDATE scf_graphs SET resilience_score = :score WHERE id = :id"
            await self.database.execute(update_query, {"score": score, "id": graph_id})
            
            # Insert Run
            query = """
                INSERT INTO scf_audit_runs (graph_id, status, resilience_score, rwa_saving_estimate, details_json)
                VALUES (:graph_id, :status, :score, :rwa, :details)
            """
            values = {
                "graph_id": graph_id,
                "status": status,
                "score": score,
                "rwa": rwa_est,
                "details": json.dumps(details)
            }
            await self.database.execute(query=query, values=values)
        except Exception as e:
            print(f"DB ERROR [log_audit]: {e}")

# Singleton
db_service = DatabaseService()
