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
8. Ảnh media lớn (banner, cover art) lưu trong assets/. Thumbnail video lấy URL từ CDN TikTok.
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
├── scripts/                ← Script Python cập nhật dữ liệu
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
    └── hero_bg.png         ← Ảnh nền khu vực hero trang chủ (AI-generated)
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
Tiêu đề, logo, heading lớn : 'Bebas Neue'    (Google Fonts)
Nội dung, UI, body text    : 'Be Vietnam Pro' (Google Fonts)
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
6. Community strip: stats + CTA Discord/TikTok
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
    "readtime": "12 phút",
    "views": "1853",
    "pinned": false,
    "related_video_id": "7608841751616359700"
  }
]
```

- `id`: Tăng dần `art-001`, `art-002`...
- `file`: Đường dẫn đến file `.md` trong `posts/`
- `related_video_id`: ID TikTok nhúng trong bài — để `""` nếu không có

---

### 6.3 data/links.json

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
  }
]
```

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

---

## 9. Quy trình deploy

```
1. Chỉnh sửa file (HTML / CSS / JS / JSON / MD)
2. git add -A
3. git commit -m "mô tả thay đổi"
4. git push
→ Cloudflare Pages tự động build & deploy trong ~30 giây
```

**Không cần build step. Cloudflare Pages deploy thẳng file tĩnh.**

---

## 10. Tham chiếu thiết kế

File `wwm-guide-v2.html` là **prototype đã được duyệt về thiết kế**.
- Giữ nguyên toàn bộ CSS variables, font, màu sắc
- KHÔNG thay đổi giao diện — chỉ tách code và kết nối data

---
