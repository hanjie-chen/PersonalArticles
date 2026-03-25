# rest api

REST API = 一个程序对另一个程序开放的“网址入口”。

平时打开网页，是“人访问网站”。 REST API 则更像是“程序访问网站”。

比如：

- 在浏览器打开 `https://example.com/articles`，看到一个网页
- 另一个程序去访问 `https://example.com/api/articles`，拿到一段数据，通常是 JSON

所以可以先把它想成：网页路由是给人看的，API 路由是给程序调用的。

再放到你项目里看

你现在项目里的这些路由：

- [app.py](/home/plain/personal-project/website/web-app/app.py#L95) 的 `/`
- [app.py](/home/plain/personal-project/website/web-app/app.py#L101) 的 `/articles`
- [app.py](/home/plain/personal-project/website/web-app/app.py#L133) 的 `/articles/<int:article_id>`

这些主要是返回 HTML 页面给人看的。

而这个：

- [app.py](/home/plain/personal-project/website/web-app/app.py#L198) 的 `/internal/reindex`

它更像 API，因为它不是让你打开看页面的，而是让别的程序调用的。调用成功后，它返回的是：

- `{"status": "ok"}`

这就是很典型的 API 风格。

---

REST API 到底“REST”在哪里？

你现在先不用死记“REST”定义。 先记住它常见的样子就够了：

- `GET /api/articles`：获取文章列表
- `GET /api/articles/1`：获取一篇文章
- `POST /api/articles`：新建一篇文章
- `DELETE /api/articles/1`：删除一篇文章

这里最重要的是两件事：

- URL 表示你要操作什么东西
- HTTP 方法表示你要做什么动作

最常见的方法：

- `GET`：读取
- `POST`：新建 / 触发动作
- `PUT` / `PATCH`：修改
- `DELETE`：删除

---

**你现在项目里已经有的最简单例子**

在你的项目里，`articles-sync` 会去调用这个接口：

意思就是：

1. `articles-sync` 这个程序发现文章变了
2. 它发一个 HTTP 请求给 `web-app`
3. `web-app` 收到后重新导入文章
4. 然后返回 `{"status": "ok"}`

这就是：

一个程序通过 URL 调另一个程序做事,这就是 API 最核心的感觉。

你现在不用急着学复杂的，先学这 3 件事就够了

---

**如果你想靠这个项目入门，我建议只走这一步**

先不要做 CRUD，不要做前后端分离。 先只做一个最简单的新接口，比如：`GET /api/hello`

返回：

```python
{"message": "hello"}
```

然后你就会第一次真正明白：

- 什么是 API 路由
- 什么是 JSON 返回
- 什么是 `GET`

这一步非常重要，而且完全不复杂。

---

**最适合你的学习顺序**

1. 先理解你现有的 `/internal/reindex`
2. 再自己加一个最简单的 `GET /api/hello`
3. 然后再做 `GET /api/articles`
4. 最后才去碰更复杂的东西

这样不会晕。

如果你愿意，下一条我可以**不讲理论**，直接带你做第一步：  
在你的 [app.py](/home/plain/personal-project/website/web-app/app.py) 里加一个最简单的 `GET /api/hello`，我会一句一句解释，保证从零开始。