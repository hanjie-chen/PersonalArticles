# GitHub Repository Dispatch

是一种允许 GitHub 外部（或者另一个不同的仓库）触发当前仓库 GitHub Actions 工作流的机制。

通俗地说，它就像是为你的仓库设置了一个“远程快门”。只要有人向 GitHub API 发送一个特定的信号（HTTP 请求），你的自动化工作流就会立刻响应并开始执行。

## 核心机制：Webhook 事件

通常情况下，GitHub Actions 是由内部事件触发的，比如 `push` 或 `pull_request`。但 `repository_dispatch` 是由外部 POST 请求触发的。

### 1. 基本触发流程

1. 发送方：一个脚本、另一个仓库、甚至是一个网页按钮。
2. API 请求：向 `https://api.github.com/repos/{owner}/{repo}/dispatches` 发送 POST 请求。
3. 身份验证：请求必须携带具有写入权限的 `Fine-grained PAT` 或传统的 `Personal Access Token`。
4. 接收方：GitHub 接收到请求后，会寻找工作流文件中定义了 `on: repository_dispatch` 的 YAML 文件。

### 2. 工作流配置示例

在 `.github/workflows/` 目录下，配置如下：

```yaml
on:
  repository_dispatch:
    types: [manual-trigger, build-event] # 只有匹配这些 type 的请求才会触发

jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - name: Receive Payload
        run: |
          echo "触发事件类型: ${{ github.event.action }}"
          echo "传递的数据: ${{ github.event.client_payload.env }}"
```

## 为什么需要它？（常见场景）

- 跨仓库联动：你有两个仓库 A 和 B。当仓库 A 完成了镜像构建，通过 Dispatch 告诉仓库 B：“我已经更新了，请你开始部署测试环境”。
- 外部系统触发：如果你在本地运行了一个爬虫脚本，或者在监控系统（如 Prometheus）中发现指标异常，可以自动发请求给 GitHub，让它执行修复脚本。
- 手动/远程控制：你可以自己写一个小程序或使用 Postman，随时随地通过 API 控制 GitHub Actions 的运行，而不必非要提交代码。

## 关键参数：Client Payload

这是 `repository_dispatch` 最强大的地方。你可以在 POST 请求的 Body 中加入 `client_payload` 字段。

- **数据传递**：你可以把版本号、环境名称、甚至是 JSON 格式的配置传给 GitHub Actions。
- **工作流引用**：在 YAML 中通过 `${{ github.event.client_payload.xxx }}` 就能直接读取这些自定义数据。

## 注意事项

1. 权限限制：发送请求的 Token 必须拥有该仓库的 `metadata:read` 和 `contents:write` 权限。
2. 默认分支：该工作流文件必须存在于 默认分支（通常是 `main` 或 `master`）中，否则触发请求可能会失效。
3. 频率限制：虽然 API 限制相对宽松，但也不建议短时间内进行成千上万次的瞬间触发。

简单来说，如果你需要让 GitHub Actions 和仓库外部的世界“打个招呼”，`repository_dispatch` 就是那根电话线。