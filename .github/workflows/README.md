# GitHub Workflows

这个目录存放仓库使用的 GitHub Actions workflows。

目前只有一条 workflow：`main` 分支每次更新，都通知 `website` 仓库开始内容同步。

## Files

- `notify-website-content-sync.yml`
  - 在 push 到 `main`，或手动触发 `workflow_dispatch` 时运行
  - 直接触发 `website` 仓库中的 `content-sync.yml`

## How It Works

workflow 不判断这次改了什么。哪些文件算笔记、如何导入和渲染，都由 `website` 决定；它的导入是增量的，内容没变的笔记会被跳过，所以只改了 README 或工具脚本时多同步一次也几乎没有成本。

连续多次 push 时，未完成的旧通知会被取消，只保留最新一次。

## Trigger and Secret

- 触发方式：
  - `push` 到 `main`
  - `workflow_dispatch`
- 依赖的 secret：
  - `WEBSITE_WORKFLOW_TRIGGER_TOKEN`

这个 token 用于调用 GitHub API，触发 `website` 仓库中的 workflow dispatch。
