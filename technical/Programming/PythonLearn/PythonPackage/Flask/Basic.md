---
Title: Flask basic knowledge
Author: 陈翰杰
Instructor: Sonnet 3.5
CoverImage: ./images/cover_image.jpg
RolloutDate: 2024-11-22
---

```
BriefIntroduction: 
Flask learning note, flask version >= 3.0.X

```

<!-- split -->

![cover](./images/cover_image.png)

# Flask Basic

Flask >= 3.0.X

reference document: [Welcome to Flask — Flask Documentation (3.0.x)](https://flask.palletsprojects.com/en/stable/)

a simple example

```python
from flask import Flask, render_template, request

app = Flask(__name__)

# configure the database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
# use memory as test
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# 初始化应用
db.init_app(app)

@app.route("/")
def index():
    # use the file in the templates
    return render_template("index.html")

@app.route("/AboutMe")
def about_me():
    return render_template("about_me.html")

# deal with 404 error
@app.errorhandler(404)
def page_not_found(error_info):  # 接受异常对象作为参数
    # print(f"Error: {error_info}, Description: {error_info.description}, URL: {request.url}") # 打印错误信息到控制台
    return render_template('404.html', error = error_info, url = request.url), 404  # 将错误信息传递给模板

```

## run the code

如果之前的代码文件叫做 hello.py 那么使用下面的命令

```shell
flask --app hello run

# or

python -m flask --app hello run
```

> ! [note]
>
> 如果 py 文件叫做 app.py / wsgi.py 可以省略 `-app` 参数直接使用 `flask run` 命令
>
> 其中 `WSGI` 的全程是 Web Server Gateway Interface

这会开启一个默认监听 localhost:5000 端口的 server

```bash
$ flask run
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

这只能本地才能访问，为了开放给某个 IP address 可以添加 `--host = ` 例如

```python
--host=0.0.0.0 - 监听所有可用的 IPv4 地址
--host=:: - 监听所有可用的 IPv6 地址
--host=192.168.0.100 - 监听特定的 IP 地址
```

> ! [note]
>
> Flask 的 `--host` 参数并不支持直接指定 IP 地址段范围（如 CIDR 表示法 192.168.0.0/24）。`--host` 参数只能指定服务器要监听的具体 IP 地址。

### enable debug mode

当修改完代码之后，查看结果效果是否符合预期，那么需要 `ctrl+c` 然后再 `flask run` 一次，但是如果 enable debug mode 那么 server 会自动 reload 修改之后的代码， 而无需关闭重启

只需添加 `--debug` 参数即可

```python
$ flask run --debug
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 129-313-345
# ...
 * Detected change in '/home/.../.../test-website/app.py', reloading
 * Restarting with stat
# ...
```

## HTML Escaping

当处理用户输入时需要特别注意 XSS 攻击。HTML Escaping 是一种防御机制，将特殊字符转换为对应的 HTML 实体（如 `<` 变成 `&lt;`），防止恶意脚本执行。

例如，用户输入 `<script>alert('hack')</script>` 

在 Flask 中，Jinja2 模板会自动转义：
```python
# 路由函数
@app.route("/post")
def post():
    user_input = "<script>alert('hack')</script>"
    return render_template('post.html', content=user_input)

# 模板文件 post.html
{{ content }}  # 会自动转义为 &lt;script&gt;alert('hack')&lt;/script&gt;
{{ content|safe }}  # 不转义，危险！除非确保内容安全
```

如需手动转义，使用：
```python
from markupsafe import escape
escaped_content = escape(user_input)
```
# Route Function

Flask 会基于 URL 匹配自动调用路由函数，我们只要在 app.py 中正确定义路由和相应的函数，并且在 templates 中使用 `url_for()` 正确引用这些函数。

> `url_for()` 函数根据在 Flask 应用中定义的路由函数名生成 URL 在这个例子中，它会生成 "/Articles" 的 URL。

例如

```python
@app.route("/")
def index():
    # use the file in the templates
    return render_template("index.html")

@app.route("/Articles")
def article_index():
    # 从数据库中获取所有文章
    articles = db.session.execute(db.select(Article_Meta_Data)).scalars().all()
    return render_template("article_index.html", articles=articles)
```

在 index.html 中

```html
    <!-- Navbar -->
    <nav class="navbar navbar-expand-sm navbar-custom fixed-top">
      <div class="container">
        <div class="collapse navbar-collapse" id="mynavbar">
          <ul class="navbar-nav ms-auto">
            <!-- 文章页面就可以包含分类和标签了 不用另外起一个页面 -->
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('article_index') }}">
                 Article
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
```


在 index.html 中，使用了 `{{ url_for('article_index') }}` 来生成链接。这里的 'article_index' 是指向在 app.py 中定义的函数名

当用户点击这个链接时，浏览器会发送一个 GET 请求到 "/Articles" 路径。

Flask 接收到这个请求后，会查找匹配 "/Articles" 路径的路由。它找到了定义的 `@app.route("/Articles")` 装饰器，因此会调用 `article_index()` 函数。

## Variable Rules

example

```python
# 文章详情页面的通用路由
@app.route('/article/<int:article_id>')
def article_detail(article_id):
    # 从数据库获取特定ID的文章
    article = Article.query.get_or_404(article_id)
    return render_template('article_detail.html', article=article)

