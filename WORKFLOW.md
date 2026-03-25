# Hướng Dẫn Vận Hành Hệ Thống (WORKFLOW)

Tài liệu này hướng dẫn chi tiết các thao tác vận hành dự án Yến Vân Guide dành cho người dùng không yêu cầu kiến thức lập trình phức tạp.

## Phần 1 — Tổng quan hệ thống

Sơ đồ hoạt động của hệ thống Yến Vân Guide:

```text
[TikTok] --(Script Python/API)--> [Máy Local (Máy tính của bạn)]
                                      |
                                      | git push
                                      v
                             [GitHub Repository]
                                      |
                                      | auto deploy (~30s)
                                      v
                            [Cloudflare Pages]
                                      |
                                      | phục vụ tĩnh
                                      v
                                 [Người đọc]
```

Các thành phần chính và vai trò:
- **Máy local**: Nơi bạn chạy lệnh tạo bài, cập nhật dữ liệu video và viết bài bằng phần mềm Obsidian.
- **GitHub Repository**: Lưu trữ toàn bộ mã nguồn, dữ liệu JSON và hình ảnh. Có GitHub Actions tự động chạy ngầm tải ảnh mới.
- **Cloudflare Pages**: Máy chủ miễn phí, tự động lấy code mới nhất từ GitHub để hiển thị lên web mỗi khi bạn push.
- **TikTok**: Nguồn cung cấp metadata và ảnh bìa video.

---

## Phần 2 — Các tác vụ thường xuyên

### Thêm video mới từ TikTok
**Khi nào làm:** Khi có thêm video mới đăng trên kênh TikTok và muốn đưa lên web.
**Thời gian ước tính:** 2-3 phút.
**Các bước:**
1. Mở trang profile TikTok trên trình duyệt, cuộn xuống để load hết hiển thị video mong muốn.
2. Nhấn F12 để mở Developer Tools, chuyển sang tab Console. Gõ chữ `allow pasting` và nhấn Enter (nếu Chrome yêu cầu).
3. Copy và dán đoạn mã sau vào Console rồi nhấn Enter:
   ```javascript
   let links = [];
   document.querySelectorAll('div[data-e2e="user-post-item"] a').forEach(a => {
     if (a.href.includes('/video/')) links.push(a.href);
   });
   console.log([...new Set(links)].join('\n'));
   ```
4. Copy danh sách URL hiện ra và dán vào file `danh-sach-video.txt` nằm ở thư mục gốc của project (xóa nội dung cũ đi).
5. Mở terminal tại thư mục dự án và chạy lệnh:
   ```bash
   python scripts/txt_to_videos_json.py
   ```
6. Kiểm tra lại web trên terminal bằng cách chạy `python -m http.server 8080`, hoặc mở mã nguồn xem file `data/videos.json` đã có video mới chưa.
7. Chạy lệnh để đưa lên web thực tế:
   ```bash
   git add -A
   git commit -m "update: them video moi"
   git push
   ```
**Kết quả mong đợi:** Web tự động có video mới ở trên cùng danh sách. Hình thumbnail được tự động tạo và tải về local thư mục `assets/thumbnails/`.
**Nếu có lỗi:** Xem tiếp ở mục Debug bên dưới.

### Thêm bài viết mới
**Khi nào làm:** Khi muốn đăng tải bài phân tích, hướng dẫn hoặc tin tức mới lên trang web.
**Thời gian ước tính:** 15-30 phút (chủ yếu là thời gian viết nội dung).
**Các bước:**
1. Chạy lệnh tạo bài viết mới tự động trong terminal (thay thế "Tên Bài Của Bạn" và "Loại Bài"):
   ```bash
   python scripts/new_post.py "Tên Bài Của Bạn" "Nhân vật"
   ```
   *(Các loại bài hợp lệ: `Nhân vật`, `Hướng dẫn`, `Meta`, `Podcast`)*
2. Terminal sẽ tạo ra 1 file `.md` tại thư mục `posts/` và thư mục ảnh tại `assets/images/slug-ten-bai-viet/`.
3. Kéo thả ảnh bìa (đặt tên luôn là `01-cover.jpg`) vào đúng thư mục ảnh vừa tạo. Các ảnh khác đặt `02-xxx.jpg`, `03-xxx.jpg`,...
4. Mở phần mềm Obsidian, tìm đến file vừa tạo trong thư mục `posts/` và bắt đầu viết bài theo định dạng Markdown. Sử dụng URL ảnh tương đối như: `![ảnh 1](assets/images/slug/02-xxx.jpg)`.
5. Mở file `data/articles.json` và bổ sung tóm tắt ngắn vào field `"description"`. Nếu bài liên kết với 1 video TikTok, hãy điền ID TikTok vào trường `"related_video_id"`.
6. Cập nhật lên web bằng cách dùng terminal:
   ```bash
   git add -A
   git commit -m "bai moi: slug-ten-bai-viet"
   git push
   ```
