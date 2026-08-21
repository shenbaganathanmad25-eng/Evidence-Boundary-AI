import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Compass } from 'lucide-react';

export default function VerdictBanner({ verdict, justification, boundarySummary, domain }) {
  const getVerdictStyle = () => {
    switch (verdict) {
      case 'VERIFIED':
        return {
          bg: 'bg-emerald-950/40 border-emerald-500/40 text-emerald-300 pulse-glow-emerald',
          badgeBg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
          icon: <CheckCircle2 className="w-7 h-7 text-emerald-400" />,
          title: 'VERIFIED'
        };
      case 'REFUTED':
        return {
          bg: 'bg-rose-950/40 border-rose-500/40 text-rose-300 pulse-glow-rose',
          badgeBg: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
          icon: <XCircle className="w-7 h-7 text-rose-400" />,
          title: 'REFUTED'
        };
      case 'INSUFFICIENTLY_VERIFIED':
      default:
        return {
          bg: 'bg-amber-950/40 border-amber-500/40 text-amber-300 pulse-glow-amber',
          badgeBg: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
          icon: <AlertTriangle className="w-7 h-7 text-amber-400" />,
          title: 'INSUFFICIENTLY VERIFIED'
        };
    }
  };

  const style = getVerdictStyle();

  return (
    <div className={`p-5 rounded-2xl border ${style.bg} transition-all duration-300 space-y-3`}>
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 pb-3">
        <div className="flex items-center gap-3">
          {style.icon}
          <div>
            <div className="text-xs uppercase tracking-widest text-slate-400 font-semibold">
              Final Evidentiary Verdict
            </div>
            <div className="text-xl font-black tracking-wide flex items-center gap-2">
              <span>{style.title}</span>
              <span className={`text-xs px-2.5 py-0.5 rounded-full border font-bold uppercase ${style.badgeBg}`}>
                {domain || 'Domain Analysis'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Justification */}
      <p className="text-sm font-medium leading-relaxed text-slate-200">
        {justification}
      </p>

      {/* Where Evidence Ends Callout */}
      {boundarySummary && (
        <div className="bg-slate-900/90 rounded-xl p-3.5 border border-slate-800 flex items-start gap-3">
          <Compass className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <span className="text-xs font-bold text-indigo-400 uppercase tracking-wide block">
              Where Evidence Ends:
            </span>
            <p className="text-xs text-slate-300 leading-normal">
              {boundarySummary}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
