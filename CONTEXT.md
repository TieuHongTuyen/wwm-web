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
| **Mục đích** | Web hướng dẫn game chuyên nghiệp — bài viết dạng trang tin tức + video nhúng TikTok/YouTube |
| **Hosting** | Cloudflare Pages (miễn phí, tự động deploy từ GitHub) |
| **Repo** | GitHub — file tĩnh, không backend |

### Kênh & cộng đồng
- TikTok: ~8.600 followers, username `@tiu.hng.tuyn`
- Discord: ~2.000 thành viên
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
8. Ảnh/icon dùng emoji hoặc CDN. KHÔNG upload file media vào repo.
9. Markdown (.md) là định dạng bài viết. KHÔNG dùng .docx hay .txt.
```

---

## 3. Cấu trúc thư mục

```
wwm-guide/
│
├── index.html              ← Trang chủ
├── articles.html           ← Danh sách bài viết
├── article.html            ← Trang đọc bài (dùng chung cho mọi bài, nhận ?id=)
├── videos.html             ← Danh sách video
├── links.html              ← Trang liên kết
│
├── posts/                  ← Bài viết dạng Markdown
│   └── [ten-bai].md
│
├── data/
│   ├── videos.json         ← Metadata video TikTok
│   ├── articles.json       ← Metadata bài viết
│   └── links.json          ← Liên kết mạng xã hội
│
└── assets/
    ├── style.css           ← CSS chung (variables, nav, footer)
    └── main.js             ← JS chung (render helpers)
