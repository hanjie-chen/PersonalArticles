# basic

Docker Compose：它主要管理一台机器上的多个容器。如果你在 `docker-compose.yml` 里定义了 5 个服务，它们全都跑在同一台服务器上。如果这台服务器宕机了，你的服务就全没了。

Kubernetes：它管理的是一堆服务器（集群）。K8S 把成百上千台机器的资源（CPU、内存）池化，你只需要告诉它：“我要运行这个镜像的 3 个副本”，它会自动挑选最空闲的机器把容器扔进去。

> 为什么叫 K8s？因为 K 和 s 之间刚好有 8 个字母（u-b-e-r-n-e-t-e）通常读作 “K-Eights”（K-诶茨）。

为了成本考虑（树莓派 8GB Mem），使用 k3s 代替 k8s 来进行实验，因为它的使用方法和 k8s 完全一样，但是轻量化了很多（吃的资源比 k8s 少多了）

## downlaod

安装 k3s

```shell
curl -sfL https://get.k3s.io | sh -
```

这条命令做的事很简单：

- 下载并安装 k3s
- 把它注册成系统服务
- 顺带安装 kubectl 等工具
- 生成 kubeconfig：/etc/rancher/k3s/k3s.yaml

完成之后检测

```
sudo systemctl status k3s
```

接下来查看服务器状态

```
$ sudo kubectl get nodes
NAME        STATUS   ROLES           AGE   VERSION
berrynode   Ready    control-plane   67s   v1.34.5+k3s1
```

这个命令是用来查看集群里有多少台机器（节点）。

- NAME: 机器名。
- STATUS: 最关键的指标。Ready 表示这台机器健康，可以接收并运行程序。
- ROLES: `control-plane` 是“大脑”，负责管理整个集群。在 K3s 默认安装下，你的机器既是管理中心也是干活的工人。
- VERSION (v1.34.5+k3s1): 你安装的 K3s 具体版本号。

查看“程序”运行情况

```shell
$ sudo kubectl get pods -A
NAMESPACE     NAME                                      READY   STATUS      RESTARTS   AGE
kube-system   coredns-695cbbfcb9-jtp4h                  1/1     Running     0          53m
kube-system   helm-install-traefik-crd-x6cdb            0/1     Completed   0          53m
kube-system   helm-install-traefik-xsqrj                0/1     Completed   2          53m
kube-system   local-path-provisioner-546dfc6456-dlsvb   1/1     Running     0          53m
kube-system   metrics-server-c8774f4f4-pjmn5            1/1     Running     0          53m
kube-system   svclb-traefik-0b082ecb-lwjsj              2/2     Running     0          51m
kube-system   traefik-788bc4688c-bhrkr                  1/1     Running     0          51m
```

Pod 是 K8s 中运行程序的最小单位。`-A` 表示查看所有命名空间（Namespace）下的 Pod。

K3s 虽然“轻量”，但它内置了一些基础服务来保证集群正常工作。输出中这些 Pod 都在 `kube-system` 命名空间下，它们是 K3s 的“内脏”：

- coredns: 负责集群内部的域名解析（比如让 A 程序能通过名字找到 B 程序）。
- helm-install-traefik: 这是 K3s 自动帮你安装 Traefik（网关/负载均衡）的任务。
- local-path-provisioner: 负责管理本地存储（让你能存数据）。
- metrics-server: 监控组件，负责统计 CPU 和内存使用量。

状态解释 (STATUS)

- Running: 已经启动成功，正常运行（如你的 `metrics-server`）。
- ContainerCreating: 正在创建中。这通常是因为 K3s 正在从网上下载镜像。

## 配置 kubctl 命令给 user

和 docker 一样，为了每次不要使用 sudo 才能使用这个命令，先把 kubeconfig 拷到你的普通用户目录：

```shell
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown plain:plain ~/.kube/config
chmod 600 ~/.kube/config
```

然后显式告诉它用自己的 kubeconfig。

```
echo 'export KUBECONFIG=$HOME/.kube/config' >> ~/.bashrc
source ~/.bashrc
```

