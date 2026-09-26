# Plan: Strava Review Sentiment & Aspect-Based Analysis Pipeline
- **Related Documents**:
  - PRD: `docs/prd/strava_sentiment_analysis.prd.md`
  - SRS: `docs/srs/strava_sentiment_analysis.srs.md`
  - ADR: `docs/adr/20260926-hybrid-aspect-and-3class-sentiment.adr.md`
- **Target Luaran**: Benchmark Publikasi Ilmiah

---

## Target Files & Modules
- `scraper.py` (Script penarikan data)
- `src/preprocessing.py` (Cleaner, Slang Normalizer, Stopwords Negation Handler, Tokenizer)
- `src/aspect_classifier.py` (Hybrid Rule-Based + Lexicon Domain Mapper)
- `src/train_classical.py` (TF-IDF + MNB, SVM, Random Forest + GridSearch + Macro F1)
- `src/train_transformer.py` (IndoBERT Fine-Tuning Script)
- `src/evaluate.py` (Confusion Matrix, Metrics Table, ROC/PR curves)

---

## Task Breakdown & Checklists

### Step 1: Data Acquisition & Validation
- [ ] Jalankan `scraper.py` untuk mengumpulkan 10.000 ulasan.
- [ ] Validasi kualitas data mentah di `data/raw/` (cek nulls, duplikasi `reviewId`).

### Step 2: Preprocessing Pipeline Module
- [ ] Buat kamus slang Indonesia ringkas & efisien di `src/preprocessing.py`.
- [ ] Setup stopword list dengan proteksi kata negasi (`tidak`, `bukan`, dll.).
- [ ] Generate output `data/processed/strava_reviews_cleaned.csv`.

### Step 3: Aspect Annotation & Sentiment Ground Truth
- [ ] Implementasikan `src/aspect_classifier.py` berbasis taksonomi 5 aspek.
- [ ] Format label sentimen 3-kelas (`POSITIVE`, `NEUTRAL`, `NEGATIVE`).
- [ ] Ekspor dataset final berlabel lengkap.

### Step 4: Multi-Model Benchmark (Classical ML)
- [ ] Ekstraksi fitur n-gram TF-IDF (1,2).
- [ ] Train & Evaluate Naive Bayes, SVM, dan Random Forest.
- [ ] Catat Macro F1, Precision, Recall, Accuracy.

### Step 5: Deep Learning (IndoBERT) & Comparative Synthesis
- [ ] Fine-tuning IndoBERT untuk klasifikasi 3-kelas.
- [ ] Sintesis tabel komparasi 4 algoritma untuk manuskrip artikel jurnal.
