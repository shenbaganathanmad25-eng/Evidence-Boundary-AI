import React from 'react';
import { ShieldAlert, Database, Zap, ExternalLink } from 'lucide-react';

export default function Header({ demoMode, setDemoMode }) {
  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
        
        {/* Brand & Tagline */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-600 to-pink-500 p-0.5 shadow-lg shadow-indigo-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <ShieldAlert className="w-5 h-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-black tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-300 bg-clip-text text-transparent">
                EVIDENCE BOUNDARY <span className="text-indigo-400">AI</span>
              </h1>
              
              {/* Prominent DEMO MODE Active Badge */}
              {demoMode && (
                <span className="text-[11px] font-extrabold px-2.5 py-0.5 rounded-md bg-amber-500/20 text-amber-300 border border-amber-500/40 uppercase tracking-widest flex items-center gap-1 shadow-lg shadow-amber-500/10 animate-pulse">
                  <Database className="w-3 h-3 text-amber-400" />
                  DEMO MODE ACTIVE
                </span>
              )}
            </div>
            <p className="text-xs text-slate-400 font-medium italic">
              "Don't just verify the claim. Find where the evidence ends."
            </p>
          </div>
        </div>

        {/* Demo Mode Toggle & Status */}
        <div className="flex items-center gap-3">
          <div className="glass-panel px-3 py-1.5 rounded-lg flex items-center gap-3 border-indigo-500/20">
            <div className="flex items-center gap-2">
              {demoMode ? (
                <Database className="w-4 h-4 text-amber-400" />
              ) : (
                <Zap className="w-4 h-4 text-emerald-400" />
              )}
              <div className="text-left">
                <div className="text-xs font-semibold text-slate-200">
                  {demoMode ? 'Demo Mode' : 'Live Literature Search'}
                </div>
                <div className="text-[10px] text-slate-400">
                  {demoMode ? 'Deterministic Fixtures' : 'OpenAlex Academic API'}
                </div>
              </div>
            </div>

            {/* Switch Toggle */}
            <button
              onClick={() => setDemoMode(!demoMode)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500/50 ${
                demoMode ? 'bg-amber-600' : 'bg-emerald-600'
              }`}
              title="Toggle between Deterministic Demo Scenarios and Live OpenAlex Literature Search"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  demoMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          <a
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            className="text-xs text-slate-400 hover:text-indigo-300 transition-colors hidden sm:flex items-center gap-1"
          >
            <span>Docs</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>

      </div>
    </header>
  );
}
