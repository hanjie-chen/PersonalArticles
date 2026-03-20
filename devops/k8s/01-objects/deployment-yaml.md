# deployment.yaml

开头

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: website-web-app
  namespace: k8s-lab
```

这一小段的意思是：

- `apiVersion: apps/v1`
  - 这份资源属于 Kubernetes 的哪个 API 组
  - `Deployment` 现在通常就是 `apps/v1`

- `kind: Deployment`
  - 这份文件要创建的资源类型
  - 这里明确告诉 k8s：我要的是一个 `Deployment`

- `metadata`
  - 资源自己的基本信息
  - 几乎所有 k8s 资源都会有这一段

- `name: website-web-app`
  - 这个 Deployment 的名字
  - 以后你会用这个名字去 `get`、`describe`、`logs`

- `namespace: k8s-lab`
  - 这份资源属于哪个 namespace
  - 也就是我们前面一直在用的实验空间

---

spec

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: website-web-app
  template:
    metadata:
      labels:
        app: website-web-app
```

这一段是 `Deployment` 最核心的骨架

- `spec` 这里开始写“这个 Deployment 想要的状态”
  
- `replicas: 1`
  - 我希望有 1 个 Pod 在跑
  - 如果 Pod 挂了，Deployment 会想办法再拉一个新的

- `selector.matchLabels`
  - Deployment 用什么规则去认领自己管理的 Pod
  - 这里的规则是：标签里 `app=website-web-app` 的 Pod 属于我

- `template`
  - 这是“Pod 模板”
  - Deployment 不是直接运行容器，它是根据这个模板去创建 Pod

- `template.metadata.labels`
  - 这是它创建出来的 Pod 会带上的标签
  - 这里必须和上面的 `selector.matchLabels` 对得上

需要注意的是

```yaml
selector.matchLabels.app = website-web-app
template.metadata.labels.app = website-web-app
```

这两个值通常要对应上。因为 Deployment 要靠这个标签去找到“这是我创建和管理的 Pod”。

你先把这段加进去。写完以后，我下一步再带你补第三段：真正的容器定义，也就是 `containers:`。

---

很好，我们继续。接下来这一段就是 `Deployment` 里最“像在运行应用”的部分了。

现在你在 [deployment.yaml](/home/plain/personal-project/website/k8s/web-app/deployment.yaml) 下面继续加这一段：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  ...
spec:
  ...
  template:
    metadata:
      ...
    spec:
      containers:
        - name: web-app
          image: website-web-app:k8s-lab
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
```

注意缩进，这一段是接在 metadata 后面的

这段的意思，我们慢慢看：

- `template.spec` 这里开始描述“Pod 具体怎么跑”
  
- `containers` 这个 Pod 里有哪些容器
  - 大多数时候一个 Pod 先只有一个主容器
  
- `- name: web-app` 这个容器的名字，是 Pod 内部的容器名，不是镜像名
  
- `image: website-web-app:k8s-lab`
  - 要运行哪个镜像
  - 这里我们先约定，后面会在树莓派本地构建这个镜像

- `imagePullPolicy: Never`
  - 告诉 k8s：不要去远端仓库拉镜像
  - 只用节点本地已经存在的镜像
  - 这对你现在“本地 k3s 实验”很合适

- `ports.containerPort: 5000`
  - 这个容器内部监听的端口
  - 因为你的 Flask/Gunicorn 是跑在 `5000`

这里还有一个很重要的小点：

`containerPort` 不是“把端口暴露给外部”  更像是在告诉 Kubernetes 和读这个文件的人，这个容器主要服务跑在 5000 端口

真正对外暴露，是后面 `Service` 的事，不是这里负责。

你现在先把这段写进去。写完以后我们先不急着 `apply`，下一步我会带你补环境变量，开始把它和你现在的 Flask 配置对应起来。

---

2 个 spec 的区别：

- 外面的 `spec` 是 Deployment 的 spec
- 里面的 `template.spec` 是 Pod 的 spec

它们不是同一个东西，只是名字都叫 `spec`，可以把 `spec` 理解成一个很朴素的词：spec = specification = 这个资源“希望长成什么样”

Kubernetes 里很多资源都会有自己的 `spec`，因为每种资源都要描述“我想要的目标状态”。

所以现在这个文件其实同时在描述两个层次的资源：

1. `Deployment`
2. `Pod`

因为 `Deployment` 本身不会直接跑容器，它是“用一个 Pod 模板去创建 Pod”。

所以结构才会像这样：

```yaml
kind: Deployment
spec:
  ...
  template:
    metadata:
      ...
    spec:
      containers:
        ...
