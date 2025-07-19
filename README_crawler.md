# 小说爬虫入门教程（以 crawl_novel_v4.py 为例）

## 1. 什么是爬虫？

爬虫（Web Crawler）是一种自动化程序，用于模拟人工浏览网页、批量抓取网页上的数据。小说爬虫就是自动化下载小说网站上的章节内容，整理成本地文件。

---

## 2. 环境准备

- **Python 版本**：推荐 3.7 及以上
- **依赖库**：
  - requests（网络请求）
  - beautifulsoup4（网页解析）
  - lxml（加速解析，可选）
  - re（正则表达式，内置）
  - time、os、json（内置）

安装依赖：
```bash
pip install requests beautifulsoup4 lxml
```

---

## 3. 网站分析

1. **目标网站**：以 `https://www.kanshudashi.com` 为例。
2. **分析章节列表页**：找到所有章节的链接（通常在目录页）。
3. **分析章节内容页**：确定正文内容和标题的 HTML 标签。

> 小技巧：按 F12 打开浏览器开发者工具，查看网页结构。

---

## 4. 代码结构与核心流程

### 4.1 类的设计

- `NovelCrawlerV4` 类：负责所有爬虫逻辑。
- 主要方法：
  - `get_all_chapter_links()`：获取所有章节链接
  - `get_chapter_content(url)`：获取单章内容
  - `crawl_novel()`：主流程，循环爬取所有章节
  - `load_progress()`/`save_progress()`：断点续爬

### 4.2 主要流程

```python
crawler = NovelCrawlerV4()
crawler.crawl_novel()
```

1. **获取章节列表**
   - 访问小说目录页，解析所有章节的链接和标题。
2. **循环爬取每一章**
   - 依次访问每个章节链接，提取标题和正文。
   - 保存到本地 txt 文件。
   - 每爬完一章，记录进度，支持断点续爬。
3. **异常处理**
   - 网络超时、内容缺失等会自动跳过并记录。

---

## 5. 关键代码讲解

### 5.1 获取章节链接
```python
response = requests.get(novel_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a', href=re.compile(r'/book/hbwlll-\\d+\\.html'))
```
- 用正则匹配所有章节的链接。

### 5.2 获取章节内容
```python
response = requests.get(chapter_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
content_div = soup.select_one('div.content')
content = content_div.get_text().strip()
```
- 选择合适的标签提取正文。

### 5.3 断点续爬
- 每爬完一章，保存已完成的章节到 json 文件。
- 下次运行时自动跳过已完成部分。

---

## 6. 反爬虫机制与应对

- **User-Agent**：模拟浏览器访问。
- **延迟请求**：`time.sleep(1)`，防止访问过快被封。
- **异常处理**：捕获网络错误，自动重试或跳过。

---

## 7. 常见报错与排查

- **网络超时**：检查网络，适当加大超时时间。
- **内容提取不到**：检查网页结构是否变化，调整选择器。
- **编码问题**：统一用 `utf-8` 读写文件。

---

## 8. 小白写爬虫的建议

1. 先用浏览器分析目标网页结构。
2. 用 requests+BeautifulSoup 先抓一页，调试提取内容。
3. 再批量抓取，注意加延迟。
4. 处理异常，保证脚本健壮。
5. 尊重网站 robots 协议和版权。

---

