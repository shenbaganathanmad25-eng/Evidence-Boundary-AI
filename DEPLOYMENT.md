# PRODUCTION DEPLOYMENT GUIDE
## Evidence Boundary AI

This document provides step-by-step options to deploy **Evidence Boundary AI** locally or to cloud platforms.

---

### Option 1: Local Single-Port Production Server (Recommended for Demos)

1. Build the production React frontend bundle:
   ```bash
   cd frontend
   npm run build
   ```

2. Start the unified FastAPI backend server:
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. Open your browser:
   - **Unified Application Dashboard**: `http://localhost:8000`
   - **Interactive API Docs (Swagger)**: `http://localhost:8000/docs`
   - **ML Prediction Endpoint**: `POST http://localhost:8000/predict`
   - **Health Check Endpoint**: `GET http://localhost:8000/health`

---

### Option 2: Docker Container Deployment

1. Build and run using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

2. Or using Docker CLI directly:
   ```bash
   docker build -t evidence-boundary-ai .
   docker run -d -p 8000:8000 evidence-boundary-ai
   ```

---

### Option 3: Deploy to Cloud (Render / Railway / GCP Cloud Run)

#### Deploy to Render:
1. Connect your repository to Render.
2. Choose **Web Service** with **Docker** runtime.
3. Render automatically reads `Dockerfile`, exposes port `8000`, and deploys.

#### Deploy to GCP Cloud Run:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/evidence-boundary-ai
gcloud run deploy evidence-boundary-ai --image gcr.io/YOUR_PROJECT_ID/evidence-boundary-ai --platform managed --port 8000 --allow-unauthenticated
```

---

### Verification Checklist

- [x] Production Frontend Built (`frontend/dist/`)
- [x] Model Artifacts Synchronized (`models/verification_model.pkl`, `models/tfidf_vectorizer.pkl`)
- [x] Static Asset Middleware Configured in FastAPI ([backend/main.py](file:///e:/EB/backend/main.py))
- [x] Dockerfile Multi-Stage Build Tested ([Dockerfile](file:///e:/EB/Dockerfile))
