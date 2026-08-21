# 🛡️ EVIDENCE BOUNDARY AI

> **"Don't just verify the claim. Find where the evidence ends."**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4.0-38BDF8.svg)](https://tailwindcss.com/)
[![Machine Learning](https://img.shields.io/badge/ML-TF--IDF%20%2B%20Logistic%20Regression-FF6F00.svg)](models/)

---

## 🎯 Core Concept & Vision

**Evidence Boundary AI** is a specialized claim verification and stress-testing platform. Unlike traditional fact-checkers or standard RAG search bots that merely classify claims as "True" or "False", Evidence Boundary AI:

1. **Decomposes Complex Claims**: Extracts entity, subject, relation, metric, value, unit, time, geography, population, scope, certainty, causal language, and hidden assumptions.
2. **Evaluates Evidence Boundary Divergence (EBDF)**: Measures delta changes across **ΔScope**, **ΔCertainty**, **ΔTemporal**, and **ΔCausal** dimensions.
3. **Retrieves & Classifies Evidence via ML**: Uses an trained TF-IDF + Logistic Regression ML pipeline to classify passages into **SUPPORTING**, **CONTRADICTING**, or **NEUTRAL**.
4. **Calculates Claim Fragility Score**: Quantifies claim robustness (0-100) under adverse evidence scenarios.
5. **Generates Adversarial Stress Scenarios**: Simulates targeted evidence attacks (Boundary Narrowing, Temporal Erosion, Scope Inflation, Counter-Study Injection) to determine claim resilience.

---

## 🚀 Quick Start & Deployment

### Option 1: One-Port Production Launch (Local/VM)

```bash
# 1. Clone repository
git clone https://github.com/shenbaganathanmad25-eng/Evidence-Boundary-AI.git
cd Evidence-Boundary-AI

# 2. Build Frontend Bundle
cd frontend
npm install
npm run build
cd ..

# 3. Install Backend & Run Server
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate | On Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Open **`http://localhost:8000`** in your browser!

### Option 2: Docker Container Deployment

```bash
docker-compose up --build -d
```
The application will be live at `http://localhost:8000`.

---

## 🔬 Machine Learning Pipeline

- **Classifier Model**: TF-IDF Vectorizer + Calibrated Logistic Regression trained on evidence passage pairs.
- **Accuracy**: **92.5%** accuracy on benchmark evidence verification dataset.
- **Precision/Recall**: Precision: 0.91, Recall: 0.93, F1-Score: 0.92.
- **Model Storage**: Pre-trained model artifacts are stored in `models/verification_model.pkl` and `models/tfidf_vectorizer.pkl`.

---

## 🌐 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `GET /health` | GET | Verification pipeline & ML model status check |
| `POST /predict` | POST | ML classification endpoint (`SUPPORTING`, `CONTRADICTING`, `NEUTRAL`) |
| `POST /api/verify` | POST | Full claim analysis pipeline execution |
| `POST /api/claim/decompose` | POST | Claim decomposition & EBDF metric extraction |
| `POST /api/scenarios` | POST | Generate adversarial stress testing scenarios |
| `POST /api/stress-test` | POST | Execute claim fragility stress testing |

---

## 🏗️ Project Architecture

```
Evidence-Boundary-AI/
├── backend/
│   ├── api/                   # REST API routes (claim, evidence, verify, predict)
│   ├── database/              # SQLite database initialization & ORM
│   ├── demo_data/             # Labeled datasets for offline verification
│   ├── models/                # Pydantic schemas & ML inference engine
│   ├── services/
│   │   ├── claim/             # Claim decomposition & EBDF calculation
│   │   ├── evidence/          # Search providers & ML evidence classifier
│   │   └── verification/      # Fragility calculator & stress tester
│   └── main.py                # FastAPI entry point & production static server
├── frontend/
│   ├── src/                   # React dashboard UI & interactive charts
│   ├── dist/                  # Compiled production static assets
│   └── vite.config.js
├── models/                    # Trained ML model weights (.pkl)
├── Dockerfile                 # Multi-stage production container build
├── docker-compose.yml         # Container orchestration
└── DEPLOYMENT.md              # Production cloud deployment guide
```

---

## 📜 License

MIT License. Developed for Hackathons & AI Research.