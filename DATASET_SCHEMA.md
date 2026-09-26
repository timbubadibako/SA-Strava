# Dataset Schema & Data Dictionary
## Project: Strava Play Store Review Sentiment Analysis

---

## 1. Skema Raw Dataset (`strava_reviews_raw.csv`)
Data mentah hasil penarikan langsung via `google-play-scraper`:

| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `reviewId` | String | ID unik ulasan Google Play | `gp:AOqpTOE1...` |
| `userName` | String | Nama akun reviewer | `Andi Pratama` |
| `content` | Text | Isi teks ulasan pengguna | `"GPS-nya sering loncat pas lari di bawah pohon rindang..."` |
| `score` | Integer | Rating bintang (1 s/d 5) | `2` |
| `thumbsUpCount` | Integer | Jumlah like yang didapat ulasan | `14` |
| `reviewCreatedVersion`| String | Versi aplikasi saat diulas | `348.9.0` |
| `at` | DateTime | Tanggal & waktu ulasan diposting | `2026-08-15 14:32:00` |
| `replyContent` | Text | Tanggapan resmi dari developer Strava | `"Hi, please check your GPS settings..."` |

---

## 2. Skema Dataset Olahan (`strava_reviews_processed.csv`)
Dataset setelah tahap pembersihan teks dan ekstraksi fitur:

| Nama Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `clean_text` | Text | Teks ulasan setelah case folding, cleaning regex, normalisasi slang, dan stopword removal. |
| `tokenized_text` | Array | Daftar kata/token hasil tokenisasi. |
| `sentiment_label` | String | Label sentimen: `POSITIVE` (score 4-5), `NEUTRAL` (score 3), `NEGATIVE` (score 1-2). |
| `aspect_category` | String | Kategori aspek ulasan: `GPS_TRACKING`, `UI_UX`, `GAMIFICATION`, `SUBSCRIPTION`, `STABILITY`. |
