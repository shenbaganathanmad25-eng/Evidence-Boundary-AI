import React, { useState } from 'react';
import { Zap, AlertOctagon, CheckCircle2, XCircle, ArrowRight, Play, ShieldAlert, AlertTriangle } from 'lucide-react';
import { runCustomStressTest } from '../services/api';

export default function StressTestPanel({ ebdfDeltas, stressTests, scenarioId, baselineVerdict }) {
  const [expandedTest, setExpandedTest] = useState(null);
  const [customCondition, setCustomCondition] = useState('');
  const [attackType, setAttackType] = useState('SCOPE_SHIFT');
  const [customResults, setCustomResults] = useState([]);
  const [runningAttack, setRunningAttack] = useState(false);
  const [activeTestRun, setActiveTestRun] = useState(null);

  if (!ebdfDeltas || !stressTests) return null;

  const allTests = [...customResults, ...stressTests];

  const handleRunCustomAttack = async () => {
    if (!customCondition.trim()) return;
    setRunningAttack(true);
    try {
      const res = await runCustomStressTest(scenarioId || 'custom', attackType, customCondition);
      setCustomResults((prev) => [res, ...prev]);
      setCustomCondition('');
    } catch (err) {
      console.error('Custom stress test failed:', err);
    } finally {
      setRunningAttack(false);
    }
  };

  const getVerdictBadge = (verdictStr) => {
    if (verdictStr === 'VERIFIED') {
      return (
        <span className="px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold flex items-center gap-1">
          🟢 VERIFIED
        </span>
      );
    } else if (verdictStr === 'REFUTED') {
      return (
        <span className="px-2.5 py-1 rounded-md bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-bold flex items-center gap-1 shadow-md shadow-rose-500/20">
          🔴 REFUTED
        </span>
      );
    } else {
      return (
        <span className="px-2.5 py-1 rounded-md bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-bold flex items-center gap-1">
          🟡 INSUFFICIENTLY VERIFIED
        </span>
      );
    }
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-6 shadow-2xl">
      
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <Zap className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-base font-black text-slate-100 tracking-wide">
              ML EVIDENCE BOUNDARY STRESS TEST SUITE
            </h2>
            <p className="text-xs text-slate-400 font-medium">
              Attacks evidence robustness (Source Removal, Causality Attack, Scope Shift) to reveal verdict collapse
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-rose-500/10 text-rose-300 border border-rose-500/30">
            {allTests.filter(t => !t.claim_survived).length} Failure Points Detected
          </span>
        </div>
      </div>

      {/* Interactive Custom Attack Vector Launcher */}
      <div className="bg-slate-900/90 p-4 rounded-xl border border-indigo-500/30 space-y-3 shadow-inner">
        <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-2">
          <AlertOctagon className="w-4 h-4 text-indigo-400" />
          Launch Interactive Attack Vector
        </span>
        
        <div className="flex flex-wrap sm:flex-nowrap items-center gap-2">
          <select
            value={attackType}
            onChange={(e) => setAttackType(e.target.value)}
            className="bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs font-semibold text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="SCOPE_SHIFT">TEST C — Scope Shift</option>
            <option value="CAUSAL_LEAP">TEST B — Causality Attack</option>
            <option value="SOURCE_REMOVAL">TEST A — Source Removal</option>
          </select>

          <input
            type="text"
            value={customCondition}
            onChange={(e) => setCustomCondition(e.target.value)}
            placeholder="e.g. Expand scope from single trial to all nationwide schools..."
            className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />

          <button
            onClick={handleRunCustomAttack}
            disabled={runningAttack || !customCondition.trim()}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shrink-0 disabled:opacity-50 shadow-lg shadow-indigo-600/30 transition-all"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>Run Attack</span>
          </button>
        </div>
      </div>

      {/* Stress Test Cards: BEFORE vs AFTER Verdict Shift */}
      <div className="space-y-4">
        <span className="text-xs font-extrabold text-slate-300 uppercase tracking-wider block">
          Executed ML Stress Tests (Before vs After Verdict Shift):
        </span>

        {allTests.map((st, idx) => {
          const isExpanded = expandedTest === idx;
          // Extract verdict before/after strings
          const beforeStr = st.original_evidence_holding?.replace('Baseline Verdict: ', '') || baselineVerdict || 'INSUFFICIENTLY_VERIFIED';
          const afterStr = st.attacked_condition?.replace('Post-Attack Verdict: ', '') || (st.claim_survived ? beforeStr : 'REFUTED');

          return (
            <div
              key={idx}
              className={`p-4 rounded-xl border transition-all duration-300 space-y-3 ${
                st.claim_survived
                  ? 'bg-emerald-950/20 border-emerald-500/30'
                  : 'bg-rose-950/30 border-rose-500/40 shadow-xl shadow-rose-950/30'
              }`}
            >
              {/* Header row */}
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-black text-slate-100 uppercase tracking-wide">
                    {st.scenario_title || st.perturbation_type}
                  </span>
                  {!st.claim_survived ? (
                    <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-extrabold uppercase">
                      CRITICAL BREAKING POINT
                    </span>
                  ) : (
                    <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-extrabold uppercase">
                      SURVIVED ATTACK
                    </span>
                  )}
                </div>

                {/* BEFORE / AFTER VERDICT INTERACTION DISPLAY */}
                <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
                  <span className="text-[10px] font-bold text-slate-400 uppercase">BEFORE:</span>
                  {getVerdictBadge(beforeStr)}
                  
                  <ArrowRight className="w-4 h-4 text-indigo-400 mx-1 shrink-0 animate-pulse" />
                  
                  <span className="text-[10px] font-bold text-slate-400 uppercase">AFTER:</span>
                  {getVerdictBadge(afterStr)}
                </div>
              </div>

              {/* Hypothesis & Breaking Point Explanation */}
              <div className="space-y-1.5">
                <p className="text-xs font-medium text-slate-200 leading-relaxed">
                  {st.breaking_point_explanation}
                </p>
              </div>

              {/* Action bar */}
              <div className="flex items-center justify-between pt-1">
                <span className="text-[10px] text-slate-400 italic">
                  ML Evidence Classifier recomputed support probabilities after perturbation.
                </span>
                
                <button
                  onClick={() => setExpandedTest(isExpanded ? null : idx)}
                  className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                >
                  <span>{isExpanded ? 'Hide Attack Payload' : 'Inspect Attack Details'}</span>
                </button>
              </div>

              {/* Expanded details */}
              {isExpanded && (
                <div className="pt-3 border-t border-slate-800 space-y-2 text-xs">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 bg-slate-950 p-3 rounded-lg border border-slate-800">
                    <div>
                      <span className="text-[10px] font-bold text-slate-500 uppercase block">
                        Original Baseline Holding:
                      </span>
                      <span className="text-slate-300 font-medium">
                        {st.original_evidence_holding}
                      </span>
                    </div>
                    <div>
                      <span className="text-[10px] font-bold text-amber-400 uppercase block">
                        Attacked Condition:
                      </span>
                      <span className="text-slate-300 font-medium">
                        {st.attacked_condition}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

    </div>
  );
}