```

把它翻译成人话就是：

- 我要创建一个 `Deployment`
- 这个 Deployment 的期望状态写在第一个 `spec` 里
- 它会拿 `template` 作为 Pod 模板
- 而这个模板里面，还要继续写“Pod 应该长什么样”
- 所以 Pod 自己也有一个 `spec`

可以把它想象成两层说明书。

第一层说明书：Deployment 这一层，它关心的是：

- 我要几个 Pod
- 我通过什么 label 识别这些 Pod
- 我应该按哪个模板去创建 Pod

对应这部分：

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: website-web-app
  template:
    ...
```

第二层说明书：Pod 这一层，它关心的是：

- Pod 里面跑哪些容器
- 用什么镜像
- 监听什么端口
- 有哪些环境变量、挂载、探针

对应这部分：

```yaml
template:
  spec:
    containers:
      ...
```

所以不是“spec 里无缘无故又套一个 spec”，而是：`Deployment.spec`，里面放了一个，`Pod template`，而这个 `Pod template` 里面当然还需要自己的 `Pod.spec`

你可以把它看成类似这种嵌套关系：

```text
Deployment
└── Deployment.spec
    └── template (Pod template)
        └── Pod.spec
            └── containers
```

如果再更生活化一点类比：

- `Deployment.spec` 像“招聘计划”，我要招人，我要找带某种标签的人，招聘模板长什么样
  
- `template.spec` 像“这个岗位的具体要求”，用什么工具，做什么工作，需要什么环境

所以两个 `spec` 是不同层级上的“配置说明”。

你现在只需要先记住这个非常够用的口诀：

- `spec`：当前这个资源的目标状态
- `Deployment.spec`：描述 Deployment 想怎么管理 Pod
- `template.spec`：描述 Pod 里面到底跑什么

## env

很好，我们继续，而且这一步会开始真正和你这个 Flask 项目接上。

接下来我们先加 **环境变量**，因为你的应用本来就是通过环境变量读配置的。你在 [web-app/config.py](/home/plain/personal-project/website/web-app/config.py) 里已经有这些：

- `SOURCE_ARTICLES_DIRECTORY`
- `RENDERED_ARTICLES_DIRECTORY`
- `SQLALCHEMY_DATABASE_URI`
- `APP_ENV`

所以这一步，本质上就是把 Compose 里“environment:”那种思路，映射到 Kubernetes。

你现在在 `containers:` 下面继续加这一段：

```yaml
          env:
            - name: APP_ENV
              value: production
            - name: SOURCE_ARTICLES_DIRECTORY
              value: /articles/src
            - name: RENDERED_ARTICLES_DIRECTORY
              value: /articles/rendered
            - name: SQLALCHEMY_DATABASE_URI
              value: sqlite:////app/instance/project.db
```

所以这一小段会接在这里后面：

```yaml
      containers:
        - name: web-app
          image: website-web-app:k8s-lab
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
          env:
            ...
```

先解释每个变量为什么这样写。

- `APP_ENV=production`
  - 让应用按生产模式跑
  - 你代码里会据此判断 `IS_DEV`

- `SOURCE_ARTICLES_DIRECTORY=/articles/src`
  - 这是应用预期的 Markdown 源目录
  - 现在先给它一个固定路径，后面再处理真正的数据来源

- `RENDERED_ARTICLES_DIRECTORY=/articles/rendered`
  - 这是渲染后 HTML 的目录
  - 后面我们会考虑挂载问题

- `SQLALCHEMY_DATABASE_URI=sqlite:////app/instance/project.db`
  - 这条最值得注意
  - 我们明确告诉 Flask 用容器里的这个 SQLite 文件
  - 也就是把“数据库文件位置”固定下来

