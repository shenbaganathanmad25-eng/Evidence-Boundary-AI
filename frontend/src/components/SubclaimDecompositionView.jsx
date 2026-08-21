import React, { useState } from 'react';
import { Layers, ChevronDown, ChevronUp, AlertCircle, Info, Sparkles } from 'lucide-react';

export default function SubclaimDecompositionView({ subclaims }) {
  const [expandedId, setExpandedId] = useState(null);

  if (!subclaims || subclaims.length === 0) return null;

  const getSeverityBadge = (label, ebdfItem) => {
    if (!ebdfItem) return null;

    const { severity, explanation } = ebdfItem;

    let badgeStyle = 'bg-slate-800 text-slate-300 border-slate-700';
    if (severity === 'LOW') badgeStyle = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
    else if (severity === 'MEDIUM') badgeStyle = 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30';
    else if (severity === 'HIGH') badgeStyle = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
    else if (severity === 'VERY HIGH' || severity === 'VERY_HIGH') badgeStyle = 'bg-rose-500/20 text-rose-300 border-rose-500/30 font-extrabold shadow-sm shadow-rose-500/20 animate-pulse';

    return (
      <div
        key={label}
        className={`px-2.5 py-1 rounded-md border text-[11px] font-bold flex items-center gap-1.5 ${badgeStyle}`}
        title={`${label}: ${explanation}`}
      >
        <span className="text-[10px] opacity-75 uppercase">{label}:</span>
        <span>{severity}</span>
      </div>
    );
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base font-bold text-slate-100">
            Claim Decomposition & EBDF Severity Scoring
          </h3>
        </div>
        <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
          {subclaims.length} Subclaim{subclaims.length > 1 ? 's' : ''} Extracted
        </span>
      </div>

      {/* Subclaims list with folded EBDF badges */}
      <div className="space-y-3">
        {subclaims.map((sc, idx) => {
          const isExpanded = expandedId === sc.id || expandedId === idx;
          const ebdf = sc.ebdf || {};

          return (
            <div
              key={sc.id || idx}
              className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 hover:border-slate-700 transition-all space-y-3"
            >
              {/* Header: Subclaim text + EBDF Severity Badges */}
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="space-y-1 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-indigo-300 border border-indigo-500/20">
                      SUBCLAIM #{idx + 1}
                    </span>
                    {sc.entity && sc.entity !== 'Unspecified' && (
                      <span className="text-[10px] font-medium text-slate-400">
                        Entity: <strong className="text-slate-200">{sc.entity}</strong>
                      </span>
                    )}
                  </div>
                  <p className="text-sm font-semibold text-slate-100 leading-snug">
                    "{sc.subclaim}"
                  </p>
                </div>

                {/* Toggle details */}
                <button
                  onClick={() => setExpandedId(isExpanded ? null : (sc.id || idx))}
                  className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 font-medium shrink-0 pt-0.5"
                >
                  <span>{isExpanded ? 'Hide Details' : 'View Entity Extraction'}</span>
                  {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
              </div>

              {/* Folded EBDF Severities Badges Row */}
              <div className="pt-2 border-t border-slate-800/80 flex flex-wrap items-center gap-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mr-1">
                  EBDF Severity Risk:
                </span>
                {getSeverityBadge('ΔScope', ebdf.scope)}
                {getSeverityBadge('ΔCertainty', ebdf.certainty)}
                {getSeverityBadge('ΔTemporal', ebdf.temporal)}
                {getSeverityBadge('ΔCausal', ebdf.causal)}
              </div>

              {/* Explanations summary */}
              {ebdf.causal?.explanation && (
                <p className="text-xs text-slate-300 italic bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60">
                  <strong className="text-amber-400 not-italic">EBDF Analysis:</strong> {ebdf.causal.explanation}
                </p>
              )}

              {/* Expandable extracted entity/semantic metadata */}
              {isExpanded && (
                <div className="pt-3 border-t border-slate-800/80 space-y-3 text-xs">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Subject</span>
                      <span className="font-semibold text-slate-200">{sc.subject || 'Unspecified'}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Relation</span>
                      <span className="font-semibold text-indigo-300">{sc.relation || 'Unspecified'}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Metric</span>
                      <span className="font-semibold text-slate-200">{sc.metric || 'Unspecified'}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Value & Unit</span>
                      <span className="font-semibold text-emerald-400">
                        {sc.value !== 'Unspecified' ? `${sc.value} ${sc.unit !== 'Unspecified' ? sc.unit : ''}` : 'Unspecified'}
                      </span>
                    </div>
                  </div>

                  {/* Additional metadata */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Population / Cohort</span>
                      <span className="text-slate-300">{sc.population || 'Unspecified'}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Causal Language</span>
                      <span className="text-amber-300 font-medium">{sc.causal_language || 'Unspecified'}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-bold block">Comparison</span>
                      <span className="text-slate-300">{sc.comparison || 'Unspecified'}</span>
                    </div>
                  </div>

                  {/* Assumptions List */}
                  {sc.assumptions && sc.assumptions.length > 0 && (
                    <div className="bg-slate-950/80 p-3 rounded-xl border border-indigo-500/20 space-y-1">
                      <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider block">
                        Implicit Assumptions ({sc.assumptions.length}):
                      </span>
                      <ul className="list-disc list-inside space-y-0.5 text-slate-300 text-[11px]">
                        {sc.assumptions.map((asm, aIdx) => (
                          <li key={aIdx}>{asm}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
