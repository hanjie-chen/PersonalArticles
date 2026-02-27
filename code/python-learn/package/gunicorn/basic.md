# basic

当我们的 flask app 开发的差不多，打算上线的时候，就需要考虑使用到生产级别的 WSGI HTTP Server

所谓 WSGI 就是 Web Server Gateway Interface

## flask run VS. Gunicorn

`flask run` 使用的是 Werkzeug 提供的开发服务器，它的设计初衷仅仅是为了测试代码是否跑得通，而 `gunicorn` 可以进程管理，负载均衡等操作

#### 并发能力 (Concurrency)

- Werkzeug： 默认情况下单进程的。如果有一个请求处理得很慢（比如上传大文件、请求外部 API），整个服务器就会卡住，其他人的请求都进不来。
- Gunicorn： 它是预分叉 (Pre-fork) 模式。启动时，它会由一个主进程（Master）生出多个工作进程（Workers）。如果有 4 个 Worker，你就可以同时处理 4 个请求。即使一个 Worker 堵塞了，其他 Worker 依然可以响应其他用户。

#### 稳定性与健壮性

- Flask 自带服务器： 遇到严重错误可能会导致进程直接退出，服务就挂了。
- Gunicorn： 主进程会监控所有 Worker。如果某个 Worker 因为内存泄漏或者代码 Bug 挂掉了，主进程会在几毫秒内自动重启一个新的 Worker。这对生产环境的“高可用性”至关重要。

#### 安全性

- Flask 自带服务器： 没有经过严格的安全审计，很容易受到 DDoS 攻击或缓慢攻击（Slowloris）。
- Gunicorn： 经过了长期的生产环境验证，对网络攻击有一定的防御能力，并且处理 HTTP 请求头更规范、更安全。

在真正的生产环境中，架构通常是这样的：

> Nginx (反向代理) -> Gunicorn (应用服务器) -> Flask (应用逻辑)

有了 Gunicorn 为什么还要 Nginx？

- Nginx (前台接待)： 擅长处理静态文件（图片、CSS、JS），处理 SSL（HTTPS），以及抗住海量的并发连接。它把筛选过的动态请求转发给 Gunicorn。
- Gunicorn (餐厅经理)： 接收 Nginx 转过来的动态请求，分配给 Worker。
- Flask (厨师)： 执行 Python 代码，返回结果。

## Gunicorn 使用
当前我们用的是：

```
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

解释：

- `gunicorn`：启动 WSGI 服务器  
- `-w 2`：启动 2 个 worker 进程（并发处理请求）  
- `-b 0.0.0.0:5000`：绑定到 5000 端口，对外可访问  
- `app:app`：  
  - 第一个 `app` = 文件名 `app.py`  
  - 第二个 `app` = 文件里的 Flask 实例 `app = Flask(__name__)`
