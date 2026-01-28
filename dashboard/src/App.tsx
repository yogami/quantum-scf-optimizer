import { useState, useEffect } from 'react';
import { Shield, Lock, Zap, Unlock, RefreshCw } from 'lucide-react';

interface AuditMetrics {
  spectral_radius: number;
  ead_volatility: number;
  adversarial_test: {
    status: string;
    lambda_injected: number;
    shock_delta: number;
    resilience_score: number;
    shock_delta: number;
    resilience_score: number;
    description: string;
  };
  governance: { tier: string, policy_locked: boolean, parameters: any };
  attribution_ledger: any[];
  benchmarks: { archer_miss_rate: string, identification_alpha: number };
}

const Dashboard = () => {
  const [metrics, setMetrics] = useState<AuditMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [policy, setPolicy] = useState('bafin_standard');
  const [scenario, setScenario] = useState('baseline');
  const [auditLog, setAuditLog] = useState<{ msg: string, desc: string }[]>([]);
  const [simulating, setSimulating] = useState(false);

  const fetchAdversarialAudit = async (p: string = policy, s: string = scenario, runTest: boolean = false) => {
    try {
      if (!runTest) setLoading(true);
      else setSimulating(true);

      const res = await fetch(`http://localhost:11885/api/live-scenario?scenario=${s}&policy=${p}&run_test=${runTest}`);
      const data = await res.json();
      setMetrics(data);

      if (runTest) {
        const passed = data.adversarial_test.status === "PASSED";
        const logMsg = passed ? "SIMULATION PASSED: POLICIES UNLOCKED" : "SIMULATION FAILED: CONSERVATIVE ENFORCED";
        setAuditLog(prev => [{ msg: logMsg, desc: `Resilience: ${(data.adversarial_test.resilience_score * 100).toFixed(1)}%` }, ...prev].slice(0, 3));
        if (!passed && policy !== 'conservative') setPolicy('conservative');
      }
    } catch (e) {
      console.error("Adversarial Sync Failed", e);
    } finally {
      setLoading(false);
      setSimulating(false);
    }
  };

  useEffect(() => { fetchAdversarialAudit(); }, []);

  const handleScenarioChange = (s: string) => {
    setScenario(s);
    fetchAdversarialAudit(policy, s, false);
  };


  const handlePolicyChange = (p: string) => {
    if (p === policy) return;
    if (metrics?.governance.policy_locked && p !== 'conservative') {
      alert("GOVERNANCE LOCK ACTIVE: Run 'Hidden Hub Simulation' to prove resilience before unlocking Aggressive tiers.");
      return;
    }
    setPolicy(p);
    fetchAdversarialAudit(p, scenario, false);
  };

  const runSimulation = () => {
    fetchAdversarialAudit(policy, scenario, true);
  };

  if (loading && !metrics) {
    return <div style={{ height: '100vh', backgroundColor: '#0B0C10', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#66FCF1', fontFamily: "'JetBrains Mono', monospace" }}>INITIALIZING ADVERSARIAL ENGINE...</div>;
  }

  const isLocked = metrics?.governance.policy_locked;

  return (
    <div style={{ height: '100vh', width: '100vw', backgroundColor: '#0B0C10', color: '#C5C6C7', overflow: 'hidden', display: 'flex', flexDirection: 'column', fontFamily: "'Inter', sans-serif" }}>
      {/* HEADER: ADVERSARIAL RESILIENCE */}
      <header style={{ height: '64px', borderBottom: '1px solid #1F2833', backgroundColor: 'rgba(31, 40, 51, 0.5)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Shield style={{ color: '#4ade80', width: '22px' }} />
          <h1 style={{ color: 'white', fontWeight: 900, fontSize: '18px', margin: 0, letterSpacing: '0.1em' }}>CASCADE<span style={{ color: '#4ade80' }}>GUARD</span></h1>
          <div style={{ display: 'flex', gap: '8px', marginLeft: '16px' }}>
            <button onClick={() => handleScenarioChange('baseline')} style={{ fontSize: '9px', fontWeight: 'bold', padding: '4px 10px', backgroundColor: scenario === 'baseline' ? '#30363D' : 'transparent', color: scenario === 'baseline' ? 'white' : '#6b7280', border: '1px solid #30363D', borderRadius: '4px', cursor: 'pointer' }}>BASELINE (N=3)</button>
            <button onClick={() => handleScenarioChange('red-sea')} style={{ fontSize: '9px', fontWeight: 'bold', padding: '4px 10px', backgroundColor: scenario === 'red-sea' ? '#30363D' : 'transparent', color: scenario === 'red-sea' ? 'white' : '#6b7280', border: '1px solid #30363D', borderRadius: '4px', cursor: 'pointer' }}>RED SEA (N=15)</button>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '24px', fontSize: '11px', fontWeight: 'bold' }}>
          <div style={{ color: '#9ca3af' }}>RESILIENCE SCORE: <span style={{ color: !isLocked ? '#4ade80' : '#FF4136' }}>{(metrics?.adversarial_test.resilience_score || 0 * 100).toFixed(1)}%</span></div>
          <div style={{ color: '#9ca3af' }}>POLICY STATE: <span style={{ color: !isLocked ? '#4ade80' : '#FF4136' }}>{!isLocked ? "UNLOCKED" : "LOCKED"}</span></div>
        </div>
      </header>

      <main style={{ flex: 1, display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: 0, overflow: 'hidden' }}>

        {/* LEFT: ADVERSARIAL INJECTION LAB */}
        <aside style={{ gridColumn: 'span 3', borderRight: '1px solid #1F2833', padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px', overflowY: 'auto' }}>
          <div style={{ color: 'white', fontWeight: 'bold', fontSize: '12px', borderBottom: '1px solid #1F2833', paddingBottom: '12px' }}>HIDDEN HUB STRESS TEST (AT 4.1)</div>

          <div style={{ padding: '16px', backgroundColor: '#161B22', borderRadius: '8px', border: '1px solid #30363D' }}>
            <div style={{ fontSize: '10px', color: '#fbbf24', fontWeight: 'bold', marginBottom: '8px' }}>INJECTION TARGET:</div>
            <div style={{ fontSize: '11px', color: '#9ca3af', lineHeight: 1.4 }}>
              "v33.0 FLOW SENTINEL: Targeting 'Capacity Chokepoints' (Max-Flow Min-Cut). Phantom edges (zero capacity) ignored."
            </div>

            <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
              <div>
                <div style={{ fontSize: '9px', color: '#4b5563' }}>BASE FLOW</div>
                <div style={{ fontSize: '14px', color: 'white', fontWeight: 'bold' }}>{metrics?.spectral_radius.toFixed(0)} Units</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '9px', color: '#4b5563' }}>SHOCKED FLOW</div>
                <div style={{ fontSize: '14px', color: '#FF4136', fontWeight: 'bold' }}>{metrics?.adversarial_test.lambda_injected.toFixed(0)} Units</div>
              </div>
            </div>
            <div style={{ marginTop: '8px', paddingTop: '8px', borderTop: '1px solid #30363D', textAlign: 'center', fontSize: '9px', color: '#FF4136' }}>
              FLOW DROP: -{(metrics?.adversarial_test.shock_delta * 100).toFixed(1)}%
            </div>
          </div>

          <button
            onClick={runSimulation}
            disabled={simulating}
            style={{
              width: '100%', padding: '12px', backgroundColor: simulating ? '#30363D' : '#fbbf24',
              color: 'black', fontWeight: 900, fontSize: '11px', border: 'none', borderRadius: '4px', cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px'
            }}>
            {simulating ? <RefreshCw className="animate-spin" size={14} /> : <Zap size={14} />}
            {simulating ? "RUNNING SIMULATION..." : "RUN HIDDEN HUB SIMULATION"}
          </button>

          {/* CHALLENGE MODE UPLOAD */}
          <div style={{ padding: '16px', backgroundColor: '#161B22', borderRadius: '8px', border: '1px solid #30363D', marginTop: '12px' }}>
            <div style={{ fontSize: '10px', color: 'white', fontWeight: 'bold', marginBottom: '8px' }}>LIVE CHALLENGE (REPRODUCIBILITY)</div>
            <div style={{ fontSize: '9px', color: '#9ca3af', marginBottom: '12px' }}>
              Upload your own graph (JSON) to validate the "Flow Sentinel" against your data.
            </div>
            <input
              type="file"
              accept=".json"
              onChange={async (e) => {
                if (!e.target.files?.[0]) return;
                const file = e.target.files[0];
                const text = await file.text();
                try {
                  setSimulating(true);
                  const json = JSON.parse(text);
                  const res = await fetch('http://localhost:11885/api/validate-file', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(json)
                  });
                  const data = await res.json();
                  setMetrics(data);

                  const passed = data.adversarial_test.status === "PASSED";
                  const logMsg = passed ? "USER DATA VALIDATED: PASSED" : `ATTACK BLOCKED: ${data.adversarial_test.status}`;
                  setAuditLog(prev => [{ msg: logMsg, desc: data.adversarial_test.description || "System blocked invalid topology." }, ...prev].slice(0, 3));
                } catch (err) {
                  alert("Invalid JSON File");
                } finally {
                  setSimulating(false);
                }
              }}
              style={{ fontSize: '9px', color: '#9ca3af' }}
            />
          </div>

          <div style={{ marginTop: 'auto', padding: '16px', backgroundColor: '#161B22', borderRadius: '8px' }}>
            <div style={{ fontSize: '10px', color: '#4ade80', fontWeight: 'bold', marginBottom: '12px' }}>SIMULATION LOG</div>
            {auditLog.map((log, i) => (
              <div key={i} style={{ marginBottom: '10px', borderBottom: '1px solid #30363D', paddingBottom: '8px' }}>
                <div style={{ fontSize: '9px', color: log.msg.includes('PASSED') ? '#4ade80' : '#FF4136', fontWeight: 'bold' }}>{log.msg}</div>
                <div style={{ fontSize: '9px', color: '#4b5563' }}>{log.desc}</div>
              </div>
            ))}
          </div>
        </aside>

        {/* CENTER: SIMULATION-GATED GOVERNANCE */}
        <section style={{ gridColumn: 'span 6', padding: '32px', backgroundColor: '#0D1117', overflowY: 'auto', position: 'relative' }}>

          {/* VISUAL DEFENSE OVERLAY */}
          {metrics?.adversarial_test?.status && metrics.adversarial_test.status !== "PASSED" && metrics.adversarial_test.status !== "NOT_RUN" && (
            <div style={{
              position: 'absolute', top: 0, left: 0, right: 0, bottom: 0,
              backgroundColor: 'rgba(255, 65, 54, 0.95)',
              display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
              zIndex: 50, backdropFilter: 'blur(4px)'
            }}>
              <Shield size={64} style={{ color: 'white', marginBottom: '24px' }} className="animate-pulse" />
              <div style={{ fontSize: '24px', fontWeight: 900, color: 'white', marginBottom: '8px' }}>ATTACK BLOCKED</div>
              <div style={{ fontSize: '14px', color: 'white', fontWeight: 'bold', backgroundColor: 'rgba(0,0,0,0.3)', padding: '8px 16px', borderRadius: '4px' }}>
                {metrics.adversarial_test.status}
              </div>
              <div style={{ fontSize: '12px', color: 'white', marginTop: '16px', maxWidth: '300px', textAlign: 'center', lineHeight: 1.5 }}>
                {metrics.adversarial_test.description}
              </div>
              <button
                onClick={() => handleScenarioChange('baseline')}
                style={{ marginTop: '32px', padding: '12px 24px', backgroundColor: 'white', color: '#FF4136', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}>
                RESET SYSTEM
              </button>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
            <div style={{ color: 'white', fontWeight: 900, fontSize: '18px' }}>SIMULATION-GATED GOVERNANCE</div>
            <div style={{ fontSize: '10px', color: !isLocked ? '#4ade80' : '#FF4136', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px' }}>
              {!isLocked ? <Unlock size={14} /> : <Lock size={14} />}
              STATUS: {!isLocked ? "TIERS UNLOCKED" : "LOCKED (RUN TEST)"}
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '32px' }}>
            {['CONSERVATIVE', 'BAFIN_STANDARD', 'AGGRESSIVE'].map(p => {
              const isActive = metrics?.governance.tier === p.toLowerCase();
              const isLockedBtn = isLocked && p !== 'CONSERVATIVE'; // Standard/Aggressive locked if test fails
              if (metrics?.adversarial_test.status.includes("FAILED")) return null; // Hide buttons if failed

              return (
                <button
                  key={p}
                  onClick={() => handlePolicyChange(p.toLowerCase())}
                  style={{
                    padding: '24px',
                    backgroundColor: isActive ? 'rgba(74, 222, 128, 0.1)' : '#161B22',
                    border: `1px solid ${isActive ? '#4ade80' : '#30363D'}`,
                    borderRadius: '8px',
                    opacity: isLockedBtn ? 0.5 : 1,
                    cursor: isLockedBtn ? 'not-allowed' : 'pointer',
                    textAlign: 'left'
                  }}>
                  <div style={{ fontSize: '10px', color: '#4b5563', fontWeight: 'bold', marginBottom: '8px', display: 'flex', justifyContent: 'space-between' }}>
                    {p} {isLockedBtn && <Lock size={10} />}
                  </div>
                  <div style={{ fontSize: '9px', color: '#9ca3af' }}>
                    {p === 'CONSERVATIVE' && "Always Unlocked (Fail-Safe)"}
                    {p === 'BAFIN_STANDARD' && "Requires Resilience > 80%"}
                    {p === 'AGGRESSIVE' && "Requires Resilience > 80%"}
                  </div>
                </button>
              );
            })}
          </div>

          <div style={{ padding: '24px', backgroundColor: 'rgba(251, 191, 36, 0.05)', border: '1px solid #fbbf24', borderRadius: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <Zap style={{ color: '#fbbf24' }} />
              <div style={{ color: '#fbbf24', fontWeight: 'bold', fontSize: '14px' }}>WHY IS THIS LOCKED?</div>
            </div>
            <p style={{ fontSize: '12px', color: '#9ca3af', lineHeight: 1.6, margin: 0 }}>
              To mitigate "Math-Washing", CascadeGuard v33.0 enforces <strong>Flow Sentinel logic</strong>.
              We simulate a "Capacity Shock" (Max-Flow Min-Cut) to measure the actual drop in system throughput
              when critical nodes fail. This creates "Incentive Compatible" governance where only real redundancy improves the score.
            </p>
          </div>
        </section>

        {/* RIGHT: P&L VOLATILITY */}
        <aside style={{ gridColumn: 'span 3', borderLeft: '1px solid #1F2833', padding: '32px', backgroundColor: '#0B0C10', display: 'flex', flexDirection: 'column', gap: '32px' }}>
          <div style={{ color: 'white', fontWeight: 'bold', fontSize: '14px', borderBottom: '1px solid #1F2833', paddingBottom: '16px' }}>ADVERSARIAL P&L (σ)</div>

          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '42px', color: 'white', fontWeight: 900, fontFamily: "'JetBrains Mono', monospace" }}>±€{metrics?.ead_volatility.toFixed(1)}M</div>
            <div style={{ fontSize: '10px', color: '#4b5563', marginTop: '12px' }}>SHOCK-WEIGHTED AT RISK</div>
          </div>

          <div style={{ padding: '20px', backgroundColor: '#161B22', borderRadius: '8px', border: '1px solid #1F2833' }}>
            <div style={{ fontSize: '10px', color: '#4ade80', fontWeight: 'bold', marginBottom: '12px' }}>RISK PARAMETERS:</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div>
                <div style={{ fontSize: '9px', color: '#4b5563' }}>LGD FLOOR:</div>
                <div style={{ fontSize: '14px', color: 'white', fontWeight: 'bold' }}>{(metrics?.governance.parameters.lgd_floor * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div style={{ fontSize: '9px', color: '#4b5563' }}>PD FLOOR:</div>
                <div style={{ fontSize: '14px', color: 'white', fontWeight: 'bold' }}>{(metrics?.governance.parameters.pd_floor * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>

          <button style={{ marginTop: 'auto', width: '100%', backgroundColor: '#4ade80', color: 'black', fontWeight: 900, fontSize: '14px', padding: '16px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            DEPLOY PILOT BUNDLE
          </button>
        </aside>
      </main>

      <footer style={{ height: '32px', borderTop: '1px solid #1F2833', backgroundColor: '#0B0C10', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 24px', fontSize: '9px', color: '#4b5563', fontFamily: "'JetBrains Mono', monospace" }}>
        <div>METHODOLOGY: FLOW_SENTINEL [v33.0]</div>
        <div style={{ color: '#fbbf24' }}>* FLOW DROP: -{(metrics?.adversarial_test.shock_delta * 100).toFixed(1)}% | RESILIENCE: {(metrics?.adversarial_test.resilience_score || 0 * 100).toFixed(1)}%</div>
        <div>PILOT STATUS: READY FOR TIER-1 TRIAL</div>
      </footer>
    </div>
  );
};

export default Dashboard;
