# pytest 基础

一个典型的、好维护的 Python 项目结构通常长这样：

```
my_project/
├── src/                # 源代码
│   └── app.py
├── tests/              # 测试文件夹
│   ├── conftest.py     # 共享配置和 Fixtures
│   ├── test_login.py   # 功能 A 的测试
│   └── test_api.py     # 功能 B 的测试
├── pytest.ini          # pytest 的主配置文件（可选）
└── requirements.txt
```

## conftest.py

接下来说一说 conftest.py 文件

它是 `pytest` 的一个插件机制配置文件。它就像是一个“全局共享站”，放在某个目录下的 `conftest.py` 会被 `pytest` 自动识别，其定义的内容可以被该目录及其子目录下的所有测试文件共享。

example

```python
import os
import sys


TESTS_DIR = os.path.dirname(__file__)
APP_DIR = os.path.abspath(os.path.join(TESTS_DIR, ".."))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
```

**`TESTS_DIR`**: 获取当前 `conftest.py` 所在的目录（通常是 `tests/`）。

**`APP_DIR`**: 找到项目的根目录（即 `tests/` 的上一级），也就是你存放源代码的地方。

**`sys.path.insert(0, APP_DIR)`**: 将项目根目录手动添加到 Python 的搜索路径中最前面。

当你直接运行 `pytest` 时，有时 Python 找不到你的源代码包（比如 `import my_app` 会报错）。这段代码确保了无论你在哪个路径下启动测试，`pytest` 都能正确地“看到”并导入你的应用程序代码。

除此之外，这个文件还可以

#### 1. 共享 Fixtures（最常用的功能）

如果你在 `conftest.py` 中定义了一个 `fixture`，那么所有的测试文件可以直接使用它，而不需要显式导入。

```python
# conftest.py
import pytest

@pytest.fixture
def login_user():
    return {"username": "admin", "access_level": "god_mode"}
```

#### 2. 配置 Hooks（钩子函数）

你可以修改 `pytest` 的运行行为。例如，在测试报告中添加自定义信息，或者根据命令行参数决定运行哪些测试。

#### 3. 加载外部插件

你可以在这里通过 `pytest_plugins = [...]` 来引入其他的插件。

## pytest 机制

打开终端，输入 `pytest` 并敲下回车时，它会执行下面的三个步骤

1. discovery

   先在文件夹里到处看，找出所有符合命名规则（`test_*.py`）的测试用例。

2. Configuration 

   在正式开演前，它会检查目录里有没有 `conftest.py`。如果找到了，那么就先读它。里面通常放的是多个测试文件共享的工具（Fixture）。比如：“所有测试开始前，先连接数据库”。

3. Execution 

   一切就绪，开始一个个运行那些 `test_` 开头的函数。

## test case

简单来说，一个测试用例（test case）就是一段代码，它专门用来验证你的程序在特定情况下的表现是否符合预期。

测试用例：就是那一个以 `test_` 开头的函数。

测试文件：就是那个 `test_xxx.py` 文件，一个文件里可以装几十个测试用例。

测试集 (Test Suite)：当你运行整个 `tests/` 目录时，所有用例加在一起就叫测试集。