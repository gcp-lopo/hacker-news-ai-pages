import requests
from bs4 import BeautifulSoup, Tag
import time
import re
import os
from typing import Optional

class NovelCrawler:
    def __init__(self):
        self.base_url = "https://www.erciyan.com"
        self.novel_url = "https://www.erciyan.com/book/94848328/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_chapter_links(self):
        """获取所有章节链接"""
        try:
            response = self.session.get(self.novel_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找章节链接
            chapter_links = []
            
            # 查找最新章节列表
            latest_chapters = soup.find_all('a', href=re.compile(r'/book/\d+/\d+\.html'))
            for link in latest_chapters:
                if isinstance(link, Tag):
                    href = link.get('href')
                    if link.text.strip() and href:
                        chapter_links.append({
                            'title': link.text.strip(),
                            'url': self.base_url + str(href)
                        })
            
            # 查找正文章节列表
            content_chapters = soup.find_all('a', href=re.compile(r'/book/\d+/\d+\.html'))
            for link in content_chapters:
                if isinstance(link, Tag):
                    href = link.get('href')
                    if link.text.strip() and href and link.text.strip() not in [ch['title'] for ch in chapter_links]:
                        chapter_links.append({
                            'title': link.text.strip(),
                            'url': self.base_url + str(href)
                        })
            
            return chapter_links
            
        except Exception as e:
            print(f"获取章节列表失败: {e}")
            return []
    
    def get_chapter_content(self, chapter_url):
        """获取章节内容"""
        try:
            response = self.session.get(chapter_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找章节标题
            title = soup.find('h1')
            title_text = title.text.strip() if title else "未知章节"
            
            # 查找章节内容
            content_div = soup.find('div', class_='content')
            if not content_div:
                content_div = soup.find('div', id='content')
            if not content_div:
                content_div = soup.find('div', class_='chapter-content')
            
            if content_div:
                # 清理内容
                content = content_div.get_text()
                # 移除多余的空白字符
                content = re.sub(r'\s+', '\n', content).strip()
                return title_text, content
            else:
                return title_text, "内容获取失败"
                
        except Exception as e:
            print(f"获取章节内容失败: {e}")
            return "获取失败", f"错误: {e}"
    
    def crawl_novel(self):
        """爬取整本小说"""
        print("开始爬取《天眼风水师》...")
        
        # 获取章节列表
        chapters = self.get_chapter_links()
        if not chapters:
            print("未找到章节列表，尝试直接访问...")
            # 如果无法获取章节列表，尝试直接访问已知章节
            chapters = [
                {'title': '第1章 风水比医学更科学（道）', 'url': 'https://www.erciyan.com/book/94848328/1.html'},
                {'title': '第2章 最惨高考', 'url': 'https://www.erciyan.com/book/94848328/2.html'},
                {'title': '第3章 南上,应验', 'url': 'https://www.erciyan.com/book/94848328/3.html'},
                # 可以继续添加更多章节
            ]
        
        print(f"找到 {len(chapters)} 个章节")
        
        # 创建小说内容
        novel_content = []
        novel_content.append("《天眼风水师》")
        novel_content.append("作者：道之光")
        novel_content.append("类别：灵异")
        novel_content.append("状态：连载")
        novel_content.append("字数：9万")
        novel_content.append("=" * 50)
        novel_content.append("")
        
        # 爬取每个章节
        for i, chapter in enumerate(chapters, 1):
            print(f"正在爬取第 {i}/{len(chapters)} 章: {chapter['title']}")
            
            title, content = self.get_chapter_content(chapter['url'])
            
            novel_content.append(f"\n{title}")
            novel_content.append("-" * 30)
            novel_content.append(content)
            novel_content.append("\n" + "=" * 50 + "\n")
            
            # 添加延迟避免被封
            time.sleep(1)
        
        # 保存为txt文件
        filename = "天眼风水师.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(novel_content))
        
        print(f"\n爬取完成！小说已保存为: {filename}")
        return filename

def main():
    crawler = NovelCrawler()
    crawler.crawl_novel()

if __name__ == "__main__":
    main() 