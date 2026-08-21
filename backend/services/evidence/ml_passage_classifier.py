import os
import logging
from typing import Dict, Any, Tuple
import joblib
from models.evidence import SupportDirectionEnum

logger = logging.getLogger("evidence_boundary.ml_passage_classifier")

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LABEL_MAPPING = {
    "SUPPORTS": "SUPPORTING",
    "REFUTES": "CONTRADICTING",
    "NOT_ENOUGH_INFO": "NEUTRAL",
    "SUPPORTING": "SUPPORTING",
    "CONTRADICTING": "CONTRADICTING",
    "NEUTRAL": "NEUTRAL"
}

class MLPassageClassifier:
    """Trained Supervised ML Classifier (TF-IDF + Logistic Regression) for predicting evidence SupportDirection."""

    def __init__(self):
        self.classifier = None
        self.vectorizer = None
        self.label_encoder = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        # Priority 1: Check models/ or models_dir/ for verification_model.pkl & tfidf_vectorizer.pkl
        candidate_dirs = [
            os.path.join(BACKEND_DIR, "models"),
            os.path.join(BACKEND_DIR, "models_dir"),
            os.path.join(os.path.dirname(BACKEND_DIR), "models")
        ]

        for m_dir in candidate_dirs:
            model_p = os.path.join(m_dir, "verification_model.pkl")
            vec_p = os.path.join(m_dir, "tfidf_vectorizer.pkl")
            enc_p = os.path.join(m_dir, "label_encoder.pkl")

            if not os.path.exists(model_p):
                model_p = os.path.join(m_dir, "evidence_classifier.pkl")

            if os.path.exists(model_p) and os.path.exists(vec_p):
                try:
                    classifier = joblib.load(model_p)
                    vectorizer = joblib.load(vec_p)
                    
                    # Verify feature count compatibility
                    test_vec = vectorizer.transform(["test [SEP] test"])
                    if hasattr(classifier, "n_features_in_") and classifier.n_features_in_ != test_vec.shape[1]:
                        logger.warning(f"Feature count mismatch at {m_dir} ({test_vec.shape[1]} vs {classifier.n_features_in_}). Skipping.")
                        continue

                    self.classifier = classifier
                    self.vectorizer = vectorizer
                    if os.path.exists(enc_p):
                        self.label_encoder = joblib.load(enc_p)
                    
                    self.is_loaded = True
                    logger.info(f"Successfully loaded matching ML Classifier from: {m_dir}")
                    return
                except Exception as e:
                    logger.error(f"Error loading model from {m_dir}: {e}")
                    continue

        logger.warning("No matching ML model files found. Using heuristic fallback.")
        self.is_loaded = False

    def classify_passage(
        self,
        subclaim_text: str,
        passage_text: str,
        confidence_threshold: float = 0.40
    ) -> Dict[str, Any]:
        """Classifies evidence passage relative to subclaim text into SUPPORTING, CONTRADICTING, or NEUTRAL with probabilities."""
        if not self.is_loaded:
            self._load_model()

        if not self.is_loaded:
            return self._heuristic_fallback(subclaim_text, passage_text)

        try:
            combined_input = f"{subclaim_text.lower().strip()} [SEP] {passage_text.lower().strip()}"
            X_vec = self.vectorizer.transform([combined_input])
            
            if hasattr(self.classifier, "predict_proba"):
                probs = self.classifier.predict_proba(X_vec)[0]
                classes = self.classifier.classes_
            else:
                scores = self.classifier.decision_function(X_vec)[0]
                exp_s = np.exp(scores - np.max(scores))
                probs = exp_s / np.sum(exp_s)
                classes = self.classifier.classes_

            if self.label_encoder is not None:
                raw_labels = self.label_encoder.inverse_transform(classes)
            else:
                raw_labels = classes

            prob_dict = {"SUPPORTING": 0.0, "CONTRADICTING": 0.0, "NEUTRAL": 0.0}
            for raw_lbl, prob in zip(raw_labels, probs):
                mapped_lbl = LABEL_MAPPING.get(str(raw_lbl).upper(), "NEUTRAL")
                prob_dict[mapped_lbl] = max(prob_dict[mapped_lbl], float(prob))

            predicted_label = max(prob_dict, key=prob_dict.get)
            max_prob = prob_dict[predicted_label]

            if max_prob < confidence_threshold:
                final_label = "NEUTRAL"
            else:
                final_label = predicted_label

            return {
                "label": final_label,
                "raw_prediction": predicted_label,
                "confidence": round(max_prob, 4),
                "probabilities": {
                    "SUPPORTING": round(prob_dict["SUPPORTING"], 4),
                    "CONTRADICTING": round(prob_dict["CONTRADICTING"], 4),
                    "NEUTRAL": round(prob_dict["NEUTRAL"], 4),
                }
            }
        except Exception as e:
            logger.error(f"Error in classify_passage: {e}. Falling back to heuristic.")
            return self._heuristic_fallback(subclaim_text, passage_text)

    def _heuristic_fallback(self, subclaim: str, passage: str) -> Dict[str, Any]:
        pass_lower = passage.lower()

        if any(w in pass_lower for w in ["failed to", "no evidence", "contradict", "zero impact", "unaffected"]):
            label = "CONTRADICTING"
            probs = {"SUPPORTING": 0.10, "CONTRADICTING": 0.80, "NEUTRAL": 0.10}
        elif any(w in pass_lower for w in ["proved", "supported", "improved", "scored higher", "increased", "reduced plasma"]):
            label = "SUPPORTING"
            probs = {"SUPPORTING": 0.82, "CONTRADICTING": 0.08, "NEUTRAL": 0.10}
        else:
            label = "NEUTRAL"
            probs = {"SUPPORTING": 0.20, "CONTRADICTING": 0.20, "NEUTRAL": 0.60}

        return {
            "label": label,
            "raw_prediction": label,
            "confidence": probs[label],
            "probabilities": probs
        }
