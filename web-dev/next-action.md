# deploy

## Azure App Services (Web App for Containers)

app services + azure container registry + azure blob storage + app services deploy slot

## 进阶方案
进阶方案 1：配置 CI/CD Pipeline

配置 GitHub Actions：

- 在你的代码仓库中添加 GitHub Actions 工作流文件。
- 配置工作流，自动构建 Docker 镜像并推送到 ACR。
- 设置自动部署到 Azure App Services。

#### 进阶方案 2：docker swarm

#### 进阶方案 3：Azure Kubernetes Service (AKS)

### 利用 AFD 的多 origin 功能
Azure Front Door (AFD) 支持多个 origin 和 origin group，你可以利用这个功能同时运行不同部署方案，进行负载均衡和性能比较。



# nginx document root

### 调整 `web-app` 中获取 HTML 的逻辑

#### 当前问题
在你的 `app.py` 中，`view_article` 路由直接读取 HTML 文件的内容并将其作为字符串传递给模板：

```python
html_path = f"{Rendered_Articles}{os.sep}{category_path}{os.sep}{article_id}.html"
with open(html_path, 'r', encoding='utf-8') as f:
    article_content = f.read()
return render_template('article_details.html', article=article, article_content=article_content)
```

现在 Nginx 接管了静态文件服务，我们需要改为生成指向 Nginx 的 URL，让前端通过 URL 加载内容。

#### 解决方案
1. **修改 `view_article` 路由**
   不再直接读取文件，而是生成静态文件的 URL：

   ```python
   @app.route("/Articles/<int:article_id>")
   def view_article(article_id):
       article = db.session.execute(
           db.select(Article_Meta_Data)
           .where(Article_Meta_Data.id == article_id)
       ).scalar()
   
       if not article:
           abort(404)
       
       # 转换 category 中的 / 为 - 以匹配文件系统路径
       category_path = article.category.replace(os.sep, '-')
       
       # 生成 Nginx 静态文件的 URL
       static_url = f"/rendered-articles/{category_path}/{article_id}.html"
       
       return render_template('article_details.html', 
                              article=article,
                              static_url=static_url)
   ```

   这里，`static_url` 是指向 Nginx 服务的相对路径，例如 `/rendered-articles/PythonLearn-PythonPackage-Flask/1.html`。

2. **修改模板 (`article_details.html`)**
   有两种方式在前端加载静态内容：

   **方式 1：使用 iframe**
   ```html
   <!-- article_details.html -->
   {% extends "base.html" %}
   
   {% block content %}
       <h1>{{ article.title }}</h1>
       <iframe src="{{ static_url }}" width="100%" height="600px" frameborder="0"></iframe>
   {% endblock %}
   ```

   **方式 2：使用 JavaScript 动态加载**
   ```html
   <!-- article_details.html -->
   {% extends "base.html" %}
   
   {% block content %}
       <h1>{{ article.title }}</h1>
       <div id="article-content"></div>
       <script>
           fetch('{{ static_url }}')
               .then(response => response.text())
               .then(data => {
                   document.getElementById('article-content').innerHTML = data;
               })
               .catch(error => console.error('Error loading article:', error));
       </script>
   {% endblock %}
   ```

   - **iframe** 简单直接，适合完整显示 HTML。
   - **JavaScript** 更灵活，可以进一步处理内容（例如提取部分 HTML），但需要额外的错误处理。

#### 选择建议
- 如果你的 HTML 文件是独立的完整页面，推荐使用 **iframe**。
- 如果需要将 HTML 内容嵌入到现有页面布局中，推荐使用 **JavaScript**。



1. **调整 `web-app` 的逻辑**
   在开发环境中，你可能仍想使用 Flask 提供静态文件以便调试。我们可以通过 `ENV` 环境变量动态注册静态路由：

   ```python
   import os
   from flask import Flask, render_template, abort, send_from_directory
   from models import db, Article_Meta_Data
   from import_articles_scripts import import_articles
   from config import Articles_Directory, Rendered_Articles
   
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
   app.config['RENDERED_ARTICLES_FOLDER'] = Rendered_Articles
   db.init_app(app)
   
   # 根据环境变量决定是否注册静态文件夹
   if os.getenv('ENV', 'dev') == 'dev':
       app.add_url_rule('/rendered-articles/<path:filename>',
                        endpoint='rendered-articles',
                        view_func=lambda filename: send_from_directory(app.config['RENDERED_ARTICLES_FOLDER'], filename))
   
   with app.app_context():
       db.drop_all()
       db.create_all()
       import_articles(Articles_Directory, db)
   
   @app.route("/Articles/<int:article_id>")
   def view_article(article_id):
       article = db.session.execute(
           db.select(Article_Meta_Data)
           .where(Article_Meta_Data.id == article_id)
       ).scalar()
   
       if not article:
           abort(404)
       
       category_path = article.category.replace(os.sep, '-')
       static_url = f"/rendered-articles/{category_path}/{article_id}.html"
       
       return render_template('article_details.html', 
                              article=article,
                              static_url=static_url)
   ```

   - 在 `ENV=dev` 时，Flask 会注册 `/rendered-articles/` 路由，方便调试。
   - 在 `ENV=prod` 时，不注册此路由，Nginx 完全接管静态文件服务。

2. **开发与生产环境的运行方式**
   - **开发环境**：直接运行 `docker-compose up`，默认 `ENV=dev`。
   - **生产环境**：运行 `ENV=prod docker-compose up`，切换到生产模式。

#### 最佳实践
- **统一配置文件**：通过环境变量在一套 `compose.yaml` 中管理开发和生产环境，避免维护两套配置文件。
- **调试便利性**：开发环境中保留 Flask 的静态服务，生产环境中利用 Nginx 的高性能。
- **安全性**：生产环境中移除不必要的挂载（如 `./web-app:/app`），减少攻击面。

---

### 完整实现后的效果
- **开发环境**：
  - `rendered_articles` 挂载到 `/rendered-articles`，你可以在主机上访问 `./web-app/rendered-articles` 查看文件。
  - Flask 可通过 `/rendered-articles/` 提供静态文件，方便调试。
  - Nginx 也能提供这些文件，但主要用于测试反向代理。
- **生产环境**：
  - `rendered_articles` 仅挂载到 `/rendered-articles` 和 Nginx 的 `/usr/share/nginx/html/rendered-articles`。
  - Nginx 高效提供静态文件，Flask 只生成 URL。

