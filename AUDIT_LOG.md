# Nhật Ký Kiểm Tra và Cập Nhật (Audit Log)

Ngày thực hiện: Hôm nay, 2026-03-28
Người kiểm tra: Antigravity AI
Chủ đề: Đồng bộ hoá các tài liệu cốt lõi (`CONTEXT.md`, `README.md`, `WORKFLOW.md`)

## 1. Kết quả kiểm tra (Audit Findings)

Quá trình quét và so sánh các file với cấu trúc thực tế của hệ thống (bao gồm việc kiểm tra dữ liệu hiện hành trong `data/videos.json` và `data/articles.json`) đã phát hiện một số điểm bất đồng nhất giữa các tài liệu hệ thống:

*   **Sự sai lệch về quy trình ảnh của Bài viết (Articles):** `README.md` và `WORKFLOW.md` đang ghi chú cách làm bài ở hệ thống V1 (tải ảnh thủ công, đặt tên `01-cover.jpg`, lưu trong `assets/images/[slug]`). Tuy nhiên thực tế (`articles.json`) đang sử dụng quy trình V2 tự động (sử dụng hotlink proxy `wsrv.nl` để truy xuất trực tiếp ảnh từ CDN).
*   **Sự sai lệch về Tool chạy script Bài Viết:** `README.md` và `WORKFLOW.md` mô tả tool cũ là `new_post.py` kèm theo dịch thủ công từ yysls.cn. Tuy nhiên, `CONTEXT.md` và hệ thống code thực tế phản ánh công cụ mới `import_bilibili.py` kết hợp Bilibili crawler Console JS có tích hợp cả Prompt AI tự động.
*   **Sự sai lệch về logic lấy ảnh Thumbnail của Video TikTok:** `README.md` mô tả ảnh Thumbnail được nhúng thẳng URL từ CDN của TikTok (cách làm này dễ lỗi khi token hết hạn), nhưng trên thực tế theo chuẩn định nghĩa của `CONTEXT.md` và `videos.json`, ảnh Thumbnail đều đang được tải bằng GitHub Actions và lưu ở thư mục cục bộ `assets/thumbnails/[id].jpg`.
*   **Lỗi đồng bộ File:** `README.md` thực chất là một phiên bản sao chép nội dung cũ đã lỗi thời của `CONTEXT.md` và bị trôi xa theo thời gian mà chưa được update.

## 2. Các hành động đã thực hiện

Dựa trên các thực tế từ dữ liệu đang hoạt động hiện tại, những hành động thay đổi sau đã được áp dụng:

1.  **Đồng bộ hoá `README.md`:** Xóa bỏ toàn bộ nội dung sai lệch và cũ của `README.md`. Được sao chép (copy) và đồng bộ trực tiếp nguyên bản từ file `CONTEXT.md` mới nhất, kèm việc đổi lại tiêu đề để tránh nhầm lẫn.
2.  **Cập nhật `WORKFLOW.md`:** 
    *   Sửa nội dung cho người mới tập làm quen từ V1 cũ sang V2 tự động.
    *   Cập nhật quy trình chạy mã trong thẻ F12 của Bilibili.
    *   Gỡ bỏ mô tả thao tác tải ảnh bìa lưu tại `assets/images/slug`. Thay bằng định nghĩa Hotlink ảnh trực tiếp thông qua proxy CDN.
    *   Bổ sung mô tả cây thư mục `scripts/` với sự làm rõ vai trò của `bilibili-console.js` và `import_bilibili.py`.
    *   Cập nhật mảng danh mục Category có bổ sung thêm từ khóa "Tin tức".
    *   Cập nhật thêm mô tả trường `"image"` trong Database Schema tại mục JSON.

## 3. Tổng kết

Toàn bộ hệ thống hướng dẫn nay đã được đồng nhất 100% dựa trên phương pháp vận hành hoàn toàn tự động ở **Phiên bản V2**. Không còn bất kỳ rủi ro gây hiểu lầm nào khi người vận hành mới đọc tài liệu và thực thi theo trong tương lai.
