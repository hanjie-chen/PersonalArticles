# Python Project file and folder name

## python package name

Python <u>package name</u> (folder name) and <u>module name</u> (`.py` filename)

- 必须使用下划线命名法（snake_case），如 `my_package`, `my_extension.py`
- 不允许使用连字符（kebab-case），如 `my-package`, `gfm-admonition-extension.py` 会导致无法通过 `import` 引入

e.g.

```bash
# ✅ 正确命名
project-root/             # 项目根目录可用连字符
├── my_app/              # Python 包（使用下划线）
│   ├── __init__.py
│   ├── utils/           # 子包（同样用下划线）
│   │   ├── __init__.py
│   │   └── markdown_helpers.py  # 模块文件（正确）
│   └── config_loader.py
└── docs/                # 普通目录（无 Python 模块）

# ❌ 错误命名
project-root/
├── my-app/              # 错误！Python 包名含连字符
│   ├── __init__.py
│   └── config-loader.py # 错误！模块名含连字符
```



### 为什么模块名不能使用 kebab-case

Python 模块名的本质：

- `.py` 文件的文件名会被直接映射为模块名。
- 模块名需遵循 Python 标识符规则（仅允许字母、数字和下划线，不能以数字开头）。

验证方法： 在 Python 解释器中测试以下名称：

```python
# 检查是否合法标识符
"my_module".isidentifier()  # ➔ True ✅
"my-module".isidentifier()  # ➔ False ❌
```

## python project file name

对于普通的 Python 文件（不涉及被其他模块导入），技术上可以使用连字符命名。但即便如此也强烈不推荐，有可能发生因命名问题引发的隐蔽错误和工具链兼容性问题。





## best practice

所有 `.py` 文件都使用小写字母和下划线（`snake_case`）禁止使用连字符、空格、大写字母（避免跨平台问题）

不参与代码导入的目录/文件，可自由选择（保持团队统一即可），例如用 `kebab-case` 命名项目根目录



## common filename

非 Python 脚本的通用目录和文件，推荐使用 `kebab-case`（连字符分隔小写字母）

适用于：

- 纯资源目录（如 `rendered-articles/`）
- Shell 脚本工具（如 `sync-articles.sh`）
- 项目组织的顶级目录（如你案例中的 `web-app`）

e.g.

```bash
project-root/
├── web-app/             # 项目主目录（符合常规命名）
├── articles-sync/       # 数据同步工具目录
│   └── sync-script.sh
└── rendered-articles/   # 生成的 HTML 内容
```

