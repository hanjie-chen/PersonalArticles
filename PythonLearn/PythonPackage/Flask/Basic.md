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
```

## HTML Escaping

当处理用户输入时需要特别注意 XSS 攻击。HTML Escaping 是一种防御机制，将特殊字符转换为对应的 HTML 实体（如 < 变成 &lt;），防止恶意脚本执行。

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
# Routing

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
