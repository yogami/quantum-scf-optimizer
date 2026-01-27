# CascadeGuard V9.0: Industrial Clarity Refinement & Live Data Integration

## 1. Overview
This update transitions CascadeGuard from a static "Mission Control" visual markup to a functioning **Live Audit Instrument**. The UI has been refined for maximum legibility ("Industrial Clarity"), and the frontend has been wired to the backend Spectral Engine to display real-time calculated risk metrics.

## 2. Key Changes

### A. UI/UX "Industrial Clarity"
- **Typography Reset**: Switched labels to `Inter` (System Sans-Serif) for clarity, reserved `JetBrains Mono` strictly for numerical data (18.42, €90.0M).
- **Layout Alignment**: Corrected the central schematic grid position (`pt-24`) to prevent label cutoff.
- **Visual Rhythm**: Increased header sizes (`text-2xl`) and metric impact (`text-7xl`) for executive readability.

### B. Live Data Pipeline
- **Backend**: Implemented `/api/live-scenario` in `api.py` (and synchronized to `server.py`).
  - constructes the real **BMW -> Bosch -> TSMC** dependency graph.
  - Runs the `SupplyChainContagionAuditor`.
  - Returns calculated `spectral_radius` (25.00) and `expected_loss` (€90.0M).
- **Frontend**: Updated `App.tsx` to:
  - Fetch from `:11885/api/live-scenario`.
  - Display a "CONNECTING..." state.
  - Render live values dynamically.

### C. Validation
- **Visual**: Verified via browser screenshots (Live Badge present, correct fonts).
- **Functional**: Verified via Playwright E2E tests (8/8 PASSED).

## 3. Deployment Status
- **Local**: Running on `:5173` (Frontend) and `:11885` (Backend).
- **Production**: Ready for Railway deployment.

## 4. Next Steps
- Deploy to Railway.
- Connect "REFRESH AUDIT" to PDF Report Generation.
