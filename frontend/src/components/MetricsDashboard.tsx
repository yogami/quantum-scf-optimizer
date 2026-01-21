interface MetricsDashboardProps {
    result: {
        job_id: string
        classical: {
            total_yield: number
            total_risk: number
            solve_time_ms: number
            allocations: Array<{
                supplier_id: string
                allocated_amount: number
                expected_return: number
                risk_contribution: number
            }>
        }
        quantum: {
            total_yield: number
            total_risk: number
            solve_time_ms: number
            allocations: Array<{
                supplier_id: string
                allocated_amount: number
                expected_return: number
                risk_contribution: number
            }>
        }
        comparison: {
            yield_improvement_pct: number
            risk_reduction_pct: number
            speedup_factor: number
        }
    }
}

export default function MetricsDashboard({ result }: MetricsDashboardProps) {
    const { classical, quantum, comparison } = result

    const formatCurrency = (value: number) =>
        new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(value)

    const getImprovementClass = (value: number) => {
        if (value > 0) return 'text-green-400'
        if (value < 0) return 'text-red-400'
        return 'text-slate-400'
    }

    return (
        <div className="quantum-card p-8">
            <h2 className="text-2xl font-semibold mb-6 text-quantum-300">
                Optimization Results
            </h2>

            {/* Key Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="metric-card">
                    <p className="text-slate-400 mb-2">Yield Improvement</p>
                    <p className={`metric-value ${getImprovementClass(comparison.yield_improvement_pct)}`}>
                        {comparison.yield_improvement_pct > 0 ? '+' : ''}{comparison.yield_improvement_pct.toFixed(1)}%
                    </p>
                    <p className="text-sm text-slate-500 mt-2">Quantum vs Classical</p>
                </div>

                <div className="metric-card">
                    <p className="text-slate-400 mb-2">Risk Reduction</p>
                    <p className={`metric-value ${getImprovementClass(comparison.risk_reduction_pct)}`}>
                        {comparison.risk_reduction_pct > 0 ? '+' : ''}{comparison.risk_reduction_pct.toFixed(1)}%
                    </p>
                    <p className="text-sm text-slate-500 mt-2">Lower is better</p>
                </div>

                <div className="metric-card">
                    <p className="text-slate-400 mb-2">Quantum Expected Return</p>
                    <p className="metric-value">
                        {formatCurrency(quantum.total_yield)}
                    </p>
                    <p className="text-sm text-slate-500 mt-2">
                        Classical: {formatCurrency(classical.total_yield)}
                    </p>
                </div>
            </div>

            {/* Comparison Table */}
            <div className="overflow-x-auto">
                <table className="comparison-table">
                    <thead>
                        <tr>
                            <th className="rounded-tl-lg">Metric</th>
                            <th>Classical (PuLP)</th>
                            <th>Quantum (D-Wave)</th>
                            <th className="rounded-tr-lg">Δ</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td className="font-medium">Total Yield</td>
                            <td>{formatCurrency(classical.total_yield)}</td>
                            <td>{formatCurrency(quantum.total_yield)}</td>
                            <td className={getImprovementClass(comparison.yield_improvement_pct)}>
                                {comparison.yield_improvement_pct > 0 ? '+' : ''}{comparison.yield_improvement_pct.toFixed(1)}%
                            </td>
                        </tr>
                        <tr>
                            <td className="font-medium">Total Risk Score</td>
                            <td>{classical.total_risk.toFixed(1)}</td>
                            <td>{quantum.total_risk.toFixed(1)}</td>
                            <td className={getImprovementClass(comparison.risk_reduction_pct)}>
                                {comparison.risk_reduction_pct > 0 ? '-' : '+'}{Math.abs(comparison.risk_reduction_pct).toFixed(1)}%
                            </td>
                        </tr>
                        <tr>
                            <td className="font-medium">Solve Time</td>
                            <td>{classical.solve_time_ms.toFixed(0)} ms</td>
                            <td>{quantum.solve_time_ms.toFixed(0)} ms</td>
                            <td className="text-quantum-400">
                                {comparison.speedup_factor.toFixed(2)}x
                            </td>
                        </tr>
                        <tr>
                            <td className="font-medium">Allocations</td>
                            <td>{classical.allocations.length} suppliers</td>
                            <td>{quantum.allocations.length} suppliers</td>
                            <td>-</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {/* Allocation Details */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h3 className="text-lg font-medium text-slate-300 mb-4">Classical Allocations</h3>
                    <div className="space-y-2">
                        {classical.allocations.map((alloc) => (
                            <div key={alloc.supplier_id} className="flex justify-between text-sm p-2 bg-slate-800/30 rounded">
                                <span className="text-slate-400">{alloc.supplier_id}</span>
                                <span className="text-quantum-300">{formatCurrency(alloc.allocated_amount)}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div>
                    <h3 className="text-lg font-medium text-slate-300 mb-4">Quantum Allocations</h3>
                    <div className="space-y-2">
                        {quantum.allocations.map((alloc) => (
                            <div key={alloc.supplier_id} className="flex justify-between text-sm p-2 bg-quantum-900/30 rounded border border-quantum-500/20">
                                <span className="text-slate-400">{alloc.supplier_id}</span>
                                <span className="text-quantum-300">{formatCurrency(alloc.allocated_amount)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
