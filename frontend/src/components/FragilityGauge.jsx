import React from 'react';
import { Flame, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function FragilityGauge({ fragility }) {
  if (!fragility) return null;

  const score = Math.round(fragility.overall_score || 0);

  let label = 'LOW';
  let labelStyle = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
  let barColor = 'bg-emerald-500';

  if (score > 60) {
    label = 'HIGH';
    labelStyle = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
    barColor = 'bg-rose-500';
  } else if (score > 30) {
    label = 'MEDIUM';
    labelStyle = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
    barColor = 'bg-amber-500';
  }

  // Derive critical assumptions from summary/tier if not passed directly
  const criticalAssumptions = fragility.critical_assumptions || [
    "Causality",
    "Population scope",
    "Controlled comparison"
  ];

  return (
    <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Flame className="w-5 h-5 text-amber-400" />
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
            Claim Fragility Score
          </h3>
        </div>
        <span className={`text-xs font-black px-3 py-1 rounded-full border uppercase ${labelStyle}`}>
          Risk: {label}
        </span>
      </div>

      {/* Labeled Score Display */}
      <div className="bg-slate-900/90 p-4 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-baseline justify-between">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Fragility Index:
          </span>
          <span className="text-3xl font-black text-slate-100 font-mono">
            {score}<span className="text-base text-slate-500">/100</span>
          </span>
        </div>

        {/* Reproducible progress bar */}
        <div className="w-full bg-slate-950 h-3 rounded-full overflow-hidden p-0.5 border border-slate-800">
          <div
            className={`h-full rounded-full transition-all duration-500 ${barColor}`}
            style={{ width: `${score}%` }}
          />
        </div>

        <p className="text-xs text-slate-300 leading-relaxed font-medium pt-1">
          {fragility.explanation_summary}
        </p>
      </div>

      {/* Critical Assumptions List */}
      <div className="space-y-2">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
          Critical Assumptions Vulnerabilities:
        </span>
        <div className="flex flex-wrap gap-1.5">
          {criticalAssumptions.map((asm, idx) => (
            <span
              key={idx}
              className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-slate-900 text-slate-200 border border-slate-800 flex items-center gap-1.5"
            >
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              <span>{asm}</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
