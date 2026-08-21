import React from 'react';
import { Search, Sparkles, BookOpen, Stethoscope, Cpu, ArrowRight, ShieldAlert } from 'lucide-react';

export default function ClaimInput({
  claimText,
  setClaimText,
  scenarios,
  onSelectScenario,
  onVerify,
  loading,
  demoMode
}) {
  const getScenarioIcon = (id) => {
    if (id.includes('education')) return <BookOpen className="w-3.5 h-3.5 text-blue-400" />;
    if (id.includes('medical')) return <Stethoscope className="w-3.5 h-3.5 text-emerald-400" />;
    if (id.includes('ai')) return <Cpu className="w-3.5 h-3.5 text-purple-400" />;
    return <Sparkles className="w-3.5 h-3.5 text-indigo-400" />;
  };

  return (
    <div className="space-y-4">
      {/* LANDING PAGE EXPLANATORY BANNER */}
      <div className="glass-panel p-5 rounded-2xl border-indigo-500/30 bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950/40 shadow-2xl">
        <div className="flex items-start gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 shrink-0">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <h2 className="text-lg font-black text-slate-100 tracking-tight">
              Evidence Boundary AI
            </h2>
            <p className="text-xs font-semibold text-indigo-300 italic">
              "Don't just verify the claim. Find where the evidence ends."
            </p>
            <p className="text-xs text-slate-300 leading-relaxed pt-1">
              Unlike a yes/no fact checker, this system examines the relationship between a claim and its evidence and identifies where the claim extends beyond what the evidence establishes.
            </p>
          </div>
        </div>
      </div>

      {/* CLAIM INPUT BOX */}
      <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4 shadow-xl">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <label className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Search className="w-4 h-4 text-indigo-400" />
            Enter Claim to Stress-Test
          </label>
          <span className="text-[11px] font-semibold text-amber-400">
            {demoMode ? '⚡ DEMO MODE — Illustrative Data Active' : '🌐 LIVE MODE — OpenAlex Search Active'}
          </span>
        </div>

        <div className="relative">
          <textarea
            value={claimText}
            onChange={(e) => setClaimText(e.target.value)}
            placeholder="e.g. AI tutoring caused a 35% increase in exam scores because students receive personalized feedback..."
            rows={3}
            className="w-full bg-slate-900/90 border border-slate-800 focus:border-indigo-500 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all resize-none font-medium"
          />
          
          <div className="absolute bottom-3 right-3 flex items-center gap-2">
            <button
              onClick={() => onVerify()}
              disabled={loading || !claimText.trim()}
              className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Analyzing Boundary...</span>
                </>
              ) : (
                <>
                  <span>VERIFY CLAIM</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>

        {/* Quick Pick Sample Scenarios */}
        <div className="pt-1 flex flex-wrap items-center gap-2">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mr-1">
            Sample Claims:
          </span>
          {scenarios.map((sc) => (
            <button
              key={sc.scenario_id}
              onClick={() => onSelectScenario(sc)}
              className="glass-panel px-3 py-1.5 rounded-lg border-slate-800 hover:border-indigo-500/40 text-xs font-medium text-slate-300 hover:text-white transition-all flex items-center gap-2 bg-slate-900/60"
            >
              {getScenarioIcon(sc.scenario_id)}
              <span>{sc.title}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
