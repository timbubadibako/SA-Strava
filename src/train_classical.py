"""
Modul Training Model Machine Learning Klasik & Evaluasi
Mendukung: Naive Bayes, Linear SVM, RBF SVM, Random Forest
Evaluasi: Accuracy, Precision, Recall, Macro F1-Score, Confusion Matrix
Standar: Jurnal SINTA 2 (Ponytail / Zero-Bloat)
"""

import time
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score, precision_score, recall_score


def load_and_split_data(
    csv_path: str = "strava_reviews_processed.csv",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Membaca dataset dan melakukan stratified train-test split."""
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["clean_text", "sentiment_label"])
    
    X = df["clean_text"]
    y = df["sentiment_label"]
    
    # Stratified split untuk menjaga rasio distribusi sentimen antar kelas
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test


def train_and_benchmark_models(
    X_train: pd.Series,
    X_test: pd.Series,
    y_train: pd.Series,
    y_test: pd.Series,
    ngram_range: Tuple[int, int] = (1, 2),
    max_features: int = 5000
) -> Dict[str, Any]:
    """Melatih multi-model dengan TF-IDF fitur dan mengembalikan metrik evaluasi lengkap."""
    print("[*] Mengekstraksi fitur TF-IDF (n-gram:", ngram_range, ", max_features:", max_features, ")...")
    vectorizer = TfidfVectorizer(
        ngram_range=ngram_range,
        max_features=max_features,
        min_df=3,
        sublinear_tf=True
    )
    
    # Fit HANYA pada train set agar terhindar dari data leakage
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    models = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.5),
        "Linear SVM": LinearSVC(C=1.0, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42, n_jobs=-1)
    }
    
    benchmark_summary = []
    detailed_results = {}
    labels_order = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
    
    for name, clf in models.items():
        print(f"[*] Melatih model: {name}...")
        start_time = time.time()
        clf.fit(X_train_vec, y_train)
        train_time = time.time() - start_time
        
        y_pred = clf.predict(X_test_vec)
        
        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=labels_order)
        
        benchmark_summary.append({
            "Model": name,
            "Accuracy": round(acc * 100, 2),
            "Precision (Macro)": round(prec_macro * 100, 2),
            "Recall (Macro)": round(rec_macro * 100, 2),
            "F1-Score (Macro)": round(f1_macro * 100, 2),
            "Train Time (s)": round(train_time, 2)
        })
        
        detailed_results[name] = {
            "model_obj": clf,
            "predictions": y_pred,
            "confusion_matrix": cm,
            "classification_report": classification_report(y_test, y_pred, labels=labels_order, output_dict=True)
        }
        
    summary_df = pd.DataFrame(benchmark_summary).sort_values(by="F1-Score (Macro)", ascending=False).reset_index(drop=True)
    
    return {
        "summary_table": summary_df,
        "detailed_results": detailed_results,
        "vectorizer": vectorizer,
        "labels_order": labels_order,
        "y_test": y_test
    }


if __name__ == "__main__":
    X_tr, X_te, y_tr, y_te = load_and_split_data()
    results = train_and_benchmark_models(X_tr, X_te, y_tr, y_te)
    print("\n=== Tabel Komparasi Model (Standar Jurnal SINTA 2) ===")
    print(results["summary_table"].to_string(index=False))
