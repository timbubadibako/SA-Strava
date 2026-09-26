# SRS: Strava Review Sentiment & Aspect-Based Analysis
- **Related PRD**: `docs/prd/strava_sentiment_analysis.prd.md`
- **Tanggal**: 2026-09-26
- **Status**: Approved

---

## 1. Data Schema & Pipeline Specifications

### 1.1 Raw Ingestion Schema (`strava_reviews_raw.csv`)
- `reviewId`: string (unique)
- `userName`: string
- `content`: string (teks ulasan mentah)
- `score`: integer (1 s/d 5)
- `thumbsUpCount`: integer
- `reviewCreatedVersion`: string
- `at`: ISO datetime
- `replyContent`: string

### 1.2 Processed Schema (`strava_reviews_processed.csv`)
- `review_id`: string
- `original_text`: string
- `clean_text`: string (lowercased, regex cleaned, slang normalized, stopword removed)
- `tokens`: list[string]
- `sentiment_label`: enum (`POSITIVE`, `NEUTRAL`, `NEGATIVE`)
- `aspect_category`: enum (`GPS_TRACKING`, `UI_UX`, `GAMIFICATION`, `SUBSCRIPTION`, `STABILITY`, `GENERAL`)
- `aspect_confidence`: float (0.0 - 1.0)

---

## 2. Text Preprocessing Specifications
1. **Case Folding**: Konversi seluruh karakter alfabet ke huruf kecil (lowercase).
2. **Regex Cleansing**:
   - Menghapus URL, mention (`@user`), hashtag.
   - Menghapus karakter non-ASCII, emoji, angka, tanda baca berlebih (`!!`, `??`).
3. **Slang & Informal Normalization**:
   - Kamus kamus/lexicon slang Bahasa Indonesia (misal: `yg` -> `yang`, `ga/gak` -> `tidak`, `bgt` -> `banget`).
4. **Stopword Removal**:
   - Stopword corpus Indonesia (NLTK / Tala) dengan pengecualian kata negasi (`tidak`, `bukan`, `belum`, `kurang`) agar tidak merusak konteks polaritas sentimen.
5. **Tokenization**:
   - NLTK WordPunct / Subword tokenization.

---

## 3. Labeling & Aspect Mapping Engine

### 3.1 Sentiment Mapping
- Rating 4 & 5 -> `POSITIVE`
- Rating 3 -> `NEUTRAL`
- Rating 1 & 2 -> `NEGATIVE`

### 3.2 Hybrid Aspect Classification Specification
- **Metode**: Hybrid matching.
  - **Tahap 1**: Domain Keyword Lexicon Mapping (Fast rule-based matching).
    - `GPS_TRACKING`: `['gps', 'sinyal', 'rute', 'jarak', 'km', 'akurasi', 'peta', 'map', 'loncat', 'elevasi']`
    - `UI_UX`: `['tampilan', 'ui', 'ux', 'menu', 'desain', 'ribet', 'simpel', 'mudah', 'font', 'gelap']`
    - `GAMIFICATION`: `['segmen', 'segment', 'leaderboard', 'kom', 'qom', 'tantangan', 'challenge', 'teman', 'kudos', 'prestasi']`
    - `SUBSCRIPTION`: `['bayar', 'langganan', 'premium', 'mahal', 'harga', 'duit', 'kunci', 'fitur berbayar', 'free trial']`
    - `STABILITY`: `['crash', 'keluar sendiri', 'baterai', 'boros', 'force close', 'error', 'bug', 'lag', 'lemot', 'jam', 'smartwatch', 'sinkron']`
  - **Tahap 2**: Semantic Similarity / Zero-Shot fallback jika keyword score ambigu atau tie.

---

## 4. Modeling & Benchmark Architecture

### 4.1 Feature Extraction
- **Classical ML**:
  - `TfidfVectorizer(ngram_range=(1, 2), max_features=5000, min_df=3)`
- **Transformer**:
  - `indobenchmark/indobert-base-p1` tokenizer & pre-trained weights.

### 4.2 Model Configurations
1. **Multinomial Naive Bayes**:
   - `alpha`: tuning via GridSearch [0.1, 0.5, 1.0].
2. **Support Vector Machine (Linear & RBF)**:
   - Kernel: `linear`, `rbf`
   - `C`: [0.1, 1.0, 10.0]
3. **Random Forest Classifier**:
   - `n_estimators`: [100, 200]
   - `max_depth`: [None, 20, 50]
4. **IndoBERT (Fine-Tuning)**:
   - Sequence Classification (3 classes: Pos, Neu, Neg).
   - Optimizer: AdamW (`lr=2e-5`), Epoch: 3 - 5, Batch Size: 16/32.

---

## 5. Metrics & Evaluation Specification
Evaluasi wajib menggunakan:
- **Stratified K-Fold (k=5)** atau Split 80% Train, 20% Test.
- **Metrik Utama**:
  - **Macro F1-Score** (prioritas utama pada imbalanced dataset).
  - Accuracy, Precision (Macro), Recall (Macro).
  - Confusion Matrix plot.
  - Training & Inference Latency (detik).
