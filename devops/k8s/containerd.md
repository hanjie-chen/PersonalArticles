# containerd

containerd 是真正负责运行容器的底层容器运行时。

也就是说：

- Kubernetes 自己不直接运行容器
- 它会把“请启动这个容器”的请求交给容器运行时
- 在你的 k3s 里，这个运行时就是 `containerd`

所以在你的环境里，大致关系可以理解成：

```text
kubectl
  -> Kubernetes API
     -> k3s
        -> containerd
           -> 运行容器
```

4. 为什么这和 Docker 不一样？

因为你本地执行：

```bash
docker build -t website-web-app:k8s-lab ./web-app
```

这个镜像是进了 Docker 自己的镜像存储

但你的 k3s 节点跑 Pod 时，不是用 Docker 当运行时，而是用：`containerd`

所以 Kubernetes 不会自动看到 Docker 那边的镜像。

这就是为什么我们需要做这一步：

- 从 Docker 导出镜像
- 再导入到 `k3s` 使用的 containerd

5. 你现在可以先记住这个够用的版本

- `kubectl`：管 Kubernetes 资源
- `containerd`：真正跑容器的底层运行时
- `k3s ctr`：查看/导入 containerd 里的镜像
- Docker build 出来的镜像，不会自动出现在 k3s 的 containerd 里

6. 后面会不会一直这么麻烦？

本地实验阶段会有这个步骤，因为我们现在是：

- 本地 build
- 本地单节点 k3s
- 不想推远端镜像仓库

以后更接近真实工作流时，常见做法会变成：

- CI 构建镜像
- 推到 GHCR / Docker Hub / 私有仓库
- k8s 直接从镜像仓库拉

那时就不用手动 `ctr images import` 了。

## container runtime

是真正负责把 image 变成 running container 的那层软件。

它通常负责这些事：

- 拉取 image
- 解压 / 准备 root filesystem
- 配置隔离环境
- 创建并启动容器进程
- 监控容器状态
- 停止、删除容器

每个 Node 上都需要一个 container runtime，Pod 才能跑起来。而 kubelet 会通过 CRI（Container Runtime Interface） 去和这个 runtime 通信。

所以在 Kubernetes 里，链路大概是这样的：

你写 Deployment/Pod YAML

 → API Server 收到

 → 调度器把 Pod 分配到某个 Node

 → 这个 Node 上的 kubelet 发现“该我启动了”

 → kubelet 通过 CRI 告诉 container runtime： “去把这个 image 拉下来，然后把 container 跑起来”

 → runtime 真正把容器创建出来。 

也就是说：Kubernetes 负责编排和调度，container runtime 负责实际执行和落地运行容器。

所以不是 Kubernetes 自己直接运行 image，而是 node 上必须有一个容器运行时，帮它把 image 启动成 container。