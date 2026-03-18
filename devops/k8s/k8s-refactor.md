# k8s-refactor

如果我们要将一个docker compose 项目重构为k8s 那么我们应该怎么做呢？

首先我们需要在项目根目录下创建一个 k8s/ 目录，类比于在项目根目录下的 compose.yml 是 Docker Compose 的运行方式，k8s/ 是 Kubernetes 的运行方式

也就是说，k8s/ 本质上更像是 compose.yml 的同类物，

接下来我们可以在 k8s/ 目录下继续创建文件夹，类似

```shell
k8s/
└── web-app/
    └── deployment.yaml
```

这些文件夹，是按照组件来进行分类的（大致按 compose.yml 里的 service 来分）

比如目前仓库现在主要有这些组件：

- `web-app`
- `articles-sync`
- `nginx-modsecurity`
- `dozzle`

如果以后继续往 k8s 里迁，目录很自然就可能长成这样：

```text
k8s/
  web-app/
  articles-sync/
  ingress/
  observability/
```

但这里有一个小细节：Kubernetes 里的组件划分，不一定永远 1:1 对应 compose 的 service。

因为到了 k8s 之后，有些东西的抽象层级会变。

举个例子：

- `web-app` 在 Compose 里是一个 service
- 到 k8s 里，它可能对应：
  - `Deployment`
  - `Service`
  - 后面也许还有 `ConfigMap`
  - 甚至 `PersistentVolumeClaim`

也就是说，一个业务组件目录里，往往会放多个 k8s 资源文件。

再比如：
- `nginx-modsecurity` 在 Compose 里是一个 service
- 到 k8s 里，后面可能不会继续保留“单独一个 nginx 容器”的形态
- 你可能会改成 `Ingress`
- 那时它就不一定还叫 `nginx-modsecurity/`，而可能变成 `ingress/`

## deployment.yml

接下来，我们来写第一份文件 `deployment.yaml`

为什么第一份文件它呢？因为如果我们的目标是“先让一个应用在 k8s 里跑起来”，那 `Deployment` 是最核心的起点。

可以这样理解每种资源的职责：

- `Deployment`：负责“跑起来这个应用”
- `Service`：负责“让别人访问到这个应用”
- `ConfigMap/Secret`：负责“给应用提供配置”
- `PVC`：负责“给应用提供持久化存储”
- `Ingress`：负责“把 HTTP/HTTPS 流量从外面引进来”

所以顺序上，最自然的是：

1. 先有应用实例
2. 再谈访问入口
3. 再谈配置、存储、入口优化

而“应用实例”这一层，在 k8s 里最常见的起点就是 `Deployment`。

因为没有 `Deployment`：
- 就没有 Pod 被持续管理
- 就没有应用真正稳定地跑着
- 后面的 `Service` 就算建了，也没有后端可以转发
