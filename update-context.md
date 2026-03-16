Cập nhật CONTEXT.md với các thay đổi sau. Chỉnh sửa trực tiếp file, không tạo file mới.

\---

## Thay đổi 1 — Nguyên tắc kỹ thuật (mục 2, dòng số 8)

Tìm dòng:

```
8. Ảnh media lớn (banner, cover art) lưu trong assets/. Thumbnail video lấy URL từ CDN TikTok.
```

Thay bằng:

```
8. Ảnh bài viết lưu trong assets/images/\[slug]/ — mỗi bài một thư mục riêng tên trùng slug.
   Thumbnail video lấy URL từ CDN TikTok qua Oembed API (không lưu local).
   KHÔNG upload ảnh lên CDN ngoài — lưu thẳng vào repo GitHub.
```

\---

## Thay đổi 2 — Cấu trúc thư mục (mục 3)

Tìm khối:

```
└── assets/
    ├── style.css           ← CSS chung (variables, nav, footer)
    ├── main.js             ← JS chung (render helpers, modal)
    └── hero\_bg.png         ← Ảnh nền khu vực hero trang chủ (AI-generated)
```

Thay bằng:

```
└── assets/
    ├── style.css           ← CSS chung (variables, nav, footer)
    ├── main.js             ← JS chung (render helpers, modal)
    ├── hero\_bg.png         ← Ảnh nền hero trang chủ (AI-generated)
    └── images/             ← Ảnh bài viết, mỗi bài 1 thư mục tên = slug
        └── \[slug]/
            ├── 01-cover.jpg
            ├── 02-\[mo-ta].jpg
            └── 03-\[mo-ta].jpg
```

\---

## Thay đổi 3 — Cập nhật mục 8 (Cấu trúc file Markdown)

Tìm dòng ở cuối mục 8:

```
- KHÔNG dùng HTML trong file .md
```

Thêm nội dung sau vào ngay bên dưới (vẫn trong mục 8):

```
### Chèn ảnh trong Markdown

Đường dẫn ảnh dùng đường dẫn tương đối từ gốc repo:
```markdown
!\[Mô tả ảnh](assets/images/phan-tich-doanh-doanh/01-cover.jpg)
```

Ảnh đầu tiên của bài luôn đặt tên `01-cover.jpg`.

```

---

## Thay đổi 4 — Thêm mục mới sau mục 8, đặt tên là mục 9

Thêm mục mới \*\*"9. Quy ước đặt tên slug và ảnh"\*\* vào sau mục 8 (đẩy các mục 9, 10 hiện tại thành 10, 11):

```markdown
## 9. Quy ước đặt tên slug và ảnh

### Slug là gì?

Slug là chuỗi định danh duy nhất của mỗi bài viết.
Quy tắc: chữ thường, dấu gạch ngang, không dấu tiếng Việt.

\*\*Quy tắc vàng: 1 bài = 1 slug = 1 thư mục ảnh\*\*

```

posts/\[slug].md                    ← file bài viết
assets/images/\[slug]/              ← thư mục ảnh của bài
data/articles.json → "file": "posts/\[slug].md"

```

Chỉ cần nhớ slug, suy ra được vị trí mọi file liên quan.

---

### Bảng slug theo loại bài

| Loại bài | Công thức | Ví dụ |
|---|---|---|
| Phân tích nhân vật | `phan-tich-\[ten]` | `phan-tich-doanh-doanh` |
| Hướng dẫn boss | `huong-dan-boss-\[ten]` | `huong-dan-boss-quy-than-sau` |
| Hướng dẫn chuỗi | `huong-dan-\[chu-de]-phan-\[so]` | `huong-dan-quy-than-sau-phan-1` |
| Podcast tin tức | `podcast-\[ngay]-\[thang]-\[nam]` | `podcast-13-03-2026` |
| Tier list / meta | `tier-list-\[chu-de]-mua-\[so]` | `tier-list-nhan-vat-mua-2` |

---

### Quy tắc đặt tên ảnh

```

\[số thứ tự 2 chữ số]-\[mô tả ngắn].jpg

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
!\[Doanh Doanh](assets/images/phan-tich-doanh-doanh/01-cover.jpg)

## Tổng quan nhân vật

!\[Tổng quan](assets/images/phan-tich-doanh-doanh/02-tong-quan.jpg)
```

\---

### Workflow thêm bài mới

```
1. Đặt slug
   ví dụ: phan-tich-van-loi

2. Tạo thư mục ảnh
   assets/images/phan-tich-van-loi/
   Upload ảnh: 01-cover.jpg, 02-...

3. Viết bài Markdown
   Lưu: posts/phan-tich-van-loi.md
   Chèn ảnh bằng đường dẫn chuẩn

4. Cập nhật articles.json
   Thêm entry mới với "file": "posts/phan-tich-van-loi.md"

5. git add -A \&\& git commit \&\& git push
   → Cloudflare tự deploy
```

```

---

## Yêu cầu thực thi

1. Chỉnh sửa trực tiếp file `CONTEXT.md` — không tạo file mới
2. Giữ nguyên toàn bộ nội dung không được đề cập thay đổi
3. Đánh lại số thứ tự mục sau khi thêm mục 9 mới (mục 9 cũ → 10, mục 10 cũ → 11)
4. Sau khi xong, tóm tắt những dòng/mục đã thay đổi để tôi kiểm tra

