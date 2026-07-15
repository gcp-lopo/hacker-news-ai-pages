# AI 与数据工作流雷达

这是 Lopo Blog 的候选资讯工具，数据源为 [The Hacker News](https://thehackernews.com/)。

它不再泛化聚合 AI 与创业新闻，而是优先筛选：

- AI 编程与开发工具；
- 数据工作流、自动化和开源工具；
- AI 使用中的数据安全、提示注入和供应链风险。

## 内容管道

```text
来源列表
→ AI 信号识别
→ 与个人内容主线相关的主题分类
→ 候选资讯队列
→ 人工阅读全文与交叉核验
→ 代码案例、检查清单或博客文章
```

`_data/content_candidates.json` 保存候选状态、入选原因和可转化方向。自动命中不代表本站推荐、事实核验或专业建议。

站点只保留标题、来源摘要、标签和原文链接，不抓取或重新发布文章全文。

## 本地运行

```bash
pip install -r requirements.txt
python fetch_hackernews_ai_articles.py
bundle install
bundle exec jekyll serve
```

Pull Request 只抓取、构建、验证并上传私有预览；合并或定时任务才会提交归档并发布到公开 Pages 仓库。
