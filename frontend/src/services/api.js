export async function fetchHealth() {
  const res = await fetch('/api/health');
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchScenarios() {
  const res = await fetch('/api/scenarios');
  if (!res.ok) throw new Error('Failed to load scenarios');
  return res.json();
}

export async function verifyClaim(claimText, demoMode = true, scenarioId = null) {
  const res = await fetch('/api/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      claim: claimText,
      demo_mode: demoMode,
      scenario_id: scenarioId
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Verification request failed');
  }
  return res.json();
}

export async function decomposeClaim(claimText) {
  const res = await fetch('/api/claim/decompose', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ claim: claimText })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Claim decomposition failed');
  }
  return res.json();
}

export async function runCustomStressTest(scenarioId, attackType, customCondition) {
  const res = await fetch('/api/stress-test', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      scenario_id: scenarioId,
      attack_type: attackType,
      custom_condition: customCondition
    })
  });
  if (!res.ok) throw new Error('Stress test execution failed');
  return res.json();
}
