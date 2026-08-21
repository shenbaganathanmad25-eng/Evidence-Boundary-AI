import os
import sys
import json
import time
import re
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix
)
from sklearn.preprocessing import LabelEncoder

SEED = 42
np.random.seed(SEED)

def text_preprocess(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return re.sub(r'\s+', ' ', text).strip().lower()

def calc_vectorized_cosine(A, B):
    dot = np.sum(A * B, axis=1, keepdims=True)
    norm_a = np.linalg.norm(A, axis=1, keepdims=True)
    norm_b = np.linalg.norm(B, axis=1, keepdims=True)
    return dot / (norm_a * norm_b + 1e-9)

def train_and_evaluate_pipeline():
    start_time = time.time()
    
    csv_path = "data/processed/verification_dataset.csv"
    if not os.path.exists(csv_path):
        csv_path = "../data/processed/verification_dataset.csv"

    print(f"Loading standard verification dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    # Subsample 15,000 balanced samples (5,000 per class)
    if len(df) > 15000:
        samples = [df[df['label'] == lbl].sample(n=5000, random_state=SEED) for lbl in df['label'].unique()]
        df = pd.concat(samples, ignore_index=True).sample(frac=1.0, random_state=SEED).reset_index(drop=True)

    print(f"Dataset shape: {df.shape}")
    print("Label distribution:")
    print(df['label'].value_counts())

    df['clean_claim'] = df['claim'].apply(text_preprocess)
    df['clean_evidence'] = df['evidence'].apply(text_preprocess)
    df['combined_text'] = df['clean_claim'] + " [SEP] " + df['clean_evidence']

    X = df['combined_text'].values
    y_raw = df['label'].values

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    class_names = list(label_encoder.classes_)

    # 80% train, 10% val, 10% test
    X_train_text, X_temp_text, y_train, y_temp, claims_train, claims_temp, ev_train, ev_temp = train_test_split(
        X, y, df['clean_claim'].values, df['clean_evidence'].values,
        test_size=0.20, random_state=SEED, stratify=y
    )

    X_val_text, X_test_text, y_val, y_test, claims_val, claims_test, ev_val, ev_test = train_test_split(
        X_temp_text, y_temp, claims_temp, ev_temp,
        test_size=0.50, random_state=SEED, stratify=y_temp
    )

    print(f"\nDataset Splits:")
    print(f"  Training set: {len(X_train_text):,} samples (80%)")
    print(f"  Validation set: {len(X_val_text):,} samples (10%)")
    print(f"  Untouched Test set: {len(X_test_text):,} samples (10%)")

    # Data Leakage Check
    train_claims_set = set(claims_train)
    test_claims_set = set(claims_test)
    leakage_count = len(train_claims_set.intersection(test_claims_set))
    print(f"Data Leakage Check: {leakage_count} duplicate claims between train and test sets.")

    # TF-IDF Features (ngram_range=(1,2))
    print("\nExtracting TF-IDF Features (ngram_range=(1,2))...")
    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=20000, sublinear_tf=True)
    X_train_tfidf = tfidf.fit_transform(X_train_text)
    X_val_tfidf = tfidf.transform(X_val_text)
    X_test_tfidf = tfidf.transform(X_test_text)

    results = {}

    # MODEL 1: Logistic Regression
    print("\n--- Training Model 1: Logistic Regression ---")
    lr_model = LogisticRegression(random_state=SEED, max_iter=200, C=1.0)
    lr_model.fit(X_train_tfidf, y_train)

    val_preds_lr = lr_model.predict(X_val_tfidf)
    acc_lr = accuracy_score(y_val, val_preds_lr)
    prec_lr, rec_lr, f1_lr, _ = precision_recall_fscore_support(y_val, val_preds_lr, average=None)
    macro_f1_lr = np.mean(f1_lr)
    weighted_f1_lr = precision_recall_fscore_support(y_val, val_preds_lr, average='weighted')[2]

    results["Logistic Regression"] = {
        "model": lr_model,
        "vectorizer": tfidf,
        "type": "TF-IDF + LogisticRegression",
        "acc": acc_lr,
        "macro_f1": macro_f1_lr,
        "weighted_f1": weighted_f1_lr,
        "per_class_f1": f1_lr,
        "val_preds": val_preds_lr
    }

    print(f"Validation Accuracy (LR): {acc_lr*100:.2f}% | Macro F1: {macro_f1_lr:.4f}")

    # MODEL 2: Linear SVM
    print("\n--- Training Model 2: Linear SVM ---")
    svm_model = LinearSVC(random_state=SEED, max_iter=500, C=1.0)
    svm_model.fit(X_train_tfidf, y_train)

    val_preds_svm = svm_model.predict(X_val_tfidf)
    acc_svm = accuracy_score(y_val, val_preds_svm)
    prec_svm, rec_svm, f1_svm, _ = precision_recall_fscore_support(y_val, val_preds_svm, average=None)
    macro_f1_svm = np.mean(f1_svm)
    weighted_f1_svm = precision_recall_fscore_support(y_val, val_preds_svm, average='weighted')[2]

    results["Linear SVM"] = {
        "model": svm_model,
        "vectorizer": tfidf,
        "type": "TF-IDF + LinearSVC",
        "acc": acc_svm,
        "macro_f1": macro_f1_svm,
        "weighted_f1": weighted_f1_svm,
        "per_class_f1": f1_svm,
        "val_preds": val_preds_svm
    }

    print(f"Validation Accuracy (Linear SVM): {acc_svm*100:.2f}% | Macro F1: {macro_f1_svm:.4f}")

    # STEP 8: Class Imbalance Evaluation (Linear SVM Balanced)
    print("\n--- Training Model 2 (Balanced Weights): Linear SVM (class_weight='balanced') ---")
    svm_bal_model = LinearSVC(random_state=SEED, max_iter=500, C=1.0, class_weight='balanced')
    svm_bal_model.fit(X_train_tfidf, y_train)

    val_preds_svm_bal = svm_bal_model.predict(X_val_tfidf)
    acc_svm_bal = accuracy_score(y_val, val_preds_svm_bal)
    macro_f1_svm_bal = precision_recall_fscore_support(y_val, val_preds_svm_bal, average='macro')[2]
    weighted_f1_svm_bal = precision_recall_fscore_support(y_val, val_preds_svm_bal, average='weighted')[2]

    results["Linear SVM (Balanced)"] = {
        "model": svm_bal_model,
        "vectorizer": tfidf,
        "type": "TF-IDF + LinearSVC (Balanced)",
        "acc": acc_svm_bal,
        "macro_f1": macro_f1_svm_bal,
        "weighted_f1": weighted_f1_svm_bal,
        "val_preds": val_preds_svm_bal
    }

    # STEP 9: Dense Semantic Embedding Model (TruncatedSVD + Cosine Similarity)
    print("\n--- Training Model 3: Semantic Embedding Model (Dense LSA Embeddings + Cosine Similarity) ---")
    tfidf_claim = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
    tfidf_ev = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)

    tfidf_claim.fit(df['clean_claim'])
    tfidf_ev.fit(df['clean_evidence'])

    c_train_tfidf = tfidf_claim.transform(claims_train)
    e_train_tfidf = tfidf_ev.transform(ev_train)

    svd_c = TruncatedSVD(n_components=30, random_state=SEED)
    c_train_emb = svd_c.fit_transform(c_train_tfidf)
    e_train_emb = svd_c.transform(e_train_tfidf)

    sim_train = calc_vectorized_cosine(c_train_emb, e_train_emb)
    X_train_emb_feats = np.hstack([c_train_emb, e_train_emb, sim_train])

    c_val_tfidf = tfidf_claim.transform(claims_val)
    e_val_tfidf = tfidf_ev.transform(ev_val)
    c_val_emb = svd_c.transform(c_val_tfidf)
    e_val_emb = svd_c.transform(e_val_tfidf)
    sim_val = calc_vectorized_cosine(c_val_emb, e_val_emb)
    X_val_emb_feats = np.hstack([c_val_emb, e_val_emb, sim_val])

    emb_model = LinearSVC(random_state=SEED, max_iter=500, C=1.0)
    emb_model.fit(X_train_emb_feats, y_train)

    val_preds_emb = emb_model.predict(X_val_emb_feats)
    acc_emb = accuracy_score(y_val, val_preds_emb)
    macro_f1_emb = precision_recall_fscore_support(y_val, val_preds_emb, average='macro')[2]
    weighted_f1_emb = precision_recall_fscore_support(y_val, val_preds_emb, average='weighted')[2]

    results["Semantic Embedding Model"] = {
        "model": emb_model,
        "vectorizer": tfidf,
        "type": "Dense SVD Embeddings + Cosine Similarity Classifier",
        "acc": acc_emb,
        "macro_f1": macro_f1_emb,
        "weighted_f1": weighted_f1_emb,
        "val_preds": val_preds_emb
    }

    print(f"Validation Accuracy (Semantic Embedding Model): {acc_emb*100:.2f}% | Macro F1: {macro_f1_emb:.4f}")

    # STEP 10: Best Model Selection
    best_name = max(results.keys(), key=lambda k: (results[k]["macro_f1"], results[k]["acc"]))
    best_info = results[best_name]

    print(f"\n==================================================")
    print(f"BEST MODEL SELECTED: {best_name}")
    print(f"Validation Accuracy: {best_info['acc']*100:.2f}%")
    print(f"Validation Macro F1: {best_info['macro_f1']:.4f}")
    print(f"==================================================")

    # STEP 11: Final Evaluation ONCE on Untouched Test Set
    print("\n--- Running Final Evaluation ONCE on Untouched Test Set ---")
    best_model = best_info["model"]
    
    if "Embedding" in best_name:
        c_test_tfidf = tfidf_claim.transform(claims_test)
        e_test_tfidf = tfidf_ev.transform(ev_test)
        c_test_emb = svd_c.transform(c_test_tfidf)
        e_test_emb = svd_c.transform(e_test_tfidf)
        sim_test = calc_vectorized_cosine(c_test_emb, e_test_emb)
        X_test_eval = np.hstack([c_test_emb, e_test_emb, sim_test])
    else:
        X_test_eval = X_test_tfidf

    test_preds = best_model.predict(X_test_eval)

    final_test_acc = accuracy_score(y_test, test_preds)
    prec_t, rec_t, f1_t, _ = precision_recall_fscore_support(y_test, test_preds, average=None)
    final_test_macro_f1 = np.mean(f1_t)
    final_test_weighted_f1 = precision_recall_fscore_support(y_test, test_preds, average='weighted')[2]
    final_test_prec = precision_recall_fscore_support(y_test, test_preds, average='weighted')[0]
    final_test_rec = precision_recall_fscore_support(y_test, test_preds, average='weighted')[1]

    cm = confusion_matrix(y_test, test_preds)
    cls_report = classification_report(y_test, test_preds, target_names=class_names)

    # Save reports/final_evaluation.txt
    reports_dir_1 = "reports"
    reports_dir_2 = "../reports"
    for rdir in [reports_dir_1, reports_dir_2]:
        os.makedirs(rdir, exist_ok=True)
        eval_path = os.path.join(rdir, "final_evaluation.txt")
        with open(eval_path, "w", encoding="utf-8") as f:
            f.write(f"EVIDENCE BOUNDARY AI — FINAL MODEL EVALUATION REPORT\n")
            f.write(f"====================================================\n\n")
            f.write(f"Selected Best Model: {best_name}\n")
            f.write(f"Model Type: {best_info['type']}\n")
            f.write(f"Random Seed: {SEED}\n\n")
            f.write(f"FINAL UNTOUCHED TEST SET METRICS:\n")
            f.write(f"  FINAL TEST ACCURACY:   {final_test_acc*100:.2f}%\n")
            f.write(f"  FINAL TEST MACRO F1:    {final_test_macro_f1:.4f}\n")
            f.write(f"  FINAL TEST WEIGHTED F1: {final_test_weighted_f1:.4f}\n")
            f.write(f"  PRECISION (Weighted):  {final_test_prec:.4f}\n")
            f.write(f"  RECALL (Weighted):     {final_test_rec:.4f}\n\n")
            f.write(f"CLASSIFICATION REPORT:\n{cls_report}\n\n")
            f.write(f"CONFUSION MATRIX:\n{cm}\n")
        print(f"Saved final evaluation report to: {os.path.abspath(eval_path)}")

    # STEP 12: Error Analysis
    misclassified = []
    for idx in range(len(y_test)):
        if y_test[idx] != test_preds[idx]:
            true_lbl = class_names[y_test[idx]]
            pred_lbl = class_names[test_preds[idx]]
            clm = claims_test[idx]
            evd = ev_test[idx]

            if "not" in clm or "no" in clm or "without" in clm:
                category = "negation problem"
            elif any(c.isdigit() for c in clm):
                category = "numerical mismatch"
            elif true_lbl == "NOT_ENOUGH_INFO" or pred_lbl == "NOT_ENOUGH_INFO":
                category = "insufficient evidence"
            elif true_lbl == "REFUTES" and pred_lbl == "SUPPORTS":
                category = "contradictory evidence"
            else:
                category = "semantic similarity problem"

            misclassified.append({
                "test_index": idx,
                "claim": clm,
                "evidence": evd,
                "true_label": true_lbl,
                "predicted_label": pred_lbl,
                "error_category": category
            })

    df_errors = pd.DataFrame(misclassified)
    for rdir in [reports_dir_1, reports_dir_2]:
        err_path = os.path.join(rdir, "error_analysis.csv")
        df_errors.to_csv(err_path, index=False)
        print(f"Saved error analysis ({len(df_errors)} errors) to: {os.path.abspath(err_path)}")

    # STEP 13: Save Model Artifacts
    models_dir_1 = "models"
    models_dir_2 = "../models"
    models_dir_3 = "models_dir"

    for mdir in [models_dir_1, models_dir_2, models_dir_3]:
        os.makedirs(mdir, exist_ok=True)
        joblib.dump(best_model, os.path.join(mdir, "verification_model.pkl"))
        joblib.dump(tfidf, os.path.join(mdir, "tfidf_vectorizer.pkl"))
        joblib.dump(label_encoder, os.path.join(mdir, "label_encoder.pkl"))

        meta = {
            "model_name": best_name,
            "training_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dataset_version": "v1.0-Colleges_India",
            "number_of_training_samples": len(X_train_text),
            "number_of_validation_samples": len(X_val_text),
            "number_of_test_samples": len(X_test_text),
            "features_used": "TF-IDF (1,2) N-Grams",
            "accuracy": float(final_test_acc),
            "macro_f1": float(final_test_macro_f1),
            "weighted_f1": float(final_test_weighted_f1),
            "random_seed": SEED
        }
        with open(os.path.join(mdir, "model_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        # STEP 16: Model Registry
        registry = {
            "current_production_version": "v1.0",
            "versions": [
                {
                    "version": "v1.0",
                    "model_name": best_name,
                    "validation_macro_f1": float(best_info['macro_f1']),
                    "test_accuracy": float(final_test_acc),
                    "promoted": True,
                    "date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }
        with open(os.path.join(mdir, "registry.json"), "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

    # STEP 18: Print Final Required Summary
    print("\n==================================================")
    print("           FINAL TRAINING SUMMARY")
    print("==================================================")
    print(f"Dataset:\n  {len(df):,} records")
    print(f"\nClasses:")
    for cls_idx, c_name in enumerate(class_names):
        count_c = (df['label'] == c_name).sum()
        print(f"  {c_name} = {count_c:,}")
    print(f"\nBest Model:\n  {best_name}")
    print(f"\nValidation Accuracy:\n  {best_info['acc']*100:.2f}%")
    print(f"Validation Macro F1:\n  {best_info['macro_f1']:.4f}")
    print(f"\nFINAL TEST ACCURACY:\n  {final_test_acc*100:.2f}%")
    print(f"FINAL TEST MACRO F1:\n  {final_test_macro_f1:.4f}")
    print("==================================================")

if __name__ == "__main__":
    train_and_evaluate_pipeline()
