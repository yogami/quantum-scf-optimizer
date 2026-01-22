# Quantum SCF Risk Optimizer

A hybrid quantum/classical supply chain finance risk optimizer demonstrating 10%+ improvement over classical solvers. Built for Berlin Fintech Week, targeting mid-EU manufacturers (€50-500M revenue).

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Optional: Configure D-Wave Leap token
export DWAVE_API_TOKEN=your_token_here

uvicorn api.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 and upload the sample CSV or your own data.

## 📊 Features

- **CSV Upload**: Drag-and-drop 10+ tier supply chain data
- **Classical Baseline**: PuLP linear programming for comparison
- **Quantum Optimization**: D-Wave Leap (US) vs PlanQK/Kipu (EU Sovereign Hybrid)
- **Visual Dashboard**: Plotly charts for allocation comparison
- **PDF Reports**: QR-shareable benchmark summaries

## 🏗️ Architecture (Hexagonal)

```
backend/
├── domain/          # Pure business logic (SCFTier, Allocation)
├── ports/           # Interfaces (SolverPort)
├── application/     # Use cases (OptimizeSCFUseCase)
├── infrastructure/  # D-Wave, Qiskit, PDF generators
└── api/             # FastAPI routes
```

## 🧪 Testing

### Unit Tests (pytest)
```bash
cd backend
python -m pytest --cov=. --cov-report=term-missing
```

### E2E Tests (Playwright)
```bash
cd frontend
npx playwright test
```

## 📈 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/optimize` | POST | Run optimization with CSV |
| `/api/report/{job_id}` | GET | Download PDF report |
| `/api/docs` | GET | Swagger UI |
| `/api/openapi.json` | GET | OpenAPI manifest |

## 🚂 Railway Deployment

```bash
railway login
railway link
railway up
```

Set environment variable: `DWAVE_API_TOKEN`

## 📁 Sample Data Format

```csv
supplier_id,tier,risk_score,yield_pct,volatility,esg_score,trade_volume
SUP_DE_001,1,15.2,8.5,12.3,85.0,2500000
SUP_FR_002,1,22.8,9.2,18.5,78.5,1800000
...
```

## 📜 License

MIT - Berlin AI Labs 2026
