# css variable

css 变量经常被定义在 `:root` 选择器中，因为 `:root` 对应 HTML 文档的根元素（即 `<html>` 标签），在此定义的变量属于 全局变量，可在整个文档的任何地方访问。

而如果我们将变量定义在特定选择器（如 `.container`）内，则它只在该元素及其后代元素中可用。

e.g.

```css
:root {
  --primary-bg: #1A1C1F; /* 全局变量 */
}
.container {
  --local-color: #60a5fa; /* 该变量仅在 .container 及其子元素内有效 */
}
```

css 变量需要以 `--` 开头，通过 `var()` 函数调用

e.g.

```css
body {
    background-color: var(--primary-bg);
}
```

## varialbe inherit

如果父元素定义了某个 CSS 变量，它的所有子元素将自动继承该变量值，子元素可以直接通过 `var()` 取用

子元素可以重新定义同名变量，覆盖父元素的值，但不影响父元素或其他兄弟元素

什么是父元素和子元素？

```html
<!-- 父元素：<div class="parent"> -->
<!-- 子元素：内部的 <p> 和另一个 <div> -->
<div class="parent">
  <p>这是一个子元素段落</p>
  <div class="child">
    这是嵌套的子元素的子元素（实际上是孙子元素）
  </div>
</div>
```

如果存在深层次的继承关系，变量的优先级：直接父元素的变量 > 祖先元素的变量，即优先查找当前最近父级的变量。