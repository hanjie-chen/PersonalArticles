# Generate `requirements.txt`

为了使得我们的 python 项目的存在可移植性，我们往往需要将我们使用了那些 python 包都列出来，甚至有时候我们需要将自己使用了 python 包的那个版本都要写清楚，防止出现只有我的环境可以运行的情况

## freeze

如果使用这个命令生成 requirements.txt

```bash
pip freeze > requirements.txt
```

那么就会造成一个问题，那就是这个命令会把当前所有的下载的包，不管是否会使用到。

特别是可能会出现的系统级别的 python 包，这就有可能在 docker build 的时候出现这个问题：
```bash
=> ERROR [4/5] RUN pip install -r requirements.txt                                                                                                                                                         6.1s
------
 > [4/5] RUN pip install -r requirements.txt:
3.692 Collecting attrs==19.3.0
3.772   Downloading attrs-19.3.0-py2.py3-none-any.whl (39 kB)
3.849 Collecting Automat==0.8.0
3.863   Downloading Automat-0.8.0-py2.py3-none-any.whl (31 kB)
3.933 Collecting blinker==1.7.0
3.949   Downloading blinker-1.7.0-py3-none-any.whl (13 kB)
4.034 Collecting certifi==2019.11.28
4.049   Downloading certifi-2019.11.28-py2.py3-none-any.whl (156 kB)
4.086      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 156.0/156.0 kB 4.7 MB/s eta 0:00:00
4.136 Collecting chardet == 3.0.4
4.150   Downloading chardet-3.0.4-py2.py3-none-any.whl (133 kB)
4.174      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 133.4/133.4 kB 7.0 MB/s eta 0:00:00
4.283 ERROR: Could not find a version that satisfies the requirement cliapp == 1.20180812.1 (from versions: 1.0.1, 1.0.2, 1.0.3, 1.0.4, 1.0.5, 1.0.6, 1.0.7, 1.0.8, 1.0.9)
4.283 ERROR: No matching distribution found for cliapp == 1.20180812.1
4.523
4.523 [notice] A new release of pip is available: 23.0.1 -> 24.3.1
4.523 [notice] To update, run: pip install --upgrade pip
```

## pip-tools

为了仅仅让有效的包放入 requirements.txt, 我么可以使用 pip-tools 中的 pip-compile 工具自动解析所有依赖关系

首先安装 pip-tools：

``` bash
pip install pip-tools
```

创建一个 requirements.in 文件，在其中列出你的直接依赖（主要的包）：

```
flask
flask-sqlalchemy
markdown
python-frontmatter
```

### `pip-compile`

使用 pip-compile 生成 requirements.txt：

``` bash
pip-compile requirements.in
```

当我们更新完 requirements.in 之后，运行 `pip-compile --upgrade requirements.in` 更新 `requirements.txt` 到最新版本

> [!note]
>
> 这个命令会重新解析 `requirements.in`，包括新添加的包
>
> 会升级 `requirements.txt` 中已有的包，但仍会遵守 `requirements.in` 的约束。



### `pip-sync`

运行 `pip-sync requirements.txt` 可以来安装/更新环境中的包

# Use `requiements.txt`

对于你的 Dockerfile，可以这样使用：

``` dockerfile
FROM python: 3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host = 0.0.0.0"]
```

这种方法会给你一个干净、可维护且可靠的依赖管理方案，特别适合 Docker 环境。

补充建议：
1. 把 requirements.in 和 requirements.txt 都加入版本控制
2. 在 requirements.txt 中的版本号最好是固定的（这是 pip-compile 默认行为）
3. 如果遇到特定包的问题，可以在 requirements.in 中指定版本范围

这样应该能解决你遇到的问题，并且提供一个更可靠的依赖管理方案。

