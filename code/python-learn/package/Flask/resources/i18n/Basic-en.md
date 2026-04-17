<!-- source_blob: c754b19ef8c577db4dac8a1608257d3343a25da6 -->

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

## Run the Code

If the previous code file is named hello.py, then use the following command:

```shell
flask --app hello run

# or

python -m flask --app hello run
```

> [!note]
>
> If the py file is named app.py / wsgi.py, you can omit the `-app` parameter and use the `flask run` command directly.
>
> `WSGI` stands for Web Server Gateway Interface.

This starts a server that listens on `localhost:5000` by default.

```bash
$ flask run
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

This can only be accessed locally. To expose it to a certain IP address, you can add `--host = `, for example:

```python
--host=0.0.0.0 - 监听所有可用的 IPv4 地址
--host=:: - 监听所有可用的 IPv6 地址
--host=192.168.0.100 - 监听特定的 IP 地址
```

> [!note]
>
> Flask's `--host` parameter does not support directly specifying an IP address range (such as CIDR notation `192.168.0.0/24`). The `--host` parameter can only specify the exact IP address the server should listen on.

### Enable Debug Mode

After modifying the code, if you want to check whether the result matches your expectations, you normally need to press `ctrl+c` and run `flask run` again. But if you enable debug mode, the server will automatically reload the modified code without needing to stop and restart it.

You only need to add the `--debug` parameter.

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

Note that debug mode here not only detects changes to `.py` files, but also changes to `.html` files in the `templates` folder[^flask-config].

## HTML Escaping

When handling user input, you need to pay special attention to XSS attacks. HTML escaping is a defense mechanism that converts special characters into their corresponding HTML entities (for example, `<` becomes `&lt;`) to prevent malicious scripts from executing.

For example, if the user enters `<script>alert('hack')</script>`

In Flask, Jinja2 templates escape automatically:
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

If you need to escape manually, use:
```python
from markupsafe import escape
escaped_content = escape(user_input)
```
# Route Function

Flask automatically calls route functions based on URL matching. You only need to define the routes and corresponding functions correctly in `app.py`, and use `url_for()` correctly in `templates` to reference those functions.

> The `url_for()` function generates a URL based on the route function name defined in the Flask application. In this example, it generates the URL for `"/Articles"`.

For example:

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

In `index.html`:

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

In `index.html`, `{{ url_for('article_index') }}` is used to generate the link. Here, `'article_index'` refers to the function name defined in `app.py`.

When the user clicks this link, the browser sends a GET request to the `"/Articles"` path.

After Flask receives this request, it looks for a route that matches the `"/Articles"` path. It finds the defined `@app.route("/Articles")` decorator, so it calls the `article_index()` function.

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

Flask provides several built-in converters:

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

### Multi-Variable Routes

```python
@app.route('/blog/<int:year>/<int:month>/<int:day>/<slug>')
def blog_post(year, month, day, slug):
    # 处理逻辑
    return f"Post from {year}-{month}-{day}: {slug}"
```

This route can match a URL like `/blog/2023/11/13/flask-routing-explained`.

Multi-parameter route definition:

```python
@app.route('/Articles/<path:category>/<title>')
def article_detail(category, title):
    # 处理逻辑
    return f"Category: {category}, Title: {title}"
```

In this example:
- `<path:category>` allows a path containing slashes, which is suitable for multi-level categories.
- `<title>` is a normal string parameter used for the article title.

Using a multi-parameter URL in a template:

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

URLs with a trailing slash (such as `/projects/`): visiting `/projects` -> automatically redirects to `/projects/`

URLs without a trailing slash (such as `/about`): visiting `/about/` -> returns a 404 error

Recommendations:
- If the URL represents a collection or directory, use a trailing slash (such as `/users/`)
- If the URL represents a specific resource or file, do not use a trailing slash (such as `/user/123` or `/about`)

This is like a file system: `/home/user/` is a directory, while `/home/user/file.txt` is a file.

## `url_for()` Function

`url_for()` is the URL generation function provided by Flask. It accepts two types of parameters:
1. The first parameter is the **endpoint** (usually the name of the view function)
2. After that, it can take any number of keyword arguments used to pass variables

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

**Special Parameters**

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

### Best Practice

Always use `url_for()`.

```python
# 不推荐
<a href="/user/john">John's profile</a>

