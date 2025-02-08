# 导航栏 navigation bar

for example

```html
<!-- Navbar -->
<nav class="navbar navbar-expand-sm navbar-custom fixed-top">
    <div class="container">
        <!-- put my personal website logo here -->
        <!-- <a class="navbar-brand" href="{{ url_for('index')}}">
            <img alt="头像" class="rounded" style="width:4vw;" src="{{ url_for('static', filename='images/headavatar/head_avatar_problem.png') }}">
            </a> -->
        <span>
            Welcome to my personal website
        </span>
        <div class="collapse navbar-collapse" id="mynavbar">
            <ul class="navbar-nav ms-auto">
                <!-- 文章页面就可以包含分类和标签了 不用另外起一个页面 -->
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('article_index') }}" class="text-decoration-none">
                        Articles
                    </a>
                </li>
                <li class="nav-item">
                    <span class="nav-link">|</span>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('about_me') }}">
                        About Me
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

代码解释：

- `<nav class="navbar navbar-expand-sm navbar-custom fixed-top">`: 

  使用 Bootstrap 的 `navbar` 类创建一个响应式导航栏，`fixed-top` 类固定在页面顶部，其中`navbar-custom` 是我自定的css格式用于设置其高度和一些其他特性

- `<div class="container">`: 使用 Bootstrap 的 `container` 类，确保导航栏中的内容居中对齐。

- `<div class="collapse navbar-collapse" id="mynavbar">`: 包含导航链接的容器，响应式时可以折叠。

- `<ul class="navbar-nav ms-auto">`: 使用 Bootstrap 的 `navbar-nav` 类创建导航链接列表，`ms-auto` 类将其右对齐。

- `<li class="nav-item">`: 每个导航项。

- `<a class="nav-link" href="{{ url_for('index') }}">`: 导航链接，使用 `nav-link` 类。



主内容 Main Content

- `<div class="main-content container-fluid flex-grow-1 d-flex align-items-center justify-content-center">`: 使用 Bootstrap 的 `container-fluid` 类创建一个全宽容器，`flex-grow-1` 类使其占据剩余空间，`d-flex` 类将其设置为弹性盒子，`align-items-center` 和 `justify-content-center` 类使内容居中对齐。
- `<div class="content-wrapper">`: 包含主内容的容器。
- `<div class="container text-center mb-4">`: 使用 Bootstrap 的 `container` 类和 `text-center` 类，使内容居中对齐，`mb-4` 类增加底部外边距。
- `<img alt="avatar" class="rounded" style="width: 8vw;" src="{{ url_for('static', filename='images/headavatar/head_avatar_problem.png') }}">`: 显示头像图片，使用 `rounded` 类使其圆角，`style` 属性设置宽度为 8vw。
- `<div class="content">`: 包含文本内容的容器。
- `<h5 class="mb-3">`: 使用 Bootstrap 的 `h5` 类创建标题，`mb-3` 类增加底部外边距。



页脚Footer

- `<footer class="footer-custom py-3 ">`: 使用自定义类 `footer-custom` 创建页脚，`py-3` 类增加上下内边距。
- `<div class="container text-center">`: 使用 Bootstrap 的 `container` 类和 `text-center` 类，使内容居中对齐。
- `<span>© 2024 for Plain Personal Website</span>`: 显示版权信息。