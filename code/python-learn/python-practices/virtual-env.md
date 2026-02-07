# Python virtual environment

当我们使用 pip install 的时候，可能会遇到这样子的问题

```bash
$ pip install flask
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.

    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.

    See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

这是因为错误提示 `externally-managed-environment` 表示当前的 Python 环境是由操作系统或发行版严格管理的（例如 Debian/Ubuntu 等系统使用 apt 管理系统包），pip 默认在这种环境下禁止直接修改系统 Python 库，以防止破坏系统的稳定性。

也就是这个 python 其实是系统 python

### 系统 Python 是什么？

- 系统 Python 是由操作系统（如 Ubuntu、Debian 等）预装的 Python 解释器，通常位于 /usr/bin/python3 或类似的路径。
- 它被操作系统用来运行一些核心功能或工具（比如包管理器、系统脚本等），因此被标记为“受外部管理”（externally managed），不允许随意修改其依赖。



python virtual environment 是一个独立的 Python 运行环境，它包含自己的 Python 解释器和独立的第三方包集合。使用虚拟环境可以让你在同一台机器上创建多个独立的项目环境，避免项目之间的依赖冲突，同时不会污染系统级安装的 Python 及其库。

Python 3.3 以后内置了 `venv` 模块，可以直接使用该模块创建虚拟环境。常见的创建命令为：

```shell
python3 -m venv <venv-name>
```

- `python3`：调用你系统中的 Python 3 解释器。
- `-m venv`：使用 `venv` 模块来创建虚拟环境。
- `venv`：指定虚拟环境的目录名称（这个名称你可以根据项目需要进行更改，例如 `env`、`.venv` 等）。

执行该命令后，会在当前目录下生成一个 `<venv-name>` 文件夹，其中包含以下几个重要子目录：

- bin (或 Scripts, Windows 中)： 存放 Python 解释器和激活脚本。
- lib (或 Lib, Windows 中)： 存放虚拟环境中安装的 Python 包。
- include: 用于存放 C 语言头文件（某些 Python 包在编译时可能会需要）。

#### **激活与退出虚拟环境**

创建好虚拟环境后，需要激活它才能使用该环境内的 Python 和包管理工具（例如 pip）。激活方式根据操作系统不同而有所区别：

**在 Linux/macOS 系统：**

```javascript
source <venv-name>/bin/activate
```

激活后，你会在命令行提示符看到虚拟环境的名称（例如 `(venv)`），这表明你当前已经在虚拟环境中工作。要退出虚拟环境，只需在终端中输入命令：

```shell
deactivate
```

这会让你回到系统默认的 Python 环境。



# Global virtual enviroment

因为我们无法对系统 python 进行操作（比如说是 pip install 命令）所以还是得创建一个 python 虚拟环境

而我们又想让这个 python 虚拟环境下载很多的python package，应用于大部分的项目（就像 anaconda3 base env），这时候需要怎么办呢？应该将这个 venv 放在哪个文件夹呢？

为了方便管理和访问，建议将全局虚拟环境存放在你的 home dir 下。一个常见的做法是使用 `~/.venv` 目录，然后在其中创建一个名为 `base` 的虚拟环境。

如果提示没有 python3-venv, 根据提示下载

```shell
$ python3 -m venv base
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.12-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /home/Plain/.venv/base/bin/python3
```

创建 base python virtual env

```shell
python3 -m venv ~/.venv/base
```

激活 env

```shell
source base/bin/activate
```

为了每次自动激活，我们可以将其写入 `~/.bashrc` 中

```shell
source ~/.venv/base/bin/activate
```

> [!note]
>
> 当然也可以设置命令每次手动启动，在 `~/.bashrc` 中添加 alias
>
> ```shell
> alias activate-base="source ~/.venv/base/bin/activate"
> ```

# VScode python interptreter set

vscode 可能无法主动搜索到这个 python virtual env, 需要手动添加路径，虚拟环境的 Python 解释器位于：

```shell
~/.venv/base/bin/python
```

