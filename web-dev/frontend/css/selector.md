# 嵌套选择器

grammer

```css
.codehilite .k {color: #7F848E}
```

这种写法属于 CSS 的嵌套选择器语法，它的核心规则是：“选择同时满足两个条件的元素”。这里的两个点号 `.` 分隔的选择器代表的是层级关系

具体来说是选择所有类名为 `k` 的元素，但这些元素必须位于某个类名为 `codehilite` 的父元素内部，类似于下面的html代码

```html
<div class="codehilite">
  <span class="k">内部的Keyword（需高亮）</span>
</div>

<span class="k">外部的Keyword（不应高亮）</span>
```

可以多重嵌套，比如说 `.parent .children .grandchild` 

# 交集选择器

grammer

```css
span.linenos.special {background-color: #ffffc0}
```

这种写法是交集选择器（要求同一元素同时满足多条件），在上面的例子中，它选择所有同时满足 **`<span>` 标签**、**类名为 `linenos`** 且 **类名为 `special`** 的元素。

它会匹配类似于下面的 html

```html
<span class="linenos special">我是目标元素</span> 
```



# 嵌套&交际选择器

可以同时使用2中选择器，例如

```css
td.linenos .special {background-color: #ffffc0}
```

会匹配类似于下面的 html

```html
<td class="linenos"> <!-- 父元素 -->
  <span class="special">直接子元素</span> 
</td>

<td class="linenos">
  <div>
    <p class="special">孙子元素或更深层</p> 
  </div>
</td>
```

