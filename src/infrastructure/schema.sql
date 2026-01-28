-- CascadeGuard Schema (PostgreSQL)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Graphs Table (Stores the Topology)
CREATE TABLE IF NOT EXISTS scf_graphs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    nodes_json JSONB NOT NULL, -- Full 'nodes' array
    edges_json JSONB NOT NULL, -- Full 'edges' array
    meta_json JSONB, -- 'meta' object
    resilience_score FLOAT DEFAULT 0.0, -- Last known score
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Audit Runs Table (Stores the Evidence)
CREATE TABLE IF NOT EXISTS scf_audit_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    graph_id UUID REFERENCES scf_graphs(id),
    status TEXT NOT NULL, -- PASSED, FAILED
    resilience_score FLOAT NOT NULL,
    rwa_saving_estimate FLOAT DEFAULT 0.0, -- The "Money"
    details_json JSONB, -- Full audit log
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for Speed
CREATE INDEX IF NOT EXISTS idx_graphs_created_at ON scf_graphs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_runs_graph_id ON scf_audit_runs(graph_id);
