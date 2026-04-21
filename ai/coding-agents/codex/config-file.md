# Codex Config Fil

Codex 的用户级配置文件默认在 `~/.codex/config.toml`，项目级配置可以放在仓库里的 `.codex/config.toml`；CLI 和 IDE 扩展共用同一套配置层。

在讲解 config.toml 配置的时候，我们也顺便讲下 toml 语法

## toml syntax

### TOML 只看三样东西

第一种是最基础的 `key = value`：

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

我的 config.toml

```toml
#:schema https://developers.openai.com/codex/config-schema.json
# =========================
# Codex 全局基础设置
# =========================

# 默认模型
model = "gpt-5.4"

# 推理强度
model_reasoning_effort = "high"

# 不弹审批
# 可选值常见有：
# - "untrusted"   : 只对不受信命令询问
# - "on-request"  : 需要越界时询问
# - "never"       : 不询问
approval_policy = "on-request"

# 沙箱模式：
# - "read-only"
# - "workspace-write"
# - "danger-full-access"
#
sandbox_mode = "danger-full-access"

# 网页搜索模式：
# - "disabled"
# - "cached"
# - "live"
web_search = "live"

# =========================
# workspace-write 的附加设置
# =========================
[sandbox_workspace_write]

# 允许沙箱内命令访问网络
# 例如 curl / git fetch / pip / npm 等
network_access = true

# 如有需要，也可以额外放开别的可写目录
# writable_roots = ["/home/plain/some-other-dir"]

# =========================
# 项目信任设置
# =========================
[projects."/home/plain/personal-project"]

# trusted 只是表示信任这个项目，允许读取项目内 .codex/config.toml
# 不是“自动批准所有修改”
trust_level = "trusted"

[features]
multi_agent = true
```

