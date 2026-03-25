import sys
import os
import json
import re
import unicodedata
from datetime import datetime

# Fix encoding tương thích Windows PowerShell
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT_DIR, "posts")
JSON_PATH = os.path.join(ROOT_DIR, "data", "articles.json")

VALID_CATEGORIES = ["Nhân vật", "Hướng dẫn", "Meta", "Podcast", "Tin tức"]

def remove_accents(input_str):
    s = re.sub(r'[đĐ]', 'd', input_str)
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    return s

def create_slug(title, category):
    slug_base = remove_accents(title).lower()
    slug_base = re.sub(r'[^a-z0-9\s-]', '', slug_base)
    slug_base = re.sub(r'[\s-]+', '-', slug_base).strip('-')
    
    if category == "Nhân vật": return f"phan-tich-{slug_base}"
    if category == "Hướng dẫn": return f"huong-dan-{slug_base}"
    if category == "Meta": return f"tier-list-{slug_base}"
    if category == "Podcast": return f"podcast-{slug_base}"
    if category == "Tin tức": return f"tin-tuc-{slug_base}"
    return slug_base

def main():
    print("=" * 50)
    print("  IMPORT BILIBILI BẰNG DỮ LIỆU F12 CONSOLE")
    print("=" * 50)
    
    if len(sys.argv) < 3:
        print("Sử dụng: python scripts/import_bilibili.py \"Tên Bài Viết\" \"Category\"")
        print("Category hợp lệ: " + " / ".join(VALID_CATEGORIES))
        sys.exit(1)

    title = sys.argv[1].strip()
    category = sys.argv[2].strip()
    
    if category not in VALID_CATEGORIES:
        print(f"[ERROR] Loại bài '{category}' không hợp lệ.")
        sys.exit(1)

    data_file = os.path.join(ROOT_DIR, 'bilibili-data.json')
    if not os.path.exists(data_file):
        print(f"[ERROR] Không tìm thấy file gốc: {data_file}")
        print("Hãy thao tác F12 trên Bilibili, dán mã JS, copy kết quả và lưu vào file này trước.")
        sys.exit(1)
        
    with open(data_file, 'r', encoding='utf-8') as f:
        try:
            b_data = json.load(f)
        except json.JSONDecodeError:
            print(f"[ERROR] File {data_file} sai định dạng JSON.")
            sys.exit(1)
            
    slug = create_slug(title, category)
    post_filepath = os.path.join(POSTS_DIR, f"{slug}.md")
    
    if os.path.exists(post_filepath):
        print(f"[ERROR] Bài viết với slug '{slug}' đã tồn tại! ({post_filepath})")
        sys.exit(1)

    # 1. Xây dựng nội dung file .md dựa trên dữ liệu F12
    # Thêm Header Lệnh AI cho người dùng copy dán thẳng lên GPT
    md_content = "<!-- \n"
    md_content += "🤖 LỆNH CHO AI CHUYÊN NGÀNH DỊCH THUẬT (COPY PHẦN NÀY DÁN VÀO CHATGPT/CLAUDE):\n"
    md_content += "---------------------------------------------------------\n"
    md_content += "Bạn là chuyên gia dịch thuật game kiếm hiệp 'Yến Vân Thập Lục Thanh' (Where Winds Meet). "
    md_content += "Hãy dịch toàn bộ văn bản tiếng Trung trong bài Markdown dưới đây sang tiếng Việt. "
    md_content += "Yêu cầu bắt buộc:\n"
    md_content += "1. Tuyệt đối giữ nguyên 100% cấu trúc Markdown và KHÔNG ĐƯỢC làm hỏng/tự sửa các đường link ảnh ![Ảnh](https://...).\n"
    md_content += "2. Dịch mượt mà, dùng văn phong game MMORPG cổ trang.\n"
    md_content += "3. Đầu ra (Output) chỉ trả lời bằng ĐOẠN CODE MARKDOWN CHUẨN đã được dịch toàn bộ, không cần giải thích thêm.\n"
    md_content += "---------------------------------------------------------\n"
    md_content += "-->\n\n"

    md_content += f"# {title}\n\n"
    if b_data.get('url'):
        # Không dùng dấu > để trích dẫn vì GitHub markdown đôi khi lỗi nếu chèn URL lớn.
        md_content += f"> Nguồn bài viết (tham khảo): [Bilibili]({b_data['url']})\n\n"
        
    img_idx = 1
    blocks = b_data.get('blocks', [])
    for block in blocks:
        if block['type'] == 'image':
            src = block['src']
            md_content += f"![Ảnh {img_idx}](https://wsrv.nl/?url={src})\n\n"
            img_idx += 1
        elif block['type'] == 'text':
            # Phục hồi dấu xuống dòng markdown
            text = block['text'].replace('\n\n', '\n\n').replace('\n', '  \n')
            # Xuất văn bản thuần tự nhiên (AI sẽ quét toàn bộ và dịch)
            md_content += f"{text}\n\n"

    # Ghi ra file markdown hoàn chỉnh
    with open(post_filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"[OK] Đã tạo bài viết    : posts/{slug}.md")
    
    # 2. Cập nhật vào data/articles.json (Tương tự như new_post.py)
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception:
        articles = []
        
    last_id_num = 0
    for a in articles:
        m = re.match(r'art-(\d+)', a.get('id', ''))
        if m:
            last_id_num = max(last_id_num, int(m.group(1)))
    new_id = f"art-{last_id_num + 1:03d}"
    
    icon_map = {
        'Hướng dẫn': '⚔️',
        'Nhân vật':  '👤',
        'Meta':      '🏆',
        'Podcast':   '🎙️',
        'Tin tức':   '📰',
    }

    # Trích xuất URL ảnh đầu tiên từ bilibili-data.json để làm ảnh bìa
    first_image_url = None
    for block in blocks:
        if block.get('type') == 'image':
            raw_src = block.get('src', '')
            if raw_src:
                first_image_url = f"https://wsrv.nl/?url={raw_src}"
            break

    new_article = {
        "id": new_id,
        "title": title,
        "category": category,
        "description": "TODO: Thêm mô tả ngắn gọn cho bài viết",
        "image": first_image_url or "",
        "file": f"posts/{slug}.md",
        "icon": icon_map.get(category, '📄'),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "pinned": False,
        "related_video_id": ""
    }
    
    articles.insert(0, new_article)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
        
    print(f"[OK] articles.json    : Đã thêm bài viết ID {new_id}")
    
    print("\n" + "=" * 50)
    print("🎉 HOÀN TẤT VIỆC TẠO DÀN BÀI VÀ METADATA TỰ ĐỘNG!")
    print("=" * 50)
    print(f"👉 1. Mở bài viết {slug}.md, COPY TOÀN BỘ thả vào ChatGPT/Claude để dịch tự động.")
    print(f"👉 2. Cập nhật description  : data/articles.json")

if __name__ == '__main__':
    main()
