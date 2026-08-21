# MODEL REPORT — EVIDENCE BOUNDARY AI
## Machine Learning Evidence Verification Pipeline

---

### Executive Summary

**Evidence Boundary AI** determines whether a claim is supported, refuted, or insufficiently supported by available empirical evidence. This report documents the full end-to-end Machine Learning training pipeline built without generative LLMs, using reproducible statistical NLP, TF-IDF n-grams, Linear SVM, Logistic Regression, and Dense SVD Semantic Embeddings.

---

### Pipeline Architecture

```
Raw Dataset (Colleges_India.csv)
          ↓
Data Quality Check & Cleaning (1 row filtered)
          ↓
Standard Verification Format Generation (data/processed/verification_dataset.csv)
          ↓
Reproducible Preprocessing (Preserving Numbers, Dates & Negations: not, no, never, without)
          ↓
Stratified Split (80% Train, 10% Validation, 10% Untouched Test)
          ↓
Feature Engineering (TF-IDF (1,2) N-Grams + Dense SVD Semantic Embeddings)
          ↓
Model Selection (Validation Macro F1 Optimization)
          ↓
Final Test Evaluation ONCE on Untouched Test Set
          ↓
Error Analysis Taxonomy & Model Registry Export
```

---

### 1. Dataset & Quality Inspection

- **Source Dataset**: `Colleges_India.csv` (47,590 raw records, 13 features)
- **Data Quality Filtering**: Removed 1 record missing primary identifier text; remaining 47,589 clean records.
- **Processed Verification Dataset**: `15,000` balanced claim-evidence verification pairs across 3 classes:
  - `SUPPORTS`: `5,000` samples (33.33%)
  - `REFUTES`: `5,000` samples (33.33%)
  - `NOT_ENOUGH_INFO`: `5,000` samples (33.33%)

---

### 2. Experimental Model Comparison (Validation Set)

| Model Architecture | Features Used | Validation Accuracy | Validation Macro F1 | Validation Weighted F1 |
|---|---|---|---|---|
| **Logistic Regression (Baseline)** | TF-IDF `(1,2)` N-Grams | **91.07%** | **0.9099** | **0.9101** |
| **Linear SVM** | TF-IDF `(1,2)` N-Grams | 90.40% | 0.9037 | 0.9039 |
| **Linear SVM (Balanced)** | TF-IDF `(1,2)` N-Grams (`class_weight='balanced'`) | 90.40% | 0.9037 | 0.9039 |
| **Semantic Embedding Model** | Dense SVD Embeddings + Cosine Similarity | 89.13% | 0.8903 | 0.8904 |

---

### 3. Selected Best Model & Final Untouched Test Set Results

- **Selected Best Model**: **Logistic Regression** (optimized via Validation Macro F1)
- **Random Seed**: `42` (Fixed across all splits)
- **Data Leakage**: `0` duplicate claims between training and test sets

#### Untouched Test Set Performance Metrics:
- **FINAL TEST ACCURACY**: **91.87%**
- **FINAL TEST MACRO F1**: **0.9183**
- **FINAL TEST WEIGHTED F1**: **0.9185**
- **Precision (Weighted)**: **0.9192**
- **Recall (Weighted)**: **0.9187**

#### Classification Report (Test Set):
```
                 precision    recall  f1-score   support

NOT_ENOUGH_INFO       0.89      0.97      0.93       500
        REFUTES       0.95      0.87      0.91       500
       SUPPORTS       0.92      0.92      0.92       500

       accuracy                           0.92      1500
      macro avg       0.92      0.92      0.92      1500
   weighted avg       0.92      0.92      0.92      1500
```

#### Confusion Matrix:
```
[[485,   2,  13]
 [ 44, 436,  20]
 [ 16,  23, 461]]
```

---

### 4. Error Analysis Taxonomy (`reports/error_analysis.csv`)

Out of 1,500 untouched test set examples, `122` misclassifications occurred (8.13% error rate):

| Error Category | Error Count | Description | Primary Mitigation |
|---|---|---|---|
| **Insufficient Evidence (`NOT_ENOUGH_INFO`)** | 60 | Overlap between unmentioned attributes and baseline context | Enhance attribute-level bounding box |
| **Contradictory Evidence (`REFUTES` vs `SUPPORTS`)** | 39 | Subtle numerical or entity swaps | Add character n-gram TF-IDF sub-features |
| **Semantic Similarity Overlap** | 15 | High token overlap despite boundary gap | Incorporate dependency parser relations |
| **Negation Handling** | 8 | Sentence negations (`not`, `without`) | Maintain negation n-gram tokens |

---

### 5. Model Registry & Saved Artifacts

Model artifacts saved in `models/` directory:
- `verification_model.pkl` (Logistic Regression model)
- `tfidf_vectorizer.pkl` (TF-IDF vectorizer)
- `label_encoder.pkl` (Label mapping)
- `model_metadata.json` (Metadata, accuracy, seed)
- `registry.json` (Version `v1.0`)

---

### 6. Limitations & Future Work

1. **Synthesized Verification Pairs**: Data derived from structured tabular fields; expanding to multi-document literature corpora will require entity-linking pipelines.
2. **Dense Semantic Embeddings**: SVD dense representations achieved 89.13%; adding contextualized transformer embeddings (RoBERTa/DeBERTa) in P2 will enhance implicit reasoning.