这里你可以顺便感受到一件事：

- Compose 里你写的是 `environment:`
- Kubernetes 里你写的是 `env:`
- 但本质上做的是同一件事：给容器注入环境变量

也就是说，很多 k8s 学习其实不是完全陌生，而是在把你已经会的 Docker/Compose 经验重新映射到另一套模型里。

你先把这一段写进去。  
写完后我们下一步只做一件事：加启动命令，也就是让这个容器知道“启动后到底执行什么”。这一步会直接对应你现在 `web-app` 镜像里的 Gunicorn 启动方式。

## cmd

好，我们继续。这一步是把“容器启动后做什么”写清楚。

在 Compose 里，如果镜像里已经有默认 `CMD`，容器启动时就会按那个默认命令跑。你的 [web-app/Dockerfile](/home/plain/personal-project/website/web-app/Dockerfile) 里默认就是：

- `gunicorn -w 2 -b 0.0.0.0:5000 app:app`

但我们在 k8s 里这第一版想多做一件小事：

- 容器启动时先确保 SQLite 表存在
- 然后再启动 Gunicorn

所以这一步我们要显式写 `command` 和 `args`。

你在容器定义里继续加这一段：

```yaml
          command:
            - /bin/sh
            - -lc
          args:
            - >
              mkdir -p /articles/src /articles/rendered /app/instance &&
              python -c "from app import app; from models import db; ctx = app.app_context(); ctx.push(); db.create_all()" &&
              gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

先别急着背，我先解释它在干什么。

**1. 为什么要有 `command` 和 `args`**
因为我们想覆盖镜像默认启动方式，改成：

- 先执行一点初始化
- 再启动 Web 服务

这里的思路跟 shell 里写启动脚本很像。

**2. `command` 是什么**
```yaml
command:
  - /bin/sh
  - -lc
```

意思是：
- 用 shell 来执行后面的整段命令字符串

你可以把它理解成类似：

```bash
/bin/sh -lc "后面那一大串命令"
```

**3. `args` 是什么**
这里面是一整串启动动作：

```sh
mkdir -p /articles/src /articles/rendered /app/instance &&
python -c "..." &&
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

分三步：

- `mkdir -p ...`
  - 先把应用依赖的目录建出来
  - 不然后面 SQLite 路径或文章目录可能不存在

- `python -c "... db.create_all()"`
  - 先把数据库表建出来
  - 这是为了让 `/articles` 这类路由不至于因为缺表直接炸掉

- `gunicorn ...`
  - 最后真正启动 Flask 应用

这一步的目标不是“完美生产方案”，而是：
- 先让 `web-app` 在 k8s 里独立跑起来
- 先不依赖 `articles-sync`
- 先不依赖完整初始化链路

所以这是一个**学习阶段的最小启动方式**。

你也可以先把这一步理解成：
- Compose 里有默认启动命令
- Kubernetes 里我们现在手动接管了启动命令
- 这样我们可以在启动前插一段初始化逻辑

你先把这段写进 [deployment.yaml](/home/plain/personal-project/website/k8s/web-app/deployment.yaml)。

写完之后，下一步我们再补一小段：
- `readinessProbe`
- `livenessProbe`

也就是 Kubernetes 怎么判断这个 Web 应用“活着没”“准备好没”。这一步会非常贴近真实场景。

## healthe check

很好，我们继续。现在开始加 Kubernetes 里很重要的一块：**探针**。

这一步的作用是让 Kubernetes 知道两件事：

- 这个容器是不是还活着
- 这个容器是不是已经准备好接收流量

对应两个概念：

- `livenessProbe`
- `readinessProbe`

你可以先这样理解：

- `livenessProbe`
  - 像“还活着吗？”
  - 如果失败很多次，Kubernetes 会重启容器

- `readinessProbe`
  - 像“已经准备好接流量了吗？”
  - 如果还没准备好，Service 不会把请求转给它

这两个很适合 Web 应用，也很值得你现在就学。

你现在在容器定义里继续加这一段：