# 在模板中使用
# article_detail.html
<a href="{{ url_for('article_detail', article_id=1) }}">查看文章1</a>
```

Flask 提供了几种内置的转换器：

```python
# 默认是字符串类型
@app.route('/user/<username>')  # 接受任何不含斜杠的文本

# 整数类型
@app.route('/post/<int:post_id>')  # 只接受正整数

# 浮点数类型
@app.route('/price/<float:amount>')  # 接受正浮点数

# 路径类型
@app.route('/files/<path:filepath>')  # 接受包含斜杠的路径

# UUID类型
@app.route('/user/<uuid:user_id>')  # 接受UUID字符串
```

### 多变量路由

```python
@app.route('/blog/<int:year>/<int:month>/<int:day>/<slug>')
def blog_post(year, month, day, slug):
    # 处理逻辑
    return f"Post from {year}-{month}-{day}: {slug}"
```

这个路由可以匹配像 `/blog/2023/11/13/flask-routing-explained` 这样的 URL。

多参数路由定义：

```python
@app.route('/Articles/<path:category>/<title>')
def article_detail(category, title):
    # 处理逻辑
    return f"Category: {category}, Title: {title}"
```

在这个例子中：
- `<path:category>` 允许包含斜杠的路径，适用于多层级分类。
- `<title>` 是一个普通的字符串参数，用于文章标题。

在 template 中使用多参数 URL：

```html
<a href="{{ url_for('article_detail', category='technology/programming', title='introduction-to-flask') }}">
    Introduction to Flask
</a>
```

## Unique URL

```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

带斜杠的URL（如 `/projects/`）: 访问 `/projects` -> 自动重定向到 `/projects/`

不带斜杠的URL（如 `/about`）: 访问 `/about/` -> 返回 404 错误

建议：
- 如果这个 URL 代表一个集合或目录，使用尾部斜杠（如 `/users/`）
- 如果这个 URL 代表一个具体资源或文件，不使用尾部斜杠（如 `/user/123` 或 `/about`）

这就像在文件系统中：`/home/user/` 是一个目录 `/home/user/file.txt` 是一个文件

## `url_for()` function

`url_for()` 是 Flask 提供的 URL 生成函数，它接受两种类型的参数：
1. 第一个参数是 **endpoint**（通常是视图函数的名称）
2. 后面可以跟任意个关键字参数，用于传递变量

for example

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

# 在视图函数中使用
with app.test_request_context():
    print(url_for('index'))                    # 输出: /
    print(url_for('login'))                    # 输出: /login
    print(url_for('login', next='/'))          # 输出: /login?next=/
    print(url_for('profile', username='John', page=2)) # 输出: /user/John?page=2
```

**特殊参数**

```python
# _external=True: 生成完整的 URL（包含域名）
url_for('index', _external=True)  
# 输出: http://localhost/

# _anchor='section1': 添加锚点
url_for('index', _anchor='section1')  
# 输出: /#section1

# _scheme='https': 指定协议
url_for('index', _external=True, _scheme='https')  
# 输出: https://localhost/
```

### best practice

始终使用 `url_for()`

```python
# 不推荐
<a href="/user/john">John's profile</a>

