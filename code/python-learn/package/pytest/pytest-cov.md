# pytest-cov

pytest-cov: 是 Pytest 的一个插件，它封装了 `coverage.py`。它的作用是：在运行测试的同时，监控 Python 解释器执行了哪些代码行，并计算出百分比。

可以通过 `pip install pytest-cov` 安装

使用方法

```shell
pytest -q
--cov=app
--cov=import_articles_scripts
--cov=markdown_render_scripts
--cov=models
--cov-report=term-missing
--cov-fail-under=30
```

`-q` (quiet) 减少冗余输出，只显示核心错误信息，适合 CI 日志。

--cov=app 指定监测目录。只有 `app` 文件夹下的代码才会被统计覆盖率。

--cov-report=term-missing **报告格式**。在终端（Terminal）直接打印结果，并且最贴心的是它会列出具体**哪些行 (Lines)** 没被覆盖到。

--cov-fail-under=30 **强制阈值（Gate）**。如果总覆盖率低于 30%，pytest 将返回一个**非零退出码**，从而直接让你的 CI 流水线挂掉（变红）。

#### A. 增加 HTML 报告 (本地调试神器)

在 CI 里你可以保留 `term-missing`，但在本地开发时，可以尝试： `--cov-report=html` 这会生成一个 `htmlcov/` 目录，点开 `index.html`，你可以像看地图一样看到代码里哪些 `if` 分支变红了（未覆盖）。

#### B. 使用 `.coveragerc` 配置文件

当 `--cov` 参数太多时，命令会变得很难读。你可以创建一个 `.coveragerc` 文件：

```toml
[run]
source =
    app
    models
    markdown_render_scripts

[report]
show_missing = True
fail_under = 30
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == .__main__.:
```

这样你的 CI 命令就可以简化为一行：`pytest`。