这是因为 k3s 安装出来的 kubectl 实际上是一个指向 k3s 的 symlink，它默认还是去读 /etc/rancher/k3s/k3s.yaml。

```shell
$ ls -l /usr/local/bin/kubectl
lrwxrwxrwx 1 root root 3 Mar  9 17:14 /usr/local/bin/kubectl -> k3s
```

# `kubectl` command

简单来说，可以把 `kubectl` 理解为集群的万能管家：

- 看状态：程序死了没？服务器累不累？
- 下命令：给我再开 3 个网页副本！
- 修错误：把那个坏掉的 Pod 重启一下。
- 进系统：像 `ssh` 一样直接进入容器内部执行命令。

> [!tip]
>
> 为什么 `kubectl` 命令叫做 `kubectl` 呢？
>
> - `kube` 取自 Kubernetes 的前四个字母。
> - `ctl` 是 Control（控制）的缩写。在 Linux 和 Unix 的世界里，这是一种约定俗成的命名传统。
>
> 如果你常用 Linux，你会发现很多核心工具都长这样：
>
> - **`systemctl`**: 控制系统服务（System Control）。
> - **`journalctl`**: 控制/查看系统日志（Journal Control）。
>
> 所以，`kubectl` 合起来的意思就是：“Kubernetes 控制器”。

## 它的本质是什么？

`kubectl` 是一个命令行工具（CLI）。虽然你是在 K3s 所在的服务器上运行它，但它本质上是一个“客户端”。

- Server (服务端)：是 K3s 的 API Server。它像是一个 7x24 小时值班的“办事大厅”窗口。
- Client (客户端)：是 `kubectl` 工具。它像是一个跑腿的，拿着你的诉求去窗口办事。

在实际的生产环境中，K8s 集群可能有几百台机器。通常不会登录到那些服务器上去操作，而是在你自己的笔记本电脑上装一个 `kubectl`，然后通过网络远程操控远在云端的集群。

当你输入一个命令（比如 `kubectl get nodes`）时，发生了以下过程：

1. 转化请求：它把你的人类语言转化成一个 API 请求。
2. 发送请求：它通过网络发送给集群的“大脑”（即 API Server）。
3. 身份验证：它会携带一个名为 `kubeconfig` 的证书文件（通常在 `/etc/rancher/k3s/k3s.yaml`），证明它有权下达指令。
4. 获取结果：API Server 查完数据库（etcd）后告诉它结果，它再把结果格式化打印在你的屏幕上。

## 命令的结构

kubectl 命令都遵循这个公式：`kubectl [动作] [资源类型] [资源名称] [参数]`

动作：你想干什么？

- `get`: 列出/查看。
- `describe`: 查看详细“体检报告”。
- `logs`: 查看程序打印的日志（报错排查神技）。
- `apply`: 根据文件内容创建或更新。
- `delete`: 删除。

资源类型：你想操作谁？

- `nodes`: 服务器节点。
- `pods`: 运行中的程序容器。
- `services`: 网络服务/地址。
- `deployments`: 管理程序的“蓝图”。

参数：额外的要求。

- `-A`: 所有命名空间。
- `-n kube-system`: 只看 `kube-system` 这个“文件夹”里的东西。
- `-o yaml`: 以完整的 YAML 格式输出结果。

## create namespace

创建一个单独的 namespace

```shell
kubectl create namespace k8s-lab
```

这个命令可以拆解为：

- **`kubectl`**: 客户端（遥控器）。
- **`create`**: 动作（我要创建一个新东西）。
- **`namespace`**: 资源类型（我要创建的东西叫“命名空间”）。
- **`k8s-lab`**: 资源名称（这个地盘的名字叫 `k8s-lab`）。

### 1. 什么是 Namespace？

可以把 Kubernetes 集群想象成一栋巨大的办公楼。

- 集群 (Cluster)：整栋大楼。
- 命名空间 (Namespace)：大楼里的独立办公室。

