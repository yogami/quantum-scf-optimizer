import { useState } from 'react'
import CSVUpload from './components/CSVUpload'
import MetricsDashboard from './components/MetricsDashboard'
import NetworkGraph from './components/NetworkGraph'

interface OptimizationResult {
    job_id: string
    classical: {
        allocations: Array<{
            supplier_id: string
            allocated_amount: number
            expected_return: number
            risk_contribution: number
        }>
        total_yield: number
        total_risk: number
        solve_time_ms: number
        solver_logs: string
    }
    quantum: {
        allocations: Array<{
            supplier_id: string
            allocated_amount: number
            expected_return: number
            risk_contribution: number
        }>
        total_yield: number
        total_risk: number
        solve_time_ms: number
        solver_logs: string
    }
    comparison: {
        yield_improvement_pct: number
        risk_reduction_pct: number
        speedup_factor: number
    }
}

function App() {
    const [result, setResult] = useState<OptimizationResult | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleOptimize = async (csvContent: string) => {
        setLoading(true)
        setError(null)

        try {
            const response = await fetch('/api/optimize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    csv_content: csvContent,
                    budget: 1000000,
                    risk_tolerance: 50,
                    esg_min: 60
                })
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || 'Optimization failed')
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Unknown error')
        } finally {
            setLoading(false)
        }
    }

    const handleDownloadPDF = async () => {
        if (!result) return

        try {
            const response = await fetch(`/api/report/${result.job_id}`)
            const blob = await response.blob()
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `scf_report_${result.job_id}.pdf`
            document.body.appendChild(a)
            a.click()
            a.remove()
            window.URL.revokeObjectURL(url)
        } catch (err) {
            setError('Failed to download PDF')
        }
    }

    return (
        <div className="min-h-screen p-8">
            {/* Header */}
            <header className="text-center mb-12">
                <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-quantum-400 to-quantum-200 bg-clip-text text-transparent">
                    Quantum SCF Risk Optimizer
                </h1>
                <p className="text-slate-400 text-lg">
                    Hybrid quantum/classical supply chain finance optimization
                </p>
                <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-quantum-900/50 border border-quantum-500/30">
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
                    <span className="text-sm text-quantum-300">Berlin AI Labs</span>
                </div>
            </header>

            <main className="max-w-7xl mx-auto">
                {/* Upload Section */}
                {!result && (
                    <CSVUpload onUpload={handleOptimize} loading={loading} />
                )}

                {/* Error Display */}
                {error && (
                    <div className="quantum-card p-6 mb-8 border-red-500/50">
                        <p className="text-red-400">{error}</p>
                        <button
                            onClick={() => { setError(null); setResult(null); }}
                            className="mt-4 btn-quantum"
                        >
                            Try Again
                        </button>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className="quantum-card p-12 text-center">
                        <div className="quantum-spinner mx-auto mb-4"></div>
                        <p className="text-quantum-300">Running quantum optimization...</p>
                        <p className="text-slate-500 text-sm mt-2">
                            Comparing classical PuLP vs D-Wave hybrid solver
                        </p>
                    </div>
                )}

                {/* Results */}
                {result && !loading && (
                    <div className="space-y-8">
                        {/* Metrics Dashboard */}
                        <MetricsDashboard result={result} />

                        {/* Network Graph */}
                        <NetworkGraph
                            classicalAllocations={result.classical.allocations}
                            quantumAllocations={result.quantum.allocations}
                        />

                        {/* Action Buttons */}
                        <div className="flex justify-center gap-4">
                            <button onClick={handleDownloadPDF} className="btn-quantum">
                                📄 Download PDF Report
                            </button>
                            <button
                                onClick={() => setResult(null)}
                                className="btn-quantum bg-gradient-to-r from-slate-600 to-slate-700"
                            >
                                🔄 New Optimization
                            </button>
                        </div>

                        {/* Solver Logs */}
                        <div className="quantum-card p-6">
                            <h3 className="text-lg font-semibold mb-4 text-quantum-300">Quantum Solver Logs</h3>
                            <pre className="bg-slate-800/50 p-4 rounded-lg text-sm text-slate-300 overflow-x-auto">
                                {result.quantum.solver_logs}
                            </pre>
                        </div>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="text-center mt-16 text-slate-500 text-sm">
                <p>© 2026 Berlin AI Labs · Quantum SCF Risk Optimizer v1.0</p>
                <p className="mt-1">Powered by D-Wave Leap & Qiskit</p>
            </footer>
        </div>
    )
}

export default App
