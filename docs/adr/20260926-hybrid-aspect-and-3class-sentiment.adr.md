# ADR: Hybrid Aspect Classification and 3-Class Sentiment Formulation
- **Date**: 2026-09-26
- **Status**: Accepted
- **Deciders**: Syifa Pajril Yaum (Researcher), AI Pair

---

## 1. Context & Problem Statement
Dalam riset ulasan Play Store Strava untuk publikasi jurnal Publikasi Ilmiah:
1. Membutuhkan anotasi 5 aspek (GPS, UI/UX, Gamifikasi, Subscription, Stabilitas) dari 10.000 ulasan tanpa beban pelabelan manual penuh yang memakan waktu lama, tetapi tetap mempertahankan reliabilitas akademis.
2. Formulasi kelas sentimen harus merefleksikan realitas rating Google Play Store dan memenuhi standar komparasi multi-model NLP.

---

## 2. Decision
1. **Hybrid Aspect Classification**:
   - Menggabungkan pendekatan Rule-Based Domain Lexicon matching (Tahap 1) dengan Transformer Embedding/Semantic fallback (Tahap 2).
   - Menghasilkan label aspek terstandar dengan akurasi interpretasi tinggi dan efisiensi waktu komputasi.
2. **3-Class Sentiment Scheme**:
   - Membagi polaritas ulasan menjadi 3 kelas: `POSITIVE` (score 4-5), `NEUTRAL` (score 3), dan `NEGATIVE` (score 1-2).
   - Menggunakan metrik **Macro F1-Score** sebagai benchmark utama untuk mengatasi skew/imbalance antar kelas.

---

## 3. Consequences & Trade-offs
### Pros:
- **Kecepatan & Skalabilitas**: 10.000 data ulasan dapat diproses dalam hitungan menit tanpa bottleneck pelabelan manual human-annotator per baris.
- **Transparansi Akademis**: Aturan leksikon kata kunci terdefinisi jelas di lampiran jurnal dan dapat diaudit oleh reviewer Publikasi Ilmiah.
- **Relevansi Pasar**: Kelas netral (rating 3) dipertahankan karena sering memuat ulasan bernada konstruktif / saran perbaikan fitur yang bernilai bagi HCI.

### Cons & Mitigations:
- **Trade-off**: Kata slang atau kiasan baru mungkin luput dari rule-based lexicon.
- **Mitigasi**: Kamus sinonim & slang dinormalisasi di tahap preprocessing, serta teks tanpa match dialokasikan ke fallback semantic classifier / kategori `GENERAL`.
