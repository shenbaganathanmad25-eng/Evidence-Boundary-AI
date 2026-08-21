import os
import logging
from typing import Dict, Any, Tuple
import joblib
from models.evidence import SupportDirectionEnum

logger = logging.getLogger("evidence_boundary.ml_passage_classifier")

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BACKEND_DIR, "models_dir")
CLASSIFIER_PATH = os.path.join(MODELS_DIR, "evidence_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")

class MLPassageClassifier:
    """Trained Supervised ML Classifier (TF-IDF + Logistic Regression) for predicting evidence SupportDirection."""

    def __init__(self):
        self.classifier = None
        self.vectorizer = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        if os.path.exists(CLASSIFIER_PATH) and os.path.exists(VECTORIZER_PATH):
            try:
                self.classifier = joblib.load(CLASSIFIER_PATH)
                self.vectorizer = joblib.load(VECTORIZER_PATH)
                self.is_loaded = True
                logger.info("Loaded pre-trained ML Evidence Classifier from disk.")
            except Exception as e:
                logger.error(f"Error loading ML model files: {e}")
                self.is_loaded = False
        else:
            logger.warning(f"ML model files not found at {CLASSIFIER_PATH}. Will train or fallback.")
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

        combined_input = f"{subclaim_text} [SEP] {passage_text}"
        X_vec = self.vectorizer.transform([combined_input])
        
        # Get prediction probabilities across classes
        probs = self.classifier.predict_proba(X_vec)[0]
        classes = self.classifier.classes_

        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probs)}
        
        # Ensure all 3 labels exist in output dictionary
        for label in ["SUPPORTING", "CONTRADICTING", "NEUTRAL"]:
            if label not in prob_dict:
                prob_dict[label] = 0.0

        # Find max probability prediction
        predicted_label = max(prob_dict, key=prob_dict.get)
        max_prob = prob_dict[predicted_label]

        # Apply threshold rule: If max probability is below threshold, default to NEUTRAL
        if max_prob < confidence_threshold:
            final_label = "NEUTRAL"
            logger.info(f"ML Classifier prediction ({predicted_label} @ {max_prob:.2f}) below threshold {confidence_threshold}. Assigned NEUTRAL.")
        else:
            final_label = predicted_label

        return {
            "label": final_label,
            "raw_prediction": predicted_label,
            "confidence": round(max_prob, 4),
            "probabilities": {
                "SUPPORTING": round(prob_dict.get("SUPPORTING", 0.0), 4),
                "CONTRADICTING": round(prob_dict.get("CONTRADICTING", 0.0), 4),
                "NEUTRAL": round(prob_dict.get("NEUTRAL", 0.0), 4),
            }
        }

    def _heuristic_fallback(self, subclaim: str, passage: str) -> Dict[str, Any]:
        pass_lower = passage.lower()
        sub_lower = subclaim.lower()

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
