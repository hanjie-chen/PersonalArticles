# rest api

REST API = 一个程序对另一个程序开放的“网址入口”。

平时打开网页，是“人访问网站”。 REST API 则更像是“程序访问网站”。

比如：

- 在浏览器打开 `https://example.com/articles`，看到一个网页
- 另一个程序去访问 `https://example.com/api/articles`，拿到一段数据，通常是 JSON

所以可以先把它想成：网页路由是给人看的，API 路由是给程序调用的。

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