**Kết quả mong đợi:** File MD được tạo đúng template, JSON được chèn tự động ID hợp lệ. Bài viết xuất hiện trên danh sách trang chủ và trang bài viết.


### Việt hóa bài từ yysls.cn
**Khi nào làm:** Khi có bài phân tích bản Trung hay trên yysls.cn cần đưa về web tiếng Việt.
**Thời gian ước tính:** 5-10 phút.
**Các bước:**
1. Mở bài gốc trên yysls.cn, copy nội dung chữ sang công cụ dịch Claude/ChatGPT để dịch sang tiếng Việt.
2. Mở terminal chạy lệnh tạo vỏ bài viết:
   ```bash
   python scripts/new_post.py "Tiêu đề tiếng Việt đã dịch" "Hướng dẫn"
   ```
3. Mở file bài viết `.md` mới sinh ra trong Obsidian.
4. Paste nội dung chữ vừa dịch. Với các vị trí ảnh, copy nguyên link ảnh gốc từ yysls.cn để giữ nguyên link ảnh (hoặc tải ảnh về, đổi tên `01`, `02` và quăng vào thư mục `assets/images/slug-cua-bai/`).
5. Update `data/articles.json` và đăng lên qua Git Push giống như viết bài mới.
**Kết quả mong đợi:** Bài viết hiện đầy đủ nội dung phiên dịch, giữ được tài nguyên hình ảnh gốc.


### Cập nhật thumbnail thủ công
**Khi nào làm:** Rất ít khi thao tác vì đã có GitHub Actions chạy mỗi 6 tiếng. Chỉ chạy khi bạn thêm quá nhiều file vào JSON nhưng bị sót tải ảnh thủ công.
**Thời gian ước tính:** 1-2 phút tùy mạng (cho 230+ video). Lần chạy lại chỉ mất ~2 giây vì các ảnh có sẵn sẽ chạy vượt qua (skip).
**Các bước:**
1. Mở terminal và chạy lệnh:
   ```bash
   python scripts/txt_to_videos_json.py --refresh-thumbnails
   ```
2. Chờ script quét toàn bộ file JSON, tải các ảnh bị sót về thư mục `assets/thumbnails/`.
3. Đẩy code lên GitHub để cập nhật file tĩnh mới.
   ```bash
   git add -A
   git commit -m "chore: force update local thumbnails"
   git push
   ```
**Kết quả mong đợi:** Terminal in ra thông báo `Tổng kết: tải mới X, có sẵn Y`. Lên trang web video sẽ có ngay hình đầy đủ.


### Kiểm tra web sau khi push
**Khi nào làm:** Luôn thực hiện ngay sau bước `git push`.
**Thời gian ước tính:** 1 phút.
**Các bước:**
1. Mở trình duyệt và truy cập trang chủ web: [URL_WEB]
2. Có thể đợi 30 giây đến 1 phút và nhấn Refresh (F5).
3. Kiểm tra bài viết gần nhất có hiện đúng nội dung không. Ấn vào thử xem ảnh thumbnail và link TikTok có nhận không.
**Kết quả mong đợi:** Mọi dữ liệu online khớp hoàn toàn với những gì thấy trên máy tính của bạn khi chạy local.

---

## Phần 3 — Tự động hóa đang chạy

Dự án hiện đang duy trì 1 workflow hoàn toàn tự động trên GitHub:

- **Tên workflow:** `Refresh TikTok Thumbnails`
- **Lịch chạy (cron):** `0 */6 * * *` (Chạy đều đặn mỗi 6 tiếng một lần).
- **Làm gì cụ thể:** Git Actions tự động dựng môi trường Python, chạy script quét file `data/videos.json` để tải các hình ảnh bị khuyết hoặc chưa đồng bộ vào `assets/thumbnails/`. Sau đó bot tự động commit và push ngược những ảnh vừa tải vào repository của bạn.
- **Cách xem log:** Truy cập repo GitHub của bạn → tab **Actions** → bấm vào workflow `Refresh TikTok Thumbnails`.
- **Cách chạy thủ công:** Tại trang Actions → Chọn *Refresh TikTok Thumbnails* ở sidebar trái → Nhấn hộp thoại xám `Run workflow` → Nút xanh **Run workflow**.

---

## Phần 4 — Cấu trúc thư mục thực tế

Cấu trúc file và thư mục gốc của project:

