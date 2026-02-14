# basic-concepts

CI/CD 不是单一的工具，而是一套流程和实践理念

- CI: continuous integration 持续集成
  - 每次提交代码后，自动执行检查：安装依赖、跑测试、构建镜像、静态检查等。
  - 目标：尽早发现问题。
- CD: continuous deployment 持续交付
  - CI 通过后，把新版本自动发布到目标环境（比如 Ubuntu 服务器）。



# Github Action

简单来说，GitHub Actions 就是 GitHub 提供的一台免费的、云端的 Linux 电脑，这台电脑平时是关机的。

通过在 `.github/workflows/` 下写 `.yml` 文件，我们可以给这台电脑下达指令：“当某个事件发生时（比如 Push 了代码），请立刻开机，执行以下命令。”

你可以把 GitHub Actions 理解为一套“自动化流程”：

- Workflow (工作流)： 整个 `.yml` 文件。代表一个完整的自动化任务。
- Event (事件/触发器)： “什么时候开始跑？”。比如 `push` 代码、有人提了 `PR`、或者你设定了定时任务。
- Job (作业)： 这一台“云电脑”要做的事。一个 Workflow 可以有好几个 Job（比如一个负责测试，一个负责部署）。
- Step (步骤)： 在这台电脑上具体敲的命令。比如 `ls`, `docker build`, `npm install`。

GitHub Actions 的强大之处在于：

1. 环境全能： 它这台“云电脑”里已经预装好了 `git`, `docker`, `python`, `node` 等几乎所有你需要的环境。
2. 市场（Actions Marketplace）： 别人写好的功能你可以直接拿来用。
   - 想登录 Docker Hub？不用自己写复杂的脚本，直接用官方的 `docker/login-action`。
   - 想发送钉钉通知？去市场搜一下直接引用。
3. 免费额度： 对于公开仓库（Public Repo），它是完全免费的。



## `name` 字段

这个 `name` 是给人类看的显示名称。

- 在 GitHub 界面上： 当你打开项目的 Actions 标签页，左侧列出的任务列表名称就是由这个 `name` 决定的。如果不写，GitHub 默认会用文件名（如 `ci.yml`）。
- 联动作用： 在的 `cd.yml` 里，有一行 `workflows: ["CI"]`。这里的 `"CI"` 对应的正是那个文件里的 `name: CI`。这就像是给程序起个名字，方便其他程序调用。



## Action 指令：`run` vs `uses`

在 GitHub Actions 中，命令有两种执行方式：

1. `run`: 执行原始的 Shell 命令（就像你在 Linux 终端敲代码一样）。
2. `uses`: 调用一个现成的、封装好的“脚本组件”（官方称为 Action）。
   - 语法：`{author}/{project-name}@{version}`
   - 常用模块：`actions/checkout@v4`（作用：把代码拉取到当前虚拟机工作目录，通常是所有 Pipeline 的第一步）。

`actions/checkout@v4` 其实是一个由 GitHub 官方维护的开源项目（地址就在 `github.com/actions/checkout`）。它内部帮你写好了极其复杂的逻辑：

- 初始化 Git 环境。
- 配置身份验证（Token）。
- 执行 `git clone`。
- 切换到正确的 Git 分支或 Commit。

你当然可以自己写 `run: git clone https://github.com/...`，但你会面临以下麻烦：

- 权限问题： 你的私有仓库需要配置 SSH Key 或 Token 才能克隆，自己写很麻烦。
- 版本问题： 你需要手动判断当前触发 CI 的是哪个分支、哪个提交点。
- 性能问题： 官方的 `checkout` 经过了极致优化（比如支持浅克隆 `--depth`，只拉取最后一层提交以节省时间）。

所以，`uses: actions/checkout@v4` 就像是 DevOps 界的“一键启动脚本”。

- **`run: docker build`**：就像是**自己做饭**。你很清楚每一道工序（切菜、开火、翻炒），对应 Linux 里的每一个原生指令。
- **`uses: actions/checkout@v4`**：就像是**点外卖**。你不需要知道外卖员是怎么骑车来的、厨师是怎么洗菜的，你只需要下达订单（`uses`），代码（饭菜）就会准时出现在你的 Ubuntu 虚拟机（餐桌）上。