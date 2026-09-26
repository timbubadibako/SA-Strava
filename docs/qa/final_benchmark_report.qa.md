# Laporan Evaluasi & Sintesis Benchmark (Standar Jurnal Publikasi Ilmiah)
## Analisis Sentimen & Aspek Ulasan Strava Google Play Store
- **Peneliti**: Syifa Pajril Yaum (NIM: 20230810123)
- **Dataset**: 9.843 Ulasan Bersih (`com.strava`, Google Play Store Indonesia)
- **Komparasi Model**: Multinomial Naive Bayes, Support Vector Machine (Linear SVM), Random Forest, IndoBERT-base-p1
- **Hardware Training**: NVIDIA GeForce RTX 3050 Laptop (6GB VRAM, CUDA 12.4, Mixed Precision FP16)
- **Status SDLC**: Phase 5 (QA & Evaluation Complete)

---

## 1. Tabel Komparasi Kinerja Multi-Model (Tabel Utama Manuskrip)

Evaluasi dihitung menggunakan Stratified 80:20 Train-Test Split (1.969 Data Uji):

| No | Model Algoritma | Ekstraksi Fitur | Accuracy (%) | Precision Macro (%) | Recall Macro (%) | **Macro F1-Score (%)** | Waktu Latih |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | **IndoBERT (Fine-Tuned)** | Subword Tokenizer | **86.90** | **67.44** | 64.77 | **65.55** | ~15-20 menit (GPU) |
| 2 | **Linear SVM** | TF-IDF (1,2-gram) | 83.70 | 63.98 | **65.39** | 64.62 | 0.11 detik (CPU) |
| 3 | **Multinomial Naive Bayes** | TF-IDF (1,2-gram) | 86.54 | 88.27 | 60.88 | 58.90 | 0.02 detik (CPU) |
| 4 | **Random Forest** | TF-IDF (1,2-gram) | 84.76 | 62.57 | 60.24 | 58.76 | 0.47 detik (CPU) |

---

## 2. Analisis & Sintesis Temuan (Pembahasan Jurnal)

### 2.1 Performa Algoritma (RQ-2)
1. **IndoBERT Unggul Tipis**: IndoBERT menghasilkan **Macro F1-Score tertinggi (65.55%)** dan akurasi (86.90%), berkat kemampuannya menangkap konteks semantik bidirectional dan relasi antarkata informal pengguna Indonesia.
2. **Efisiensi Linear SVM**: Linear SVM membuktikan performa yang sangat kompetitif (Macro F1 = 64.62%), hanya terpaut **0.93%** di bawah IndoBERT, dengan waktu komputasi yang ribuan kali lebih cepat (0.11 detik vs ~15 menit). Hal ini menjadikannya alternatif terbaik untuk implementasi production edge/real-time.
3. **Kelemahan Kelas Netral (Imbalance)**: Skor Macro F1 tertahan di kisaran 65% karena kelas Netral (rating 3) memiliki sampel jauh lebih sedikit (~623 sampel) dibandingkan Positif (~6.889 sampel).

---

## 3. Distribusi Sentimen terhadap 5 Aspek Kunci (RQ-1 / HCI Insights)

| Kategori Aspek | Total Ulasan | Negatif (%) | Netral (%) | Positif (%) | Dominasi Sentimen & Temuan Utama |
| :--- | :---: | :---: | :---: | :---: | :--- |
| 💳 **Subscription** | 462 | **73.3%** | 5.0% | 21.6% | **Negatif Mutlak**: Keluhan harga mahal & fitur segmen yang dikunci di paywall. |
| 🔋 **Stability** | 652 | **55.8%** | 14.4% | 29.8% | **Negatif**: Isu force close, baterai boros, dan sinkronisasi smartwatch gagal. |
| 🛰️ **GPS Tracking** | 1.436 | 40.7% | 15.7% | **43.5%** | **Berimbang**: Pujian rute akurat vs keluhan GPS drift/loncat di area tertutup. |
| 📱 **UI/UX** | 286 | 27.6% | 6.3% | **66.1%** | **Positif Kuat**: Pengguna menyukai tampilan antarmuka yang bersih & modern. |
| 🏆 **Gamification** | 140 | 30.0% | 10.7% | **59.3%** | **Positif**: Antusiasme tinggi terhadap fitur leaderboard, kudos, dan tantangan klub. |

---

## 4. Rekomendasi Desain untuk Aplikasi LARI2 (Sumbangsih Praktis)
1. **Model Monetisasi Transparan**: Hindari mengunci fitur esensial navigasi ke paywall subscription agresif yang menjadi pemicu 73% sentimen negatif di Strava.
2. **Offline-first GPS Smoothing**: Implementasikan algoritma Kalman Filter untuk mengurangi GPS jumping/drift saat pelari melewati pepohonan atau gedung tinggi.
3. **Battery Saver Mode**: Tambahkan optimasi background tracking hemat daya agar tidak memicu crash sistem pada ponsel Android kelas menengah ke bawah.
