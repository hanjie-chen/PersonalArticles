# claude-code

下载 claude code（以下简称 cc）

[Quickstart - Claude Code Docs](https://code.claude.com/docs/en/quickstart)

windows 上面只需要一行代码

```powershell
irm https://claude.ai/install.ps1 | iex
```

使用下面的命令查看 cc 当前版本和最新版本

```shell
claude --version
claude doctor
```

如果有新版本，可以使用这个命令升级

```shell
claude update
```

# command

/model: 切换模型和思考强度

/btw: 在当前上下文开一个临时的对话框询问信息（by the way）提问完成之后关闭不会污染上下文。使用方法是 ` /btw <question> ` 在命令之后空格直接加上问题。然后 esc 退出

/insights: 会生成一份HTML报告，分析你过去一个月使用Claude Code的习惯，包括你最常用哪些命令，你有哪些重复性的操作模式，然后给你推荐一些自定义命令和Skills。
这个命令生成的报告存储位置是固定在 ` ~/.claude/usage-data/report.html ` 每次运行 `/insights` 会覆盖上一次的报告，不会保留历史。

@filename: 使用 @ 可以引用文件，需要注意 @ 和之前的字符需要保持一个空格

# CLAUDE.md

一个好的 claude.md 需要包含这些内容

 1. 项目一句话简介 — 让cc秒懂这是什么
  2. 目录结构 + 每个文件夹的用途 — 让cc需要找什么就去哪里，不用乱翻
  3. 关键设定文件索引 — 按需读取
  4. 当前进度 — 做到那里，现在在解决什么问题

# claude code 配置

claude code 模型权限、默认模式、项目规则、hooks、sandbox 等正式配置主要放在 `settings.json`，

如果要手动配 Claude Code，主要看这三层：

- 用户级：`~/.claude/settings.json`，对所有项目生效
- 项目级：`<repo>/.claude/settings.json`，会随 git 分享给团队
- 本地项目级：`<repo>/.claude/settings.local.json`，只在你本机这个仓库生效，且会被 git ignore

优先级是 Local > Project > User。

## user settings.json

接下来我们来详细解释这个文件，我们先来看一个最基础的 settings.json

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "opus[1m]",
  "effortLevel": "medium",
  "defaultMode": "acceptEdits"
}
```

- schema: 配置官方给了 JSON Schema，编辑器能直接做自动补全和校验，减少拼错 key、配错位置这种低级错误。
- model: 选择模型
- effortLevel: 选择思考强度

接下来我们来看这一个字段 defaultMode 字段

权限模式，支持这些值：

- default 标准模式。
  - 默认可以读取文件
  - 想要执行命令的时候会问你，如果点击了 yes, don't ask again, 那么 cluade 会按项目目录 + 命令记住，以后类似命令就不再问
  - 修改文件是也会询问，但是这个 don't ask again 只到本轮 session 结束
- acceptEdits
  - 在 default 基础上加上默认可以修改文件的权限
- plan 只能分析，不能改文件，也不能跑命令
- dontAsk 没有预先放行的工具，一律自动拒绝
- bypassPermissions 几乎跳过权限提示

然后我们再来看 permission 字段

这个字段是“精细权限规则”。

- `allow`：直接允许
- `ask`：每次问
- `deny`：直接拒绝

并且规则匹配顺序是：先 deny，再 ask，再 allow，第一条匹配就生效。

# Context engineer

参考这篇文章：https://www.zhihu.com/question/1945503640539333416/answer/2016306836769355199

# 自动压缩造成的问题

当我们的 ctx(context windows) 达到 95% 的时候，会出发自动压缩，这往往会造成一些问题，比如说忘记我们之前的约定，一个好的方案是，我们在达到这个限制之前主动使用 `/compact` 命令，压缩。

但是我们不可能每个对话结束之后都使用 `/cost`, `/usage` 命令看当前的使用情况，所以我们可以在 cc(version ≥ v2.1.132) 底部配置一个状态行（Status Line）实时显示 token 用量。

## 配置状态行

效果：底部实时显示 `[Opus] ctx: 35% | $0.25`

**第一步**：创建脚本 `~/.claude/statusline-command.sh`

```sh
#!/bin/sh
input=$(cat)

# 模型名称简化
model=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
case "$model" in
  *Opus*)   short="Opus" ;;
  *Sonnet*) short="Sonnet" ;;
  *Haiku*)  short="Haiku" ;;
  *)        short=$(echo "$model" | sed 's/Claude //; s/ [0-9].*//' | cut -c1-10) ;;
esac

# 上下文使用百分比
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$used_pct" ]; then
  actual_floor=$(echo "$used_pct" | awk '{printf "%d", $1}')
  ctx_str="ctx: ${actual_floor}%"
else
  ctx_str="ctx: -"
fi

# 根据 token 用量估算费用
total_input=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
total_output=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')
model_id=$(echo "$input" | jq -r '.model.id // ""')

case "$model_id" in
  *opus*)   input_price="15";  output_price="75" ;;
  *sonnet*) input_price="3";   output_price="15" ;;
  *haiku*)  input_price="0.8"; output_price="4" ;;
  *)        input_price="3";   output_price="15" ;;
esac

cost_str=$(awk -v ti="$total_input" -v to="$total_output" \
               -v ip="$input_price" -v op="$output_price" \
  'BEGIN { printf "$%.2f", (ti/1000000*ip)+(to/1000000*op) }')

printf "[%s] %s | %s" "$short" "$ctx_str" "$cost_str"
```

记得给执行权限：`chmod +x ~/.claude/statusline-command.sh`

前置依赖：需要安装 jq（`brew install jq` / `apt install jq`）

**第二步**：在 `~/.claude/settings.json` 中添加 statusLine 字段

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash ~/.claude/statusline-command.sh"
  }
}
```

重启 cc 即可生效。

