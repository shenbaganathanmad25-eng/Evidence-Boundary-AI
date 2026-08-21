import sys
import os
import json
import joblib
import numpy as np

def load_prediction_artifacts():
    model_dir = "models"
    if not os.path.exists(os.path.join(model_dir, "verification_model.pkl")):
        model_dir = "models_dir"
    if not os.path.exists(os.path.join(model_dir, "verification_model.pkl")):
        model_dir = "../models"

    model = joblib.load(os.path.join(model_dir, "verification_model.pkl"))
    vectorizer = joblib.load(os.path.join(model_dir, "tfidf_vectorizer.pkl"))
    label_encoder = joblib.load(os.path.join(model_dir, "label_encoder.pkl"))
    
    meta_path = os.path.join(model_dir, "model_metadata.json")
    version = "v1.0"
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            version = meta.get("dataset_version", "v1.0")

    return model, vectorizer, label_encoder, version

def predict(claim: str, evidence: str) -> dict:
    """Accepts claim and evidence strings and returns prediction, confidence, model_version, similarity_score."""
    model, vectorizer, label_encoder, version = load_prediction_artifacts()

    claim_clean = claim.strip().lower()
    evidence_clean = evidence.strip().lower()

    combined = f"{claim_clean} [SEP] {evidence_clean}"
    X_vec = vectorizer.transform([combined])

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_vec)[0]
        pred_idx = np.argmax(probs)
        confidence = float(probs[pred_idx])
    else:
        scores = model.decision_function(X_vec)[0]
        pred_idx = np.argmax(scores)
        confidence = float(1.0 / (1.0 + np.exp(-max(scores))))

    prediction_label = label_encoder.inverse_transform([pred_idx])[0]

    claim_words = set(claim_clean.split())
    ev_words = set(evidence_clean.split())
    intersection = claim_words.intersection(ev_words)
    union = claim_words.union(ev_words)
    sim_score = float(len(intersection) / max(1, len(union)))

    if confidence < 0.40:
        prediction_label = "NOT_ENOUGH_INFO"

    return {
        "prediction": str(prediction_label),
        "confidence": round(confidence, 4),
        "model_version": str(version),
        "similarity_score": round(sim_score, 4)
    }

if __name__ == "__main__":
    if len(sys.argv) > 2:
        c = sys.argv[1]
        e = sys.argv[2]
    else:
        c = "Jawaharlal Nehru Rajkeeya Mahavidyalaya is located in Nicobars district, Andaman and Nicobar Islands."
        e = "College: Jawaharlal Nehru Rajkeeya Mahavidyalaya (affiliated college). Location: Nicobars, Andaman and Nicobar Islands. Management: Central Government."

    res = predict(c, e)
    print(json.dumps(res, indent=2))
