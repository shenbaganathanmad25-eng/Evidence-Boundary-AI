# EVIDENCE BOUNDARY AI

> **Tagline:** *"Don't just verify the claim. Find where the evidence ends."*

![Evidence Boundary AI](/docs/banner.png)

---

## 🎯 Positioning & Core Philosophy

**EVIDENCE BOUNDARY AI** is a hackathon-grade AI verification platform built to solve a critical limitation of modern AI fact-checkers and simple RAG systems: **binary verification masks hidden boundary extrapolations.**

Most AI claims are not 100% false; they take a **small kernel of empirical truth** and **over-extrapolate it** into unverified universal assertions.

**Evidence Boundary AI answers five critical questions:**
1. **What exactly is the claim saying?** (Decomposed into granular subclaims)
2. **What does the evidence actually establish?** (Empirical supported boundary)
3. **Where does the claim go beyond the evidence?** (Extrapolated unsupported gap)
4. **What evidence would be required to support the unsupported portion?** (Missing evidence requirements & killer questions)
5. **How robust is the claim when its evidence is deliberately attacked?** (Claim Fragility Score & EBDF stress testing)

---

## 🛠️ Architecture & Pipeline Overview

```
User Claim ──► Claim Decomposition ──► Evidence Retrieval ──► Evidence Normalization
                                                                      │
Final Verdict ◄── Fragility Score ◄── EBDF Stress Testing ◄───────────┘
```

### The Evidence Boundary Delta Framework (EBDF)
1. **\(\Delta\text{Scope}\)**: Population & sample demographic shifts.
2. **\(\Delta\text{Certainty}\)**: Modal elevation from correlation to direct causation.
3. **\(\Delta\text{Temporal}\)**: Extrapolating short-term trials over multi-year windows.
4. **\(\Delta\text{Causal}\)**: Confounding mechanisms and unisolated variables.

---

## 🚀 Key Features

### P0 (Core Demo Features - Fully Working)
- ⚡ **Demo Mode Engine**: Built-in, deterministic pre-packaged scenarios across Education, Medicine, and AI Benchmarks that work instantly without API rate limits or network dependency.
- ⚖️ **Visual Evidence Boundary Map**: Split-screen dashboard contrasting the **Supported Evidence Boundary** (with citations & sample sizes) against the **Unsupported / Extrapolated Boundary** (with boundary gap callouts).
- 🔥 **Claim Fragility Score (0 - 100%)**: Deterministic score calculation with full metric transparency (Unsupported boundary gap penalty + Stress test failure penalty + EBDF delta penalty).
- 💥 **Evidence Boundary Stress-Test Engine**: Interactive attack vector launcher allowing custom perturbation attacks against any claim scenario.
- 🏆 **Final Verdict Banner**: High-impact badge classification (`VERIFIED`, `INSUFFICIENTLY VERIFIED`, `REFUTED`).

### P1 (Extended Intelligence Features - Fully Working)
- 🌐 **OpenAlex Academic Evidence Provider**: Live integration with OpenAlex academic graph for real peer-reviewed paper search.
- ❓ **Killer Question Engine**: Automated generation of boundary-testing questions aimed at uncovering implicit assumptions.
- 🔍 **Missing Evidence Finder**: Specific empirical trial or longitudinal data requirements needed to reach full verification.
- 🧬 **Evidence Mutation Detector**: Highlighting phrasing exaggerations between original source quotes and claim assertions.

### P2 (Roadmap & Architectural Design - "Designed for, not yet implemented")
- 🕸️ **Evidence Independence Graph**: Provenance graph detecting citation overlap & circular reference loops.
- ⌛ **Temporal Evidence Lifecycle**: Tracking decay of empirical validity over multi-year study windows.
- 📜 **Evidence Passport Export**: Exportable PDF/JSON evidentiary audit certificate for compliance teams.
- 🛡️ **Security Hardening Suite**: Prompt injection isolation sandbox for untrusted external literature.

---

## 📦 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Start the Backend API (FastAPI)
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
API Documentation will be live at `http://127.0.0.1:8000/docs`.

### 2. Start the Frontend (Vite + React)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 📸 Final Verdict Types

| Verdict | Description |
| :--- | :--- |
| **VERIFIED** | All decomposed subclaims fall within supported empirical boundaries. |
| **INSUFFICIENTLY VERIFIED** | Initial premise is backed by evidence, but secondary assertions exceed empirical scope. |
| **REFUTED** | Core assertions are contradicted by peer-reviewed literature or neuroimaging/PET data. |

---

## 📜 Technical Principles

- **Deterministic Transparency**: Every score traces back to visible evidence gaps and stress-test failure rates.
- **Untrusted External Data**: External evidence is isolated and sanitized.
- **No Fabricated Sources**: All citations derive from verified OpenAlex IDs or curated STAR/Cochrane benchmark datasets.

*Built for Hackathon Excellence.*
