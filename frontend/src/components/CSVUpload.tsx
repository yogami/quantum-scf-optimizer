import { useCallback, useState } from 'react'

interface CSVUploadProps {
    onUpload: (csvContent: string) => void
    loading: boolean
}

export default function CSVUpload({ onUpload, loading }: CSVUploadProps) {
    const [isDragging, setIsDragging] = useState(false)
    const [fileName, setFileName] = useState<string | null>(null)

    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setIsDragging(true)
        } else if (e.type === 'dragleave') {
            setIsDragging(false)
        }
    }, [])

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault()
        e.stopPropagation()
        setIsDragging(false)

        const files = e.dataTransfer.files
        if (files?.[0]) {
            processFile(files[0])
        }
    }, [])

    const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files
        if (files?.[0]) {
            processFile(files[0])
        }
    }, [])

    const processFile = (file: File) => {
        if (!file.name.endsWith('.csv')) {
            alert('Please upload a CSV file')
            return
        }

        setFileName(file.name)
        const reader = new FileReader()
        reader.onload = (e) => {
            const content = e.target?.result as string
            onUpload(content)
        }
        reader.readAsText(file)
    }

    const loadSample = async () => {
        try {
            const response = await fetch('/sample_scf_10tier.csv')
            const content = await response.text()
            setFileName('sample_scf_10tier.csv')
            onUpload(content)
        } catch (err) {
            alert('Failed to load sample CSV')
        }
    }

    return (
        <div className="quantum-card p-8 mb-8">
            <h2 className="text-2xl font-semibold mb-6 text-quantum-300">
                Upload Supply Chain Data
            </h2>

            <div
                className={`dropzone p-12 text-center rounded-xl cursor-pointer ${isDragging ? 'active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById('fileInput')?.click()}
            >
                <input
                    id="fileInput"
                    type="file"
                    accept=".csv"
                    onChange={handleFileInput}
                    className="hidden"
                    disabled={loading}
                />

                <div className="text-5xl mb-4">📊</div>

                {fileName ? (
                    <p className="text-quantum-300 font-medium">{fileName}</p>
                ) : (
                    <>
                        <p className="text-lg text-slate-300 mb-2">
                            Drag & drop your CSV file here
                        </p>
                        <p className="text-slate-500">
                            or click to browse
                        </p>
                    </>
                )}
            </div>

            <div className="mt-6 flex items-center justify-center gap-4">
                <span className="text-slate-500">or</span>
                <button
                    onClick={loadSample}
                    disabled={loading}
                    className="text-quantum-400 hover:text-quantum-300 underline transition-colors"
                >
                    Load 10-tier sample data
                </button>
            </div>

            <div className="mt-8 p-4 bg-slate-800/30 rounded-lg">
                <p className="text-sm text-slate-400 mb-2">Required CSV columns:</p>
                <code className="text-xs text-quantum-400">
                    supplier_id, tier, risk_score, yield_pct, volatility, esg_score, trade_volume
                </code>
            </div>
        </div>
    )
}