```text
wwm-guide/
├── index.html           ← Trang chủ (Sửa tay khi cần cấu trúc HTML)
├── articles.html        ← Trang danh sách bài (Sửa tay)
├── article.html         ← Trang ruột đọc bài chung (Sửa tay)
├── videos.html          ← Trang xem toàn bộ video (Sửa tay)
├── links.html           ← Trang liên kết mạng xã hội (Sửa tay)
├── danh-sach-video.txt  ← Dán link TikTok vào đây (KHÔNG commit)
├── export-tiktok-videos.csv ← Export excel tải từ TikTok để xử lý tag (KHÔNG commit)
├── .gitignore           ← Chứa cấu hình lờ đi các file tạm, file rác (Sửa tay)
│
├── .github/
│   └── workflows/
│       └── refresh-thumbnails.yml  ← Config tự động thu hình của Bot (Sửa tay)
│
├── scripts/
│   ├── new_post.py             ← Tool hỗ trợ tự động sinh sườn bài (Sinh tự động / Hạn chế sửa)
│   ├── csv_to_videos_json.py   ← Lấy data tiktok CSV import (Hạn chế sửa)
│   └── txt_to_videos_json.py   ← Kéo metadata/ảnh từ txt/database (Hạn chế sửa)
│
├── posts/               ← Nơi cất giữ file bài (.md) của Obsidian (Tự động sinh/Sửa tay ruột bài)
│   ├── phan-tich-doanh-doanh.md
│   └── ...
│
├── data/
│   ├── videos.json      ← Cơ sở dữ liệu tiktok video (Tự động sinh/Hạn chế sửa)
│   ├── articles.json    ← Database thông tin của bài viết (Bắt buộc sửa tay bổ sung Description và related_video_id)
│   └── links.json       ← Liên kết nền tảng mạng xã hội (Sửa tay)
│
└── assets/
    ├── style.css        ← Thư viện giao diện, mã màu dùng chung (Sửa tay)
    ├── main.js          ← Logic API, chuyển trang, hiệu ứng Javascript (Sửa tay)
    ├── thumbnails/      ← Nơi tập kết ảnh bìa video thu thập được (Tự động sinh)
    └── images/          ← Nơi tự do cất ảnh minh họa khi viết bài (Thêm/Sửa bằng tay)
        └── slug-bai-viet-a/ ...
```

---

## Phần 5 — Cấu trúc dữ liệu JSON (tra cứu nhanh)

### data/videos.json
Cơ sở dữ liệu video. File này **được sinh tự động 100% bằng script Python**. Hạn chế chỉnh sửa bằng tay.
- Tên trường | Kiểu | Mô tả | Ví dụ
- `id` | String | ID chuỗi số từ url TikTok | `"7616618393407393045"`
- `title` | String | Tên dọn dẹp + Prefix | `"[Podcast] TIN TỨC NGÀY 13-03-2026"`
- `tags` | Array | Tag phân loại (`Hướng dẫn`, `Nhân vật`, `Tổng hợp`, `Meta`, `Event`) | `["Tổng hợp"]`
- `date` | String | Định dạng `YYYY-MM-DD` | `"2026-03-13"`
- `thumbnail` | String | Link relative đến kho ảnh local | `"assets/thumbnails/7616618393407393045.jpg"`
- `pinned` | Bool | (True) sẽ ưu tiên kẹp video đỉnh | `false`

### data/articles.json
Cơ sở dữ liệu metadata bài viết (hiển thị trang ngoài/tìm bài). Script tự gen đoạn đầu, **bắt buộc người dùng nhập "description" bằng tay**.
- Tên trường | Kiểu | Mô tả | Ví dụ
- `id` | String | Khóa ID tự tăng `art-001` | `"art-001"`
- `title` | String | Tiêu đề lớn hiển thị ngoài | `"Hướng dẫn chạy map"`
- `category` | String | Thể loại dùng lọc. Gồm `Nhân vật|Hướng dẫn|Meta|Podcast` | `"Hướng dẫn"`
- `description` | String | Tóm tắt khoảng 2-3 câu | `"Tài liệu về chạy map nhanh chóng..."`
- `file` | String | Địa chỉ file `.md` chứa text | `"posts/huong-dan-map.md"`
- `icon` | String | Icon hiển thị kế bên thẻ tag category | `"⚔️"`
- `date` | String | Time khởi tạo bài viết | `"2026-03-16"`
- `pinned` | Bool | (True) lên đầu trang index.html | `false`
- `related_video_id` | String | Nhúng Frame ID Tiktok vào cuối trang | `"7570720856855399698"`

### data/links.json
Chứa liên kết ở nút trang links.
- Tên trường | Kiểu | Mô tả | Ví dụ
- `name` | String | Tên mạng xã hội hiển thị | `"TikTok"`
- `url` | String | Link tuyệt đối để điều chuyển | `"https://tiktok.com/@tiu... "`

Lưu ý: Thiếu dấu phẩy `,` cuối mỗi đối tượng ở object cũ sẽ gây lỗi hỏng toàn web. Hãy sử dụng JSON validator nếu không rành.

---

## Phần 6 — Debug các lỗi thường gặp

