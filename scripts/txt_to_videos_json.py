"""
txt_to_videos_json.py
Đọc danh-sach-video.txt, gọi TikTok Oembed API để lấy chi tiết Title và Thumbnail

Cách dùng:
  python scripts/txt_to_videos_json.py                   # Chỉ thêm video mới
  python scripts/txt_to_videos_json.py --refresh-thumbnails  # Làm mới thumbnail cho toàn bộ video
"""

import json
import re
import sys
import urllib.request
import urllib.error
import os
import time

os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
TXT_PATH  = ROOT / "danh-sach-video.txt"
JSON_PATH = ROOT / "data" / "videos.json"

REFRESH_THUMBNAILS = "--refresh-thumbnails" in sys.argv

if not REFRESH_THUMBNAILS and not TXT_PATH.exists():
    print(f"Không tìm thấy file {TXT_PATH}")
    exit(1)

lines = []
if not REFRESH_THUMBNAILS:
    with open(TXT_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    print(f"Tổng số URL tìm thấy: {len(lines)}")
else:
    print("⚡ Chế độ: Làm mới TOÀN BỘ thumbnail (--refresh-thumbnails)")

def detect_tags(title: str) -> list:
    cap_lower = title.lower()
    if "[podcast]" in cap_lower or "tin tức" in cap_lower:
        return ["Tổng hợp"]
    if "[phân tích]" in cap_lower or "phân tích" in cap_lower:
        return ["Nhân vật"]
    if "[hướng dẫn]" in cap_lower or "hướng dẫn" in cap_lower:
        return ["Hướng dẫn"]
    if "[meta]" in cap_lower or "tier list" in cap_lower or "cập nhật" in cap_lower or "ưu hóa" in cap_lower:
        return ["Meta"]
    if "[event]" in cap_lower or "event" in cap_lower or "sự kiện" in cap_lower:
        return ["Event"]
    return ["Hướng dẫn"]

def clean_title(title: str) -> str:
    # Title gốc trả về từ oembed có thể chứa ký hiệu lạ hoặc đuôi tài khoản
    # Ví dụ: "#WhereWindsMeet #TieuHuongTuyen ... | Yến Vân Guide"
    for marker in [" #", "\n#"]:
        idx = title.find(marker)
        if idx > 0:
            title = title[:idx]
    
    if " | " in title:
        parts = title.split(" | ")
        clean_parts = [p for p in parts if "《" not in p and "》" not in p]
        if clean_parts:
            title = " | ".join(clean_parts[:2])
        else:
            title = parts[0]
            
    title = re.sub(r'《[^》]*》', '', title)
    return title.strip()

videos = []
base_date = datetime.now()

# Đọc danh sách file JSON cũ nếu tồn tại (để bảo toàn Date và Thumbnail cho video cũ)
existing_videos = {}
if JSON_PATH.exists():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            old_data = json.load(f)
            for v in old_data:
                existing_videos[v["id"]] = v
    except:
        pass

if REFRESH_THUMBNAILS:
    changed_count = 0
    updated_videos = []
    
    old_data_list = []
    if JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            try:
                old_data_list = json.load(f)
            except:
                pass
                
    for v in old_data_list:
        video_id = v["id"]
        url = f"https://www.tiktok.com/@tiu.hng.tuyn/video/{video_id}"
        oembed_url = f"https://www.tiktok.com/oembed?url={url}"
        
        try:
            req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                thumb_url = data.get("thumbnail_url", "")
                
                if thumb_url and thumb_url != v.get("thumbnail"):
                    v["thumbnail"] = thumb_url
                    changed_count += 1
                    print(f"  [↻] Đã làm mới thumbnail: {video_id}")
        except Exception as e:
            print(f"  [-] Lỗi fetch {video_id}: {e}")
        
        updated_videos.append(v)
        time.sleep(0.5)
        
    if changed_count == 0:
        print("No changes detected")
        exit(0)
    else:
        JSON_PATH.parent.mkdir(exist_ok=True)
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(updated_videos, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Đã cập nhật layout/thumbnail cho {changed_count} video vào {JSON_PATH}")
        exit(0)
else:
    for idx, url in enumerate(lines):
        # Lấy ID từ URL (VD: https://www.tiktok.com/@tiu.hng.tuyn/video/7616618393407393045)
        match = re.search(r'/video/(\d+)', url)
        if not match:
            continue
        video_id = match.group(1)
        
        # Nếu video ID này đã tồn tại trong file JSON cũ
        if video_id in existing_videos:
            # Chế độ thường: dùng data cũ (siêu nhanh)
            videos.append(existing_videos[video_id])
            continue

        # Gọi Oembed API
        oembed_url = f"https://www.tiktok.com/oembed?url={url}"
        try:
            req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                thumb_url = data.get("thumbnail_url", "")

                raw_title = data.get("title", "")
                clean_t = clean_title(raw_title)
                if not clean_t:
                    clean_t = f"Video Yến Vân Guide #{video_id[-5:]}"  # Fallback

                # Tạo ngày lùi dần cho gọn
                fake_date = (base_date - timedelta(days=idx)).strftime("%Y-%m-%d")
                
                v = {
                    "id": video_id,
                    "title": clean_t,
                    "tags": detect_tags(clean_t),
                    "date": fake_date,
                    "thumbnail": thumb_url,
                    "pinned": False,
                }
                videos.append(v)
                print(f"  [+] Đã lấy info: {video_id} ({clean_t[:30]}...)")
                
        except Exception as e:
            print(f"  [-] Lỗi fetch {video_id}: {e}")

    # Sắp xếp mới nhất trước
    videos.sort(key=lambda x: str(x.get("date", "")), reverse=True)

    JSON_PATH.parent.mkdir(exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Đã ghi {len(videos)} video vào {JSON_PATH}")
