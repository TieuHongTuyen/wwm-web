# CONTEXT.md — Yến Vân Guide (Where Winds Meet)
> **Đọc toàn bộ file này trước khi làm bất cứ việc gì.**
> Đây là tài liệu duy nhất mô tả dự án. Mọi quyết định kỹ thuật và thiết kế đều đã được thống nhất ở đây.

---

## 1. Tổng quan dự án

| | |
|---|---|
| **Tên web** | Yến Vân Guide |
| **Game** | Where Winds Meet (Yến Vân Thập Lục Thanh) |
| **Ngôn ngữ** | Tiếng Việt hoàn toàn |
| **Mục đích** | Web hướng dẫn game chuyên nghiệp — bài viết dạng trang tin tức + video nhúng TikTok |
| **Hosting** | Cloudflare Pages (miễn phí, tự động deploy từ GitHub) |
| **Repo** | https://github.com/TieuHongTuyen/wwm-web |

### Kênh & cộng đồng
- TikTok: ~8.600 followers — [@tiu.hng.tuyn](https://tiktok.com/@tiu.hng.tuyn)
- Discord (SangTacViet): ~2.000 thành viên — [Tham gia](https://discord.com/invite/CzfJeDdvtt)
- YouTube: [@TieuHongTuyen](https://www.youtube.com/@TieuHongTuyen)
- Facebook: [tieu.hong.tuyen](https://www.facebook.com/tieu.hong.tuyen)
- WWM Map: [wwmmap.pages.dev](https://wwmmap.pages.dev/) — Bản đồ tương tác 12,000+ POI
- Nội dung chính: `[Hướng dẫn]`, `[Phân tích]`, `[Podcast]`

---

## 2. Nguyên tắc kỹ thuật — TUYỆT ĐỐI KHÔNG VI PHẠM

```
1. HTML + CSS + JavaScript thuần. KHÔNG dùng React, Vue, hay bất kỳ framework nào.
2. KHÔNG cần build step. Cloudflare Pages deploy trực tiếp file tĩnh.
3. Mọi nội dung lưu trong file JSON (data/) hoặc Markdown (posts/).
   KHÔNG hardcode nội dung vào HTML.
4. Thêm video  = thêm 1 dòng vào data/videos.json. Không đụng HTML.
5. Thêm bài viết = tạo file .md trong posts/ + thêm 1 dòng vào data/articles.json.
6. Mỗi trang HTML độc lập. Hỏng 1 trang không ảnh hưởng trang khác.
7. KHÔNG dùng localStorage, sessionStorage, hay bất kỳ browser storage nào.
8. Ảnh bài viết lưu trong assets/images/[slug]/ — mỗi bài một thư mục riêng tên trùng slug.
   Thumbnail video lấy URL từ CDN TikTok qua Oembed API (không lưu local).
   KHÔNG upload ảnh lên CDN ngoài — lưu thẳng vào repo GitHub.
9. Markdown (.md) là định dạng bài viết. KHÔNG dùng .docx hay .txt.
```

---

## 3. Cấu trúc thư mục

```
wwm-guide/
│
├── index.html              ← Trang chủ
├── articles.html           ← Danh sách bài viết
├── article.html            ← Trang đọc bài (dùng chung, nhận ?id=)
├── videos.html             ← Danh sách video (Load More pagination)
├── links.html              ← Trang liên kết
├── .gitignore              ← Loại bỏ file tạm và CSV local
│
├── scripts/                ← Script Python tiện ích
│   ├── new_post.py            ← Tạo bài viết mới tự động (1 lệnh)
│   ├── csv_to_videos_json.py  ← Import từ file CSV analytics TikTok (tối đa 20 video)
│   └── txt_to_videos_json.py  ← Import từ file danh-sach-video.txt (không giới hạn)
│
├── posts/                  ← Bài viết dạng Markdown
│   └── [ten-bai].md
│
├── data/
│   ├── videos.json         ← Metadata video TikTok (228+ video)
│   ├── articles.json       ← Metadata bài viết
│   └── links.json          ← Liên kết mạng xã hội
│
└── assets/
    ├── style.css           ← CSS chung (variables, nav, footer)
    ├── main.js             ← JS chung (render helpers, modal)
    ├── hero_bg.png         ← Ảnh nền hero trang chủ (AI-generated)
    └── images/             ← Ảnh bài viết, mỗi bài 1 thư mục tên = slug
        └── [slug]/
            ├── 01-cover.jpg
            ├── 02-[mo-ta].jpg
            └── 03-[mo-ta].jpg
```

### File chỉ dùng local, KHÔNG commit lên GitHub
```
danh-sach-video.txt         ← Danh sách URL video lấy từ DevTools console TikTok
export-tiktok-videos.csv    ← Export từ TikTok Analytics (tối đa 20 video)
```

---

## 4. Quy trình cập nhật video

### Quy trình chuẩn (không giới hạn số lượng):
1. Vào trang profile TikTok trên trình duyệt, cuộn để load hết video
2. Nhấn F12 → Tab Console → gõ `allow pasting` → Enter
3. Dán đoạn JS sau và Enter:
```javascript
let links = [];
document.querySelectorAll('div[data-e2e="user-post-item"] a').forEach(a => {
  if (a.href.includes('/video/')) links.push(a.href);
});
console.log([...new Set(links)].join('\n'));
```
4. Copy kết quả → lưu vào `danh-sach-video.txt` (thư mục gốc)
5. Chạy: `python scripts/txt_to_videos_json.py`
6. `data/videos.json` tự động cập nhật với đầy đủ Tiêu đề, Tag, Thumbnail

### Script txt_to_videos_json.py sẽ:
- Đọc từng URL trong `danh-sach-video.txt`
- Gọi TikTok Oembed API lấy **title** và **thumbnail_url**
- Tự động phân loại tag dựa theo tiêu đề
- **Bảo toàn data cũ**: video đã có trong JSON sẽ không bị ghi đè
- Chỉ gọi API cho video mới (chưa có trong JSON)

### Quy trình cập nhật thumbnail (khi link ảnh TikTok hết hạn):
```
python scripts/txt_to_videos_json.py
```
Chạy lại script là đủ — nó sẽ làm mới toàn bộ thumbnail URL từ API.

---

## 5. Thiết kế & giao diện

### 5.1 Tông màu — Dark Game Editorial

```css
:root {
  /* Nền */
  --bg:       #0a0c0f;
  --bg2:      #111318;
  --bg3:      #181c24;
  --surface:  #1e2330;
  --surface2: #252b3a;

  /* Accent */
  --accent:   #e8b84b;   /* vàng gold — màu nhấn chính */
  --accent2:  #f0d080;   /* vàng sáng hơn, dùng hover */
  --teal:     #4ecdc4;   /* badge Nhân vật */
  --blue:     #4a9eff;   /* badge Meta */
  --red:      #e05252;   /* badge Podcast */

  /* Text */
  --text:     #e8eaf0;
  --text2:    #9aa0b4;
  --text3:    #5a6070;

  /* Border */
  --border:   rgba(232,184,75,0.15);
  --border2:  rgba(255,255,255,0.06);
}
```

### 5.2 Typography

```
Tiêu đề, logo, heading lớn : 'Oswald' weight 700   (Google Fonts — hỗ trợ đầy đủ tiếng Việt)
Nội dung, UI, body text    : 'Be Vietnam Pro'       (Google Fonts)
```

### 5.3 Phong cách
- Dark game editorial — tối, vàng gold nổi bật
- Nav: fixed top, blur backdrop, height 60px
- Card hover: `translateY(-4px)` + border accent sáng
- Transition: `0.2s ease` toàn bộ
- Border radius: 8–12px card, 6px badge/button
- Scrollbar: 4px width, màu accent

### 5.4 Layout từng trang

**index.html**
1. Nav (fixed, dùng chung tất cả trang)
2. Hero: grid 2 cột — trái (tiêu đề + stats + CTA), phải (`hero_bg.png` làm nền + overlay gradient + featured card)
3. Category strip: 4 ô — Hướng dẫn / Nhân vật / Video / Podcast
4. Section "Bài viết nổi bật": editorial grid 1 to + 2 nhỏ
5. Section "Video mới nhất": 5 card 9:16 (top 5 mới nhất từ videos.json)
6. Community strip: stats + Liên kết nổi bật
7. Footer

**articles.html**
1. Nav, Page hero, Filter bar (Tất cả / Hướng dẫn / Nhân vật / Podcast / Meta)
2. Layout 2 cột: danh sách bài + sidebar (video gần nhất + bài đọc nhiều)
3. Click → `article.html?id=art-xxx`

**article.html**
1. Fetch `articles.json` → tìm bài theo `?id=`
2. Fetch file `.md` → render bằng `marked.js` (CDN)
3. `##` headings có border-left 3px vàng
4. Nếu có `related_video_id`: render video embed block + nút mở modal

**videos.html**
1. Page hero, Filter bar (từ tags trong JSON)
2. Grid 5 cột, card 9:16, ảnh bìa từ `thumbnail` URL
3. **Load More pagination**: mỗi lần hiển thị 20 video, nút "Tải thêm video ↓"
4. Click card → Modal TikTok Player API

**links.html**: Avatar hexagon + danh sách link card

---

## 6. Cấu trúc dữ liệu JSON

### 6.1 data/videos.json

```json
[
  {
    "id": "7616618393407393045",
    "title": "[Podcast] TIN TỨC NGÀY 13-03-2026",
    "tags": ["Tổng hợp"],
    "date": "2026-03-13",
    "thumbnail": "https://p16-sign-va.tiktokcdn.com/...",
    "pinned": false
  }
]
```

- `id`: ID TikTok — số ở cuối URL video
- `title`: Giữ nguyên prefix `[Podcast]`, `[Hướng dẫn]`, `[Phân tích]`
- `tags`: Mảng, chỉ dùng tag chuẩn ở mục 7
- `date`: `YYYY-MM-DD`
- `thumbnail`: URL ảnh bìa trực tiếp từ CDN TikTok (lấy qua Oembed API). Có thể làm mới bằng cách chạy lại script.
- `pinned`: `true` = lên đầu danh sách

**Nhúng TikTok (Modal):**
```html
<iframe
  src="https://www.tiktok.com/player/v1/{id}?autoplay=1&loop=1&muted=0&volume=0.5"
  sandbox="allow-popups allow-popups-to-escape-sandbox allow-scripts allow-top-navigation allow-same-origin"
  allowfullscreen>
</iframe>
```

---

### 6.2 data/articles.json

```json
[
  {
    "id": "art-001",
    "title": "Phân tích Doanh Doanh — Cơ chế, Lên đồ và Combo tối ưu",
    "category": "Nhân vật",
    "description": "Phân tích sâu về bộ kỹ năng, cách lên đồ và combo trong meta 2.3.",
    "file": "posts/phan-tich-doanh-doanh.md",
    "icon": "👤",
    "date": "2026-02-20",
    "pinned": false,
    "related_video_id": "7608841751616359700"
  }
]
```

- `id`: Tự động tăng dần — dùng `python scripts/new_post.py` để sinh tự động
- `file`: Đường dẫn đến file `.md` trong `posts/`
- `related_video_id`: ID TikTok nhúng trong bài — để `""` nếu không có
- **Không có** trường `readtime` hay `views` — đã loại bỏ khỏi hệ thống

---

### 6.3 data/links.json

```json
[
  { "name": "TikTok",              "url": "https://tiktok.com/@tiu.hng.tuyn",                   "order": 1 },
  { "name": "Discord — SangTacViet","url": "https://discord.com/invite/CzfJeDdvtt",              "order": 2 },
  { "name": "Facebook",            "url": "https://www.facebook.com/tieu.hong.tuyen",           "order": 3 },
  { "name": "YouTube",             "url": "https://www.youtube.com/@TieuHongTuyen",             "order": 4 },
  { "name": "WWM Map",             "url": "https://wwmmap.pages.dev/",                          "order": 5 }
]
```

Mỗi entry có đầy đủ: `name`, `description`, `url`, `icon`, `color`, `bg`, `order`.

---

## 7. Tag & Category chuẩn

### Tags video
```
Hướng dẫn   — gameplay, boss, chiến thuật
Nhân vật    — phân tích, review nhân vật
Tổng hợp    — podcast, tin tức
Meta        — tier list, đội hình, ranking
Event       — sự kiện giới hạn thời gian
```

### Category bài viết + badge CSS
```
Hướng dẫn → .badge-guide   bg: rgba(232,184,75,0.15)  color: var(--accent)
Nhân vật   → .badge-char    bg: rgba(78,205,196,0.12)  color: var(--teal)
Meta       → .badge-meta    bg: rgba(74,158,255,0.12)  color: var(--blue)
Podcast    → .badge-podcast bg: rgba(224,82,82,0.12)   color: var(--red)
```

---

## 8. Cấu trúc file Markdown (posts/)

Tên file: chữ thường, dấu gạch ngang, không dấu tiếng Việt.
Ví dụ: `posts/phan-tich-doanh-doanh.md`

```markdown
# Tiêu đề bài viết

Đoạn mở đầu / lead paragraph...

## Mục lớn thứ nhất

Nội dung đoạn văn. **Chữ đậm** để nhấn mạnh.

- Mục danh sách 1
- Mục danh sách 2

## Mục lớn thứ hai

Tiếp tục nội dung...
```

**Quy tắc:**
- `#` — tiêu đề bài, chỉ dùng 1 lần ở đầu file
- `##` — mục lớn (render với border-left 3px vàng)
- KHÔNG dùng HTML trong file .md

### Chèn ảnh trong Markdown

Đường dẫn ảnh dùng đường dẫn tương đối từ gốc repo:
```markdown
![Mô tả ảnh](assets/images/phan-tich-doanh-doanh/01-cover.jpg)
```

Ảnh đầu tiên của bài luôn đặt tên `01-cover.jpg`.

---

## 9. Quy ước đặt tên slug và ảnh

### Slug là gì?

Slug là chuỗi định danh duy nhất của mỗi bài viết.
Quy tắc: chữ thường, dấu gạch ngang, không dấu tiếng Việt.

**Quy tắc vàng: 1 bài = 1 slug = 1 thư mục ảnh**

```
posts/[slug].md                    ← file bài viết
assets/images/[slug]/              ← thư mục ảnh của bài
data/articles.json → "file": "posts/[slug].md"
```

Chỉ cần nhớ slug, suy ra được vị trí mọi file liên quan.

---

### Bảng slug theo loại bài

| Loại bài | Công thức | Ví dụ |
|---|---|---|
| Phân tích nhân vật | `phan-tich-[ten]` | `phan-tich-doanh-doanh` |
| Hướng dẫn boss | `huong-dan-boss-[ten]` | `huong-dan-boss-quy-than-sau` |
| Hướng dẫn chuỗi | `huong-dan-[chu-de]-phan-[so]` | `huong-dan-quy-than-sau-phan-1` |
| Podcast tin tức | `podcast-[ngay]-[thang]-[nam]` | `podcast-13-03-2026` |
| Tier list / meta | `tier-list-[chu-de]-mua-[so]` | `tier-list-nhan-vat-mua-2` |

---

### Quy tắc đặt tên ảnh

```
[số thứ tự 2 chữ số]-[mô tả ngắn].jpg

01-cover.jpg          ← ảnh đầu tiên luôn là cover
02-ky-nang-e.jpg
03-combo-pvp.jpg
04-len-do.jpg
```

- Số thứ tự 2 chữ số để GitHub sort đúng thứ tự
- Mô tả: chữ thường, gạch ngang, không dấu
- Định dạng: `.jpg` — nén tốt nhất cho ảnh game
- Kích thước: dưới 500KB mỗi ảnh

---

### Ví dụ đầy đủ

Slug: `phan-tich-doanh-doanh`

```
posts/phan-tich-doanh-doanh.md

assets/images/phan-tich-doanh-doanh/
├── 01-cover.jpg
├── 02-tong-quan.jpg
├── 03-ky-nang-e.jpg
└── 04-len-do.jpg
```

Trong `articles.json`:
```json
"file": "posts/phan-tich-doanh-doanh.md"
```

Trong file `.md`:
```markdown
![Doanh Doanh](assets/images/phan-tich-doanh-doanh/01-cover.jpg)

## Tổng quan nhân vật

![Tổng quan](assets/images/phan-tich-doanh-doanh/02-tong-quan.jpg)
```

---

### Workflow thêm bài mới

```
Bước 1 — Tạo bài mới bằng script (terminal)
  python scripts/new_post.py "Tên bài" "Loại bài"
  Loại bài hợp lệ: Nhân vật · Hướng dẫn · Meta · Podcast
  Script tự tạo: slug, thư mục ảnh, file .md từ template, entry JSON

Bước 2 — Chuẩn bị ảnh
  Thả ảnh bìa vào assets/images/[slug]/
  Đặt tên ảnh bìa: 01-cover.jpg
  Đặt tên ảnh tiếp theo: 02-[mo-ta].jpg, 03-[mo-ta].jpg...

Bước 3 — Viết bài trong Obsidian
  Mở Obsidian (vault = thư mục wwm-web/)
  Mở file posts/[slug].md
  Viết nội dung theo đúng cấu trúc template
  Kéo thả ảnh vào đúng vị trí trong bài
  Dùng Markdown links chuẩn cho phần Xem thêm:
    [Tên bài](slug-bai-lien-quan)
  KHÔNG dùng [[Wikilinks]] — sẽ không render được trên web

Bước 4 — Hoàn thiện metadata
  Mở data/articles.json
  Điền "description" cho bài vừa viết
  Điền "related_video_id" nếu có video TikTok liên quan

Bước 5 — Deploy
  git add -A && git commit -m "bai moi: [slug]" && git push
  Cloudflare Pages tự deploy trong ~30 giây
```

### Obsidian Graph View

```
Nhấn Ctrl+G trong Obsidian để xem bản đồ liên kết giữa các bài.
Các bài có link [Xem thêm] trỏ vào nhau sẽ hiện đường nối trên graph.
Dùng graph để:
- Phát hiện bài nào bị cô lập (chưa liên kết) → ưu tiên viết bài liên quan
- Xác định bài nào là hub trung tâm (nhiều bài trỏ vào) → đánh dấu pinned: true
- Lên kế hoạch nội dung theo cụm chủ đề
```

---

## 10. Quy trình deploy

```
1. Chỉnh sửa file (HTML / CSS / JS / JSON / MD)
2. git add -A
3. git commit -m "mô tả thay đổi"
4. git push
→ Cloudflare Pages tự động build & deploy trong ~30 giây
```

**Không cần build step. Cloudflare Pages deploy thẳng file tĩnh.**

---

## 11. Tham chiếu thiết kế

File `wwm-guide-v2.html` là **prototype đã được duyệt về thiết kế**.
- Giữ nguyên toàn bộ CSS variables, font, màu sắc
- KHÔNG thay đổi giao diện — chỉ tách code và kết nối data

---