当你执行 `kubectl create namespace k8s-lab` 时，你就在大楼里挂上了一个“k8s-lab”的门牌号。

为什么要分办公室？

1. 隔离性：你在 `k8s-lab` 办公室里折腾（删除、修改），不会影响到旁边 `kube-system` 办公室里的核心组件。
2. 整洁性：如果你把所有的 Pod 都堆在一起，`kubectl get pods` 出来的列表会长得让你绝望。分了空间后，你可以只看某个空间里的东西。
3. 权限控制：以后你可以规定“张三只能进入 `k8s-lab` 办公室，不能进入核心机房 `kube-system`”。

### 2. 执行完会发生什么？

当你敲下回车，`kubectl` 会告诉 API Server：“老板，开个新房间，名字叫 k8s-lab。”

可以通过这个命令看到成果：

```shell
sudo kubectl get ns
```

(注：`ns` 是 `namespace` 的缩写，kubectl 懂这种偷懒的写法)

你应该会看到：

- default: 默认办公室（你不指定时，东西都扔这）。
- kube-system: 核心机房（K3s 自己的组件在那）。
- k8s-lab: 你刚刚亲手开辟的实验室。

### 3. 如何使用这个“新房间”？

创建完之后，它现在是空的。如果你想在这个实验室里跑程序，你需要在命令后面加一个 `-n`（namespace 的缩写）参数。

比如，你想看看你的实验室里有没有东西：

```shell
sudo kubectl get pods -n k8s-lab
```

你会得到 `No resources found in k8s-lab namespace.`，因为你还没往里搬家具呢。

> [!note]
>
> 如果不加 `-n`，所有的命令默认都是在操作 `default` 空间。
>
> 新手容易遇到这样的情况：
>
> 1. 在 `k8s-lab` 里创建了一个程序。输入 `kubectl get pods` 发现啥也没有，急得满头大汗。
> 2. 其实程序在那跑得好好的，只是他在 `default` 办公室里找 `k8s-lab` 的人。

## create deployment

使用下面的命令创建一个 deployment

```shell
kubectl -n k8s-lab create deployment demo-nginx --image=nginx:stable
```

命令详解

- `-n k8s-lab`: 指定 namespace。告诉遥控器：“去 `k8s-lab` 房间操作”

- `create deployment`: 动作 + 资源类型。

  创建一个 Deployment（部署），而它像一个“监工”。你告诉它“我要运行 Nginx”，它负责帮你盯着。如果 Nginx 意外挂了，监工会自动再启动一个。

- `demo-nginx`: 这个部署的名字。

- `--image=nginx:stable`: 告诉 K3s 去哪里拉货。

  - `image`（镜像）就像是装好系统的“光盘”或“U盘”。
  - `nginx:stable` 指的是从官方仓库下载“稳定版”的 Nginx。

### 执行后发生了什么？

当你按下回车，集群内部会发生一连串连锁反应：

1. 登记造册：API Server 把你的要求记在数据库里。
2. 分派任务：调度器（Scheduler）看了一眼你的服务器（berrynode），发现它挺闲的，就把任务派给了它。
3. 下载镜像：你的机器发现本地没有 `nginx:stable` 这张“光盘”，于是开始从 Docker Hub 联网下载（Pulling）。
4. 启动容器：下载完成后，K3s 启动容器，并把它封装在一个 Pod 里。

### 验证结果

执行完命令后，运行下面两个命令来“监工”：

查看部署进度

```shell
$ kubectl get deployment -n k8s-lab
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
demo-nginx   1/1     1            1           2m1s
```

你会看到 `READY 0/1` 变成 `1/1`。

查看真正的干活仔（Pod）

```shell
$ kubectl get pods -n k8s-lab
NAME                         READY   STATUS    RESTARTS   AGE
demo-nginx-99b6475d5-t8mrl   1/1     Running   0          113s
```

你会发现多了一个名字叫 `demo-nginx-xxxxxx` 的 Pod。那个后缀随机字符是 Deployment 自动生成的。

### 为什么不直接创建 Pod？

