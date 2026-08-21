import React from 'react';
import { HelpCircle, Layers, Split, AlertCircle } from 'lucide-react';

export default function P1ExtensionsPanel({ killerQuestions, missingRequirements, mutations }) {
  if (!killerQuestions && !missingRequirements && !mutations) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
      
      {/* 1. KILLER QUESTION ENGINE */}
      <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
          <HelpCircle className="w-4 h-4 text-purple-400" />
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            Killer Question Engine (P1)
          </h3>
        </div>
        <p className="text-[11px] text-slate-400">
          Probing questions designed to challenge boundary assumptions:
        </p>
        <ul className="space-y-2 text-xs text-slate-300">
          {(killerQuestions || []).map((q, idx) => (
            <li key={idx} className="bg-slate-900/80 p-2.5 rounded-lg border border-purple-500/20 flex items-start gap-2">
              <span className="text-purple-400 font-bold text-xs shrink-0">{idx + 1}.</span>
              <span className="font-medium leading-normal">{q}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 2. MISSING EVIDENCE FINDER */}
      <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
          <Layers className="w-4 h-4 text-blue-400" />
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            Missing Evidence Finder (P1)
          </h3>
        </div>
        <p className="text-[11px] text-slate-400">
          Data required to elevate claim to full verification:
        </p>
        <ul className="space-y-2 text-xs text-slate-300">
          {(missingRequirements || []).map((req, idx) => (
            <li key={idx} className="bg-slate-900/80 p-2.5 rounded-lg border border-blue-500/20 flex items-start gap-2">
              <span className="text-blue-400 font-bold text-xs shrink-0">•</span>
              <span className="font-medium leading-normal">{req}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 3. EVIDENCE MUTATION DETECTOR */}
      <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-3">
        <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
          <Split className="w-4 h-4 text-amber-400" />
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">
            Evidence Mutation Detector (P1)
          </h3>
        </div>
        <p className="text-[11px] text-slate-400">
          Phrasing exaggerations detected between source & claim:
        </p>
        <ul className="space-y-2 text-xs text-slate-300">
          {(mutations || []).map((m, idx) => (
            <li key={idx} className="bg-slate-900/80 p-2.5 rounded-lg border border-amber-500/20 flex items-start gap-2">
              <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
              <span className="font-medium leading-normal italic text-amber-200/90">{m}</span>
            </li>
          ))}
        </ul>
      </div>

    </div>
  );
}
