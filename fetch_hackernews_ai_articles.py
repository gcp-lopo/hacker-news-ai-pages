import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import yaml
import re

BASE_URL = "https://thehackernews.com/"
KEYWORDS = ["ai", "artificial intelligence", "startup", "创业", "founder", "machine learning", "generative ai"]
HEADERS = {"User-Agent": "Mozilla/5.0"}

# 脚本启动时强制写入一行，确认有写入权限
with open("debug_output.txt", "w", encoding="utf-8") as debugf:
    debugf.write("[DEBUG] Debug start.\n")

def fetch_articles(pages=1):
    articles = []
    for page in range(1, pages + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}search/label/Artificial%20Intelligence?updated-max=&max-results=10"
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")
        if page == 1:
            with open("debug_output.txt", "a", encoding="utf-8") as debugf:
                debugf.write("[DEBUG] Homepage <body> preview:\n")
                if soup.body is not None:
                    debugf.write(str(soup.body.prettify()[:30000]) + "\n\n")
                else:
                    debugf.write("[DEBUG] soup.body is None\n\n")
        if resp.status_code != 200:
            with open("debug_output.txt", "a", encoding="utf-8") as debugf:
                debugf.write(f"[DEBUG] Failed to fetch list page: {url}, status: {resp.status_code}\n")
            continue
        # 新的首页文章抓取逻辑
        for post in soup.select('.body-post'):
            link_tag = post.select_one('.story-link')
            link = str(link_tag['href']) if link_tag and link_tag.has_attr('href') else ''
            title_tag = post.select_one('.home-title')
            title = title_tag.get_text(strip=True) if title_tag else ''
            desc_tag = post.select_one('.home-desc')
            desc = desc_tag.get_text(strip=True) if desc_tag else ''
            date_tag = post.select_one('.h-datetime')
            date = date_tag.get_text(strip=True) if date_tag else datetime.now().strftime("%Y-%m-%d")
            tags_tag = post.select_one('.h-tags')
            tags = tags_tag.get_text(strip=True) if tags_tag else ''
            content = desc
            # 详情页正文抓取
            if link:
                try:
                    detail_resp = requests.get(link, headers=HEADERS, timeout=10)
                    if detail_resp.status_code == 200:
                        detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                        body_tag = (
                            detail_soup.select_one(".articlebody") or
                            detail_soup.select_one(".post-content") or
                            detail_soup.select_one("article") or
                            detail_soup.select_one("#articlebody") or
                            detail_soup.select_one(".body-post")
                        )
                        if body_tag:
                            content = body_tag.get_text("\n", strip=True)
                            # 每4句话新起一段
                            sentences = re.split(r'(?<=[.!?。！？])\s+', content)
                            paragraphs = [' '.join(sentences[i:i+4]).strip() for i in range(0, len(sentences), 4)]
                            content = '\n\n'.join([p for p in paragraphs if p])
                        else:
                            paragraphs = detail_soup.find_all("p")
                            content = "\n".join([
                                p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30
                            ])
                            sentences = re.split(r'(?<=[.!?。！？])\s+', content)
                            paragraphs = [' '.join(sentences[i:i+4]).strip() for i in range(0, len(sentences), 4)]
                            content = '\n\n'.join([p for p in paragraphs if p])
                        with open("debug_output.txt", "a", encoding="utf-8") as debugf:
                            debugf.write(f"[DEBUG] {link} content length: {len(content)}\n")
                            debugf.write(str(detail_soup.prettify()[:2000]) + "\n\n")
                    else:
                        with open("debug_output.txt", "a", encoding="utf-8") as debugf:
                            debugf.write(f"[DEBUG] Failed to fetch detail page: {link}, status: {detail_resp.status_code}\n")
                except Exception as e:
                    content = f"[抓取正文失败: {e}]"
                    with open("debug_output.txt", "a", encoding="utf-8") as debugf:
                        debugf.write(f"[DEBUG] Exception fetching detail page: {link}, error: {e}\n")
            content_for_filter = f"{title} {content}".lower()
            if any(kw in content_for_filter for kw in KEYWORDS):
                articles.append({
                    "title": title,
                    "content": content,
                    "date": date,
                    "tags": tags,
                    "link": link
                })
    return articles

def save_articles_md(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("_archives", exist_ok=True)
    md_path = f"_archives/{today}.md"
    # 构建 front matter
    fm = {
        "layout": "archive-article",
        "title": f"{today} AI创业新闻",
        "date": today,
        "articles": [
            {"title": art["title"], "anchor": f"article-{i+1}"} for i, art in enumerate(articles)
        ]
    }
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(fm, f, allow_unicode=True, sort_keys=False)
        f.write("---\n\n")
        f.write(f"# {today} AI创业新闻\n\n")
        for idx, article in enumerate(articles, 1):
            title = article.get("title", "无标题")
            content = article.get("content", "")
            anchor = f"article-{idx}"
            f.write(f"## <a id='{anchor}'></a>{title}\n\n")
            if content:
                f.write(f"{content}\n\n")

def main():
    articles = fetch_articles(pages=2)  # 恢复多页抓取
    save_articles_md(articles)
    print(f"Fetched and archived {len(articles)} AI/创业 related articles.")

if __name__ == "__main__":
    main() 