你可能会问：“我只想跑个 Nginx，为什么要搞个 Deployment 这么复杂的词？”

这里先记住一个核心关系：

- Pod 是真正运行容器的最小单位
- Deployment 不是容器本身，它是“管理 Pod 的控制器”

这就是 Kubernetes 的聪明之处：

- 如果你直接 `create pod`，那个 Pod 就像个临时工，死了就死了。
- 如果你 `create deployment`，它就是个正式工。如果你手动删掉那个 Pod，Deployment 会惊呼“哎呀，少了一个人！”，然后瞬间秒出一个一模一样的新 Pod。

这就是所谓的“声明式管理”：你只管说“我要 1 个 Nginx”，至于怎么维持这个状态，那是 K8s 的事。从“手动操作员”变成了“项目经理”。不再关心具体的容器怎么启动，只下达了一个“部署 Nginx”的长期指令。

## expose service

使用这个命令来创建 service

```shell
kubectl -n k8s-lab expose deployment demo-nginx --port=80 --target-port=80 --type=ClusterIP
```

命令拆解

- `expose deployment demo-nginx`: 意思是对外声明：“我要让大家能找到 `demo-nginx` 这个部署出来的程序。”
- `--port=80`: 这是 Service 的端口。也就是这根“内部电话线”的号码。
- `--target-port=80`: 这是 Pod 的端口。也就是 Nginx 程序本身监听的端口。通常两者设为一样。
- `--type=ClusterIP`: 这是服务类型。`ClusterIP` 是默认选项，意思是：“只在集群内部可见”。
  - 就像公司内部的短号，外面的人打不进来，但大楼里其他办公室（Namespace）的人可以拨这个号找到你。

在 Kubernetes 中，Pod（也就是运行 Nginx 的容器）是“短命”的。如果它重启了，IP 地址就会变。你不能指望通过一个随时会变的 IP 去访问服务。于是，Service（服务） 诞生了。

kubectl expose 命令创建了一个名为 Service 的抽象层。它像是一个固定的接线员，无论后面的 Pod 怎么变、怎么死、怎么换 IP，只要找这个接线员，就能找到 Nginx。

### Service 的“黑科技”：负载均衡器

即便你以后把 Nginx 扩展到了 10 个 Pod，也只需要拨打这一个 Service 的“电话号码”。

- 稳定性：Service 有一个固定 IP，永远不变。
- 智能分发：当你访问 Service IP 时，它会自动把请求发给后面那堆 Pod 里的其中一个。如果某个 Pod 坏了，Service 会自动把它踢出名单。

### 查看结果？

运行以下命令，看看你的“电话线”接好了没：

```shell
$ kubectl get svc -n k8s-lab
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
demo-nginx   ClusterIP   10.43.171.100   <none>        80/TCP    69s
```

注：`svc` 是 `service` 的缩写

你会看到一行输出：

- NAME: `demo-nginx`（默认跟 Deployment 同名）。
- TYPE: `ClusterIP`。
- CLUSTER-IP: 这是一个 10.43.x.x 左右的虚拟 IP。
- PORT(S): `80/TCP`。

### 为什么叫 ClusterIP？

这是一个新手最容易困惑的地方：你现在还不能从你的 Windows/Mac 浏览器里访问这个 IP。

- 它的范围：这个 IP 只在你的 `berrynode` 内部有效。
- 它的意义：它是为了让集群里的其他程序（比如你的数据库或后端）能找到这个 Nginx。

### endpoints

具体来说，当你访问 Service IP 时，它会自动把请求发给后面那堆 Pod 里的其中一个，这是通过 endpoints 的机制来实现的，它维护了一堆 pod ip, 用于 service 选择

## k8s modules

control plane: deployments --> Pod --> container

data plane: clients --> service --> Pod --> containers

- Pod：真正装着容器，容器就在这里运行
- Deployment：负责“我希望始终有几个 Pod 活着”
- Service：给 Pod 提供稳定入口，因为 Pod 本身名字和 IP 都可能变
