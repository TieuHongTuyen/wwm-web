import sys
import os
import json
import re
import unicodedata
from datetime import datetime

# Cấu hình đường dẫn tuyệt đối
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT_DIR, "posts")
IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images")
JSON_PATH = os.path.join(ROOT_DIR, "data", "articles.json")

def remove_accents(input_str):
    """Xóa bỏ dấu tiếng Việt"""
    s = re.sub(r'[đĐ]', 'd', input_str)
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    return s

def create_slug(title):
    """Tạo slug chuẩn từ tiêu đề"""
    slug = remove_accents(title).lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s-]+', '-', slug).strip('-')
    return slug

def main():
    if len(sys.argv) < 2:
        print('Cách dùng: python scripts/new_post.py "Tiêu đề bài viết" ["Danh mục"]')
        sys.exit(1)
        
    title = sys.argv[1].strip()
    category = "Hướng dẫn" # Mặc định
    if len(sys.argv) >= 3:
        category = sys.argv[2].strip()
        
    slug = create_slug(title)
    
    # 1. Tạo thư mục ảnh
    img_dir = os.path.join(IMAGES_DIR, slug)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(f"✅ Đã tạo thư mục ảnh: assets/images/{slug}/")
    else:
        print(f"⚠️ Thư mục ảnh đã tồn tại: assets/images/{slug}/")
        
    # 2. Tạo file Markdown bài viết
    md_path = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"![Cover](assets/images/{slug}/01-cover.jpg)\n\n")
            f.write("Đoạn mở đầu tóm tắt nội dung bài viết...\n\n")
            f.write("## Mục 1\n\nNội dung mục 1...\n")
        print(f"✅ Đã tạo file bài viết mẫu: posts/{slug}.md")
    else:
        print(f"⚠️ File bài viết đã tồn tại: posts/{slug}.md")
        
    # 3. Cập nhật articles.json
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception:
        articles = []
        
    # Tránh trùng lặp bài viết vào JSON
    for a in articles:
        if a.get('file') == f"posts/{slug}.md":
            print("⚠️ File bài viết này đã có trong articles.json rồi, bỏ qua cập nhật JSON!")
            print(f"\n🎉 HOÀN TẤT! Hãy mở file posts/{slug}.md để viết bài.")
            sys.exit(0)
            
    # Tự động sinh ID mới (tìm ID lớn nhất hiện tại)
    last_id_num = 0
    for a in articles:
        m = re.match(r'art-(\d+)', a.get('id', ''))
        if m:
            last_id_num = max(last_id_num, int(m.group(1)))
    new_id = f"art-{last_id_num + 1:03d}"
    
    # Map icon theo category
    icon_map = {
        'Hướng dẫn': '⚔️',
        'Nhân vật': '👤',
        'Meta': '🏆',
        'Podcast': '🎙️',
        'Event': '🎪'
    }
    
    new_article = {
        "id": new_id,
        "title": title,
        "category": category,
        "description": "Cập nhật mô tả ngắn của bài viết để hiển thị ngoài trang chủ...",
        "file": f"posts/{slug}.md",
        "icon": icon_map.get(category, '📄'),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "pinned": False,
        "related_video_id": ""
    }
    
    # Chèn lên đầu mảng
    articles.insert(0, new_article)
    
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Đã nạp bài viết mới vào thẻ JSON: data/articles.json (ID sinh tự động: {new_id})")
    print(f"\n🎉 HOÀN TẤT!")
    print(f"1. Hãy copy ảnh ném vào mục assets/images/{slug}/ (đổi tên ảnh đầu thành 01-cover.jpg)")
    print(f"2. Cập nhật file posts/{slug}.md để viết bài")
    print("3. Cập nhật lại description trong articles.json")

if __name__ == "__main__":
    main()
