// Dán toàn bộ mã này vào Console (nhấn F12 chuyển qua tab Console) trên trang web Bilibili và Enter.
(() => {
    let blocks = [];
    let seenImg = new Set();

    console.log("Đang tiến hành quét phân tích nội dung trang...");

    // Tìm vùng chứa bài viết chính của trang (Hỗ trợ 3 loại Bilibili khác nhau)
    let container = document.querySelector('.opus-read, .opus-module-content, .article-holder, .dyn-card, .bili-rich-text__content');
    
    if (container) {
        // Quét tất cả ảnh và thẻ văn bản theo đúng thứ tự xuất hiện từ trên xuống dưới
        let elements = container.querySelectorAll('img, p, span, div.text');
        
        let currentTextBundle = ""; // Dùng để gom tất cả các dòng text lại thành 1 cục lớn cho đến khi gặp ảnh
        
        elements.forEach(el => {
            if (el.tagName === 'IMG') {
                // Khi gặp một bức ảnh, ta xử lý chuỗi chữ (Bundle) đã tích tụ từ trước đó
                if (currentTextBundle.trim().length > 0) {
                    blocks.push({ type: 'text', text: currentTextBundle.trim() });
                    currentTextBundle = ""; // Reset cục chữ về rỗng
                }
                
                // Lấy link ảnh
                let src = el.getAttribute('data-src') || el.src;
                if (src && src.includes('hdslb.com')) {
                    // Tránh các sticker bé
                    if ((el.width > 50 && el.height > 50) || el.width === 0 || el.className.includes('opus') || el.className.includes('article') || el.className.includes('bili')) {
                        if (src.startsWith('//')) src = 'https:' + src;
                        if (src.includes('@')) src = src.split('@')[0];
                        
                        if (!seenImg.has(src)) {
                            seenImg.add(src);
                            blocks.push({ type: 'image', src: src });
                        }
                    }
                }
            } else {
                // Xử lý Thẻ Văn Bản (P, DIV, SPAN)
                // Phải chắc chắn nó là thẻ chỉ chứa chữ, ko chứa các khối block bự khác lồng vào nhau, để chống lặp chữ
                if (el.children.length === 0 || (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3)) {
                    let text = (el.innerText || el.textContent || "").trim();
                    // Loại bỏ văn bản rác hoặc quá ngắn
                    if (text.length > 3 && !text.includes('未经作者授权')) {
                        // Nối văn bản này vào cục Bundle lớn (Xuống dòng 2 lần cho dễ đọc)
                        currentTextBundle += text + "\n\n";
                    }
                }
            }
        });

        // Xử lý nốt phần chữ còn thừa ở cuối cùng (nếu bài viết kết thúc bằng chữ thay vì ảnh)
        if (currentTextBundle.trim().length > 0) {
            blocks.push({ type: 'text', text: currentTextBundle.trim() });
        }
    } else {
        console.error("Không tìm thấy vùng nội dung bài viết. Có thể đây là trang chủ hoặc giao diện chưa từng ghi nhận!");
        return;
    }

    let result = {
        url: window.location.href,
        blocks: blocks
    };
    
    let jsonStr = JSON.stringify(result, null, 2);
    
    // Hack tạo element ẩn để copy text tự động vào Clipboard
    const copyEl = document.createElement('textarea');
    copyEl.value = jsonStr;
    document.body.appendChild(copyEl);
    copyEl.select();
    document.execCommand('copy');
    document.body.removeChild(copyEl);
    
    console.log("%c✅ ĐÃ COPY DỮ LIỆU CẤU TRÚC CHUẨN VÀO CHUỘT (CLIPBOARD)!", "color: lightgreen; font-size: 16px; font-weight: bold;");
    console.log(`Đã gom được: ${seenImg.size} Ảnh và cấu trúc văn bản theo đúng thứ tự gốc.`);
    console.log("👉 Về VS Code > Mở 'bilibili-data.json' > Nhấn Ctrl+V để dán đè dữ liệu mới > Save lại > Chạy Python script.");
})();
