# GitHub Pages 自动部署详细教程（双仓库方案）

本教程适用于：**源码/爬虫/配置私有，仅公开静态网页**，并实现每天自动抓取、自动部署到 GitHub Pages。

---

## 1. 仓库准备

### 1.1 创建私有源码仓库
- 仓库名建议：`hacker-news-ai-source`
- 选择 Private（私有）
- 存放所有源码、爬虫、配置、Actions 等

### 1.2 创建公开静态网页仓库
- 仓库名建议：`hacker-news-ai-pages`
- 选择 Public（公开）
- 只存静态网页（HTML/CSS/JS），用于 GitHub Pages

---

## 2. 生成 GitHub Token 并配置 Secrets

### 2.1 生成 Token
1. 打开 [GitHub Token 设置](https://github.com/settings/tokens)
2. 点击“Generate new token”
3. 备注如 `pages-deploy-token`，勾选 `repo` 权限
4. 生成后**复制 Token**，妥善保存

### 2.2 配置 Secrets
1. 打开私有仓库（`hacker-news-ai-source`）
2. 进入 Settings → Secrets → Actions
3. 新建一个 secret：
   - Name: `PAGES_DEPLOY_TOKEN`
   - Value: 粘贴刚才生成的 Token

---

## 3. 配置 GitHub Actions（私有仓库）

在 `hacker-news-ai-source` 仓库根目录下新建 `.github/workflows/deploy.yml`，内容如下：

```yaml
name: Auto Crawler & Deploy to Public Pages

on:
  schedule:
    - cron: '0 2 * * *'   # 每天UTC时间2点（北京时间10点）自动运行
  workflow_dispatch:      # 允许手动触发

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run crawler and generate static site
        run: |
          # 运行你的爬虫和静态站点生成命令
          python crawl_novel_v4.py
          # 假设生成的静态网页在 _site 目录

      - name: Checkout public pages repo
        uses: actions/checkout@v3
        with:
          repository: gcp-lopo/hacker-news-ai-pages
          ref: main
          path: public-pages
          token: ${{ secrets.PAGES_DEPLOY_TOKEN }}

      - name: Copy generated site to public repo
        run: |
          rm -rf public-pages/*
          cp -r _site/* public-pages/
          cd public-pages
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
          git push origin main
```

> **注意：**
> - `repository: gcp-lopo/hacker-news-ai-pages` 已替换为你的用户名和公开仓库名
> - `_site` 为静态网页目录，如有不同请自行修改

---

## 4. 配置公开仓库为 GitHub Pages

1. 打开 `hacker-news-ai-pages` 仓库
2. 进入 Settings → Pages
3. 选择 `main` 分支作为 Pages 源，保存
4. 稍等片刻，访问分配的 GitHub Pages 地址即可

---

## 5. 常见问题与注意事项

- **首次推送**：公开仓库需有至少一次初始化提交（如 README.md），否则无法推送
- **Token 权限**：只需 `repo` 权限即可推送到公开仓库
- **静态目录**：确保 Actions 里复制的是你生成的静态网页目录
- **定时任务**：cron 表达式可调整为你希望的时间
- **私有仓库 Actions**：免费账户可用，私有仓库 Actions 有免费额度限制
- **公开仓库内容**：只有 HTML/CSS/JS 公开，源码、爬虫、配置等全部私有

---

如有疑问，欢迎随时提问！ 

---

## 6. 本地项目迁移到私有源码仓库的操作步骤

### 6.1 克隆私有源码仓库到本地

```bash
git clone https://github.com/gcp-lopo/hacker-news-ai-source.git
```

### 6.2 拷贝项目内容到新仓库

1. 将你本地的 `Hacker-News-Ai` 文件夹里的所有内容（包括隐藏文件如 `.github`、`.gitignore` 等）**复制到 `hacker-news-ai-source` 文件夹**（即刚刚 clone 下来的目录）里。
2. 如果 `hacker-news-ai-source` 目录里有默认的 `README.md` 或其他初始化文件，可以选择覆盖或合并。

### 6.3 提交并推送到 GitHub

在 `hacker-news-ai-source` 目录下执行：

```bash
git add .
git commit -m "Initial import of all project files"
git push
```

### 6.4 检查 Actions 和 Secrets

1. 确认 `.github/workflows/deploy.yml` 已在仓库中。
2. 确认你已经在 GitHub 仓库的 Settings → Secrets → Actions 里添加了 `PAGES_DEPLOY_TOKEN`。

### 6.5 等待自动部署

- 你可以在 GitHub 上的 Actions 页面看到自动部署流程。
- 首次部署后，静态网页会自动推送到 `hacker-news-ai-pages` 仓库。

---

> 之后所有开发、更新都在 `hacker-news-ai-source` 仓库进行，静态网页自动同步到公开仓库。 