```yaml
          readinessProbe:
            httpGet:
              path: /
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 5000
            initialDelaySeconds: 15
            periodSeconds: 10
```

这一段的意思：

**`readinessProbe`**
- 用 HTTP GET 请求 `http://容器IP:5000/`
- 如果这个请求成功，说明应用已经可以接流量
- `initialDelaySeconds: 5`
  - 容器启动后先等 5 秒再检查
- `periodSeconds: 5`
  - 每 5 秒检查一次

**`livenessProbe`**
- 也是请求 `/`
- 但它回答的是“这个进程现在还健康吗”
- `initialDelaySeconds: 15`
  - 给应用更长一点启动时间
- `periodSeconds: 10`
  - 每 10 秒检查一次

为什么这里我们先用 `/`：
- 你的 Flask 根路由是存在的
- 比较简单
- 作为第一版探针路径够用了

后面如果你想更规范，我们可以专门加一个 `/healthz` 路由给 k8s 用，但现在先不用把事情搞复杂。

这一步你顺便可以理解一个很现实的区别：

- 应用“启动了”不等于“可以接流量”
- Kubernetes 需要靠探针来判断这个状态

这也是为什么 k8s 比单纯 `docker run` 更像一个编排系统，它不只是把进程拉起来，还会持续观察它的状态。

你先把这段加进去。  
写完后，我们就只差最后一小块 Deployment 内容了：

- `volumeMounts`
- `volumes`

也就是把 `/articles/src`、`/articles/rendered`、`/app/instance` 这些目录在 Pod 里准备好。然后这第一版 `deployment.yaml` 就完整了。

## volume

好，我们把这份 `Deployment` 的最后一块补上。

这一步是 **volumeMounts / volumes**，也就是给容器准备目录。  
你现在这个 Flask 应用运行时会依赖这些路径：

- `/articles/src`
- `/articles/rendered`
- `/app/instance`

所以我们先给它们最简单的挂载方式：`emptyDir`。

你可以把 `emptyDir` 暂时理解成：

- Pod 启动时，给这个 Pod 一块临时目录
- Pod 删除后，数据就没了
- 适合学习阶段和临时实验
- 不适合真正持久化 SQLite 或文章数据

这正适合你现在的节奏：先跑起来，再谈持久化。

你先在容器里加这一段，接在 `livenessProbe` 后面：

```yaml
          volumeMounts:
            - name: articles-src
              mountPath: /articles/src
            - name: rendered-articles
              mountPath: /articles/rendered
            - name: webapp-instance
              mountPath: /app/instance
```

这段意思是：

- 把一个叫 `articles-src` 的 volume 挂到 `/articles/src`
- 把一个叫 `rendered-articles` 的 volume 挂到 `/articles/rendered`
- 把一个叫 `webapp-instance` 的 volume 挂到 `/app/instance`

注意这里还只是“挂载声明”，真正这个 volume 是什么，还要在 Pod spec 里定义。

所以接着在 **容器定义结束之后**，也就是和 `containers:` 同级的位置，加这一段：

```yaml
      volumes:
        - name: articles-src
          emptyDir: {}
        - name: rendered-articles
          emptyDir: {}
        - name: webapp-instance
          emptyDir: {}
```

这里要特别注意缩进：

- `volumes:` 是 `template.spec` 下面的
- 它和 `containers:` 是同级
- 不是写在容器内部

你可以把关系理解成：

- `volumeMounts`：容器这边说“我要把哪些卷挂到哪些路径”
- `volumes`：Pod 这边说“这些卷本体是什么”

也就是说：

```text
Pod 先定义 volumes
Container 再把 volumes mount 进去
```

这和 Docker 里的“定义 volume 然后挂到容器路径”其实很像，只是 Kubernetes 拆成了两个层次。

如果都写完了，你这份第一版 [deployment.yaml](/home/plain/personal-project/website/k8s/web-app/deployment.yaml) 就完整了。

然后下一步我们不会立刻跳很多内容，只做两件事：

1. 我帮你一起从头检查这份 YAML 的整体结构
2. 然后再写第二个文件：`k8s/web-app/service.yaml`

也就是说，我们马上就能进入“让它能被访问”的那一步了。