# 推荐
<a href="{{ url_for('profile', username='john') }}">John's profile</a>
```
If the URL rules are modified in the future, you only need to update the route decorator instead of changing every link in all templates.

**Handling Static Files**

```python
# 访问静态文件
url_for('static', filename='style.css')      # 输出: /static/style.css
url_for('static', filename='js/script.js')   # 输出: /static/js/script.js
```

**Using in Templates**

```html
<!-- 在 Jinja2 模板中使用 -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<a href="{{ url_for('profile', username='john') }}">John's Profile</a>
```

## HTTP Methods

Flask can distinguish different HTTP methods for the same path.

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

# Static Folder

`static` is a built-in special endpoint in Flask. Flask registers this endpoint by default to handle static files, so you cannot create a view function named `'static'`, because that would conflict with Flask's built-in static file handling.

## Default Static Folder

You can modify the configuration to change the default static folder.

```python
# 修改静态文件夹和URL路径
app = Flask(__name__,
           static_folder='assets',        # 改变物理文件夹名
           static_url_path='/resources'   # 改变URL路径
)

# 现在可以这样访问静态文件
url_for('static', filename='style.css')  # 输出: /resources/style.css
```

- `static_folder` is the folder name in the **physical file system** where static files are actually stored
- `static_url_path` is the prefix in the **URL path** used to access static files

The purpose of this design is to decouple the physical storage path from the URL path.

```python
app = Flask(__name__,
           static_folder='assets',        # 文件实际存储在 assets/ 目录
           static_url_path='/public'      # URL 以 /public 开头
)
```

File system structure:

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

URL access:

```python
url_for('static', filename='css/style.css')    # 输出: /public/css/style.css
url_for('static', filename='images/logo.png')  # 输出: /public/images/logo.png
```

### Advantage

This design can hide the actual server file structure and is also more flexible.

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

Different environments can use different folders while keeping the same URL structure.

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

## Add a Custom Static Folder

In addition to the default `static` folder for static files, if you want to create another static folder for convenient use with `url_for()`, you can do it like this:

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

Both methods above can add an extra static folder. The core is the `send_from_directory` function, which Flask provides for securely sending files.

It sends files from a specified directory to the client and supports file downloads and static file serving.

```python
send_from_directory(directory, path, **kwargs)
```

- `directory`: the directory path where the file is located
- `path`: the filename to send
- `**kwargs`: other optional parameters (such as `mimetype`, `as_attachment`, etc.)

for example

```python
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('uploads', filename)
```

**Main features**:

- **Security**: automatically handles path traversal attacks and prevents access to files outside the directory
- **Convenience**: automatically handles MIME types
- **Flexibility**: can control whether the file opens directly in the browser or is downloaded as an attachment

**Code example - file download**:

```python
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/download/<filename>')
def download_file(filename):
    # 作为附件下载
    return send_from_directory('uploads', 
                             filename,
                             as_attachment=True)

@app.route('/view/<filename>')
def view_file(filename):
    # 直接在浏览器中查看
    return send_from_directory('uploads', filename)
```

### `@app.route` VS `add_url_rule`

If the static folder needs additional processing logic (such as permission checks, logging, etc.), use the `@app.route` approach; if it only provides file access, use the `add_url_rule` approach.

## Detailed Explanation of `add_url_rule`

```python
app.add_url_rule('/rendered_articles/<path:filename>',
                 endpoint='rendered_articles',
                 view_func=lambda filename: send_from_directory(app.config['RENDERED_ARTICLES_FOLDER'], filename))
```

This code does the following:

- Creates a URL rule to handle all requests beginning with `/rendered_articles/`
- When a URL such as `/rendered_articles/some-file.html` is accessed, it automatically calls the specified `view_func`
- `view_func` uses `send_from_directory` to send the file

### Actual Workflow

In the code, this rule is mainly used in the `article_details.html` template:

```python
@app.route("/Articles/<int:article_id>")
def view_article(article_id):
    # ...
    relative_path = f"{category_path}/{html_filename}"
    # 这个路径最终会通过模板被访问：/rendered_articles/category_path/article_id.html
```

```python
# 当用户访问 /rendered_articles/some-category/123.html 时：

# 1. Flask 匹配 URL 规则
'/rendered_articles/<path:filename>' 匹配这个请求

# 2. 提取 filename 参数
filename = 'some-category/123.html'

# 3. 调用 view_func
send_from_directory(app.config['RENDERED_ARTICLES_FOLDER'], filename)

# 4. 返回文件内容给用户
```

# Render Template

Flask uses the `render_template` function to load HTML files. By default, it looks for template files in the `templates` folder.

How it works: load the specified template file -> inject the passed variable data into the template -> return the rendered HTML string

> [!note]
>
> You can change the default `templates` folder by setting `template_folder`
>
> ```python
> app = Flask(__name__, template_folder='my_templates')
> ```

for example

```
/ project structure
├── app.py
└── templates/
    └── hello.html
