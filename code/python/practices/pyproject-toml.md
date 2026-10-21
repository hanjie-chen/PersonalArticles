# pyproject.toml 是什么

有时候我们往往能看到一个 python 项目中，包含 `pyproject.toml` 这个文件，这是Python 项目更加现代、标准化的方式。Python Packaging 官方也明确推荐现代项目使用它：[Writing your pyproject.toml - Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

### 从 requirements.txt 说起
在我的 website 项目中，使用 requirements.txt 来帮助构建一个能够让我的代码运行起来的 docker image

这个文件里面包含了我的 python 代码运行起来的所需要的各种依赖 package

例如

```
pypdf==6.0.0
trafilatura==2.0.0
```

### 一个比喻：购物清单 vs 说明书

可以先用一个简单比喻：

- `requirements.txt`：环境的“购物清单”，意思是告诉 pip ，请给这个环境安装这些包。
- `pyproject.toml`：这个 Python 项目的“说明书”，不只是装什么，还包括这个项目本身是什么、怎么被安装。

### 说明书里写了什么

#### [project]：项目的身份
```
[project]
name = "daily-brief"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["pypdf", "trafilatura"]
```

也就是：

- 这个项目叫什么
- 版本是多少
- 至少需要什么 Python 版本

#### [build-system]：怎么把它装起来

```
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

它告诉 Python：“如果要把当前项目安装或打包，请使用 `setuptools` 这个工具。”

### pip install -e . 发生了什么
当执行：

```
pip install -e .
```

`pip` 会读取 `pyproject.toml`，用 `setuptools` 安装当前项目，同时安装 `pypdf` 和 `trafilatura` 等依赖。

`-e` 参数，表示可编辑安装：不是把代码复制到 site-packages，而是建一个指向当前目录的链接，改代码立刻生效，不用重装。

对边改边跑的场景特别实用。

### 一句话总结

`requirements.txt` 主要描述“环境里装什么”；`pyproject.toml` 描述“这是一个什么项目，以及怎样安装和构建它”。

### Next action

那么问题来了：`requirements.txt` 和 `pyproject.toml` 是替代关系还是共存关系？