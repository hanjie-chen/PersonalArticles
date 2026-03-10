# pod-details

我们可以使用 describe 命令查看 pod details 信息

```shell
$ kubectl -n k8s-lab describe pod demo-nginx-99b6475d5
Name:             demo-nginx-99b6475d5-t8mrl
Namespace:        k8s-lab
Priority:         0
Service Account:  default
Node:             berrynode/192.168.31.184
Start Time:       Tue, 10 Mar 2026 15:43:52 +0800
Labels:           app=demo-nginx
                  pod-template-hash=99b6475d5
Annotations:      <none>
Status:           Running
IP:               10.42.0.11
IPs:
  IP:           10.42.0.11
Controlled By:  ReplicaSet/demo-nginx-99b6475d5
Containers:
  nginx:
    Container ID:   containerd://25ece6ae19ee12ca4f4a90ae3c164e31432273b03cfe73b0da7feaa71612258a
    Image:          nginx:stable
    Image ID:       docker.io/library/nginx@sha256:810ad1346ec7fd3d0a246c178f2b82e73a43640c691774405adfd38a751ecce8
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 10 Mar 2026 18:41:55 +0800
    Last State:     Terminated
      Reason:       Unknown
      Exit Code:    255
      Started:      Tue, 10 Mar 2026 15:44:23 +0800
      Finished:     Tue, 10 Mar 2026 18:41:41 +0800
    Ready:          True
    Restart Count:  1
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-8jlkc (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-8jlkc:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:                      <none>
```

### 1. 关键身份验证

- Node: berrynode/192.168.31.184：明确告诉了你，这个 Pod 跑在你的哪台机器上。
- IP: 10.42.0.11：这就是这个 Pod 的私人内网 IP。Service 就是把流量转发到这个 IP 的。
- Controlled By: ReplicaSet/...：印证了我们之前的说法，它的“直接上级”是那个叫 ReplicaSet 的包工头。

### 2. 容器状态：它曾经“死过”一次！

注意看 `Containers` 这一块，这里隐藏了一个小故事：

- Restart Count: 1：这个 Pod 重启过 1 次。
- Last State: Terminated (Exit Code: 255)：
  - 它之前在那跑得好好的（15:44 开始），但在 18:41 的时候突然“去世”了。
  - Exit Code 255 结合 Reason: Unknown，通常意味着宿主机发生了某些变动，比如你的 K3s 服务重启了，或者是机器断网、休眠后恢复。
- State: Running (Started: 18:41:55)：
  - 紧接着，K8s 发现它死了，立刻在几秒钟内（18:41:55）重新启动了一个新的容器实例。这就是 K8s 的自愈能力。

### 3. Conditions（健康检查四部曲）

这几项全是 `True`，说明它已经通过了所有关卡：

1. PodScheduled：已经找好位置住下了。
2. Initialized：初始化已完成。
3. ContainersReady：容器里的 Nginx 已经准备好了。
4. Ready：整个 Pod 可以对外接客了。

### 4. Mounts & Volumes（隐藏的通行证）

你可能会奇怪：“我没挂载磁盘啊，怎么有个 `Mounts`？”

- kube-api-access-8jlkc：这是 K8s 自动塞给每个 Pod 的“身份证明”。
- 容器通过这个特殊的文件夹，可以拿到集群的证书，知道自己是谁，怎么跟 API Server 说话。

### 5. QoS Class: BestEffort

这代表了 Pod 的资源优先级。

- 因为你创建时没有指定这个 Nginx 最少用多少内存、最多用多少 CPU，所以 K8s 把它归类为 `BestEffort`。
- 意思是：如果服务器资源不够了，K8s 会优先考虑“驱逐”这类 Pod，把资源留给那些明确声明了资源需求的“VIP Pod”。