#### Thumbnail hiển thị ảnh vỡ trên web
**Nguyên nhân:** Có thể web load sai url / CDN hết hạn token, hoặc chưa chạy script update local thumbnail sau khi đổi máy.
**Cách kiểm tra:** Bật F12 Inspect, xem tab Network hoặc Console log báo `404 Not Found` thư mục ảnh.
**Cách sửa:** Chạy thủ công lệnh `python scripts/txt_to_videos_json.py --refresh-thumbnails` ở terminal để ép máy tự bốc lại mọi ảnh hỏng và `git push`.

#### Script Python bị treo khi chạy trên Windows
**Nguyên nhân:** Khung PowerShell mặc định của Win không đáp ứng cấu trúc UTF-8 tiếng Việt, bị tắc luồng encode.
**Cách kiểm tra:** Terminal chớp nháy và đứng im không hiện log `[+] Đã lấy info` hơn 10 giây.
**Cách sửa:** Mở qua phần mềm Powershell phiên bản 7, PowerShell của Windows Terminal mới nhất. Code đã cố rào cứng qua dòng lệnh cấu hình `PYTHONIOENCODING`. Nếu vẫn treo, ấn `Ctrl+C` gõ `chcp 65001` và chạy lại.

#### Web không cập nhật sau khi git push
**Nguyên nhân:** Cloudflare Pages đang build, bị nghẽn do file dung lượng quá lớn (commit đính kèm nhiều ảnh), hoặc bạn chưa `git add` toàn bộ các thay đổi sửa file JSON.
**Cách kiểm tra:** Login Cloudflare vào mục Project Deployments. Nếu status là `Failure`.
**Cách sửa:** Luôn gõ chuẩn kịch bản: `git add -A` → `git commit -m "update"` → `git push`. Nếu lỗi file vượt giới hạn, nén chất lượng nhỏ đi (< 500KB một ảnh bài).

#### Bài viết không hiển thị hoặc hiển thị sai
**Nguyên nhân:** Format `data/articles.json` rớt dấu `${"` hoặc quên dấu phẩy ngăn cách danh sách. File markdown chưa lưu.
**Cách kiểm tra:** Ở file `.json` dùng VS Code thì tên biến sẽ bị vạch đỏ bôi dưới chân.
**Cách sửa:** Check đuôi ngoặc đơn `}` xem có đính kèm `,` không. Đối chiếu format gốc.

#### Video không load được trong modal 
**Nguyên nhân:** Copypaste bị sót chữ hoặc thừa ký tự vào field `related_video_id` hoặc nhầm URL cả cục Tiktok.
**Cách kiểm tra:** Màn hình Frame đen xì hiện logo Tiktok.
**Cách sửa:** Sửa lại chuỗi ID 19 ký tự chuẩn xác vào bài viết và đẩy lại Github.

#### Filter tag không hoạt động
**Nguyên nhân:** Sửa metadata tay viết hoa thường không giống khai báo (ví dụ nhập `huong dan` hoặc `Hướng Dẫn` - chữ D thay vì chữ d).
**Cách sửa:** Sửa lại chính xác tên tag: `Hướng dẫn`, `Nhân vật`, `Tổng hợp`, `Meta`, `Event`.

#### GitHub Actions workflow bị fail
**Nguyên nhân:** Github chặn không cho ghi/commit tự động file Thumbnail.
**Cách kiểm tra:** Nhận email đỏ báo `Workflow run failed`.
**Cách sửa:** Ở trang Github nhấn ô **Settings** → **Actions > General** → Tìm mục *Workflow permissions* bấm chọn quyền `Read and write permissions`. Tick **Save**.

#### Lỗi encoding tiếng Việt khi chạy script 
**Nguyên nhân:** Khác chuẩn `UTF-8`.
**Cách kiểm tra:** In ra toàn biến mã hỏi chấm kiểu ``.
**Cách sửa:** Tại thư mục text txt, chọn Save As format Encoding chuyển về `UTF-8`. Script Auto Gen tự lo liệu điều này trong hàm lưu rồi.

---

## Phần 7 — Thông tin hệ thống (tra cứu nhanh)

| Thành phần | Địa chỉ/Thông tin |
|---|---|
| Web | **[URL_WEB]** (Hãy thay mốc này bằng link Cloudflare thực) |
| GitHub Repo | [https://github.com/TieuHongTuyen/wwm-web](https://github.com/TieuHongTuyen/wwm-web) |
| TikTok | [@tiu.hng.tuyn](https://tiktok.com/@tiu.hng.tuyn) |
| CF Dashboard| [dash.cloudflare.com](https://dash.cloudflare.com/) |
| Git Actions | [https://github.com/TieuHongTuyen/wwm-web/actions](https://github.com/TieuHongTuyen/wwm-web/actions) |
