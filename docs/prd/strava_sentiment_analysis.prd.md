# PRD: Strava Review Sentiment & Aspect-Based Analysis
- **Peneliti / Author**: Syifa Pajril Yaum (NIM: 20230810123)
- **Target Luaran**: Jurnal Nasional Terakreditasi Publikasi Ilmiah (Jalur Bebas Skripsi)
- **Tanggal**: 2026-09-26
- **Status**: Approved

---

## 1. Problem Statement & Objectives
Strava merupakan salah satu aplikasi pelacak kebugaran dan lari terpopuler di Indonesia. Namun, pengembang sering kali kesulitan mengisolasi umpan balik spesifik dari ribuan ulasan teks bebas di Google Play Store.

### Tujuan Penelitian:
1. **RQ-1**: Memetakan sentimen pengguna Indonesia terhadap 5 aspek kunci aplikasi (GPS & Tracking, UI/UX, Gamifikasi & Fitur Sosial, Langganan/Monetisasi, Stabilitas Sistem).
2. **RQ-2**: Mengevaluasi dan membandingkan performa 4 model klasifikasi (Multinomial Naive Bayes, Support Vector Machine, Random Forest, IndoBERT) pada klasifikasi sentimen teks ulasan berbahasa Indonesia.

---

## 2. User Personas & User Stories
- **Persona 1: Peneliti / Akademisi NLP**: Membutuhkan dataset benchmark ulasan berbahasa Indonesia dengan label sentimen 3-kelas dan aspek terstandar serta hasil komparasi metrik yang valid (Macro F1-Score).
- **Persona 2: Tim Pengembang Aplikasi LARI2 / HCI Designer**: Membutuhkan sintesis empiris mengenai pain points pelari Indonesia (misal: GPS drift, paywall segment) untuk dasar perancangan antarmuka dan gamifikasi.

---

## 3. Functional Scope
- [x] **In Scope**:
  - Penarikan 10.000 ulasan Google Play Store berbahasa Indonesia untuk paket `com.strava`.
  - Pipeline preprocessing teks: case folding, regex cleaning, normalisasi slang/alay, stopword removal, stemming opsional (Sastrawi).
  - Skema pelabelan sentimen 3 kelas: Positif (score 4-5), Netral (score 3), Negatif (score 1-2).
  - Klasifikasi 5 aspek ulasan menggunakan pendekatan Hybrid (Rule-based keyword lexicon + zero-shot/few-shot embedding).
  - Ekstraksi fitur teks: TF-IDF (unigram & bigram) untuk ML klasik, tokenizer subword untuk IndoBERT.
  - Komparasi 4 algoritma: MNB, SVM, Random Forest, IndoBERT.
  - Evaluasi komprehensif: Confusion Matrix, Accuracy, Precision, Recall, Macro F1-Score, dan latensi komputasi.
- [ ] **Out of Scope**:
  - Ulasan di luar aplikasi Strava (Garmin Connect, Nike Run Club).
  - Ulasan berbahasa non-Indonesia atau multi-bahasa tanpa konteks lokal.
  - Analisis ulasan dari Apple App Store.

---

## 4. Non-Functional Requirements (NFR)
- **Reproducibility**: Seluruh seed random (`random_state=42`) dikunci agar hasil eksperimen dapat direplikasi penguji jurnal.
- **Efficiency (Ponytail)**: Pipeline modular, kode minimalis tanpa boilerplate berlebih, penanganan class imbalance (SMOTE / class weights).
- **Standard Storage**: Format output intermediate dan final berupa CSV/Parquet terstruktur.

---

## 5. Acceptance Criteria (Publikasi Ilmiah Standard)
- [ ] Minimal 10.000 ulasan mentah berhasil ditarik dan tervalidasi.
- [ ] Dataset bersih terbebas dari duplikasi ulasan dan teks kosong.
- [ ] Klasifikasi aspek berhasil melabeli ulasan ke dalam 5 taksonomi dengan ambiguitas terendah.
- [ ] Komparasi model dievaluasi menggunakan stratified 5-fold cross-validation / train-test split (80:20).
- [ ] Tabel komparasi metrik (Accuracy, Precision, Recall, Macro F1) siap dikutip langsung ke manuskrip jurnal.
