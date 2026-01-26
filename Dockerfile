# Multi-stage build to ensure both Node and Python environments are pristine
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install
COPY frontend/ ./frontend/
RUN cd frontend && npm run build

# Production image
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for reportlab/pillow if needed
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Copy the built frontend from the previous stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure the port is bound to 0.0.0.0
CMD uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT:-8080}
