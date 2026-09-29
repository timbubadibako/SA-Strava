"""
Script Scraping Ulasan Apple App Store untuk Strava (ID: 426826309)
Metode: Native iTunes RSS Customer Reviews API (Zero Extra Dependency)
Region: Indonesia ('id')
"""

import time
import json
import urllib.request
import pandas as pd

APP_ID = "426826309"  # Apple ID resmi untuk Strava
COUNTRY = "id"
OUTPUT_FILE = "strava_appstore_reviews_raw.csv"

all_reviews = []
print(f"[*] Memulai scraping ulasan Apple App Store (Region: {COUNTRY.upper()})...")

# iTunes RSS API menyediakan hingga 10 halaman (maksimum 500 ulasan resmi terbaru dari Apple)
for page in range(1, 11):
    url = f"https://itunes.apple.com/{COUNTRY}/rss/customerreviews/page={page}/id={APP_ID}/sortBy=mostRecent/json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            entries = data.get("feed", {}).get("entry", [])
            
            # Entry index 0 adalah metadata aplikasi, ulasan dimulai dari index 1
            reviews_batch = entries[1:] if len(entries) > 1 else []
            if not reviews_batch:
                print(f"[!] Halaman {page} kosong atau mencapai batas ulasan.")
                break
                
            for entry in reviews_batch:
                rev_id = entry.get("id", {}).get("label", "")
                author = entry.get("author", {}).get("name", {}).get("label", "")
                title = entry.get("title", {}).get("label", "")
                content = entry.get("content", {}).get("label", "")
                full_text = f"{title}. {content}".strip() if title else content
                score = int(entry.get("im:rating", {}).get("label", 0))
                version = entry.get("im:version", {}).get("label", "")
                updated_at = entry.get("updated", {}).get("label", "")
                
                all_reviews.append({
                    "reviewId": rev_id,
                    "userName": author,
                    "content": full_text,
                    "score": score,
                    "reviewCreatedVersion": version,
                    "at": updated_at,
                    "platform": "Apple App Store"
                })
                
            print(f"[+] Halaman {page}: Berhasil menarik {len(reviews_batch)} ulasan (Total sementara: {len(all_reviews)})")
            time.sleep(1)
            
    except Exception as e:
        print(f"[!] Selesai atau batasan halaman {page}: {e}")
        break

if all_reviews:
    df = pd.DataFrame(all_reviews).drop_duplicates(subset=["reviewId"])
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"\n[OK] Sukses menyimpan {len(df)} ulasan unik Apple App Store ke '{OUTPUT_FILE}'.")
else:
    print("\n[!] Gagal menarik ulasan App Store.")
