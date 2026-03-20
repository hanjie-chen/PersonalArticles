# service.yaml

文件 service.yaml

然后先只写最开头这几行：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: website-web-app
  namespace: k8s-lab
```

这一段你应该已经开始熟悉了，因为结构和 `Deployment` 很像：

- `apiVersion: v1`: `Service` 属于 core API，所以这里不是 `apps/v1`, 而是 `v1`
  
- `kind: Service` 表示我们这次创建的是一个 `Service`
  
- `metadata.name` 这个 Service 的名字叫 `website-web-app`
  
- `metadata.namespace`
  - 也放在 `k8s-lab` 里，和 Deployment 同一个 namespace
  - 这样它们才在同一个逻辑空间里配合工作

这里你可以顺手建立一个感觉：

- `Deployment` 名字叫 `website-web-app`
- `Service` 也叫 `website-web-app`

这很常见，不冲突，因为它们是不同 kind 的资源。 反而这样命名更清晰，说明它们都是这个组件的一部分。

## spec

这一段就是 `Service` 的核心了。

```yaml
spec:
  selector:
    app: website-web-app
  ports:
    - name: http
      port: 80
      targetPort: 5000
  type: NodePort
```

1. `selector`

```yaml
selector:
  app: website-web-app
```

这表示这个 Service 要把流量转发给哪些 Pod。

它找 Pod 的方式不是看名字，而是看标签。也就是说，这里是在说：

- 找标签里有 `app=website-web-app` 的 Pod
- 然后把请求转发给它们

这就和你在 `deployment.yaml` 里写的 Pod template label 对上了：

```yaml
template:
  metadata:
    labels:
      app: website-web-app
```

这里非常关键的一点是：

- Service 的 `selector`
- 要匹配 Pod 的 `labels`

如果对不上，Service 就找不到后端 Pod，流量就转不出去。

2. `ports`

```yaml
ports:
  - name: http
    port: 80
    targetPort: 5000
```

这里最容易混淆，我帮你拆开：

- `port: 80`
  - Service 自己对外提供的端口
  - 也可以理解成“别人访问这个 Service 时使用的端口”

- `targetPort: 5000`
  - Service 最终转发到 Pod 容器里的哪个端口
  - 你的 Flask/Gunicorn 在容器里监听的是 `5000`

所以这段的意思是：

- 别人访问 Service 的 `80`
- Service 再把流量转到 Pod 的 `5000`

你可以把它理解成一种“端口映射”。

3. `type: NodePort`

```yaml
type: NodePort
```

这表示：
- 这个 Service 不只是集群内部可访问
- 它还会在 Node 上开放一个高位端口
- 这样你就可以通过 `Node IP : NodePort` 访问它

因为你现在是单节点 k3s，所以这里的 Node 就是你的树莓派。

这也是为什么我们现在第一版先用 `NodePort`：
- 比 `Ingress` 简单
- 很适合本地实验
- 可以很快看到结果

