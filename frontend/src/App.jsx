import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ClaimInput from './components/ClaimInput';
import SubclaimDecompositionView from './components/SubclaimDecompositionView';
import BoundaryMap from './components/BoundaryMap';
import StressTestPanel from './components/StressTestPanel';
import FragilityGauge from './components/FragilityGauge';
import VerdictBanner from './components/VerdictBanner';
import P1ExtensionsPanel from './components/P1ExtensionsPanel';
import Footer from './components/Footer';
import { fetchScenarios, verifyClaim, decomposeClaim } from './services/api';

export default function App() {
  const [demoMode, setDemoMode] = useState(true);
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [claimText, setClaimText] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [decomposedSubclaims, setDecomposedSubclaims] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load scenarios on mount
  useEffect(() => {
    async function init() {
      try {
        const scList = await fetchScenarios();
        setScenarios(scList);
        if (scList.length > 0) {
          const firstSc = scList[0];
          setSelectedScenario(firstSc);
          setClaimText(firstSc.raw_claim);
          handleVerify(firstSc.raw_claim, true, firstSc.scenario_id);
        }
      } catch (err) {
        console.error('Failed to initialize scenarios:', err);
      }
    }
    init();
  }, []);

  const handleSelectScenario = (sc) => {
    setSelectedScenario(sc);
    setClaimText(sc.raw_claim);
    handleVerify(sc.raw_claim, demoMode, sc.scenario_id);
  };

  const handleVerify = async (textToVerify = claimText, isDemo = demoMode, scId = selectedScenario?.scenario_id) => {
    if (!textToVerify.trim()) return;
    setLoading(true);
    setError(null);
    try {
      // 1. Fetch full verification response
      const data = await verifyClaim(textToVerify, isDemo, scId);
      setVerificationResult(data);

      // 2. Fetch folded claim decomposition with EBDF severities
      const decomp = await decomposeClaim(textToVerify);
      setDecomposedSubclaims(decomp.subclaims || []);
    } catch (err) {
      console.error('Verification error:', err);
      setError(err.message || 'Failed to analyze evidence boundary.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Header */}
      <Header demoMode={demoMode} setDemoMode={setDemoMode} />

      {/* Main Dashboard Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        
        {/* Claim Input & Landing Page Explanatory Banner */}
        <ClaimInput
          claimText={claimText}
          setClaimText={setClaimText}
          scenarios={scenarios}
          onSelectScenario={handleSelectScenario}
          onVerify={() => handleVerify(claimText, demoMode, null)}
          loading={loading}
          demoMode={demoMode}
        />

        {/* Error alert if any */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-950/60 border border-rose-500/50 text-rose-200 text-xs font-semibold">
            ⚠️ Verification Error: {error}
          </div>
        )}

        {/* Complete Dashboard Screen Hierarchy */}
        {verificationResult && (
          <div className="space-y-6">
            
            {/* 1. CLAIM DECOMPOSITION & 2. ML CLAIM CLASSIFICATION */}
            {decomposedSubclaims.length > 0 && (
              <SubclaimDecompositionView subclaims={decomposedSubclaims} />
            )}

            {/* 3. EVIDENCE BOUNDARY MAP & 4. EVIDENCE LIST & 5. ML EVIDENCE CLASSIFICATION */}
            <BoundaryMap
              subClaims={verificationResult.sub_claims}
              evidence={verificationResult.evidence}
              decomposedSubclaims={decomposedSubclaims}
            />

            {/* 6. ML EVIDENCE BOUNDARY STRESS TEST */}
            <StressTestPanel
              ebdfDeltas={verificationResult.ebdf_deltas}
              stressTests={verificationResult.stress_test_results}
              scenarioId={verificationResult.claim_id}
              baselineVerdict={verificationResult.verdict}
            />

            {/* 7. REPRODUCIBLE CLAIM FRAGILITY SCORE */}
            <FragilityGauge fragility={verificationResult.fragility} />

            {/* 8. FINAL VERDICT BANNER */}
            <VerdictBanner
              verdict={verificationResult.verdict}
              justification={verificationResult.verdict_justification}
              boundarySummary={verificationResult.boundary_summary}
              domain={verificationResult.domain}
            />

            {/* P1 Extensions (Killer Questions & Missing Evidence) */}
            <P1ExtensionsPanel
              killerQuestions={verificationResult.killer_questions}
              missingRequirements={verificationResult.missing_evidence_requirements}
              mutations={verificationResult.evidence_mutations}
            />

          </div>
        )}

        {/* Footer with P2 Roadmap */}
        <Footer />

      </main>
    </div>
  );
}
