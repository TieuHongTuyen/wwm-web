"""
csv_to_videos_json.py
Parse export-tiktok-videos.csv → data/videos.json

CSV columns (row 1 header):
  0  Video caption
  1  Posted date  (HH:MM:SS DD/M/YY)
  2  Video ID
  3  Video URL
  4  Video views
  5  Like count
  6  Comment count
  7  Share count
  8  Favorites count
  9  Reach
  10 Video duration
  11 Total time watched
  12 Average time watched
  13 Watched full video rate
  14 New followers
  15 Profile views
  16 Traffic source   (multiline cell)
  17 Gender distribution
  18 Top countries
  19 Viewer types
  20 Audience retention (multiline - 300+ rows)
  21 Engagement likes   (multiline - 300+ rows)

Tag detection từ tiêu đề:
  [Podcast]   → Tổng hợp
  [Hướng dẫn] → Hướng dẫn
  [Phân tích] → Nhân vật
  [Event]     → Event
  còn lại     → Hướng dẫn
"""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV_PATH  = ROOT / "export-tiktok-videos.csv"
JSON_PATH = ROOT / "data" / "videos.json"

# Đọc file với csv.reader (tự xử lý quoted multiline fields)
with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
data_rows = rows[1:]

print(f"Total rows (including empty): {len(data_rows)}")

def detect_tags(caption: str) -> list:
    cap_lower = caption.lower()
    if "[podcast]" in cap_lower or "tin tức" in cap_lower:
        return ["Tổng hợp"]
    if "[phân tích]" in cap_lower or "phân tích" in cap_lower:
        return ["Nhân vật"]
    if "[hướng dẫn]" in cap_lower or "hướng dẫn" in cap_lower:
        return ["Hướng dẫn"]
    if "[meta]" in cap_lower or "tier list" in cap_lower or "meta" in cap_lower:
        return ["Meta"]
    if "[event]" in cap_lower or "event" in cap_lower or "sự kiện" in cap_lower:
        return ["Event"]
    return ["Hướng dẫn"]

def clean_title(caption: str) -> str:
    """
    1. Bỏ hashtag và mọi thứ sau đó
    2. Lấy 2 segment đầu sau split ' | '
       VD: '[HD] Phần 05 | QUÁCH HÂN - QUỶ THẦN SẦU | Hướng dẫn《...》'
       → '[HD] Phần 05 | QUÁCH HÂN - QUỶ THẦN SẦU'
    3. Bỏ nội dung trong 《》
    4. Chuẩn hoá khoảng trắng
    """
    title = caption

    # Bỏ hashtag
    for marker in [" #", "\n#"]:
        idx = title.find(marker)
        if idx > 0:
            title = title[:idx]

    # Lấy tối đa 2 segment (bỏ brand suffix 《Yến Vân...》 ở cuối)
    if " | " in title:
        parts = title.split(" | ")
        # Lấy 2 parts đầu, bỏ phần có 《 (brand)
        clean_parts = [p for p in parts if "《" not in p and "》" not in p]
        if clean_parts:
            title = " | ".join(clean_parts[:2])
        else:
            title = parts[0]  # fallback

    # Bỏ nội dung trong 《》 còn sót
    title = re.sub(r'《[^》]*》', '', title)

    return title.strip()

import urllib.request
import urllib.error

def fetch_tiktok_thumbnail(video_id: str, video_url: str) -> str:
    """Gọi TikTok Oembed để lấy thumbnail_url (Direct CDN URL của TikTok)"""
    oembed_url = f"https://www.tiktok.com/oembed?url={video_url}"
    try:
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            thumb_url = data.get("thumbnail_url")
            
            if thumb_url:
                print(f"  [+] Fetched Oembed URL: {video_id}")
                return thumb_url
    except Exception as e:
        print(f"  [-] Failed Oembed {video_id}: {e}")
        
    return ""

def parse_date(date_str: str) -> str:
    """
    Các dạng: '13:09:40 13/3/26'  →  '2026-03-13'
    """
    date_str = date_str.strip()
    # Remove time part
    parts = date_str.split(" ")
    date_part = parts[-1]  # 'DD/M/YY' or 'DD/MM/YY'
    try:
        d, m, y = date_part.split("/")
        year = int(y)
        if year < 100:
            year += 2000
        return f"{year:04d}-{int(m):02d}-{int(d):02d}"
    except Exception:
        return date_str

videos = []
for row in data_rows:
    # Bỏ qua dòng trống
    if not row or not row[0].strip():
        continue
    # Cần ít nhất 4 cột (caption, date, id, url)
    if len(row) < 4:
        continue

    caption = row[0].strip()
    date_raw = row[1].strip() if len(row) > 1 else ""
    video_id = row[2].strip() if len(row) > 2 else ""
    video_url = row[3].strip() if len(row) > 3 else f"https://www.tiktok.com/@tiu.hng.tuyn/video/{video_id}"
    views    = row[4].strip() if len(row) > 4 else "0"

    if not video_id:
        continue

    title = clean_title(caption)
    tags  = detect_tags(caption)
    date  = parse_date(date_raw)
    thumbnail = fetch_tiktok_thumbnail(video_id, video_url)

    v = {
        "id":        video_id,
        "title":     title,
        "tags":      tags,
        "date":      date,
        "thumbnail": thumbnail,
        "pinned":    False,
    }
    videos.append(v)

# Sắp xếp mới nhất trước
videos.sort(key=lambda v: v["date"], reverse=True)

print(f"Videos parsed: {len(videos)}")

# Preview 5 đầu
for v in videos[:5]:
    print(f"  {v['date']}  {v['id']}  {v['tags']}  {v['title'][:60]}")

JSON_PATH.parent.mkdir(exist_ok=True)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)

print(f"\n✅ Đã ghi {len(videos)} video vào {JSON_PATH}")
