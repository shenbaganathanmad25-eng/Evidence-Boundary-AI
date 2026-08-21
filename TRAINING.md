# TRAINING AND REPRODUCIBILITY GUIDE
## Evidence Boundary AI — ML Evidence Verification Pipeline

This document provides step-by-step instructions to reproduce the dataset preparation, model training, evaluation, inference, and API deployment for **Evidence Boundary AI**.

---

### 1. Environment & Prerequisites

- **Python Version**: `Python 3.13` (or 3.10+)
- **Fixed Random Seed**: `42`
- **Key Libraries**: `scikit-learn`, `pandas`, `numpy`, `joblib`, `fastapi`, `uvicorn`

Install dependencies:
```bash
pip install -r requirements.txt
```

---

### 2. Step 1: Prepare Dataset

To convert raw college metadata into standard claim-evidence verification pairs (`SUPPORTS`, `REFUTES`, `NOT_ENOUGH_INFO`):

```bash
cd backend
python scripts/prepare_dataset.py
```

Output file created:
- `data/processed/verification_dataset.csv` (15,000 to 75,000 balanced records)

---

### 3. Step 2: Train & Evaluate Models

To run the complete reproducible training pipeline (TF-IDF extraction, Logistic Regression, Linear SVM, and Semantic SVD Embedding model):

```bash
cd backend
python scripts/train_verification_model.py
```

Execution Workflow:
1. Preprocesses claim and evidence text (preserving numbers, dates, and negation keywords `not`, `no`, `never`, `without`).
2. Stratified 80/10/10 split with random seed `42`.
3. Checks for data leakage between train and test sets.
4. Trains Logistic Regression baseline, Linear SVM, and Dense Semantic SVD Embedding model.
5. Evaluates model selection strictly on the validation set.
6. Evaluates selected best model ONCE on the untouched test set.
7. Performs automated error analysis and saves artifacts.

---

### 4. Output Artifacts Generated

Model Artifacts (`models/`):
- `verification_model.pkl`: Serialized trained classifier model
- `tfidf_vectorizer.pkl`: Fitted TF-IDF feature vectorizer
- `label_encoder.pkl`: Label encoder mapping `SUPPORTS`, `REFUTES`, `NOT_ENOUGH_INFO`
- `model_metadata.json`: Model version, training parameters, accuracy, macro F1, and random seed
- `registry.json`: Version control registry

Evaluation Reports (`reports/`):
- `reports/final_evaluation.txt`: Untouched test set metrics, classification report, and confusion matrix
- `reports/error_analysis.csv`: Categorized error taxonomy

---

### 5. Step 3: Run Inference

To classify a single claim and evidence pair via CLI:

```bash
python predict.py "Jawaharlal Nehru Rajkeeya Mahavidyalaya is located in Nicobars." "College: Jawaharlal Nehru Rajkeeya Mahavidyalaya. Location: Nicobars, Andaman."
```

Example JSON Output:
```json
{
  "prediction": "SUPPORTS",
  "confidence": 0.9812,
  "model_version": "v1.0-Colleges_India",
  "similarity_score": 0.4500
}
```

---

### 6. Step 4: Start REST API Server

To launch the FastAPI production server providing `POST /predict` and `GET /health`:

```bash
cd backend
python main.py
```

API Endpoints:
- `POST http://127.0.0.1:8000/predict`
- `GET http://127.0.0.1:8000/health`
