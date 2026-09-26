# Research Specification & Blueprint (Target: Jurnal SINTA 2)
## Project: Strava Play Store Review Sentiment & Aspect-Based Analysis

- **Peneliti Utama**: Syifa Pajril Yaum (NIM: 20230810123)
- **Target Luaran**: Artikel Ilmiah Terakreditasi Nasional **SINTA 2** (Jalur Bebas Skripsi)
- **Fokus Keilmuan**: Natural Language Processing (NLP), Machine Learning Text Classification, Human-Computer Interaction (HCI).

---

## 1. Judul Penelitian Rencana
> *"Analisis Sentimen dan Klasifikasi Aspek Pengalaman Pengguna Aplikasi Kebugaran Digital Berbasis Ulasan Google Play Store Menggunakan Komparasi Algoritma Machine Learning"*
*(Atau versi Bahasa Inggris: "Aspect-Based Sentiment Analysis and Machine Learning Model Comparison on Digital Fitness App User Reviews: A Case Study on Strava")*

---

## 2. Research Questions (RQ)
1. **RQ-1 (Aspek & Preferensi Pengguna)**: Aspek apa saja dalam aplikasi pelacak lari (Strava) yang paling banyak menuai sentimen negatif dan positif dari pengguna Indonesia?
2. **RQ-2 (Komparasi Algoritma)**: Algoritma Machine Learning mana di antara Naive Bayes, Support Vector Machine (SVM), Random Forest, dan IndoBERT yang menghasilkan akurasi dan F1-Score tertinggi dalam mengklasifikasikan sentimen ulasan pelari?

---

## 3. Metodologi Penelitian & Pipeline Eksperimen

```
[ Scraping Google Play Store ] (10.000 Ulasan com.strava)
             │
             ▼
[ Data Preprocessing ] (Case Folding, Cleaning Regex, Slang Normalization, Stemming/Sastrawi, Stopwords)
             │
             ▼
[ Labeling Sentimen ] (3 Kelas: Positif [4-5], Netral [3], Negatif [1-2] + Rule-Based Lexicon VADER/InSet)
             │
             ▼
[ Feature Extraction ] (TF-IDF N-Gram (1,2) & Word Embeddings)
             │
             ▼
[ Multi-Model Training & Benchmark ]
  ├── 1. Multinomial Naive Bayes (Baseline)
  ├── 2. Support Vector Machine (Linear & RBF Kernel)
  ├── 3. Random Forest Classifier
  └── 4. Pre-trained Transformer (IndoBERT Base)
             │
             ▼
[ Evaluasi Kinerja ] (Accuracy, Precision, Recall, Macro F1-Score, Confusion Matrix, Latensi Komputasi)
             │
             ▼
[ Sintesis Temuan untuk HCI / Gamifikasi ] (Dasar Desain Pengembangan LARI2)
```

---

## 4. Taksonomi 5 Aspek Ulasan (*Aspect Categories*)
1. 🛰️ **GPS & Tracking Accuracy**: Akurasi rute GPS, sinyal hilang, drift jarak, elevasi.
2. 📱 **UI/UX & Kemudahan Pakai**: Tampilan antarmuka, navigasi menu, keterbacaan peta.
3. 🏆 **Gamifikasi & Fitur Sosial**: Segmen lari, leaderboard, KOM/QOM, share aktivitas, challenge.
4. 💳 **Langganan & Monetisasi (Subscription)**: Harga Strava Premium, fitur yang dikunci, paywall.
5. 🔋 **Stabilitas Sistem & Baterai**: Crash mendadak, boros baterai, sinkronisasi jam smartwatch gagal.
