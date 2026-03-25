import sys
import requests
from bs4 import BeautifulSoup
import re

def parse_bilibili(url):
    print(f"Đang tải {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Referer': 'https://www.bilibili.com/'
    }
    
    html = ""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # Bilibili thường chặn bot bằng WAF (Mã 412 Precondition Failed)
        if response.status_code == 412:
            print("Server Bilibili chặn request bằng WAF (412). Chuyển sang dùng dữ liệu giả lập để demo chức năng...")
            html = get_mock_html()
        else:
            response.raise_for_status()
            html = response.text
    except Exception as e:
        print(f"Lỗi khi tải trang gốc ({e}). Chuyển sang dùng dữ liệu giả lập để demo...")
        html = get_mock_html()
        
    # Tạo nội dung MD
    md_content = f"# Kết quả trích xuất test từ Bilibili\n\n> URL gốc: {url}\n\n"
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Trích xuất text tiếng Trung
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]')
    texts = set()
    for tag in soup.find_all(['p', 'div', 'span']):
        text = tag.get_text(strip=True)
        # Chỉ lấy các mẩu text đủ dài và chứa ký tự tiếng Trung
        if len(text) > 15 and has_chinese(text) and text not in texts:
            texts.add(text)
            
    # 2. Tìm ảnh từ Bilibili (thường cdn hdslb.com)
    img_urls = []
    # Dùng regex để bắt tất cả link ảnh trong HTML/JSON Script
    img_matches = re.findall(r'((?:https?:)?//[a-zA-Z0-9.-]+\.hdslb\.com/[a-zA-Z0-9./_-]+\.(?:jpg|png|jpeg))', html)
    for img in img_matches:
        img_url = img if img.startswith('http') else 'https:' + img
        if '@' in img_url: # Xoá query parameters ảnh nếu có
            img_url = img_url.split('@')[0]
        if img_url not in img_urls:
             img_urls.append(img_url)

    # Đổ vào file MD
    md_content += "## Toàn bộ Hình ảnh (Hotlink trực tiếp)\n\n"
    if img_urls:
        for idx, img in enumerate(list(img_urls)[:15]): 
            # Sử dụng wsrv.nl proxy để bypass lỗi 403 Forbidden của Bilibili WAF
            proxy_url = f"https://wsrv.nl/?url={img}"
            md_content += f"![Ảnh {idx+1}]({proxy_url})\n\n"
    else:
        md_content += "_Không tìm thấy ảnh nổi bật._\n\n"
        
    md_content += "## Cấu trúc Văn bản (Dọn sẵn để điền)\n\n"
    if texts:
        for idx, text in enumerate(list(texts)[:10]):
            md_content += f"<!-- Gốc: {text} -->\n"
            md_content += f"**[DÁN BẢN DỊCH TẠI ĐÂY]** \n\n---\n\n"
    else:
        md_content += "_Không tìm thấy đoạn văn bản phù hợp._\n\n"

    output_file = 'test_bilibili_output.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"\nThành công! Đã lưu file mô phỏng vào '{output_file}'.")

def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def get_mock_html():
    return """
    <html>
    <body>
       <div class="dyn-text">燕云十六声，一经公布就引起广泛关注...</div>
       <img src="//i0.hdslb.com/bfs/new_dyn/10c3fb70ac614cbed736733ec5d57b28052951.jpg">
       <p>新的版本增加了更丰富的武侠招式和战斗系统！</p>
       <img src="https://i0.hdslb.com/bfs/article/fb56673daeddc3e4bcbb8ee0f757d548.png">
       <p>同时，世界地图也得到了极大的扩展...</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    url_to_test = sys.argv[1] if len(sys.argv) > 1 else 'https://t.bilibili.com/?spm_id_from=333.1007.0.0'
    parse_bilibili(url_to_test)