# 推荐
<a href="{{ url_for('profile', username='john') }}">John's profile</a>
```
如果以后修改了 URL 规则，只需要修改路由装饰器，而不需要修改所有模板中的链接。

**处理静态文件**

```python
# 访问静态文件
url_for('static', filename='style.css')      # 输出: /static/style.css
url_for('static', filename='js/script.js')   # 输出: /static/js/script.js
```

**在模板中使用**

```html
<!-- 在 Jinja2 模板中使用 -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<a href="{{ url_for('profile', username='john') }}">John's Profile</a>
```

## HTTP methods

flask 可以区分到同一个路径不同的 HTTP methods

```python
from flask import request


# 使用 reqeust.method 来区分
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


# 或者直接定义路由函数的时候使用
@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()    
```

# Static folder

'static' 是 Flask 中的一个内置特殊 endpoint，Flask 默认会注册这个端点来处理静态文件，所以不能创建名为 'static' 的视图函数，因为这会与 Flask 的内置静态文件处理冲突

**Flask 如何处理静态文件**

```python
from flask import Flask
app = Flask(__name__,
           static_folder='static',     # 默认值，可以修改
           static_url_path='/static'   # 默认值，可以修改
)
```
- `static_folder`: 指定存放静态文件的文件夹路径
- `static_url_path`: 指定访问静态文件的 URL 前缀

## default static folder

可以通过改变配置 修改默认的静态文件夹

```python
# 修改静态文件夹和URL路径
app = Flask(__name__,
           static_folder='assets',        # 改变物理文件夹名
           static_url_path='/resources'   # 改变URL路径
)

# 现在可以这样访问静态文件
url_for('static', filename='style.css')  # 输出: /resources/style.css
```

- `static_folder` 是**物理文件系统**中实际存储静态文件的文件夹名称
- `static_url_path` 是**URL路径**中用来访问静态文件的前缀

这样设计的目的是为了解耦物理存储路径和URL路径

```python
app = Flask(__name__,
           static_folder='assets',        # 文件实际存储在 assets/ 目录
           static_url_path='/public'      # URL 以 /public 开头
)
```

文件系统结构：

```
your_flask_app/
├── assets/              # 实际的文件夹
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── logo.png
├── templates/
└── app.py
```

URL访问方式：

```python
url_for('static', filename='css/style.css')    # 输出: /public/css/style.css
url_for('static', filename='images/logo.png')  # 输出: /public/images/logo.png
```

### Advantage

使用这种设计可以隐藏实际的服务器文件结构，而且更加灵活

```python
# 开发环境
app = Flask(__name__,
           static_folder='dev_assets',
           static_url_path='/static')

# 生产环境
app = Flask(__name__,
           static_folder='prod_assets',
           static_url_path='/static')
```

不同环境可以使用不同的文件夹，但保持相同的URL结构

for example

```python
# 例1：多版本静态文件
app = Flask(__name__,
           static_folder='assets_v2',
           static_url_path='/static')

# 在模板中的使用不变
# <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
# 实际访问的是 assets_v2/css/style.css 文件
# 但URL显示为 /static/css/style.css

# 例2：开发和生产环境配置
if app.debug:
    app.static_folder = 'dev_assets'    # 开发环境使用未压缩的文件
else:
    app.static_folder = 'prod_assets'   # 生产环境使用压缩后的文件
app.static_url_path = '/static'         # URL保持一致
```



## add customize static folder

除了默认的 static 作为静态文件 如果想要再创建一个静态文件夹方便 `url_for()` 调用 可以这么做

```python
# 装饰器方式
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('uploads', filename)

# 等价于
def serve_uploads(filename):
    return send_from_directory('uploads', filename)
app.add_url_rule('/uploads/<path:filename>', 'serve_uploads', serve_uploads)
```

### `send_from_directory()`

这两种方式能够添加额外的静态文件夹，核心在于 `send_from_directory` 函数：

```python
from flask import send_from_directory

# 基本使用
@app.route('/files/<path:filename>')
def serve_files(filename):
    return send_from_directory('files_folder', filename)

# 带安全检查的使用
@app.route('/files/<path:filename>')
def serve_files_safe(filename):
    try:
        return send_from_directory('files_folder', filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
```

`send_from_directory` 不仅仅是简单地读取和发送文件，而是包含了完整的安全检查、MIME 类型处理、缓存控制等功能，确保文件传输的安全性和效率。

### `@app.route` VS `add_url_rule`

如果静态文件夹需要额外的处理逻辑（如权限检查、日志记录等）就用 @app.route 方式；如果只是单纯提供文件访问就用 add_url_rule 方式。

# next

[Quickstart — Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates)
