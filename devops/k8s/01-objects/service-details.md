# service-details

同样地我们可以使用 describe 命令查看那 service 情况

```shell
$ kubectl -n k8s-lab describe svc demo-nginx
Name:                     demo-nginx
Namespace:                k8s-lab
Labels:                   app=demo-nginx
Annotations:              <none>
Selector:                 app=demo-nginx
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.43.171.100
IPs:                      10.43.171.100
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
Endpoints:                10.42.0.11:80
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
```

### 1. 核心映射逻辑：谁在找谁？

这部分解释了 Service 是如何精准定位到你的 Nginx 的：

- Selector (app=demo-nginx)：这是 Service 的“寻人启事”。它在集群里大喊：“谁身上贴着 `app=demo-nginx` 的标签？”
- Endpoints (10.42.0.11:80)：这是整份报告最亮眼的地方！
  - 还记得你刚才看 Pod 的时候，Pod 的 IP 是 `10.42.0.11` 吗？
  - Service 已经成功找到了这个 Pod，并把它记录在自己的“联系人名单”里了。
  - 如果你以后把 Pod 扩展到 3 个，这里就会出现 3 个 IP 地址。

### 2. IP 地址：虚与实的结合

- IP (10.43.171.100)：这是 Service 的 ClusterIP。
  - 这是一个虚拟 IP (VIP)。它并不对应任何真实的网卡，而是由 K3s 的网络插件（kube-proxy）维护的一套规则。
  - 它的特点是永恒不变。只要你不删这个 Service，这个 IP 就会一直有效。
- Port (80/TCP)：这是接线员接听的号码。
- TargetPort (80/TCP)：这是接线员把电话转接到厨房（Pod）时的内部号码。

### 3. 流量策略

- Session Affinity (None)：会话亲和性。`None` 表示请求会随机分配。如果设为 `ClientIP`，那么来自同一个用户的请求会总是发给同一个 Pod。
- Internal Traffic Policy (Cluster)：内部流量策略。表示集群内的任何节点都可以访问这个 Service。

### 4. 关键点：为什么 Endpoints 很重要？

在排查故障时，这是必看的一项：

- 如果你的网站打不开，你 `describe svc` 发现 Endpoints 是 `<none>`，那就说明 Service 没找到 Pod。
- 这通常是因为你手抖把 Deployment 里的标签写错了，或者是 Pod 还没启动成功。
- 你的输出显示 `10.42.0.11:80`，说明链路已经完全打通了。

# service 底层逻辑

我们可以使用 `kubectl get svc demo-nginx -o yaml` 观察 Service 的网络实现。

**`clusterIPs`**: 这是一个列表，展示了该服务分配到的虚拟 IP。

**`nodePort`**: 当 Service 类型为 `NodePort` 时，这里会显示 K8s 在物理机上强行开启的端口号（如 `32166`），这是外部流量进入集群的入口。

**`externalTrafficPolicy`**: 决定了外部流量是如何在节点间路由的。

```shell
kubectl -n k8s-lab get svc demo-nginx -o yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2026-03-10T07:58:56Z"
  labels:
    app: demo-nginx
  name: demo-nginx
  namespace: k8s-lab
  resourceVersion: "54053"
  uid: 2e46036a-bd9a-4652-af73-c94747f9dc8c
spec:
  clusterIP: 10.43.171.100
  clusterIPs:
  - 10.43.171.100
  externalTrafficPolicy: Cluster
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - nodePort: 32166
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: demo-nginx
  sessionAffinity: None
  type: NodePort
status:
  loadBalancer: {}
```

