import React, { useState } from 'react';
import { ShieldCheck, ShieldOff, Database, ExternalLink, X, Info, Layers, CheckCircle2, XCircle } from 'lucide-react';

export default function BoundaryMap({ subClaims, evidence, decomposedSubclaims }) {
  const [selectedSubclaim, setSelectedSubclaim] = useState(null);

  if (!subClaims || subClaims.length === 0) return null;

  const supportedSubClaims = subClaims.filter((sc) => sc.is_supported);
  const unsupportedSubClaims = subClaims.filter((sc) => !sc.is_supported);

  const getEvidenceForSubclaim = (subId) => {
    return (evidence || []).filter((ev) => ev.subclaim_id === subId || ev.sub_claim_id === subId);
  };

  const getFullDecomposition = (subId) => {
    return (decomposedSubclaims || []).find((d) => d.id === subId) || {};
  };

  const getSupportDirectionBadge = (dir) => {
    if (dir === 'SUPPORTING') {
      return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">ML: SUPPORTING</span>;
    } else if (dir === 'CONTRADICTING') {
      return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">ML: CONTRADICTING</span>;
    } else {
      return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">ML: NEUTRAL</span>;
    }
  };

  return (
    <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-indigo-400" />
          <div>
            <h2 className="text-base font-black text-slate-100 uppercase tracking-wide">
              Evidence Boundary Map
            </h2>
            <p className="text-xs text-slate-400">
              Click any subclaim card below to inspect extracted NLP attributes & ML probabilities
            </p>
          </div>
        </div>
        <span className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-900 text-slate-300 border border-slate-800">
          Split-Screen Boundary Visualizer
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        
        {/* LEFT COLUMN: SUPPORTED BOUNDARY */}
        <div className="space-y-3">
          <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider">
                EVIDENCE-SUPPORTED REGION ({supportedSubClaims.length})
              </h3>
            </div>
          </div>

          {supportedSubClaims.map((sc) => {
            const evList = getEvidenceForSubclaim(sc.id);
            return (
              <div
                key={sc.id}
                onClick={() => setSelectedSubclaim(sc)}
                className="supported-card p-4 rounded-xl space-y-3 cursor-pointer hover:border-emerald-400/60 transition-all shadow-lg shadow-emerald-950/20 group"
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="text-xs font-bold text-emerald-300 bg-emerald-900/60 px-2 py-0.5 rounded border border-emerald-500/30">
                    SUBCLAIM #{sc.id}
                  </span>
                  <span className="text-[10px] font-bold text-emerald-400 group-hover:underline">
                    Click to Inspect ➔
                  </span>
                </div>

                <p className="text-xs font-semibold text-slate-100 leading-relaxed">
                  "{sc.text}"
                </p>

                {/* Evidence snippet summary */}
                {evList.length > 0 && (
                  <div className="bg-slate-950/80 p-2.5 rounded-lg border border-emerald-500/20 text-xs space-y-1">
                    <div className="flex justify-between items-center text-[10px]">
                      <span className="font-semibold text-emerald-200 line-clamp-1">{evList[0].source_title}</span>
                      {getSupportDirectionBadge(evList[0].support_direction)}
                    </div>
                    <p className="text-[11px] text-slate-300 italic line-clamp-2">
                      "{evList[0].passage}"
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* RIGHT COLUMN: CLAIM-EXTENDS-BEYOND-EVIDENCE REGION */}
        <div className="space-y-3">
          <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-300">
            <div className="flex items-center gap-2">
              <ShieldOff className="w-4 h-4 text-rose-400" />
              <h3 className="text-xs font-bold uppercase tracking-wider">
                CLAIM-EXTENDS-BEYOND-EVIDENCE REGION ({unsupportedSubClaims.length})
              </h3>
            </div>
          </div>

          {unsupportedSubClaims.map((sc) => {
            const evList = getEvidenceForSubclaim(sc.id);
            return (
              <div
                key={sc.id}
                onClick={() => setSelectedSubclaim(sc)}
                className="unsupported-card p-4 rounded-xl space-y-3 cursor-pointer hover:border-rose-400/60 transition-all shadow-lg shadow-rose-950/20 group"
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="text-xs font-bold text-rose-300 bg-rose-900/60 px-2 py-0.5 rounded border border-rose-500/30">
                    SUBCLAIM #{sc.id}
                  </span>
                  <span className="text-[10px] font-bold text-rose-400 group-hover:underline">
                    Click to Inspect ➔
                  </span>
                </div>

                <p className="text-xs font-semibold text-slate-100 leading-relaxed">
                  "{sc.text}"
                </p>

                <div className="bg-slate-950/90 p-2.5 rounded-lg border border-rose-500/30 text-xs">
                  <span className="text-[10px] font-bold text-rose-400 uppercase block mb-0.5">Boundary Gap:</span>
                  <p className="text-xs text-rose-200/90 leading-tight">
                    {sc.boundary_gap_description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

      </div>

      {/* CLICKABLE SUBCLAIM INSPECTION MODAL */}
      {selectedSubclaim && (() => {
        const fullDecomp = getFullDecomposition(selectedSubclaim.id);
        const subEvList = getEvidenceForSubclaim(selectedSubclaim.id);
        const supportingEv = subEvList.filter(ev => ev.support_direction === 'SUPPORTING');
        const contradictingEv = subEvList.filter(ev => ev.support_direction === 'CONTRADICTING');
        const neutralEv = subEvList.filter(ev => ev.support_direction === 'NEUTRAL' || !ev.support_direction);

        return (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
            <div className="glass-panel p-6 rounded-2xl border-indigo-500/40 max-w-3xl w-full max-h-[90vh] overflow-y-auto space-y-5 shadow-2xl relative">
              
              {/* Modal Header */}
              <div className="flex items-start justify-between gap-3 border-b border-slate-800 pb-3">
                <div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    SUBCLAIM INSPECTION #{selectedSubclaim.id}
                  </span>
                  <h3 className="text-base font-bold text-slate-100 pt-1 leading-snug">
                    "{selectedSubclaim.text}"
                  </h3>
                </div>
                <button
                  onClick={() => setSelectedSubclaim(null)}
                  className="p-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Extracted NLP Features */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider block">
                  Extracted NLP Features & Attributes:
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-slate-900/90 p-3 rounded-xl border border-slate-800 text-xs">
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Entity</span>
                    <span className="text-slate-200 font-medium">{fullDecomp.entity || 'Unspecified'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Subject</span>
                    <span className="text-slate-200 font-medium">{fullDecomp.subject || 'Unspecified'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Relation</span>
                    <span className="text-indigo-300 font-medium">{fullDecomp.relation || 'Unspecified'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Value & Unit</span>
                    <span className="text-emerald-400 font-medium">
                      {fullDecomp.value !== 'Unspecified' ? `${fullDecomp.value} ${fullDecomp.unit !== 'Unspecified' ? fullDecomp.unit : ''}` : 'Unspecified'}
                    </span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Population</span>
                    <span className="text-slate-200">{fullDecomp.population || 'Unspecified'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Geography</span>
                    <span className="text-slate-200">{fullDecomp.geography || 'Global'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Timeframe</span>
                    <span className="text-slate-200">{fullDecomp.time || 'Unspecified'}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-500 uppercase block">Causal Phrase</span>
                    <span className="text-amber-300">{fullDecomp.causal_language || 'Asserted'}</span>
                  </div>
                </div>
              </div>

              {/* Categorized Evidence & ML Probabilities */}
              <div className="space-y-3">
                <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
                  ML Evidence Classification & Probabilities:
                </span>

                {/* Supporting Evidence */}
                {supportingEv.length > 0 && (
                  <div className="space-y-2">
                    <span className="text-[11px] font-bold text-emerald-400 uppercase block">
                      Supporting Evidence ({supportingEv.length}):
                    </span>
                    {supportingEv.map(ev => (
                      <div key={ev.id} className="bg-emerald-950/30 p-3 rounded-xl border border-emerald-500/30 text-xs space-y-1">
                        <div className="flex justify-between font-semibold text-emerald-200">
                          <span>{ev.source_title}</span>
                          <span className="text-[10px] text-emerald-400 font-mono">
                            ML Prob: SUPPORTING ({(ev.relevance * 100).toFixed(0)}%)
                          </span>
                        </div>
                        <p className="text-slate-300 italic">"{ev.passage}"</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* Contradicting Evidence */}
                {contradictingEv.length > 0 && (
                  <div className="space-y-2">
                    <span className="text-[11px] font-bold text-rose-400 uppercase block">
                      Contradicting Evidence ({contradictingEv.length}):
                    </span>
                    {contradictingEv.map(ev => (
                      <div key={ev.id} className="bg-rose-950/30 p-3 rounded-xl border border-rose-500/30 text-xs space-y-1">
                        <div className="flex justify-between font-semibold text-rose-200">
                          <span>{ev.source_title}</span>
                          <span className="text-[10px] text-rose-400 font-mono">
                            ML Prob: CONTRADICTING ({(ev.relevance * 100).toFixed(0)}%)
                          </span>
                        </div>
                        <p className="text-slate-300 italic">"{ev.passage}"</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* Neutral Evidence */}
                {neutralEv.length > 0 && (
                  <div className="space-y-2">
                    <span className="text-[11px] font-bold text-slate-400 uppercase block">
                      Neutral / Baseline Evidence ({neutralEv.length}):
                    </span>
                    {neutralEv.map(ev => (
                      <div key={ev.id} className="bg-slate-900 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
                        <div className="flex justify-between font-semibold text-slate-300">
                          <span>{ev.source_title}</span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            ML Prob: NEUTRAL ({(ev.relevance * 100).toFixed(0)}%)
                          </span>
                        </div>
                        <p className="text-slate-400 italic">"{ev.passage}"</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Close Button */}
              <div className="pt-2 text-right">
                <button
                  onClick={() => setSelectedSubclaim(null)}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-lg"
                >
                  Close Inspection
                </button>
              </div>

            </div>
          </div>
        );
      })()}

    </div>
  );
}
