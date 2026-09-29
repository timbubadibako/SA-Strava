# Laporan Analisis Lintas Platform: Google Play Store vs Apple App Store
## Penguatan Latar Belakang Riset & Problem Statement
- **Aplikasi**: Strava Running & Cycling
- **Dataset**:
  - Google Play Store (Android): **9.843 ulasan bersih**
  - Apple App Store (iOS): **440 ulasan bersih** (Region Indonesia via iTunes RSS API)
- **Fokus**: Komparasi Sentimen Pengguna Lintas Sistem Operasi untuk Penguatan Latar Belakang Manuskrip

---

## 1. Komparasi Sentimen Makro (Android vs iOS)

| Platform | Total Ulasan Bersih | Positif (%) | Netral (%) | Negatif (%) | Rata-rata Skor Bintang |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Google Play Store (Android)** | 9.843 | **69.99%** | 6.33% | 23.68% | ~4.02 ⭐ |
| **Apple App Store (iOS)** | 440 | 47.95% | 8.18% | **43.86%** | ~3.15 ⭐ |

> [!IMPORTANT]
> **Temuan Kritis**: Sentimen negatif di Apple App Store melonjak hampir **2x lipat (43.86%)** dibanding Play Store (23.68%). Ini membuktikan friksi pengguna Strava bukan hanya isu fragmentasi HP Android murah, melainkan masalah mendasar pada model bisnis dan integrasi perangkat.

---

## 2. Komparasi Polaritas per Aspek (Play Store vs App Store)

| Kategori Aspek | Play Store: Negatif (%) | App Store: Negatif (%) | Play Store: Positif (%) | App Store: Positif (%) | Insight Lintas Platform |
| :--- | :---: | :---: | :---: | :---: | :--- |
| 💳 **Subscription** | 73.4% | **95.0%** | 21.6% | **2.5%** | **Sentimen negatif mutlak di iOS**: Keluhan pemotongan saldo otomatis (*auto-renewal*) via Apple ID tanpa notifikasi yang jelas (nominal Rp 349.000,-). |
| 🔋 **Stability** | 55.8% | **58.3%** | 29.8% | 25.0% | Isu crash dan login gagal terjadi di kedua OS, ditambah sinkronisasi Apple Watch / smartwatch pihak ketiga yang sering putus di iOS. |
| 🛰️ **GPS Tracking** | 40.7% | **53.7%** | 43.5% | 35.8% | Di App Store, sentimen negatif GPS justru **melebihi sentimen positif** (53.7% vs 35.8%), mematahkan anggapan bahwa perangkat iOS bebas masalah akurasi lokasi. |
| 📱 **UI/UX** | 27.6% | 30.8% | 66.1% | 53.8% | Desain antarmuka tetap diapresiasi relatif positif di kedua platform. |
| 🏆 **Gamification** | 30.0% | 50.0% | 59.3% | 43.8% | Di iOS, segregasi fitur kompetitif (segmen/KOM) ke tier berbayar memicu kekecewaan pelari kompetitif. |

---

## 3. Sintesis Teks Narasi untuk Bab 1 (Latar Belakang Penelitian)

Paragraf siap pakai untuk dimasukkan langsung ke Bab Latar Belakang (Introduction):

> *"Meskipun Strava diakui secara global sebagai platform pelacak kebugaran terdepan, analisis empiris terhadap ulasan pengguna di Indonesia mengungkap kesenjangan kepuasan yang tajam antara ekspektasi pengguna dan realitas performa aplikasi. Analisis awal lintas platform (*cross-platform exploratory analysis*) terhadap 9.843 ulasan Google Play Store dan 440 ulasan Apple App Store menunjukkan bahwa sentimen negatif pengguna iOS mencapai 43,86%, jauh lebih tinggi dibandingkan pengguna Android (23,68%).*
>
> *Secara spesifik, aspek **Subscription & Monetisasi** menjadi titik friksi paling kritis dengan rasio ketidakpuasan mencapai 73,4% di Android dan 95,0% di iOS, didominasi oleh keluhan perpanjangan langganan otomatis dan penguncian fitur navigasi esensial ke balik paywall. Selain itu, aspek **GPS & Tracking** yang merupakan nilai jual utama aplikasi justru menuai sentimen negatif sebesar 40,7% di Android dan 53,7% di iOS, yang dipicu oleh isu data drift, diskoneksi background tracking, serta inkompatibilitas sinkronisasi smartwatch. Fakta empiris ini menegaskan urgensi dilakukannya pemetaan aspek pengalaman pengguna (Aspect-Based Sentiment Analysis) secara terotomatisasi dan komparatif guna menghasilkan rekomendasi desain sistem kebugaran digital yang lebih adaptif dan transparan terhadap karakteristik pelari lokal."*
