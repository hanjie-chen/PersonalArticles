存在如下的css样式

```css
/* 全局变量定义 */
:root {
    --primary-bg: #1A1C1F;
    --navbar-bg: rgba(28, 30, 34, 0.95);
    --text-primary: #DBDCE2;
    --text-secondary: #9ca3af;
    --accent-color: #3b82f6;
    --hover-color: #60a5fa;
}

body {
    color: var(--text-primary) !important;
    background-color: var(--primary-bg);
    font-family: 'JetBrainsMono', 'PingFangSC', monospace;
}

/* 导航栏样式优化 */
.navbar-custom {
    background-color: var(--navbar-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    height: 6vh;
    transition: all 0.3s ease;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 导航栏链接样式 */
.navbar-custom .navbar-nav .nav-link {
    color: var(--text-primary);
    padding: 0.5rem 1rem;
    position: relative;
    transition: color 0.3s ease;
    font-weight: 500;
}

/* 导航栏链接悬停效果 */
.navbar-custom .navbar-nav .nav-link:hover {
    color: var(--accent-color);
}

/* 导航栏链接激活状态 */
.navbar-custom .navbar-nav .nav-link.active {
    color: var(--accent-color);
}

/* 添加链接下划线动画效果 */
.navbar-custom .navbar-nav .nav-link::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 50%;
    background-color: var(--accent-color);
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

.navbar-custom .navbar-nav .nav-link:hover::after {
    width: 100%;
}

/* 分隔符样式优化 */
.navbar-custom .navbar-nav .nav-link span {
    color: var(--text-secondary);
    opacity: 0.5;
}

/* 主内容区域 */
.main-content {
    height: 88vh;
    padding-top: 6vh; /* 确保内容不会被导航栏遮挡 */
}

/* 页脚样式 */
.footer-custom {
    height: 6vh;
    background-color: var(--navbar-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}
```

# css variable

`:root` 是一个特殊的CSS伪类，它匹配文档的根元素（在HTML中就是`<html>`元素）。我们通常在这里定义全局CSS变量：

```css
:root {
    --primary-color: #3b82f6;    /* 以--开头定义变量 */
    --text-color: #DBDCE2;
    --spacing-unit: 8px;
    --max-width: 1200px;
}
```

通过使用 `var()` 函数来引用这些变量：
```css
.my-element {
    color: var(--text-color);
    margin: var(--spacing-unit);
    /* var()还可以提供后备值（fallback value） */
    background-color: var(--bg-color, #ffffff);  /* 如果--bg-color未定义，将使用#ffffff */
}
```

变量作用域

```css
:root {
    --color: blue;    /* 全局作用域 */
}

.container {
    --color: red;     /* 局部作用域，只在.container及其子元素中生效 */
    background: var(--color);  /* 红色 */
}

.other-element {
    color: var(--color);  /* 蓝色，使用全局变量 */
}
```

修改变量

```css
/* 可以通过媒体查询改变变量值 */
:root {
    --sidebar-width: 300px;
}

@media screen and (max-width: 768px) {
    :root {
        --sidebar-width: 200px;
    }
}
```

**JavaScript交互**

```javascript
// 获取CSS变量值
getComputedStyle(document.documentElement)
    .getPropertyValue('--primary-color');

// 设置CSS变量值
document.documentElement.style
    .setProperty('--primary-color', '#ff0000');
```

实际应用示例 - 主题切换

```css
/* 浅色主题 */
:root {
    --bg-color: #ffffff;
    --text-color: #333333;
}

/* 深色主题 */
:root[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #ffffff;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}
```