## 9. 参考资料
- [requests 官方文档](https://docs.python-requests.org/zh_CN/latest/)
- [BeautifulSoup4 文档](https://beautifulsoup.readthedocs.io/zh_CN/latest/)
- [Python 正则表达式](https://docs.python.org/zh-cn/3/library/re.html)

---

如有疑问，欢迎提问！ 

---

## 10. crawl_novel_v4.py 代码逐行讲解

下面以主要结构和关键函数为例，逐行详细注释说明：

### 10.1 导入依赖
```python
import requests  # 用于发送网络请求
from bs4 import BeautifulSoup, Tag  # 网页解析库
import time  # 控制请求间隔，防止被封
import re  # 正则表达式，提取链接和内容
import os  # 文件和路径操作
import json  # 进度保存为json
from typing import Optional  # 类型提示
```

### 10.2 爬虫类初始化
```python
class NovelCrawlerV4:
    def __init__(self):
        self.base_url = "https://www.kanshudashi.com"  # 网站主域名
        self.novel_url = "https://www.kanshudashi.com/book/hbwlll.html"  # 小说目录页
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }  # 伪装成浏览器，防止被封
        self.session = requests.Session()  # 会话对象，自动管理cookie
        self.session.headers.update(self.headers)  # 设置请求头
        self.progress_file = "crawl_progress_v4.json"  # 进度保存文件
```

### 10.3 进度加载与保存
```python
    def load_progress(self):
        """加载爬取进度"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)  # 读取已完成章节
            except:
                return {"completed_chapters": [], "failed_chapters": []}
        return {"completed_chapters": [], "failed_chapters": []}

    def save_progress(self, progress):
        """保存爬取进度"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)  # 保存为json
```

### 10.4 检查章节URL是否存在
```python
    def test_chapter_url(self, chapter_num):
        url = f"https://www.kanshudashi.com/book/hbwlll-{chapter_num}.html"  # 拼接章节链接
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                content = soup.get_text()
                # 判断页面内容是否像小说正文
                if len(content) > 1000 and ('这是我' in content or '师父' in content or '施主' in content):
                    return True
            return False
        except:
            return False
```

### 10.5 获取章节标题
```python
    def get_chapter_title(self, chapter_num):
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
```

### 10.6 获取所有章节链接
```python
    def get_all_chapter_links(self):
        all_chapters = []  # 存储所有章节
        try:
            # 方式1：从目录页提取
            response = self.session.get(self.novel_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            chapters = self.extract_chapters_from_page(soup)
            if chapters:
                all_chapters.extend(chapters)
            # 方式2：遍历所有可能的章节号，测试是否存在
            test_ranges = [ (1, 100), (101, 200), ... ]  # 章节号分段
            for start, end in test_ranges:
                for i in range(start, end + 1):
                    if self.test_chapter_url(i):
                        title = self.get_chapter_title(i)
                        all_chapters.append({'title': title, 'url': f"https://www.kanshudashi.com/book/hbwlll-{i}.html"})
                    time.sleep(0.5)  # 防止请求过快
            # 去重、排序
            ...
            return unique_chapters
        except Exception as e:
            print(f"获取章节列表失败: {e}")
            return []
```

### 10.7 提取章节链接（辅助函数）
```python
    def extract_chapters_from_page(self, soup):
        chapters = []
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            if isinstance(link, Tag):
                href = link.get('href')
                text = link.text.strip()
                if href and text and re.match(r'/book/hbwlll-\d+\.html', str(href)):
                    chapters.append({'title': text, 'url': self.base_url + str(href)})
        return chapters
```

### 10.8 获取章节内容
```python
    def get_chapter_content(self, chapter_url):
        try:
            response = self.session.get(chapter_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1') or soup.find('h2') or soup.find('div', class_='chapter-title')
            title_text = title.text.strip() if title else "未知章节"
            # 多种选择器尝试正文div
            selectors = [ 'div.content', 'div#content', ... ]
            for selector in selectors:
                content_div = soup.select_one(selector)
                if content_div:
                    break
            if not content_div:
                # 兜底：找包含大量文本的div
                ...
            if content_div:
                content = content_div.get_text()
                content = re.sub(r'\s+', '\n', content).strip()
                return title_text, content
            else:
                return title_text, "内容获取失败"
        except Exception as e:
            print(f"获取章节内容失败: {e}")
            return "获取失败", f"错误: {e}"
```

### 10.9 主流程：爬取整本小说
```python
    def crawl_novel(self, max_chapters=None, resume=True):
        print("开始爬取《天眼风水师》完整版...")
        progress = self.load_progress() if resume else {"completed_chapters": [], "failed_chapters": []}
        completed_urls = set(progress["completed_chapters"])
        chapters = self.get_all_chapter_links()
        if not chapters:
            print("未找到章节列表")
            return None
        if resume:
            chapters = [ch for ch in chapters if ch['url'] not in completed_urls]
        if max_chapters and len(chapters) > max_chapters:
            chapters = chapters[:max_chapters]
        novel_content = ["《天眼风水师》", ...]  # 小说元信息
        for i, chapter in enumerate(chapters, 1):
            print(f"正在爬取第 {i}/{len(chapters)} 章: {chapter['title']}")
            title, content = self.get_chapter_content(chapter['url'])
            if "获取失败" not in title and "内容获取失败" not in content:
                novel_content.append(f"\n{title}")
                novel_content.append("-" * 30)
                novel_content.append(content)
                novel_content.append("\n" + "=" * 50 + "\n")
                progress["completed_chapters"].append(chapter['url'])
                self.save_progress(progress)
            else:
                print(f"章节 {chapter['title']} 爬取失败")
                progress["failed_chapters"].append({"title": chapter['title'], "url": chapter['url'], "error": content})
                self.save_progress(progress)
            time.sleep(1)
        filename = "天眼风水师_完整版_v4.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(novel_content))
        print(f"\n爬取完成！小说已保存为: {filename}")
        print(f"成功爬取: {len(progress['completed_chapters'])} 章")
        print(f"失败章节: {len(progress['failed_chapters'])} 章")
        return filename
```

### 10.10 程序入口
```python
def main():
    crawler = NovelCrawlerV4()
    crawler.crawl_novel(max_chapters=None, resume=True)

if __name__ == "__main__":
    main()
```

---

> 以上为 crawl_novel_v4.py 的主要结构和关键函数逐行讲解。建议新手结合实际代码和注释多调试、多尝试，遇到问题多查文档和报错信息。 