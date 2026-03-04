# security fix

当我们通过 pip-audit/trivy 发现漏洞之后，可以使用 dependabot/renovate 来自动修复。

例如项目可能依赖 50 个 Python 包。随着时间推移：

- 版本过时：`requests` 从 2.20 升到了 2.31。
- 安全漏洞：`django` 3.2 被爆出有注入风险，官方发布了 3.2.20 修复版。

手动更新很痛苦：得一个个查版本、改 `requirements.txt`、测试。

而它们会盯着这些包，一旦有新版本，就自动在你的 GitHub/GitLab 上开一个 Pull Request (PR)。只需要点一下“合并”，代码就更新了。

## Dependabot vs. Renovate

### Dependabot

- 优点：开箱即用。你不需要安装任何东西，只要在仓库里放个 `.github/dependabot.yml` 配置文件就行。
- 体验：界面极其简洁，直接集成在 GitHub 的 Security 标签页里。
- 缺点：配置的灵活性稍差，主要针对主流语言。

### Renovate

由 Mend 维护的开源工具，支持 GitHub, GitLab, Bitbucket, Azure DevOps。

- 优点：极其强大且专业。它可以把几十个小版本的更新“合并”成一个 PR，减少对你的骚扰；它还能自动合并（Automerge）那些通过了测试的次要更新。
- 体验：适合大团队，如果你对 PR 的频率、分组、自动合并有严格要求，选它。
- 缺点：配置项非常多（几百个参数），新手可能会看晕。

## CI example

为了让你理解它们怎么配合，这里有一个典型的自动化链条：

1. Renovate/Dependabot 发现 `urllib3` 有安全更新。
2. 它自动提交一个 PR，修改了的 `requirements.txt`。
3. CI 流程 被触发：
   - 运行 `pytest`（确保更新后代码没坏）。
   - 运行 `pip-audit`（确保新版本没有引入新漏洞）。
   - 运行 `Trivy`（如果是 Docker 项目，确保构建出的镜像安全）。
4. 你看到所有绿灯通过，点下 Merge。

# Dependabot

对于 dependabot 来说，只需要在代码仓库里创建 `.github/dependabot.yml`，内容大概长这样：

```yaml
version: 2
updates:
  - package-ecosystem: "pip"      # 监控 Python (requirements.txt, setup.py 等)
    directory: "/web-app"         # 关键！说明你的 Python 项目不在根目录，而是在 web-app 文件夹下
    schedule:
      interval: "weekly"          # 每周检查一次
      day: "monday"               # 每周一凌晨 3:00 (新加坡时间) 检查
      time: "03:00"               # 这样你周一上班就能看到所有的更新 PR
      timezone: "Asia/Singapore"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "python"
    commit-message:
      prefix: "deps(pip)"
    groups:
      pip-minor-patch:      # 组名
        patterns: ["*"]     # 匹配所有包
        update-types:       # 只有小版本 (minor) 和补丁 (patch) 升级才会合并
          - "minor"
          - "patch"

  - package-ecosystem: "github-actions" # 监控你用的 actions (如 actions/checkout@v3 -> @v4)
    directory: "/"                      # Actions 的配置文件通常在根目录的 .github/workflows
    schedule:
      interval: "weekly"
      day: "monday"
      time: "03:30"                     # 比 Python 晚半小时，错峰执行
      timezone: "Asia/Singapore"
    open-pull-requests-limit: 3
    labels:
      - "dependencies"
      - "ci"
    commit-message:
      prefix: "deps(actions)"
    groups:
      github-actions:
        patterns:
          - "*"
```

**`open-pull-requests-limit`**:

- 限制同时开启的 PR 数量。比如 `pip` 设为 5，意味着如果已经有 5 个更新 PR 你没处理，Dependabot 就不会再开新的。这能防止你的 GitHub 首页被 PR 淹没。

**`labels`**:

- 自动给 PR 贴标签（如 `dependencies`）。这样你可以通过 GitHub 的过滤器快速筛选出哪些是机器人自动生成的 PR。

**`commit-message`**:

- 设置提交信息的开头（如 `deps(pip): ...`）。这对维护整洁的 Git 历史非常有帮助，一眼就能看出这是依赖更新。

## 运行流程

1. 每周一凌晨：Dependabot 准时起床。
2. 扫描 `/web-app`：看看有没有 Python 包更新，把所有补丁级更新塞进一个名为 `deps(pip)` 的 PR。（new branch）
3. 扫描 Actions：看看有没有插件更新，有的话新建一个 branch 并且 commit, 跑通 CI 之后 PR。
4. 周一早晨：你上班打开电脑，发现两个整洁的 PR 躺在仓库里，CI 已经帮你跑过了。如果没有变动破坏（Breaking changes），你直接点 Merge 即可。

> [!note]
>
> 当我们第一次配置好 `.github/dependabot.yml` 或者是修改了这个文件， git push 之后就会开启一次扫描，而不是等到设定的周一才开始跑