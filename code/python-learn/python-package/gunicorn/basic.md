# basic

## 为什么会出现这个错误？
你现在的 `app.py` 在导入时执行了：

```python
db.create_all()
```

当你用 **Gunicorn 启动多个 worker**（比如 `-w 2`），发生了这样一件事：

1. Gunicorn 主进程启动  
2. 它创建 **2 个 worker 进程**  
3. **每个 worker 都会加载 `app.py`**  
4. 于是 `db.create_all()` **被同时执行两次**

SQLite 不支持这种并发“建表”，于是第二个 worker 报错：

```
table article_meta_data already exists
```

结果：worker 启动失败 → Gunicorn 整体退出 → Nginx 502

## Gunicorn 命令含义
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

---

## 为什么 `--preload` 能解决？
`--preload` 会让 Gunicorn 在主进程里先加载应用一次，然后再 fork worker。这样 `db.create_all()` 只执行一次，就不会冲突。

## 两个可行修复方案

### 方案 A（推荐）
加 `--preload`：
```
gunicorn -w 2 -b 0.0.0.0:5000 --preload app:app
```
- 仍然有 2 个 worker  
- 只执行一次初始化  
- 改动最小

### 方案 B（更简单）
只用 1 个 worker：
```
gunicorn -w 1 -b 0.0.0.0:5000 app:app
```
- 没有并发  
- 也不会冲突  
- 性能低一点

---

你想让我选 **A** 还是 **B**？