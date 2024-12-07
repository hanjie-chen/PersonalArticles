我一开始的想法是把渲染完成的 html 文件直接一股脑的全部放到 rendered_articles 这个文件夹下面，然后为了防止同名文件，我打算使用数据库的主键 id 作为html 的文件名称，例如

```perl
➜ rendered_articles
├───1.html
├───2.html
├───3.html
├───4.html
└───5.html
```

但是这样子会遇到一个问题，那就是如果源文件需要使用 images 里面的资源，那么他又要去哪里找呢？所以我又想着需要把 images 文件夹拷贝过去

所以问题来了，把这个 images 文件夹放在哪里？

我的想法是，在 rendered_articles 中每一个分类都创建一个文件夹，然后把images文件夹 copy 进去即可，然后把属于这个 category 的文章都放在这个文件夹下，这样子就无需修改 html 中的图片引用方式，我都是使用相对路径来引用图片的，例如 `./images/cover_image.jpg`

而这个文件夹的命令，则是把 category 中的 `/` 更换为 `-` 例如

```perl
rendered_articles/
├── PythonLearn-PythonPackage-SQLAlchemy
│   ├── 2.html
│   └── images
│       └── cover_image.png
├── PythonLearn-PythonPackage-flask-sqlalchemy
│   ├── 3.html
│   └── images
│       └── cover_image.webp
└── ToolGuide-GitGuide
    ├── 1.html
    └── images
        └── cover_image.png
```





# 路由设计问题

- 问题描述：如何优雅地处理多层级目录结构的路由，避免为每个可能的路径都写一个路由函数

- 你期望的URL结构：`Articles/PythonLearn/PythonPackage/Flask/<title>`
- 困扰：
  - 简单的 `@app.route("/Articles/<title>")` 无法处理层级结构
  - 手动定义每个路径的路由函数太过繁琐
  - 倾向于使用 `@app.route("/Articles/<path:category>/<title>")` 但需要确认具体实现方式

```python
from flask import Flask, render_template, abort
from werkzeug.routing import BaseConverter
from typing import Optional, List

class CategoryConverter(BaseConverter):
    def to_python(self, value: str) -> List[str]:
        return value.split('/')
    
    def to_url(self, value: List[str]) -> str:
        return '/'.join(value)

app = Flask(__name__)
app.url_map.converters['category'] = CategoryConverter

@app.route('/articles/<category:categories>/<title>')
def view_article(categories: List[str], title: str):
    # 将categories列表转换为路径字符串
    category_path = '/'.join(categories)
    
    # 查询文章
    article = db.session.execute(
        db.select(Article_Meta_Data).where(
            db.and_(
                Article_Meta_Data.category == category_path,
                Article_Meta_Data.title == title
            )
        )
    ).scalar_one_or_none()
    
    if not article:
        abort(404)
    
    # 渲染模板，使用数据库ID找到对应的HTML文件
    return render_template(f'rendered_articles/{article.id}.html')

# 可选：添加一个重定向路由，支持直接通过ID访问文章
@app.route('/articles/by-id/<int:article_id>')
def view_article_by_id(article_id: int):
    article = db.session.get(Article_Meta_Data, article_id)
    if not article:
        abort(404)
    
    # 重定向到规范的URL
    categories = article.category.split('/')
    return redirect(url_for('view_article', categories=categories, title=article.title))
```

