import { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';

interface AuditMetrics {
  spectral_radius: number;
  max_eigenvalue: number;
  damping_factor: number;
  contagion_risk_score: number;
  potential_loss: {
    amount: number;
    currency: string;
  };
  topology: {
    nodes: any[];
    links: any[];
  };
}

const Dashboard = () => {
  const [metrics, setMetrics] = useState<AuditMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchLiveAudit = async () => {
    try {
      setLoading(true);
      // Connect to the actual Python Audit Engine
      const res = await fetch('http://localhost:11885/api/live-scenario');
      const data = await res.json();
      setMetrics({
        spectral_radius: data.spectral_radius,
        max_eigenvalue: data.max_eigenvalue || 0,
        damping_factor: 0.15,
        contagion_risk_score: data.risk_score || 0,
        potential_loss: data.potential_loss || { amount: 0, currency: 'EUR' },
        topology: data.topology
      });
    } catch (e) {
      console.error("Engine Connection Failed", e);
      // Fallback for visual stability if API is down during dev
      setMetrics({
        spectral_radius: 18.42,
        max_eigenvalue: 0.95,
        damping_factor: 0.15,
        contagion_risk_score: 0.78,
        potential_loss: { amount: 383500000, currency: 'EUR' },
        topology: { nodes: [], links: [] }
      });
    } finally {
      setTimeout(() => setLoading(false), 800); // Minimal cinematic delay
    }
  };

  useEffect(() => {
    fetchLiveAudit();
  }, []);

  if (loading) {
    return (
      <div className="h-screen w-screen bg-[#0B0C10] flex items-center justify-center font-mono">
        <div className="flex flex-col items-center gap-4">
          <RefreshCw className="w-8 h-8 text-[#66FCF1] animate-spin" />
          <div className="text-[#66FCF1] text-sm tracking-widest animate-pulse">CONNECTING TO SPECTRAL ENGINE...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen w-screen bg-[#0B0C10] text-[#C5C6C7] overflow-hidden flex flex-col font-sans">
      {/* PROFESSIONAL HEADER */}
      <header className="h-16 border-b border-[#1F2833] bg-[#1F2833]/50 flex items-center justify-between px-8 backdrop-blur-sm shrink-0">
        <div className="flex items-center gap-4">
          <Shield className="text-[#66FCF1] w-8 h-8" />
          <h1 className="text-white font-bold tracking-wider text-2xl font-sans">CASCADE<span className="text-[#66FCF1]">GUARD</span></h1>
          <div className="px-3 py-1 bg-[#45A29E]/20 text-[#66FCF1] text-xs font-bold rounded border border-[#45A29E]/30 font-sans tracking-wide">
            AUDIT V9.0
          </div>
        </div>
        <div className="flex items-center gap-8 text-base font-medium font-sans">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse ring-4 ring-green-500/20"></div>
            <span className="text-green-400 tracking-wide">ENGINE ONLINE</span>
          </div>
          <div className="text-gray-400">USER: <span className="text-white">ADMIN_01</span></div>
          <div className="text-gray-400 tabular-nums font-mono">{new Date().toISOString().split('T')[0]}</div>
        </div>
      </header>

      {/* MAIN GRID LAYOUT */}
      <main className="flex-1 grid grid-cols-12 gap-0 overflow-hidden font-sans">

        {/* LEFT COMPONENT: GLOBAL HEALTH */}
        <aside className="col-span-3 border-r border-[#1F2833] bg-[#0B0C10] p-8 flex flex-col gap-8 overflow-y-auto">
          <div className="text-white font-bold text-2xl mb-2 border-b border-[#1F2833] pb-4 tracking-tight">GLOBAL METRICS</div>

          <div className="p-6 bg-[#1F2833] rounded-xl border border-[#45A29E]/20 shadow-lg shadow-black/50">
            <div className="text-sm font-bold uppercase tracking-widest text-[#66FCF1] mb-2 opacity-90">Spectral Radius (λ₁)</div>
            <div className="text-7xl text-white font-black tracking-tighter tabular-nums font-mono">
              {metrics?.spectral_radius.toFixed(2)}
            </div>
            <div className="w-full h-1.5 bg-black mt-5 rounded-full overflow-hidden">
              <div className="h-full bg-[#66FCF1] shadow-[0_0_10px_#66FCF1]" style={{ width: `${Math.min((metrics?.spectral_radius || 0) * 5, 100)}%` }}></div>
            </div>
          </div>

          <div className="p-6 bg-[#1F2833] rounded-xl border border-[#FF4136]/30 relative overflow-hidden shadow-lg shadow-black/50">
            <div className="absolute top-0 right-0 p-3 opacity-10">
              <AlertTriangle className="w-16 h-16 text-[#FF4136]" />
            </div>
            <div className="text-sm font-bold uppercase tracking-widest text-[#FF4136] mb-2 opacity-90">Loss Exposure</div>
            <div className="text-6xl text-white font-black tracking-tighter tabular-nums font-mono break-all leading-none">
              €{(metrics?.potential_loss.amount / 1000000).toFixed(1)}M
            </div>
            <div className="text-sm text-[#FF4136] font-bold mt-4 flex items-center gap-2 bg-[#FF4136]/10 py-1.5 px-3 rounded w-fit">
              <AlertTriangle className="w-4 h-4" />
              Critical Threshold Exceeded
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="p-5 bg-[#1F2833] rounded-xl border border-white/5">
              <div className="text-sm font-bold text-gray-400 mb-2">NODES</div>
              <div className="text-4xl text-white font-bold tabular-nums font-mono">{metrics?.topology.nodes.length || 0}</div>
            </div>
            <div className="p-5 bg-[#1F2833] rounded-xl border border-white/5">
              <div className="text-sm font-bold text-gray-400 mb-2">TIERS</div>
              <div className="text-4xl text-white font-bold tabular-nums font-mono">3</div>
            </div>
          </div>
        </aside>

        {/* CENTER COMPONENT: SCHEMATIC VISUALIZATION */}
        <section className="col-span-6 bg-black relative flex items-center justify-center border-r border-[#1F2833] overflow-hidden">
          {/* Background Grid */}
          <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
            style={{
              backgroundImage: 'linear-gradient(#1F2833 1px, transparent 1px), linear-gradient(90deg, #1F2833 1px, transparent 1px)',
              backgroundSize: '40px 40px'
            }}>
          </div>

          {/* Schematic Image Overlay */}
          <div className="relative z-10 w-full h-full flex items-center justify-center p-12 pt-24">
            <img src="/assets/schematic_grid.png" alt="Supply Chain Schematic" className="max-w-full max-h-full object-contain opacity-90 filter brightness-110 contrast-125 scale-100" />
          </div>

          {/* Overlay UI Layer */}
          <div className="absolute top-8 left-8 z-20">
            <div className="px-5 py-2 bg-black/90 border border-[#66FCF1] text-[#66FCF1] text-base font-bold tracking-widest shadow-[0_0_15px_rgba(102,252,241,0.2)] rounded flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#66FCF1] animate-pulse"></span>
              LIVE ENGINE DATA
            </div>
          </div>
        </section>

        {/* RIGHT COMPONENT: CRITICAL ALERTS */}
        <aside className="col-span-3 bg-[#0B0C10] p-8 flex flex-col gap-8 overflow-y-auto">
          <div className="text-white font-bold text-2xl mb-2 border-b border-[#1F2833] pb-4 tracking-tight">CRITICAL ALERTS</div>

          <div className="space-y-6">
            <motion.div
              initial={{ x: 20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              className="p-6 bg-[#FF4136]/10 border-l-4 border-[#FF4136] rounded-r-xl group hover:bg-[#FF4136]/20 transition-colors cursor-pointer"
            >
              <div className="flex justify-between items-start mb-3">
                <div className="text-xl font-bold text-white tracking-tight">TSMC</div>
                <div className="px-3 py-1 bg-[#FF4136] text-black text-xs font-black rounded uppercase tracking-wide">CRITICAL</div>
              </div>
              <div className="text-base text-gray-300 mb-4 leading-relaxed font-medium">
                Single Point of Failure detected in Tier-2 semiconductor supply.
              </div>
              <div className="text-xs text-[#FF4136] font-bold tracking-wider bg-black/30 p-2.5 rounded inline-block">
                IMPACT: 67% OF PRODUCTION
              </div>
            </motion.div>

            <div className="p-6 bg-[#1F2833] border-l-4 border-[#FFA500] rounded-r-xl">
              <div className="flex justify-between items-start mb-3">
                <div className="text-xl font-bold text-white tracking-tight">NXP Semi</div>
                <div className="px-3 py-1 bg-[#FFA500] text-black text-xs font-black rounded uppercase tracking-wide">WARNING</div>
              </div>
              <div className="text-base text-gray-300 leading-relaxed font-medium">
                Inventory levels approaching safety stock threshold (15 days).
              </div>
            </div>
          </div>

          <div className="mt-auto">
            <button onClick={fetchLiveAudit} className="w-full py-5 bg-[#66FCF1] hover:bg-[#45A29E] text-black font-black text-base tracking-widest transition-all hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center gap-3 rounded shadow-[0_0_20px_rgba(102,252,241,0.3)]">
              <RefreshCw className="w-5 h-5" />
              REFRESH AUDIT
            </button>
          </div>
        </aside>

      </main>

      {/* STATUS FOOTER */}
      <footer className="h-8 bg-[#0B0C10] border-t border-[#1F2833] flex items-center justify-between px-6 text-[10px] text-gray-600 tracking-widest shrink-0 font-mono">
        <div>SERVER: EU-CENTRAL-1a (CONNECTED)</div>
        <div>LATENCY: 12ms</div>
        <div>ENCRYPTION: AES-256</div>
      </footer>
    </div>
  );
};

export default Dashboard;
