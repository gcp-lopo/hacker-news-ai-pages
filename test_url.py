import requests
from bs4 import BeautifulSoup, Tag
import re

def test_website():
    """测试网站结构"""
    url = "https://www.kanshudashi.com/book/hbwlll.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("正在访问网站...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print("网站标题:", soup.title.text if soup.title else "无标题")
        
        # 查找所有链接
        all_links = soup.find_all('a', href=True)
        print(f"总共找到 {len(all_links)} 个链接")
        
        # 查找可能的章节链接
        chapter_links = []
        for link in all_links:
            if isinstance(link, Tag):
                href = link.get('href')
                text = link.text.strip()
                if href and text and ('第' in text or 'chapter' in str(href).lower()):
                    chapter_links.append({
                        'text': text,
                        'href': href
                    })
                    print(f"章节链接: {text} -> {href}")
        
        print(f"\n找到 {len(chapter_links)} 个章节链接")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_website() 