```

### Nguyên tắc độc lập

| File | Chỉ đọc từ | Không đụng vào |
|---|---|---|
| `videos.json` | — | — |
| `articles.json` | — | — |
| `posts/*.md` | — | — |
| `videos.html` | `videos.json` | articles, posts |
| `articles.html` | `articles.json` | videos, posts |
| `article.html` | `articles.json` + `posts/*.md` | videos |
| `index.html` | Tất cả JSON (chỉ đọc) | Không ghi gì |

---

## 4. Thiết kế & giao diện

### 4.1 Tông màu — Dark Game Editorial

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

### 4.2 Typography

```
Tiêu đề, logo, heading lớn : 'Bebas Neue'    (Google Fonts)
Nội dung, UI, body text    : 'Be Vietnam Pro' (Google Fonts)

<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### 4.3 Phong cách
- Dark game editorial — tối, vàng gold nổi bật
- Nav: fixed top, blur backdrop, height 60px
- Card hover: `translateY(-4px)` + border accent sáng
- Transition: `0.2s ease` toàn bộ
- Border radius: 8–12px card, 6px badge/button
- Scrollbar: 4px width, màu accent

### 4.4 Layout từng trang

**index.html**
1. Nav (fixed, dùng chung tất cả trang)
2. Hero: grid 2 cột — trái (tiêu đề Bebas Neue lớn + stats + 2 CTA button), phải (decorative dark grid + featured card nổi bật)
3. Category strip: 4 ô ngang — Hướng dẫn / Nhân vật / Video / Podcast
4. Section "Bài viết nổi bật": editorial grid — 1 card to trái + 2 card nhỏ phải xếp dọc
5. Section "Video mới nhất": 5 card dọc tỷ lệ 9:16
6. Community strip: stats + CTA Discord/TikTok
7. Footer đơn giản

**articles.html**
1. Nav
2. Page hero: tiêu đề + đếm số bài
3. Filter bar: pill buttons (Tất cả / Hướng dẫn / Nhân vật / Podcast / Meta)
4. Layout 2 cột: main (danh sách bài dạng list-item) + sidebar (video liên quan + bài đọc nhiều)
5. Mỗi list-item: thumbnail emoji + badge category + tiêu đề lớn + mô tả 2 dòng + meta (ngày, thời gian đọc, lượt xem)
6. Click bài → điều hướng sang `article.html?id=art-xxx`

**article.html**
1. Nav
2. Nội dung căn giữa, max-width 740px, padding rộng
3. Header bài: badge + tiêu đề Bebas Neue cỡ lớn + lead paragraph + metadata
4. Divider
5. Body: render từ Markdown — `##` có border-left 3px accent vàng
6. Nếu `related_video_id` tồn tại: render video embed block (preview + nút mở modal)
7. Back button về articles.html

**videos.html**
1. Nav
2. Page hero
3. Filter bar: tags
4. Grid 5 cột, card tỷ lệ 9:16, click → modal TikTok embed

**links.html**
1. Nav
2. Avatar hexagon gradient + tên + bio
3. Danh sách link card (icon màu + tên + mô tả + mũi tên)

---

## 5. Cấu trúc dữ liệu JSON

### 5.1 data/videos.json

```json
[
  {
    "id": "7616618393407393045",
    "title": "[Podcast] Tin tức ngày 13-03-2026",
    "tags": ["Tổng hợp"],
    "date": "2026-03-13",
    "pinned": false
  }
]
```

- `id`: ID TikTok — số dài ở cuối URL video
- `title`: Giữ nguyên prefix `[Podcast]`, `[Hướng dẫn]`, `[Phân tích]`
- `tags`: Mảng, chỉ dùng tag chuẩn ở mục 6
- `date`: `YYYY-MM-DD`
- `pinned`: `true` = lên đầu danh sách

**Nhúng TikTok:**
```html
<blockquote class="tiktok-embed"
  cite="https://www.tiktok.com/@tiu.hng.tuyn/video/{id}"
  data-video-id="{id}">
</blockquote>
<script async src="https://www.tiktok.com/embed.js"></script>
```

---

### 5.2 data/articles.json

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
    "readtime": "12 phút",
    "views": "1853",
    "pinned": false,
    "related_video_id": "7608841751616359700"
  }
]
```

- `id`: Tăng dần `art-001`, `art-002`...
- `file`: Đường dẫn đến file `.md` trong `posts/`
- `icon`: Emoji làm thumbnail card
- `related_video_id`: ID TikTok nhúng vào trong bài — để `""` nếu không có
- Các field còn lại: tự giải thích

---

### 5.3 data/links.json

```json
[
  {
    "name": "TikTok",
    "description": "8.600+ followers · Video mới mỗi ngày",
    "url": "https://tiktok.com/@tiu.hng.tuyn",
    "icon": "🎵",
    "color": "#e8b84b",
    "bg": "rgba(232,184,75,0.1)",
    "order": 1
  },
  {
    "name": "Discord",
    "description": "2.000+ thành viên · Hỏi đáp thực chiến",
    "url": "https://discord.gg/INVITE_CODE",
    "icon": "💬",
    "color": "#5865F2",
    "bg": "rgba(88,101,242,0.12)",
    "order": 2
  },
  {
    "name": "Facebook",
    "description": "Group cộng đồng game thủ Việt",
    "url": "https://facebook.com/groups/TEN_GROUP",
    "icon": "👥",
    "color": "#1877F2",
    "bg": "rgba(24,119,242,0.1)",
    "order": 3
  },
  {
    "name": "YouTube",
    "description": "Video dài · Phân tích chi tiết",
    "url": "https://youtube.com/@TEN_KENH",
    "icon": "▶",
    "color": "#FF0000",
    "bg": "rgba(255,0,0,0.1)",
    "order": 4
  }
]
```

Thay `INVITE_CODE`, `TEN_GROUP`, `TEN_KENH` bằng link thật trước khi deploy.

---

## 6. Tag & Category chuẩn

### Tags video
```
Hướng dẫn   — gameplay, boss, chiến thuật
Nhân vật    — phân tích, review nhân vật
Tổng hợp    — podcast, tin tức, tổng hợp
Meta        — tier list, đội hình, ranking
Event       — sự kiện giới hạn thời gian
```

### Category bài viết + badge CSS
```
Hướng dẫn → .badge-guide   bg: rgba(232,184,75,0.15)  color: var(--accent)
Nhân vật   → .badge-char    bg: rgba(78,205,196,0.12)  color: var(--teal)
Meta       → .badge-meta    bg: rgba(74,158,255,0.12)  color: var(--blue)
Podcast    → .badge-podcast bg: rgba(224,82,82,0.12)   color: var(--red)
Event      → .badge-guide
```

---

## 7. Cấu trúc file Markdown (posts/)

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
- `**text**` — in đậm
- `- item` — danh sách
- Dòng trống giữa các đoạn văn
- KHÔNG dùng HTML trong file .md

---

## 8. Cơ chế article.html đọc Markdown

`article.html` nhận query string `?id=art-001` từ URL.

```javascript
// Bước 1: Lấy id từ URL
const id = new URLSearchParams(location.search).get('id');

// Bước 2: Fetch articles.json, tìm bài khớp id
const res = await fetch('data/articles.json');
const articles = await res.json();
const article = articles.find(a => a.id === id);

// Bước 3: Fetch file .md
const mdRes = await fetch(article.file);
const markdown = await mdRes.text();

// Bước 4: Convert và inject
// Dùng marked.js từ CDN:
// <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/9.1.6/marked.min.js"></script>
document.getElementById('article-body').innerHTML = marked.parse(markdown);

// Bước 5: Nếu có video liên quan
if (article.related_video_id) {
  // render video embed block bên dưới nội dung
}
```

---

## 9. Tham chiếu thiết kế

File `wwm-guide-v2.html` là **prototype đã được duyệt về thiết kế**.

Khi build web thật từ file này:
- Giữ nguyên toàn bộ CSS variables, font, màu sắc
- Tách thành các file theo cấu trúc mục 3
- Thay dữ liệu hardcode trong HTML bằng fetch JSON/Markdown thật
- KHÔNG thay đổi giao diện — chỉ tách code và kết nối data

---
