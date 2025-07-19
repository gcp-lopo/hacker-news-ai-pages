# Hacker News AI 创业新闻聚合

本项目每日自动抓取 [The Hacker News](https://thehackernews.com/) 上与 AI 创业相关的文章，按日期自动存档为 `.md` 文件，并通过 GitHub Pages 提供极简、科技感、带导航栏的聚合展示。

## 功能特性
- 每日自动抓取 AI 创业相关新闻
- 按日期自动归档为 Markdown 文件
- 首页和每个存档页左侧均有可跳转的导航栏
- 支持 GitHub Actions 自动化与 GitHub Pages 静态托管
- 极简、科技感 UI

## 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 本地抓取：`python fetch_hackernews_ai_articles.py`
3. 本地预览：`bundle exec jekyll serve`
4. 访问：`http://localhost:4000/hacker-news-ai/`

## 自动化
- 已配置 GitHub Actions，每天自动抓取并归档
- 归档文件位于 `_archives/YYYY-MM-DD.md`

## 目录结构
- `_archives/`：每日新闻归档（Markdown）
- `_includes/`：导航栏等可复用组件
- `_layouts/`：页面布局模板
- `assets/`：样式与脚本
- `index.html`：首页
- `archives.md`：历史归档页
- `fetch_hackernews_ai_articles.py`：抓取脚本

## 访问效果
- 首页展示今日新闻，左侧导航可跳转各归档
- 每日归档页展示当天所有新闻，左侧导航可跳转各新闻

--- 