import React from 'react';
import { ShieldCheck, GitBranch, Network, FileCheck, Lock, Clock } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="mt-12 border-t border-slate-800/80 bg-slate-950/80 p-6 rounded-2xl space-y-6">
      
      {/* P2 Roadmap Banner: Designed for, not yet implemented */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-indigo-400" />
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Architecture Roadmap (Designed for, not yet implemented in P0/P1 MVP):
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 text-xs">
          
          <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 text-indigo-400 font-bold">
              <Network className="w-3.5 h-3.5" />
              <span>Evidence Independence Graph</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Provenance visualizer detecting citation overlap & circular reference loops.
            </p>
          </div>

          <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 text-purple-400 font-bold">
              <Clock className="w-3.5 h-3.5" />
              <span>Temporal Evidence Lifecycle</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Tracking decay of empirical validity over multi-year study windows.
            </p>
          </div>

          <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 text-emerald-400 font-bold">
              <FileCheck className="w-3.5 h-3.5" />
              <span>Evidence Passport Export</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Exportable PDF/JSON evidentiary audit certificate for compliance teams.
            </p>
          </div>

          <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 text-amber-400 font-bold">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Adaptive Verification L1-L6</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Multi-tiered depth modes from rapid sanity checks to full meta-analyses.
            </p>
          </div>

          <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 text-pink-400 font-bold">
              <Lock className="w-3.5 h-3.5" />
              <span>Security Hardening Suite</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Prompt injection isolation sandbox for untrusted external literature.
            </p>
          </div>

          <div className="bg-slate-900/60 p-3 rounded-xl border border-slate-800 space-y-1">
            <div className="flex items-center gap-1.5 text-blue-400 font-bold">
              <GitBranch className="w-3.5 h-3.5" />
              <span>Multi-way Conflict Taxonomy</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Categorizing evidence disagreements by methodology vs sample bias.
            </p>
          </div>

        </div>
      </div>

      <div className="border-t border-slate-800/60 pt-4 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500 font-medium">
        <span>EVIDENCE BOUNDARY AI &copy; 2026 — Built for Hackathon Excellence</span>
        <span>Tagline: "Don't just verify the claim. Find where the evidence ends."</span>
      </div>

    </footer>
  );
}
