"""
Modul Preprocessing & Aspect-Based Sentiment Labeling
Dataset: Google Play Store Reviews (com.strava)
Standar: Riset Jurnal Publikasi Ilmiah (Ponytail / Zero-Bloat)
"""

import re
import pandas as pd
from typing import Dict, List, Tuple

# Kamus Normalisasi Kata Slang & Singkatan Bahasa Indonesia
SLANG_DICT: Dict[str, str] = {
    "yg": "yang", "ga": "tidak", "gak": "tidak", "nggak": "tidak", "ngga": "tidak",
    "g": "tidak", "tdk": "tidak", "bgt": "banget", "bgtt": "banget", "bgtz": "banget",
    "bgtu": "begitu", "tp": "tapi", "tpi": "tapi", "dgn": "dengan", "dg": "dengan",
    "sdh": "sudah", "udh": "sudah", "udah": "sudah", "dah": "sudah", "blm": "belum",
    "blom": "belum", "krn": "karena", "karna": "karena", "jd": "jadi", "jdi": "jadi",
    "utk": "untuk", "untk": "untuk", "klo": "kalau", "kalo": "kalau", "kl": "kalau",
    "aja": "saja", "aj": "saja", "dr": "dari", "dri": "dari", "sy": "saya",
    "ak": "aku", "gw": "saya", "gue": "saya", "lu": "kamu", "lo": "kamu",
    "bisaa": "bisa", "bisaaa": "bisa", "bener": "benar", "beneran": "benar",
    "baguss": "bagus", "mantapp": "mantap", "mantul": "mantap", "apk": "aplikasi",
    "app": "aplikasi", "apps": "aplikasi", "apik": "bagus", "oke": "bagus",
    "ok": "bagus", "sip": "bagus", "lemot": "lambat", "ngebug": "gangguan",
    "ngelag": "lambat", "force close": "keluar sendiri", "fc": "keluar sendiri",
    "paywall": "berbayar", "subs": "langganan", "sub": "langganan"
}

# Stopwords Bahasa Indonesia esensial (Negation words dikecualikan agar polaritas aman)
NEGATION_WORDS = {"tidak", "bukan", "belum", "kurang", "jangan", "tak", "tiada"}
STOPWORDS_BASE = {
    "yang", "untuk", "pada", "ke", "para", "namun", "menurut", "antara", "dia",
    "dua", "ia", "seperti", "jika", "sehingga", "kembali", "dan", "ini", "karena",
    "oleh", "saat", "oleh karena itu", "setelah", "kurang", "adalah", "itu",
    "atas", "kemudian", "serta", "saja", "telah", "bisa", "ada", "mereka",
    "dalam", "bisa", "dari", "akan", "dengan", "ia", "terhadap", "atau", "juga",
    "kita", "kami", "kamu", "saya", "anda", "begitu", "mengapa", "kenapa", "sangat"
}
ACTIVE_STOPWORDS = STOPWORDS_BASE - NEGATION_WORDS

# Taksonomi Kata Kunci 5 Aspek Strava
ASPECT_LEXICONS: Dict[str, List[str]] = {
    "GPS_TRACKING": [
        "gps", "sinyal", "rute", "jarak", "km", "kilometer", "akurasi", "peta",
        "map", "loncat", "elevasi", "ketinggian", "kecepatan", "pace", "lokasi",
        "tracking", "lacak", "akurat", "nyasar", "garmin", "jalur"
    ],
    "UI_UX": [
        "tampilan", "ui", "ux", "menu", "desain", "antarmuka", "ribet", "simpel",
        "mudah", "font", "gelap", "tema", "navigasi", "grafik", "tombol",
        "tulisan", "user friendly", "bingung", "sederhana"
    ],
    "GAMIFICATION": [
        "segmen", "segment", "leaderboard", "kom", "qom", "peringkat", "tantangan",
        "challenge", "teman", "kudos", "prestasi", "medali", "trofi", "lomba",
        "rekor", "komunitas", "klub", "feed", "bagikan", "share"
    ],
    "SUBSCRIPTION": [
        "bayar", "langganan", "premium", "mahal", "harga", "duit", "uang", "kunci",
        "fitur berbayar", "free trial", "biaya", "berlangganan", "beli", "promo"
    ],
    "STABILITY": [
        "crash", "keluar sendiri", "baterai", "boros", "panas", "force close",
        "error", "bug", "lag", "lambat", "lemot", "jam", "smartwatch",
        "sinkron", "sync", "koneksi", "gagal", "rusak", "macet", "hang"
    ]
}


