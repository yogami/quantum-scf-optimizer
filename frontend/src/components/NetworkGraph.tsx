import Plot from 'react-plotly.js'

interface Allocation {
    supplier_id: string
    allocated_amount: number
    expected_return: number
    risk_contribution: number
}

interface NetworkGraphProps {
    classicalAllocations: Allocation[]
    quantumAllocations: Allocation[]
}

export default function NetworkGraph({ classicalAllocations, quantumAllocations }: NetworkGraphProps) {
    // Create bar chart data
    const allSuppliers = [...new Set([
        ...classicalAllocations.map(a => a.supplier_id),
        ...quantumAllocations.map(a => a.supplier_id)
    ])].sort()

    const classicalData = allSuppliers.map(sup => {
        const alloc = classicalAllocations.find(a => a.supplier_id === sup)
        return alloc ? alloc.allocated_amount : 0
    })

    const quantumData = allSuppliers.map(sup => {
        const alloc = quantumAllocations.find(a => a.supplier_id === sup)
        return alloc ? alloc.allocated_amount : 0
    })

    return (
        <div className="quantum-card p-8">
            <h2 className="text-2xl font-semibold mb-6 text-quantum-300">
                Allocation Comparison
            </h2>

            <Plot
                data={[
                    {
                        x: allSuppliers,
                        y: classicalData,
                        type: 'bar',
                        name: 'Classical',
                        marker: { color: '#64748b' }
                    },
                    {
                        x: allSuppliers,
                        y: quantumData,
                        type: 'bar',
                        name: 'Quantum',
                        marker: {
                            color: '#0ea5e9',
                            line: { color: '#38bdf8', width: 1 }
                        }
                    }
                ]}
                layout={{
                    barmode: 'group',
                    paper_bgcolor: 'transparent',
                    plot_bgcolor: 'transparent',
                    font: { color: '#94a3b8' },
                    xaxis: {
                        title: { text: 'Supplier' },
                        gridcolor: 'rgba(148, 163, 184, 0.1)'
                    },
                    yaxis: {
                        title: { text: 'Allocation (€)' },
                        gridcolor: 'rgba(148, 163, 184, 0.1)',
                        tickformat: ',.0f'
                    },
                    legend: {
                        orientation: 'h',
                        y: 1.1,
                        x: 0.5,
                        xanchor: 'center'
                    },
                    margin: { t: 40, r: 20, b: 60, l: 80 }
                }}
                config={{
                    displayModeBar: false,
                    responsive: true
                }}
                style={{ width: '100%', height: '400px' }}
            />

            {/* Risk vs Return scatter */}
            <div className="mt-8">
                <h3 className="text-lg font-medium text-slate-300 mb-4">Risk vs Return Analysis</h3>
                <Plot
                    data={[
                        {
                            x: classicalAllocations.map(a => a.risk_contribution),
                            y: classicalAllocations.map(a => a.expected_return),
                            text: classicalAllocations.map(a => a.supplier_id),
                            type: 'scatter',
                            mode: 'text+markers' as any,
                            name: 'Classical',
                            textposition: 'top center',
                            marker: {
                                size: 12,
                                color: '#64748b',
                                opacity: 0.7
                            }
                        },
                        {
                            x: quantumAllocations.map(a => a.risk_contribution),
                            y: quantumAllocations.map(a => a.expected_return),
                            text: quantumAllocations.map(a => a.supplier_id),
                            type: 'scatter',
                            mode: 'text+markers' as any,
                            name: 'Quantum',
                            textposition: 'top center',
                            marker: {
                                size: 14,
                                color: '#0ea5e9',
                                line: { color: '#38bdf8', width: 2 }
                            }
                        }
                    ]}
                    layout={{
                        paper_bgcolor: 'transparent',
                        plot_bgcolor: 'transparent',
                        font: { color: '#94a3b8' },
                        xaxis: {
                            title: { text: 'Risk Contribution' },
                            gridcolor: 'rgba(148, 163, 184, 0.1)'
                        },
                        yaxis: {
                            title: { text: 'Expected Return (€)' },
                            gridcolor: 'rgba(148, 163, 184, 0.1)',
                            tickformat: ',.0f'
                        },
                        legend: {
                            orientation: 'h',
                            y: 1.15,
                            x: 0.5,
                            xanchor: 'center'
                        },
                        margin: { t: 40, r: 20, b: 60, l: 80 }
                    }}
                    config={{
                        displayModeBar: false,
                        responsive: true
                    }}
                    style={{ width: '100%', height: '350px' }}
                />
            </div>
        </div>
    )
}
