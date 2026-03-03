# lint

静态代码分析

`Lint` 检查的是代码的“对错”和“潜在风险”。

- 它的作用： 自动扫描代码中不符合语法规范、容易引发 Bug 的地方（比如使用了未定义的变量、遗漏了分号、或者使用了危险的函数）。
- 通俗理解： 就像文章的错别字检查。它不管你的逻辑好不好，但它能揪出明显的低级错误。

## python lint - ruff

使用 python ruff

```shell
$ ruff check .
All checks passed!
```

`All checks passed!` 结束，所有预设的 Lint 规则都没有被触发。

python 注释 `# noqa: E402` 是什么

- E402 是“导入不在文件顶部”。
- 在某些情况下例如 tests/conftest.py 里我们需要先改 sys.path，再 import app/models，这是有意为之（否则导入不到本地模块）。
- `# noqa: E402` 是告诉 ruff：这行违反 E402 是预期行为，请忽略。
- 不加的话 lint 会一直红，但代码逻辑其实是对的。



### format check

代码格式检查

```shell
ruff format .
13 files left unchanged
```

13 个文件的排版全都符合规范，所以一个字都没改。



## shell lint

使用 shellcheck

需要下载

```shell
# 下载
sudo apt install -y shellchck
# 检查
shellcheck -x scripts/deploy/*.sh articles-sync/*.sh
```

`-x` 参数：跟随外部文件 (External Sources)

- 默认情况： 如果你的脚本里有一行 `source ./config.sh`（引用了另一个文件的变量），ShellCheck 默认不会去检查那个被引用的文件，甚至会因为找不到变量定义而报错。
- `-x` 的作用： 它告诉 ShellCheck：“允许追踪外部引用的文件”。它会顺着 `source` 或 `.` 指令去读取关联的文件，从而给出更准确的分析。

shell 注释 `# shellcheck source=scripts/deploy/service_wait.sh` 的意义

- 这些脚本有 source "${SCRIPT_DIR}/service_wait.sh"。
- ShellCheck 静态分析时不一定能推断动态路径，会报“找不到 source 文件”。
- 加这行注释是给 lint 一个明确路径提示。
- 运行行为不变，只影响静态检查准确性。