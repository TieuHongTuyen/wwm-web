import sys
import os
import json
import re
import unicodedata
from datetime import datetime

# Fix encoding cho Windows PowerShell — không gây treo
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Cấu hình đường dẫn tuyệt đối
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT_DIR, "posts")
IMAGES_DIR = os.path.join(ROOT_DIR, "assets", "images")
JSON_PATH = os.path.join(ROOT_DIR, "data", "articles.json")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")

# Map loại bài → file template
TEMPLATE_MAP = {
    "Nhân vật":  "nhan-vat.md",
    "Hướng dẫn": "huong-dan-boss.md",
    "Meta":      "meta-tier-list.md",
    "Podcast":   "podcast.md",
    "Tin tức":   "tin-tuc.md",
}

VALID_CATEGORIES = list(TEMPLATE_MAP.keys())

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

def prompt_title():
    """Nhập tiêu đề từ bàn phím, không cho để trống"""
    while True:
        title = input("Tieu de bai viet: ").strip()
        if title:
            return title
        print("[!] Tieu de khong duoc de trong. Vui long nhap lai.")

def prompt_category():
    """Chọn loại bài bằng số"""
    print("Loai bai:")
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input(f"Chon (1-{len(VALID_CATEGORIES)}): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(VALID_CATEGORIES):
                return VALID_CATEGORIES[idx]
        print(f"[!] Vui long nhap so tu 1 den {len(VALID_CATEGORIES)}.")

def main():
    print("=" * 50)
    print("TAO BAI VIET MOI")
    print("=" * 50)

    # Ưu tiên đối số dòng lệnh nếu có, fallback về interactive
    if len(sys.argv) >= 3:
        title    = sys.argv[1].strip()
        category = sys.argv[2].strip()
        if category not in TEMPLATE_MAP:
            print(f'[!] Loai bai "{category}" khong hop le.')
            print('Loai bai hop le: ' + ' / '.join(VALID_CATEGORIES))
            sys.exit(1)
    else:
        title    = prompt_title()
        print()
        category = prompt_category()

    print()

    slug          = create_slug(title)
    template_file = TEMPLATE_MAP[category]
    template_path = os.path.join(TEMPLATES_DIR, template_file)

    # Preview trước khi tạo
    print(f"  Title    : {title}")
    print(f"  Category : {category}")
    print(f"  Slug     : {slug}")
    print()
    confirm = input("Xac nhan tao bai? (Enter = co / n = huy): ").strip().lower()
    if confirm == 'n':
        print("Da huy.")
        sys.exit(0)
    print()

    # 1. Tạo thư mục ảnh
    img_dir = os.path.join(IMAGES_DIR, slug)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
        print(f"[OK] Thu muc anh: assets/images/{slug}/")
    else:
        print(f"[!!] Thu muc anh da ton tai: assets/images/{slug}/")

    # 2. Tạo file Markdown từ template
    md_path = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        if not os.path.exists(template_path):
            print(f"[ERROR] Khong tim thay template: templates/{template_file}")
            print(f"        Hay chay Cursor de tao thu muc templates/ truoc.")
            sys.exit(1)

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Thay placeholder [slug] bằng slug thật
        content = content.replace('[slug]', slug)

        # Điền tiêu đề vào dòng đầu (# )
        content = re.sub(r'^# \n', f'# {title}\n', content, count=1)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[OK] Bai viet: posts/{slug}.md")
    else:
        print(f"[!!] File bai viet da ton tai: posts/{slug}.md")

    # 3. Cập nhật articles.json
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception:
        articles = []

    # Tránh trùng lặp
    for a in articles:
        if a.get('file') == f"posts/{slug}.md":
            print(f"[!!] Bai nay da co trong articles.json, bo qua cap nhat JSON.")
            _print_summary(slug, template_file, None)
            sys.exit(0)

    # Tự động sinh ID mới
    last_id_num = 0
    for a in articles:
        m = re.match(r'art-(\d+)', a.get('id', ''))
        if m:
            last_id_num = max(last_id_num, int(m.group(1)))
    new_id = f"art-{last_id_num + 1:03d}"

    # Map icon theo category
    icon_map = {
        'Huong dan': 'sword',
        'Hướng dẫn': '⚔️',
        'Nhân vật':  '👤',
        'Meta':      '🏆',
        'Podcast':   '🎙️',
        'Tin tức':   '📰',
    }

    new_article = {
        "id":               new_id,
        "title":            title,
        "category":         category,
        "description":      "",
        "file":             f"posts/{slug}.md",
        "icon":             icon_map.get(category, '📄'),
        "date":             datetime.now().strftime("%Y-%m-%d"),
        "pinned":           False,
        "related_video_id": ""
    }

    # Chèn lên đầu mảng
    articles.insert(0, new_article)

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"[OK] articles.json: da them {new_id}")
    _print_summary(slug, template_file, new_id)

def _print_summary(slug, template_file, new_id):
    print("")
    print("=" * 50)
    print("HOAN THANH")
    print("=" * 50)
    print(f"  Slug       : {slug}")
    print(f"  Template   : templates/{template_file}")
    print(f"  Bai viet   : posts/{slug}.md")
    print(f"  Thu muc anh: assets/images/{slug}/")
    if new_id:
        print(f"  JSON ID    : {new_id}")
    print("")
    print("VIEC CAN LAM TIEP THEO:")
    print(f"  1. Tha anh bia vao assets/images/{slug}/")
    print(f"     Dat ten anh bia: 01-cover.jpg")
    print(f"  2. Mo posts/{slug}.md trong Obsidian va viet noi dung")
    print(f"  3. Dien 'description' trong data/articles.json")
    print(f"  4. git add -A && git commit -m 'bai moi: {slug}' && git push")
    print("=" * 50)

if __name__ == "__main__":
    main()
