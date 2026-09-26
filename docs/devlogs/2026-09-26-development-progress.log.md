# Dev Log: Strava Review Sentiment & Aspect-Based Analysis
- **Date**: 2026-09-26
- **Engineer**: Syifa Pajril Yaum & AI Assistant
- **Target**: Jurnal Publikasi Ilmiah

---

## Session Timeline
- `[09:14]`: Inisialisasi SDLC Phase 1-3 (PRD, SRS, ADR, Plan) ke dalam `docs/`.
- `[09:19]`: Sinkronisasi Git repository ke `https://github.com/timbubadibako/SA-Strava.git` (branch `main`).
- `[09:40]`: Verifikasi hardware & setup environment:
  - GPU: NVIDIA GeForce RTX 3050 Laptop (6GB VRAM)
  - CUDA: 12.4 + PyTorch 2.6.0
  - Env: Shared `nlp-env` via `uv`
- `[19:06]`: Verifikasi dataset mentah `strava_reviews_raw.csv` (10.000 ulasan Play Store).
- `[19:09]`: Eksekusi `src/preprocess.py`:
  - 9.843 ulasan bersih setelah regex cleaning, normalisasi slang, dan stopword removal (dengan proteksi kata negasi).
  - Ekstraksi 5 aspek (GPS_TRACKING, UI_UX, GAMIFICATION, SUBSCRIPTION, STABILITY).
- `[19:14]`: Eksekusi `src/train_classical.py`:
  - Baseline model terlatih (TF-IDF 1-2 gram):
    - Linear SVM: Macro F1 = 64.62%
    - Multinomial Naive Bayes: Macro F1 = 58.90%
    - Random Forest: Macro F1 = 58.76%
- `[19:15]`: Pembuatan `analysis_dashboard.ipynb` untuk eksplorasi visual grafik & heatmap confusion matrix.
- `[19:17]`: Pembuatan modul Deep Learning `src/train_transformer.py` (Fine-Tuning IndoBERT).

---

## Next Action
- Menjalankan `src/train_transformer.py` secara mandiri oleh user menggunakan akselerasi CUDA GPU.
