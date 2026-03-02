## npm 安装包有两种“作用域”

npm 安装一个包，本质是在文件系统里放两样东西：

1. 包本体（JS 代码 + 依赖）
2. 可执行命令（比如 `codex` 这个命令），其实是一个“入口脚本”，最后还是交给 `node` 跑

npm 有两种常用安装位置：

### 项目本地安装（local install）

命令：`npm i <pkg>`（不加 `-g`）

- 包会被安装到：`当前目录/node_modules/`
- 可执行命令会在：`当前目录/node_modules/.bin/`
- 你要运行它通常用：`npx <cmd>` 或 `./node_modules/.bin/<cmd>`

这像是：**这个工具只给当前项目用**。

### 全局安装（global install）

命令：`npm i -g <pkg>`

- 包会被安装到：一个“全局目录”（由 npm 的 `prefix` 决定）
- 可执行命令会被放到：`<prefix>/bin/`（例如 `codex`）

这样子在任何目录都能直接敲 `codex`。

## `-g` 参数

`-g` = global（全局安装）。

- 不加 `-g`：装到“当前项目”里（local）
- 加 `-g`：装到“全局目录”里（global），并把命令放到全局 `bin` 目录，方便你随处执行

（如果 `npm bin` 不支持，就用下面这个更稳的：）

```bash
npm config get prefix
# 全局命令一般在 <prefix>/bin
```

------

## 为什么“全局安装”在 Linux 上经常出问题？

问题不在 `-g` 本身，而在 默认的全局目录通常是系统目录，例如：

- `/usr/lib/node_modules`、`/usr/local/lib/node_modules`
- 可执行文件在 `/usr/bin` 或 `/usr/local/bin`

这些目录通常需要管理员权限写入。

所以当你执行：

```bash
npm i -g @openai/codex
```

如果 npm 的 prefix 指向系统路径，你会遇到经典报错：`EACCES: permission denied`（权限不足）。

### 那我用 sudo 不就行了？

可以，但不推荐作为常态，因为会带来两个常见坑：

1. 权限/所有权混乱
   今天你 `sudo npm i -g ...` 装的文件属于 root，明天你不加 sudo 升级/卸载就会失败；或者反过来导致残留一堆 root-owned 文件。
2. 环境不一致
   sudo 运行时的环境变量（PATH、npm 配置、nvm 等）可能跟你用户的不一样，导致“装是装上了，但你用户跑不到/找不到命令”。

所以我之前说“别用全局”更准确的意思是：

> 别把全局装到系统目录里（避免 sudo + 权限坑）。而不是说“永远不要 -g”。

## 最推荐的方案：用户级“全局”（仍然 `-g`，但装在 home）

做法是把 npm 的 `prefix` 改到你自己的 home：

- `prefix=$HOME/.npm-global`
- 于是全局包路径变成：`~/.npm-global/lib/node_modules`
- 全局命令路径变成：`~/.npm-global/bin`
- 不需要 sudo，也不会污染系统目录
- 你在任何目录都能跑 `codex`

这就是我推荐的路线：仍然全局安装，只是“全局”对你这个用户全局，而不是系统全局。

------

## 5) 你现在应该怎么做（基于你已装好 node/npm）

先看你当前的全局 prefix 指到哪里：

```bash
npm config get prefix
```

- 如果输出类似 `/usr` 或 `/usr/local`：那就是“系统级全局”，容易权限坑
- 如果输出在你的 home 下：那就已经是“用户级全局”，直接装就行

### 如果你想按推荐做（用户级全局）

执行一次：

```bash
mkdir -p ~/.npm-global
npm config set prefix "$HOME/.npm-global"
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

然后安装 Codex CLI：

```bash
npm i -g @openai/codex
codex --version
```

如果你把下面两条输出贴出来，我可以直接告诉你“你现在属于哪种情况，下一步最短命令是什么”：

```bash
npm config get prefix
echo $PATH
```