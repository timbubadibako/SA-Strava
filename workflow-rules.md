# Workflow Rules & Research Guidelines
## Project: Strava Sentiment Analysis

Setiap script dan analisis data di direktori ini **WAJIB MENGIKUTI STANDAR ILMIAH BERIKUT**:

---

## 1. Reproducibility & Random Seed
- Selalu gunakan `random_state=42` pada setiap split data (`train_test_split`) dan inisialisasi model (SVM, Random Forest, Logistic Regression).
- Simpan rasio pembagian data standar: **80% Training Data, 20% Testing Data** (atau Stratified K-Fold Cross Validation $k=5$).

## 2. Pencegahan Data Leakage
- Fitur TF-IDF Vectorizer wajib di-`fit` HANYA pada data Training (`fit_transform`), dan di-`transform` pada data Testing.
- Dilarang keras melakukan preprocessing/resampling (seperti SMOTE) sebelum data dibagi menjadi Train-Test.

## 3. Metrik Evaluasi Komprehensif
- Jangan hanya melaporkan *Accuracy* (karena sentimen ulasan sering *imbalanced*).
- Laporkan secara lengkap: **Macro Precision, Macro Recall, Macro F1-Score**, dan tabel **Confusion Matrix**.

## 4. Keamanan & Sanitasi Data
- Jangan simpan data sensitif pengguna (seperti nomor telepon jika ada di ulasan).
- Kolom `userName` wajib di-anonimkan saat naskah dipublikasikan ke jurnal.
