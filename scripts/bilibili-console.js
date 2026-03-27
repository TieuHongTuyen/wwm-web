// Dán toàn bộ mã này vào Console (nhấn F12 chuyển qua tab Console) trên trang web Bilibili và Enter.
(() => {
    let blocks = [];
    let seenImg = new Set();

    console.log("Đang tiến hành quét phân tích nội dung trang...");

    // Tìm vùng chứa bài viết chính của trang (Hỗ trợ 3 loại Bilibili khác nhau)
    let container = document.querySelector('.opus-read, .opus-module-content, .article-holder, .dyn-card, .bili-rich-text__content');
    
    if (container) {
        // Quét tất cả ảnh và thẻ văn bản theo đúng cấu trúc DOM thật để không bị mất chữ khi có thẻ in đậm (b), tiêu đề (h1-h6), hay canh giữa (center)
        let walker = document.createTreeWalker(
            container,
            NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    if (node.nodeType === 1 && ['SCRIPT', 'STYLE', 'SVG', 'NOSCRIPT'].includes(node.tagName)) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            },
            false
        );

        let currentTextBundle = "";
        let node;
        let blockTags = ['P', 'DIV', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI', 'BR', 'CENTER', 'SECTION', 'FIGURE', 'FIGCAPTION'];
        
        while ((node = walker.nextNode())) {
            if (node.nodeType === 3) { // Text node
                let text = node.nodeValue.replace(/[\r\n\t]+/g, ' '); 
                if (text.trim().length > 0 && !text.includes('未经作者授权')) {
                    if (currentTextBundle.endsWith('\n')) {
                        currentTextBundle += text.trimStart();
                    } else {
                        currentTextBundle += text;
                    }
                }
            } else if (node.nodeType === 1) { // Element node
                if (node.tagName === 'IMG') {
                    if (currentTextBundle.trim().length > 0) {
                        blocks.push({ type: 'text', text: currentTextBundle.trim() });
                    }
                    currentTextBundle = ""; 
                    
                    let src = node.getAttribute('data-src') || node.src;
                    if (src && src.includes('hdslb.com')) {
                        if ((node.width > 50 && node.height > 50) || node.width === 0 || node.className.includes('opus') || node.className.includes('article') || node.className.includes('bili')) {
                            if (src.startsWith('//')) src = 'https:' + src;
                            if (src.includes('@')) src = src.split('@')[0];
                            if (!seenImg.has(src)) {
                                seenImg.add(src);
                                blocks.push({ type: 'image', src: src });
                            }
                        }
                    }
                } else if (blockTags.includes(node.tagName)) {
                    if (currentTextBundle.trim().length > 0 && !currentTextBundle.endsWith('\n\n')) {
                        currentTextBundle = currentTextBundle.trimEnd() + '\n\n';
                    }
                }
            }
        }

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
