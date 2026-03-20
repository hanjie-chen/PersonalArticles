# codex cli使用指南

下载 codex cli

```shell
npm i -g @openai/codex
# macos download
brew install codex
```

> [!note]
>
> 在用 npm 命令安装时需要注意全局 prefix 最好放到用户目下，而不是系统目录下，详见 [npm-guide](../npm/npm.md)

验证

```shell
which codex
codex --version
```

登录

```shell
# 查看登录状态
codex login status
# 打开网页登录
codex login
```

## AGENTS.md

Codex 会在每次启动时自动读取并合并一条“指令链”：

- 全局：`~/.codex/AGENTS.md`
- 项目：从 repo root（通常是 Git root）一路走到当前工作目录，每层目录最多取一个 `AGENTS.md`，并按“root → leaf”顺序依次注入。 

作用：把你每次都要重复说的“工作协议/目录说明/输出格式”固化下来。

## interactive mode

使用命令 `codex` 直接进入交互模式

<img src="./images/interactive-mode.png" alt="interactive mode" style="zoom:50%;" />

使用 `/` 可以设定和查看某些内容，比如说选择模型

<img src="./images/select.png" alt="codex cli select" style="zoom:50%;" />

实际上的命令不仅仅是上线显示的这些，比较常用的命令有

status

<img src="./images/status.png" alt="status" style="zoom:50%;" />

如果我们需要开启一段新对话，那么我们可以使用

- `/clear`：清屏 + 开新对话（从头开始聊）。

# plan mode

Plan mode 会先让 Codex 做“方案设计 / 执行分解”，再进入真正的修改与实现，而不是一上来就直接改代码。

更适合复杂任务。比如重构、迁移、跨多个文件的大改动、需要分阶段验证的任务。因为它会更强调“步骤、里程碑、顺序、边界”，降低一上来改偏的概率。

可能会先问你问题，如果还需要补充信息，Codex 会先问你，而不是直接动手。

区分：

- 普通 Agent/直接实现模式：你说做什么，它尽快开始看文件、跑命令、改代码”。
- Plan mode：先出施工方案、拆步骤、确认方向，再继续”。

# config.toml

Codex 的用户级配置默认在 `~/.codex/config.toml`，项目级配置可以放在仓库里的 `.codex/config.toml`；CLI 和 IDE 扩展共用同一套配置层。

在讲解 config.toml 配置的时候，我们也顺便讲下 toml 语法

## toml syntax

### TOML 只看三样东西

第一种是最基础的 `键 = 值`：

```toml
model = "gpt-5.4"
approval_policy = "on-request"
```

第二种是“表”，也就是分组，用方括号表示：

```toml
[sandbox_workspace_write]
network_access = true
```

第三种是数组：

```toml
project_root_markers = [".git", ".hg"]
```

它本质是 key/value 配置；**缩进只是空白，不参与语义**。

真正决定结构的是 `key = value` 和 `[table]` 这种表头。并且，一旦进入某个 `[table]`，后面的键会一直属于这个表，直到下一个表头或文件结束。 

### 方括号分区

```toml
[sandbox_workspace_write]
network_access = true
```

它的意思：

- 现在开始进入 `sandbox_workspace_write` 这个分组
- 接下来写的键，默认都属于这个分组
- 直到你再写一个新的 `[xxx]`

## Codex  `config.toml`

你可以把一个 Codex 配置文件理解成这 3 层：

### 第一层：全局根键

这些直接写在最外层，不放进任何 `[table]` 里：

```toml
model = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
```

这些是最常改的几个键。官方文档里明确列了：

- `model`
- `approval_policy`
- `sandbox_mode`
- `web_search`
- `model_reasoning_effort`

 `sandbox_mode` : read-only, workspace-write, danger-full-access, 

`model_reasoning_effort` :minimal, low, medium, high, xhigh`

`web_search` : disabled, cached, live，默认是 `"cached"`。

### 第二层：某个功能对应的配置表

比如：

```toml
[sandbox_workspace_write]
network_access = true
writable_roots = []
```

这表示“仅当 `sandbox_mode = "workspace-write"` 时，这些额外参数才生效”。官方文档对这个表下支持的键列得很明确：`network_access`、`writable_roots`、`exclude_tmpdir_env_var`、`exclude_slash_tmp`。 ([OpenAI开发者](https://developers.openai.com/codex/config-sample/))

### 第三层：特殊分组

比如：

```toml
[windows]
sandbox = "elevated"
```

这是 Windows 原生运行 Codex 时 的设置。官方文档建议原生 Windows 优先用 `elevated`，`unelevated` 作为回退。

### config.toml example

```toml
# ========== 全局默认设置 ==========
model = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

# ========== 仅当 sandbox_mode = "workspace-write" 时生效 ==========
[sandbox_workspace_write]
network_access = false

# ========== 仅在 Windows 原生运行 Codex 时有意义 ==========
[windows]
sandbox = "elevated"
```

你可以这样理解：

- 上面 5 行：全局默认值
- `[sandbox_workspace_write]`：给某个功能块补充参数
- `[windows]`：Windows 专用参数

### Codex 常见 section

#### 全局根键

```toml
model = "gpt-5.4"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
```

#### workspace-write 细节

```toml
[sandbox_workspace_write]
network_access = true
writable_roots = []
```

#### Windows 原生模式

```toml
[windows]
sandbox = "elevated"
```

#### profile 预设

```toml
[profiles.default]
model = "gpt-5.4"
approval_policy = "on-request"
sandbox_mode = "read-only"
```

#### 项目信任状态

```toml
[projects."/absolute/path/to/project"]
trust_level = "trusted"
```

### Check

第一，在文件顶部加注释分块：

```toml
# ========== model ==========
model = "gpt-5.4"
model_reasoning_effort = "high"

# ========== permissions ==========
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

# ========== workspace-write ==========
[sandbox_workspace_write]
network_access = true
```

第二，在 VS Code 里装 TOML 插件，并给 `config.toml` 加 schema：

```toml
#:schema https://developers.openai.com/codex/config-schema.json
```

可以用这个 schema 来获得自动补全和诊断。



# 修改 config.toml

修改 config.toml 可以在 vscode plugin 中即刻生效，无需 reload