```

```python
from flask import render_template
# 路由函数
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', person=name)
```

```html
<!-- hello.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Hello Page</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```

## Jinja2

Flask uses Jinja2 as its template engine by default, so it has some advanced features.

> [!note]
>
> For more details, see [Template Designer Documentation — Jinja Documentation (3.1.x)](https://jinja.palletsprojects.com/en/stable/templates/)

### Delimiters

`{{ }}` - used to output the value of a variable or expression

The variables here are passed in by the `render_template` function.

```html
<p>Hello, {{ username }}</p>
<p>Current time: {{ datetime.now() }}</p>
```

`{% %}` - used for control logic (`if` statements, `for` loops, etc.)

```html
{% if user.is_logged_in %}
    <p>Welcome back!</p>
{% else %}
    <p>Please log in</p>
{% endif %}
```

`{# #}` - used for comments

This kind of comment is removed when the template is rendered, while HTML comments are sent to the browser.

```html
<!-- 这个注释会在页面源代码中可见 -->
<p>Hello World</p>

{# 这个注释在最终的HTML中完全不可见 #}
<p>Hello World</p>
```

### Global Variable

### Template Inheritance

This is one of Jinja2's most powerful features, implemented with the `{% extends %}` and `{% block %}` tags.

```html
<!-- base.html -->
<!doctype html>
<html>
    <head>
        {% block head %}
        
        {% endblock %}
    </head>
    <body>
        {% block body %}
        
        {% endblock %}
    </body>
</html>

<!-- child.html -->
{% extends "base.html" %}
{% block head %}
    <title>My Page</title>
{% endblock %}

{% block body %}
    <h1>Hello World!</h1>
{% endblock %}
```

### Macros

Macros are similar to functions in other programming languages and let you reuse template code.

```html
{# macros.html #}
{% macro input_field(name, label, type="text", value="", required=False) %}
    <div class="form-group">
        <label for="{{ name }}">{{ label }}</label>
        <input type="{{ type }}" 
               name="{{ name }}" 
               id="{{ name }}"
               value="{{ value }}"
               {% if required %}required{% endif %}>
    </div>
{% endmacro %}

{% macro alert(message, type="info") %}
    <div class="alert alert-{{ type }}">
        {{ message }}
    </div>
{% endmacro %}
```

Using macros:

```html
{# form.html #}
{% from "macros.html" import input_field, alert %}

<form method="post">
    {{ input_field("username", "用户名", required=True) }}
    {{ input_field("password", "密码", type="password", required=True) }}
    {{ input_field("email", "邮箱", type="email") }}
    
    {% if error %}
        {{ alert(error, type="danger") }}
    {% endif %}
    
    <button type="submit">提交</button>
</form>
```

### Include

You can use `{% include %}` to include other template files:

```html
{# components/header.html #}
<header>
    <h1>网站标题</h1>
    <nav>...</nav>
</header>

{# components/footer.html #}
<footer>
    <p>版权信息</p>
</footer>

{# page.html #}
<!DOCTYPE html>
<html>
<body>
    {% include 'components/header.html' %}
    
    <main>
        <h2>页面内容</h2>
    </main>
    
    {% include 'components/footer.html' %}
</body>
</html>
```

### Import

You can import an entire template file as a module:

```html
{# forms.html #}
{% macro input(name, type="text") %}
    <input type="{{ type }}" name="{{ name }}">
{% endmacro %}

{% macro textarea(name, rows=5) %}
    <textarea name="{{ name }}" rows="{{ rows }}"></textarea>
{% endmacro %}

{# page.html #}
{% import 'forms.html' as forms %}

<form>
    {{ forms.input('username') }}
    {{ forms.textarea('description') }}
</form>
```

### Context Processors

Register a context processor in Flask to make variables available in all templates:

```python
@app.context_processor
def utility_processor():
    def format_price(amount):
        return f"¥{amount:.2f}"
    
    return dict(
        format_price=format_price,
        current_year=datetime.now().year
    )
```

Use in any template:

```html
<p>Price: {{ format_price(100) }}</p>
<footer>&copy; {{ current_year }}</footer>
```

# Redirects and Errors

next : [Quickstart — Flask Documentation (3.1.x)](https://flask.palletsprojects.com/en/stable/quickstart/#redirects-and-errors)

# Reference

[^flask-config]: Reference document [Configuration Handling — Flask Documentation (3.1.x)
