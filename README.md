# SA-Strava: Strava Play Store Review Sentiment & Aspect-Based Analysis

Repositori riset komparasi model Machine Learning dan Deep Learning (IndoBERT) pada ulasan aplikasi Strava berbahasa Indonesia untuk publikasi artikel ilmiah dan pengembangan sistem kebugaran.

---

## 🏆 Hasil Benchmark Model

Pengujian pada 9.843 ulasan bersih menggunakan Stratified 80:20 Split (1.969 Data Uji):

| Peringkat | Model Algoritma | Akurasi | Precision (Macro) | Recall (Macro) | **Macro F1-Score** | Waktu Latih |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **IndoBERT (Fine-Tuned)** | **86.90%** | **67.44%** | 64.77% | **65.55%** | ~15-20 min (RTX 3050 GPU) |
| 🥈 | **Linear SVM** | 83.70% | 63.98% | **65.39%** | **64.62%** | 0.11 s (CPU) |
| 🥉 | **Multinomial Naive Bayes** | 86.54% | 88.27% | 60.88% | **58.90%** | 0.02 s (CPU) |
| 4 | **Random Forest** | 84.76% | 62.57% | 60.24% | **58.76%** | 0.47 s (CPU) |

---

## 📊 Temuan 5 Aspek Kunci Pengguna Strava
- 💳 **Subscription (Langganan)**: **73.3% Negatif** (keluhan harga mahal & fitur dikunci).
- 🔋 **Stability (Baterai & Crash)**: **55.8% Negatif** (isu force close & boros baterai).
- 🛰️ **GPS Tracking**: **43.5% Positif** vs **40.7% Negatif** (akurasi rute vs GPS drift).
- 📱 **UI/UX**: **66.1% Positif** (antarmuka mudah & intuitif).
- 🏆 **Gamification**: **59.3% Positif** (kudos, leaderboard, challenge).

---

## 📂 Struktur Repositori & SDLC
- `docs/prd/`: Product Requirement Document riset.
- `docs/srs/`: Software Requirement Specification & API/Schema.
- `docs/adr/`: Architecture Decision Record (Hybrid Aspect & 3-Class Sentiment).
- `docs/plans/`: Implementation Plan & checklist.
- `docs/qa/`: Laporan komparasi metrik lengkap & sintesis pembahasan jurnal ([`final_benchmark_report.qa.md`](docs/qa/final_benchmark_report.qa.md)).
- `src/preprocess.py`: Modul pembersihan teks, normalisasi slang, dan ekstraksi aspek.
- `src/train_classical.py`: Training pipeline MNB, SVM, Random Forest.
- `src/train_transformer.py`: Fine-tuning IndoBERT (PyTorch + CUDA).
- `analysis_dashboard.ipynb`: Visualisasi interaktif grafik distribusi sentimen & confusion matrix.

---

## 🚀 Cara Menjalankan

1. Setup environment via `uv`:
   ```bash
   uv venv C:/Users/seeva/.venvs/nlp-env --python 3.10
   uv pip install --python C:/Users/seeva/.venvs/nlp-env torch torchvision --index-url https://download.pytorch.org/whl/cu124
   uv pip install --python C:/Users/seeva/.venvs/nlp-env pandas scikit-learn transformers datasets accelerate matplotlib seaborn ipykernel
   ```

2. Jalankan Preprocessing Data:
   ```bash
   python src/preprocess.py
   ```

3. Jalankan Benchmark ML Klasik:
   ```bash
   python src/train_classical.py
   ```

4. Jalankan Training IndoBERT:
   ```bash
   python src/train_transformer.py
   ```
