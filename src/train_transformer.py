"""
Modul Fine-Tuning IndoBERT (indobenchmark/indobert-base-p1) untuk Klasifikasi Sentimen 3-Kelas
Arsitektur: Transformer Sequence Classification + RTX 3050 CUDA Acceleration
Standar: Riset Jurnal SINTA 2 (Ponytail / Zero-Bloat)
"""

import os
import torch
import numpy as np
import pandas as pd
from typing import Dict
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from datasets import Dataset

# Mapping Label Sentimen ke ID Numerik
LABEL_TO_ID = {"NEGATIVE": 0, "NEUTRAL": 1, "POSITIVE": 2}
ID_TO_LABEL = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
MODEL_NAME = "indobenchmark/indobert-base-p1"
OUTPUT_DIR = "./results_indobert"


def compute_metrics(eval_pred) -> Dict[str, float]:
    """Menghitung metrik Macro F1, Precision, Recall, dan Accuracy untuk evaluasi jurnal."""
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    
    acc = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="macro", zero_division=0
    )
    return {
        "accuracy": round(acc * 100, 2),
        "precision_macro": round(precision * 100, 2),
        "recall_macro": round(recall * 100, 2),
        "f1_macro": round(f1 * 100, 2)
    }


def main():
    # 1. Device check
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("=" * 60)
    print(f"[*] Menjalankan Training IndoBERT pada Device: {device.upper()}")
    if device == "cuda":
        print(f"[*] GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"[*] VRAM Available: {round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)} GB")
    print("=" * 60)

    # 2. Muat dan Split Data
    csv_file = "strava_reviews_processed.csv"
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"File {csv_file} belum ada! Jalankan src/preprocess.py terlebih dahulu.")
    
    print(f"[*] Membaca data: {csv_file}...")
    df = pd.read_csv(csv_file).dropna(subset=["clean_text", "sentiment_label"])
    df["label"] = df["sentiment_label"].map(LABEL_TO_ID)

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["label"]
    )
    print(f"[+] Data Train: {len(train_df)} | Data Test/Eval: {len(test_df)}")

    # 3. Tokenisasi
    print(f"[*] Memuat Tokenizer: {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize_fn(batch):
        return tokenizer(batch["clean_text"], truncation=True, max_length=128)

    train_ds = Dataset.from_pandas(train_df[["clean_text", "label"]])
    test_ds = Dataset.from_pandas(test_df[["clean_text", "label"]])

    print("[*] Melakukan tokenisasi dataset...")
    train_tokenized = train_ds.map(tokenize_fn, batched=True, remove_columns=["clean_text"])
    test_tokenized = test_ds.map(tokenize_fn, batched=True, remove_columns=["clean_text"])

    # 4. Inisialisasi Model
    print(f"[*] Menginisialisasi Pretrained Model: {MODEL_NAME}...")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
        id2label=ID_TO_LABEL,
        label2id=LABEL_TO_ID
    )

    # 5. Konfigurasi Training Arguments (Disesuaikan untuk VRAM 6GB RTX 3050)
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(), # Aktifkan Mixed Precision jika GPU ready
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        report_to="none"
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=test_tokenized,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )

    # 6. Training Execution
    print("\n[*] Memulai Proses Fine-Tuning IndoBERT...")
    train_result = trainer.train()
    print("[OK] Fine-Tuning Selesai!")

    # 7. Evaluasi Akhir
    print("\n[*] Menjalankan Evaluasi Akhir pada Test Set...")
    eval_results = trainer.evaluate()
    print("\n=== Hasil Benchmark IndoBERT (Standar SINTA 2) ===")
    print(f"Accuracy         : {eval_results.get('eval_accuracy', 0)}%")
    print(f"Precision (Macro): {eval_results.get('eval_precision_macro', 0)}%")
    print(f"Recall (Macro)   : {eval_results.get('eval_recall_macro', 0)}%")
    print(f"F1-Score (Macro) : {eval_results.get('eval_f1_macro', 0)}%")

    # Simpan model terbaik
    save_path = "./models/indobert_sentiment_best"
    trainer.save_model(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"\n[OK] Model terbaik disimpan di folder: '{save_path}'")


if __name__ == "__main__":
    main()
