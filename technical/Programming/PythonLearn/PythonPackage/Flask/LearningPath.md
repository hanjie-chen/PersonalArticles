# Learning Path

从你的描述和代码来看，你的学习方向是正确的。让我详细分析一下：

1. **你的现状**:
   - 已经掌握了基本的数据库操作（SQLAlchemy + Flask-SQLAlchemy）
   - 已经建立了基本的路由结构
   - 明确了需求（将markdown渲染为html并提供静态文件服务）

2. **关于学习Flask文档的决定**:
   这是个很好的决定。官方文档是最权威的学习资源。

3. **需要掌握的Flask知识程度**:
对于你的个人网站项目，你需要重点掌握以下Flask概念：

   - **基础概念**:
     - 路由系统（已经有基础了）
     - 请求-响应循环
     - 上下文（Application Context和Request Context）

   - **重点需要学习的部分**:
     - 静态文件处理（这是你当前的痛点）
     - 模板系统（Jinja2）
     - 蓝图（Blueprint）- 用于更好地组织代码
     - 错误处理（已经开始使用了）

4. **对你当前代码的建议**:
   ```python
   # 1. 静态文件处理
   # 不建议使用add_url_rule来注册静态文件夹
   # 推荐使用Flask的标准静态文件配置：
   app = Flask(__name__, 
               static_folder='rendered_articles',  # 静态文件夹路径
               static_url_path='/articles')        # URL前缀
   
   # 2. 数据库初始化
   # 建议移到单独的init_db函数中
   def init_db():
       with app.app_context():
           db.drop_all()
           db.create_all()
           import_articles(db, Articles_Directory)
   
   # 3. 文章渲染部分
   @app.route("/Articles/<title>")
   def view_articles(title):
       article = db.session.execute(
           db.select(Article_Meta_Data)
           .where(Article_Meta_Data.title == title)
       ).scalar_one_or_none()  # 使用scalar_one_or_none更安全
       
       if not article:
           abort(404)  # 使用abort更符合Flask风格
           
       # Markdown转HTML的处理
       html_content = convert_markdown_to_html(article.content)
       return render_template('article.html', article=article, content=html_content)
   ```

5. **建议的下一步**:

   a. **先完成必要的Flask学习**:
      - 完整阅读Flask官方文档的Quick Start和Tutorial部分
      - 特别关注静态文件配置部分

   b. **实现Markdown转HTML功能**:
      - 可以使用Python的markdown库
      - 考虑使用Flask-Markdown扩展

   c. **优化项目结构**:
      ```
      your_project/
      ├── app/
      │   ├── __init__.py
      │   ├── routes/
      │   ├── models/
      │   ├── templates/
      │   ├── static/
      │   └── rendered_articles/
      ├── scripts/
      │   └── import_articles.py
      ├── config.py
      └── run.py
      ```

总的来说，你的方向是对的，建议花1-2天时间过一遍Flask官方文档的核心部分，然后就可以继续开发了。记住，不需要完全精通Flask才能继续开发，在开发过程中遇到问题再查询文档是很正常的学习方式。