def clean_text(text: str) -> str:
    """Membersihkan karakter tak perlu, emoji, URL, angka dan tanda baca."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"[-+]?[0-9]+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_slang(text: str) -> str:
    """Menyelaraskan slang dan singkatan informal."""
    tokens = text.split()
    normalized_tokens = [SLANG_DICT.get(token, token) for token in tokens]
    return " ".join(normalized_tokens)


def remove_stopwords(text: str) -> str:
    """Menghapus stopword sembari menjaga kata negasi."""
    tokens = text.split()
    filtered = [token for token in tokens if token not in ACTIVE_STOPWORDS]
    return " ".join(filtered)


def map_sentiment(score: int) -> str:
    """Memetakan skor rating bintang 1-5 ke 3 kelas sentimen."""
    if score >= 4:
        return "POSITIVE"
    elif score == 3:
        return "NEUTRAL"
    else:
        return "NEGATIVE"


def detect_aspect(text: str) -> str:
    """Klasifikasi aspek ulasan berbasis domain keyword matching."""
    scores: Dict[str, int] = {aspect: 0 for aspect in ASPECT_LEXICONS}
    tokens = set(text.split())

    for aspect, keywords in ASPECT_LEXICONS.items():
        for kw in keywords:
            if kw in tokens or kw in text:
                scores[aspect] += 1

    max_score = max(scores.values())
    if max_score == 0:
        return "GENERAL"
    
    # Pilih aspek dengan kecocokan terbanyak
    for aspect, score in scores.items():
        if score == max_score:
            return aspect
    return "GENERAL"


def process_dataset(input_csv: str, output_csv: str) -> pd.DataFrame:
    """Menjalankan seluruh pipeline pembersihan dan ekstraksi fitur."""
    print(f"[*] Membaca data mentah: {input_csv}")
    df = pd.read_csv(input_csv)

    # 1. Hapus nilai kosong
    df = df.dropna(subset=["content", "score"]).copy()
    print(f"[+] Total baris valid: {len(df)}")

    # 2. Text Cleansing
    print("[*] Menjalankan pembersihan teks (regex, slang, stopword)...")
    df["clean_text"] = df["content"].apply(clean_text)
    df["clean_text"] = df["clean_text"].apply(normalize_slang)
    df["clean_text"] = df["clean_text"].apply(remove_stopwords)

    # Filter teks yang menjadi kosong setelah cleaning
    df = df[df["clean_text"].str.strip() != ""].copy()
    print(f"[+] Total setelah pembersihan: {len(df)} ulasan")

    # 3. Labeling Sentimen & Aspek
    print("[*] Melabeli sentimen 3-kelas dan 5-kategori aspek...")
    df["sentiment_label"] = df["score"].apply(map_sentiment)
    df["aspect_category"] = df["clean_text"].apply(detect_aspect)

    # 4. Ringkas kolom output
    columns_to_keep = [
        "reviewId", "userName", "score", "at",
        "content", "clean_text", "sentiment_label", "aspect_category"
    ]
    df_out = df[[c for c in columns_to_keep if c in df.columns]]

    # 5. Simpan hasil
    df_out.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"[OK] Berhasil menyimpan dataset bersih: {output_csv}")
    
    # Print ringkasan
    print("\n=== Ringkasan Distribusi Sentimen ===")
    print(df_out["sentiment_label"].value_counts())
    print("\n=== Ringkasan Distribusi Aspek ===")
    print(df_out["aspect_category"].value_counts())

    return df_out


if __name__ == "__main__":
    INPUT_FILE = "strava_reviews_raw.csv"
    OUTPUT_FILE = "strava_reviews_processed.csv"
    process_dataset(INPUT_FILE, OUTPUT_FILE)
