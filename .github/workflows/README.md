# GitHub Workflows

这个目录存放仓库使用的 GitHub Actions workflows。

目前这里只有一条与内容发布相关的 workflow，用来在 `main` 分支出现可发布内容变更时，通知 `website` 仓库开始内容同步。

## Files

- `notify-website-content-sync.yml`
  - 在 push 到 `main`，或手动触发 `workflow_dispatch` 时运行
  - 检查这次变更中是否包含会影响网站发布结果的内容
  - 如果检测结果为 `true`，则触发 `website` 仓库中的 `content-sync.yml`

## How It Works

这条 workflow 的职责比较简单：

1. checkout 仓库，并拿到本次比较所需的 git 历史
2. 生成本次变更的文件列表
3. 调用 `.kb-tools/website_sync/detect_publish_affecting_changes.py`
4. 读取检测结果
5. 如果命中了 publish-affecting changes，则请求 `website` 仓库执行内容同步 workflow

这里需要注意：

- workflow 负责 orchestration，不负责定义“哪些路径算可发布内容”
- 路径判定规则集中放在 `.kb-tools/website_sync/`
- 这样可以把规则本身独立测试，而不是全部写死在 workflow YAML 里

## Trigger and Secret

- 触发方式：
  - `push` 到 `main`
  - `workflow_dispatch`
- 依赖的 secret：
  - `WEBSITE_WORKFLOW_TRIGGER_TOKEN`

这个 token 用于调用 GitHub API，触发 `website` 仓库中的 workflow dispatch。

## Notes

- 如果只是修改 `README.md`、工具脚本、模板目录或其他不影响网站发布结果的内容，这条 workflow 仍然会运行，但检测步骤会给出 `should_trigger=false`
- 如果你要调整“什么变更才应该触发网站同步”，优先修改 `.kb-tools/website_sync/` 中的规则和测试，而不是先改这份 workflow
