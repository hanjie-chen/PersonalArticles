# env file

`.env` 文件是现代软件工程（不仅仅是 Python）中的“标配”。

在 Docker Compose 的上下文中，`.env` 文件扮演着“变量仓库”的角色。

---

### 1. `.env` 文件是什么？

简单来说，它就是一个纯文本文件，里面全是键值对 (Key-Value Pairs)。它的格式非常简单，通常长这样：

```bash
# .env 文件内容示例
POSTGRES_PASSWORD=mysecretpassword
PORT=8080
APP_ENV=production
API_KEY=abcdef123456
```

为什么叫 `.env`？

*   `.` 开头：在 Linux/Unix 系统中表示这是个隐藏文件。
*   `env`：代表 Environment (环境变量)。

---

### 2. 为什么要用它？（三大理由）

不管是写 Python、Node.js、Go 还是用 Docker，使用 `.env` 的核心逻辑是一样的：把“配置”和“代码”分离。

#### **理由 A：安全性 (Security)**
想象一下，如果你的数据库密码直接写在 `docker-compose.yml` 或者代码里：
*   当你把代码上传到 GitHub 时，全世界都能看到你的密码。
*   **做法：** 密码写在 `.env` 里，然后告诉 Git **忽略**这个文件（通过 `.gitignore`）。这样，你的代码库里只有逻辑，没有秘密。

#### **理由 B：灵活性 (Flexibility)**
*   **开发环境**：你用的数据库地址是 `localhost`。
*   **生产环境**：你用的数据库地址是 `db.production.com`。
*   **做法：** 代码不用改，只需要在不同环境放一个不同的 `.env` 文件，程序启动时读取里面的值即可。

#### **理由 C：统一管理**
*   当你需要修改端口号时，不需要去翻几十个代码文件，只需要改 `.env` 里的一行。

---

### 3. Docker Compose 如何使用 `.env`？

Docker Compose 对 `.env` 有原生支持，不需要安装额外插件。它主要有两种用法：

#### **用法一：填空题（变量替换）**

这是最常用的功能。Docker Compose 在读取 `compose.yml` 之前，会自动先读同级目录下的 `.env` 文件，把里面的值填进去。

**1. 准备 `.env` 文件：**
```bash
TAG=v1.0
DB_PASS=123456
```

**2. 编写 `compose.yml` (使用 `${变量名}` 占位)：**
```yaml
services:
  web:
    image: my-app:${TAG}  # 这里会被替换成 v1.0
    environment:
      - PASSWORD=${DB_PASS} # 这里会被替换成 123456
```

**3. 执行命令：**
当你运行 `docker compose up` 时，Docker 实际执行的是 `image: my-app:v1.0` 和密码 `123456`。

#### **用法二：直接把整个文件塞给容器**

有时候你的程序（比如一个 Python Flask 应用）需要读取几十个环境变量。你不想在 `compose.yml` 里一行一行写 `environment:`。

你可以直接用 `env_file` 指令：

```yaml
services:
  web:
    image: my-app
    # 这一行告诉 Docker：把 .env 里的所有变量都注入到这个容器里去！
    env_file:
      - .env
```

这样，你的 Python 代码中就可以直接通过 `os.getenv('SOME_VAR')` 读到 `.env` 里的值了。

---

### 4. 工程中的“潜规则” (Best Practices)

既然你提到了工程化，这里有两个非常重要的“行规”：

#### **规则 1：绝对不要提交 `.env` 到 Git**
`.env` 里通常包含密码、API Key。如果提交上去，就相当于把家门钥匙挂在门把手上。
**操作：** 在 `.gitignore` 文件中添加一行：
```
.env
```

#### **规则 2：提供一个模版 (`.env.example` 或 `.env.template`)**
既然不提交 `.env`，新来的同事怎么知道需要配置哪些变量呢？
你会提交一个**不包含真实密码**的模版文件，比如 `.env.example`：

```bash
# .env.example (这个文件要提交到 Git)
POSTGRES_PASSWORD=   # 留空，让同事自己填
PORT=8080            # 给个默认值
API_KEY=             # 留空
```
新同事拉取代码后，只需复制一份改名为 `.env` 填上自己的密码即可。

### 总结

*   `.env` 是**“配置中心”**。
*   **Docker Compose 会自动读取它**。
*   它让你的 `compose.yml` 变成了**“完形填空”**，不同的环境填不同的词。
*   **切记：** 真实密码放 `.env`，且不要上传 Git；模版放 `.env.example`，上传 Git。