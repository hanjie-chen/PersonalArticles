# deployment-details

我们可以使用 `describe` 命令查看 deployments 的详细信息

```
$ kubectl -n k8s-lab describe deployment demo-nginx
Name:                   demo-nginx
Namespace:              k8s-lab
CreationTimestamp:      Tue, 10 Mar 2026 15:43:52 +0800
Labels:                 app=demo-nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=demo-nginx
Replicas:               1 desired | 1 updated | 1 total | 1 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=demo-nginx
  Containers:
   nginx:
    Image:         nginx:stable
    Port:          <none>
    Host Port:     <none>
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   demo-nginx-99b6475d5 (1/1 replicas created)
Events:          <none>
```

如果说 `get` 只是看一眼对方“在不在”，那么 `describe` 就是要把这个人的**家庭背景、工作职责、当前健康状况、甚至是最近干了什么**全部查个底朝天。

### 1. 基础信息：身份标签

- Namespace (k8s-lab)：确认了这个“办公设备”放在哪个房间。
- Labels (app=demo-nginx)：Service 就是通过这个 `app=demo-nginx` 找到这个 Deployment 管理的 Pod 的。
- Selector (app=demo-nginx)：这是 Deployment 的“认亲指南”。它告诉 Deployment：“只要看到带有这个标签的 Pod，就是你亲生的，你要负责管好它们。”

### 2. 副本状态 (Replicas)

```shell
1 desired | 1 updated | 1 total | 1 available | 0 unavailable
```

- Desired (1)：期望值。你告诉 K8s：“我想要 1 个 Nginx”。
- Available (1)：可用值。目前真正跑起来且健康的 Nginx 数量。
- 结论：期望 1 个，实到 1 个，状态非常完美。

### 3. 更新策略 (StrategyType)

StrategyType：RollingUpdate 

- 当你以后想把 Nginx 从 `stable` 版升级到新版本时，K8s 不会一把全部关掉。
- 它会先起一个新版的，再关一个旧版的（滚动），保证你的网站在升级过程中不停机。

### 4. Pod 模板 (Pod Template)

这部分描述了 Deployment 以后“克隆” Pod 时会使用的模板：

- Image (nginx:stable)：使用的镜像。
- Environment / Mounts：目前都是 `<none>`，说明你还没给它设置环境变量或挂载磁盘。

### 5. 状态与事件 (Conditions & Events)

这部分是用来排错的核心区：

- Conditions：
  - `Progressing: True`：说明部署任务正在进行或已成功完成。
  - `Available: True`：说明你的程序已经准备好接客了。
- Events (事件流)：
  - 你的输出里显示为 `<none>`，是因为时间过去比较久，旧的日志被清理了。
  - 重要提示：如果以后你的程序起不来，这里会显示类似 `Failed to pull image` 或者 `Insufficient memory`。这是你修 Bug 时的第一站。

### ReplicaSet

看到最后一行 `NewReplicaSet: demo-nginx-99b6475d5` 了吗？

这里揭示了 K8s 真正的层级结构：

1. Deployment（你是项目经理）：负责定方案、管升级。
2. ReplicaSet（它是包工头）：Deployment 自动创建它，由它去盯着具体的 Pod 数量。
3. Pod（它是打工人）：真正干活的。

所以你的 `demo-nginx-xxxx-yyyy` 这种名字，中间那一串 `xxxx` 其实就是这个 **ReplicaSet** 的 ID。

# 查看原始 yaml

我们可以通过使用 `kubectl get deployment demo-nginx -o yaml` 可以看到 K8s 数据库中存储的完整定义。

```shell
$ kubectl -n k8s-lab get deployment demo-nginx -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
  creationTimestamp: "2026-03-10T07:43:52Z"
  generation: 1
  labels:
    app: demo-nginx
  name: demo-nginx
  namespace: k8s-lab
  resourceVersion: "28629"
  uid: 187b0960-c5e3-4125-adfc-6289fafaa13f
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: demo-nginx
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: demo-nginx
    spec:
      containers:
      - image: nginx:stable
        imagePullPolicy: IfNotPresent
        name: nginx
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  availableReplicas: 1
  conditions:
  - lastTransitionTime: "2026-03-10T07:43:52Z"
    lastUpdateTime: "2026-03-10T07:44:23Z"
    message: ReplicaSet "demo-nginx-99b6475d5" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  - lastTransitionTime: "2026-03-10T10:41:57Z"
    lastUpdateTime: "2026-03-10T10:41:57Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  observedGeneration: 1
  readyReplicas: 1
  replicas: 1
  updatedReplicas: 1
```

关键字段 `spec.strategy`: 这里详细定义了“滚动更新”的细节，比如 `maxSurge: 25%`（更新时允许超出的 Pod 比例）。

关键字段 `status`: 记录了 `availableReplicas` 等实时观察到的状态，这是 K8s 控制循环（Control Loop）的判断依据。

技巧：可以用这个命令导出模板：`kubectl get deploy x -o yaml > template.yaml`。