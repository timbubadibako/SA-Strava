"""
Script Scraping 10.000 Ulasan Google Play Store untuk Strava
Target Paket: com.strava | Bahasa: Indonesia | Negara: ID
"""

import time
import pandas as pd
from google_play_scraper import reviews, Sort

APP_ID = 'com.strava'
TARGET_COUNT = 10000
OUTPUT_FILE = 'strava_reviews_raw.csv'

print(f"[*] Memulai scraping ulasan aplikasi: {APP_ID}")
print(f"[*] Target penarikan: {TARGET_COUNT} ulasan...")

all_reviews = []
continuation_token = None
batch_size = 200 # Google Play Scraper maksimal 200 per call

try:
    while len(all_reviews) < TARGET_COUNT:
        result, continuation_token = reviews(
            APP_ID,
            lang='id',
            country='id',
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=continuation_token
        )
        
        if not result:
            print("[!] Tidak ada ulasan lagi yang dapat ditarik.")
            break
            
        all_reviews.extend(result)
        print(f"[+] Berhasil menarik: {len(all_reviews)} / {TARGET_COUNT} ulasan...")
        
        # Jeda anti-rate limit
        time.sleep(1)
        
        if not continuation_token:
            print("[!] Tidak ada continuation token lagi.")
            break

    # Potong jika lebih dari target
    all_reviews = all_reviews[:TARGET_COUNT]

    # Ekspor ke DataFrame & CSV
    df = pd.DataFrame(all_reviews)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"\n[✓] SUKSES! {len(df)} ulasan berhasil disimpan ke '{OUTPUT_FILE}'.")

except Exception as e:
    print(f"\n[X] Terjadi error: {e}")
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"[!] Menyimpan {len(df)} ulasan yang berhasil ditarik sebelum crash.")
