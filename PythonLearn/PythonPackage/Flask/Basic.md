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
next: [Quickstart — Flask Documentation (3.0.x)](https://flask.palletsprojects.com/en/stable/quickstart/#routing)
