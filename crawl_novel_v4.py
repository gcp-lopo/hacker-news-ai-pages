import requests
from bs4 import BeautifulSoup, Tag
import time
import re
import os
import json
from typing import Optional

class NovelCrawlerV4:
    def __init__(self):
        self.base_url = "https://www.kanshudashi.com"
        self.novel_url = "https://www.kanshudashi.com/book/hbwlll.html"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.progress_file = "crawl_progress_v4.json"
        
    def load_progress(self):
        """加载爬取进度"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"completed_chapters": [], "failed_chapters": []}
        return {"completed_chapters": [], "failed_chapters": []}
    
    def save_progress(self, progress):
        """保存爬取进度"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
    
    def test_chapter_url(self, chapter_num):
        """测试章节URL是否存在"""
        url = f"https://www.kanshudashi.com/book/hbwlll-{chapter_num}.html"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # 检查是否包含章节内容
                content = soup.get_text()
                if len(content) > 1000 and ('这是我' in content or '师父' in content or '施主' in content):
                    return True
            return False
        except:
            return False
    
    def get_chapter_title(self, chapter_num):
        """获取章节标题"""
        url = f"https://www.kanshudashi.com/book/hbwlll-{chapter_num}.html"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('h1') or soup.find('h2') or soup.find('div', class_='chapter-title')
                if title:
                    return title.text.strip()
                else:
                    return f"第{chapter_num}章"
            return f"第{chapter_num}章"
        except:
            return f"第{chapter_num}章"
    
    def get_all_chapter_links(self):
        """获取所有章节链接（包括测试缺失的章节）"""
        all_chapters = []
        
        try:
            # 方法1：从首页获取已知章节
            print(f"从首页获取章节: {self.novel_url}")
            response = self.session.get(self.novel_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            chapters = self.extract_chapters_from_page(soup)
            if chapters:
                all_chapters.extend(chapters)
                print(f"从首页获取到 {len(chapters)} 个章节")
            
            # 方法2：测试所有可能的章节URL（1-909）
            print("测试所有可能的章节URL（1-909）...")
            existing_chapters = []
            
            # 先测试一些关键章节
            test_ranges = [
                (1, 100),      # 前100章
                (101, 200),    # 101-200章
                (201, 300),    # 201-300章
                (301, 400),    # 301-400章
                (401, 500),    # 401-500章
                (501, 600),    # 501-600章
                (601, 700),    # 601-700章
                (701, 800),    # 701-800章
                (801, 889),    # 801-889章
                (890, 909),    # 篇外章节
            ]
            
            for start, end in test_ranges:
                print(f"测试章节 {start}-{end}...")
                for i in range(start, end + 1):
                    if self.test_chapter_url(i):
                        title = self.get_chapter_title(i)
                        existing_chapters.append({
                            'title': title,
                            'url': f"https://www.kanshudashi.com/book/hbwlll-{i}.html"
                        })
                        print(f"找到章节 {i}: {title}")
                    time.sleep(0.5)  # 避免请求过快
            
            all_chapters.extend(existing_chapters)
            
            # 去重并排序
            unique_chapters = []
            seen_urls = set()
            for chapter in all_chapters:
                if chapter['url'] not in seen_urls:
                    unique_chapters.append(chapter)
                    seen_urls.add(chapter['url'])
            
            # 按章节号排序
            def get_chapter_number(chapter):
                match = re.search(r'hbwlll-(\d+)', chapter['url'])
                return int(match.group(1)) if match else 0
            
            unique_chapters.sort(key=get_chapter_number)
            
            print(f"总共找到 {len(unique_chapters)} 个唯一章节")
            return unique_chapters
            
        except Exception as e:
            print(f"获取章节列表失败: {e}")
            return []
    
    def extract_chapters_from_page(self, soup):
        """从页面中提取章节链接"""
        chapters = []
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            if isinstance(link, Tag):
                href = link.get('href')
                text = link.text.strip()
                # 匹配章节链接格式 /book/hbwlll-数字.html
                if href and text and re.match(r'/book/hbwlll-\d+\.html', str(href)):
                    chapters.append({
                        'title': text,
                        'url': self.base_url + str(href)
                    })
        
        return chapters
    
    def get_chapter_content(self, chapter_url):
        """获取章节内容"""
        try:
            response = self.session.get(chapter_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 查找章节标题
            title = soup.find('h1') or soup.find('h2') or soup.find('div', class_='chapter-title')
            title_text = title.text.strip() if title else "未知章节"
            
            # 查找章节内容 - 根据网站结构查找
            content_div = None
            
            # 尝试多种可能的内容容器
            selectors = [
                'div.content',
                'div#content',
                'div.chapter-content',
                'div.article-content',
                'div.read-content',
                'div.novel-content'
            ]
            
            for selector in selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    break
            
            # 如果还是没找到，尝试查找包含大量文本的div
            if not content_div:
                divs = soup.find_all('div')
                for div in divs:
                    if isinstance(div, Tag):
                        text = div.get_text()
                        # 如果div包含大量文本且包含章节内容特征
                        if len(text) > 500 and ('这是我' in text or '师父' in text or '施主' in text):
                            content_div = div
                            break
            
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
    
    def crawl_novel(self, max_chapters=None, resume=True):
        """爬取整本小说"""
        print("开始爬取《天眼风水师》完整版...")
        print(f"目标网站: {self.novel_url}")
        
        # 加载进度
        progress = self.load_progress() if resume else {"completed_chapters": [], "failed_chapters": []}
        completed_urls = set(progress["completed_chapters"])
        
        # 获取所有章节列表
        chapters = self.get_all_chapter_links()
        if not chapters:
            print("未找到章节列表")
            return None
        
        # 过滤已完成的章节
        if resume:
            chapters = [ch for ch in chapters if ch['url'] not in completed_urls]
            print(f"跳过已完成的 {len(completed_urls)} 章，剩余 {len(chapters)} 章待爬取")
        
        # 限制章节数量（如果指定了max_chapters）
        if max_chapters and len(chapters) > max_chapters:
            chapters = chapters[:max_chapters]
        
        print(f"准备爬取 {len(chapters)} 个章节")
        
        # 创建小说内容
        novel_content = []
        novel_content.append("《天眼风水师》")
        novel_content.append("作者：道之光")
        novel_content.append("主角：王三合")
        novel_content.append("别名：《改命记实录》")
        novel_content.append("类别：都市小说")
        novel_content.append("状态：连载")
        novel_content.append("字数：318.61万字")
        novel_content.append("更新至：第909章 【篇外：师父的师父】")
        novel_content.append("=" * 50)
        novel_content.append("")
        novel_content.append("【可实操的风水小说】【涉及风水，道医，心理学，经济学，看头像，看手机号码】")
        novel_content.append("【干货知识】【用科学解释玄学】【借助风水常识，为自己开运转运】")
        novel_content.append("师父匆匆教了我预测术，传给我几本书，还没来得及正式上山，就让我下山渡世……这儿上哪儿说理去？")
        novel_content.append("我在红尘中，渡世修行。")
        novel_content.append("")
        
        # 爬取每个章节
        for i, chapter in enumerate(chapters, 1):
            print(f"正在爬取第 {i}/{len(chapters)} 章: {chapter['title']}")
            
            title, content = self.get_chapter_content(chapter['url'])
            
            if "获取失败" not in title and "内容获取失败" not in content:
                novel_content.append(f"\n{title}")
                novel_content.append("-" * 30)
                novel_content.append(content)
                novel_content.append("\n" + "=" * 50 + "\n")
                
                # 更新进度
                progress["completed_chapters"].append(chapter['url'])
                self.save_progress(progress)
            else:
                print(f"章节 {chapter['title']} 爬取失败")
                progress["failed_chapters"].append({
                    "title": chapter['title'],
                    "url": chapter['url'],
                    "error": content
                })
                self.save_progress(progress)
            
            # 添加延迟避免被封
            time.sleep(1)
        
        # 保存为txt文件
        filename = "天眼风水师_完整版_v4.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(novel_content))
        
        print(f"\n爬取完成！小说已保存为: {filename}")
        print(f"成功爬取: {len(progress['completed_chapters'])} 章")
        print(f"失败章节: {len(progress['failed_chapters'])} 章")
        return filename

def main():
    crawler = NovelCrawlerV4()
    # 爬取所有章节
    crawler.crawl_novel(max_chapters=None, resume=True)

if __name__ == "__main__":
    main() 