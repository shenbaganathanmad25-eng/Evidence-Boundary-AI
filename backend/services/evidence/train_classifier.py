import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BACKEND_DIR, "data", "evidence_training.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models_dir")
CLASSIFIER_PATH = os.path.join(MODELS_DIR, "evidence_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")

def train_and_save_classifier():
    """Trains TF-IDF + Logistic Regression ML Evidence Classifier and evaluates performance metrics."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Training dataset not found at: {DATA_PATH}")

    # Load dataset
    df = pd.read_csv(DATA_PATH)
    
    # Combine subclaim and evidence text for feature representation
    df['combined_text'] = df['subclaim'].astype(str) + " [SEP] " + df['evidence'].astype(str)
    X = df['combined_text']
    y = df['label']

    # Train/Test split with fixed random seed
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000, stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Logistic Regression Classifier
    classifier = LogisticRegression(C=1.0, max_iter=200, random_state=42)
    classifier.fit(X_train_tfidf, y_train)

    # Predictions & Evaluation
    y_pred = classifier.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_test, y_pred, labels=["SUPPORTING", "CONTRADICTING", "NEUTRAL"])

    print("=== ML EVIDENCE CLASSIFIER EVALUATION ===")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("Confusion Matrix (SUPPORTING, CONTRADICTING, NEUTRAL):")
    print(cm)
    print("=========================================")

    # Save artifacts
    joblib.dump(classifier, CLASSIFIER_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Saved trained ML model to: {CLASSIFIER_PATH}")
    print(f"Saved TF-IDF vectorizer to: {VECTORIZER_PATH}")

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "confusion_matrix": cm.tolist()
    }

if __name__ == "__main__":
    train_and_save_classifier()
