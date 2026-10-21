## background

当我们在一台 ubuntu server 中使用 pip install 命令的时候，可能会遇到这样子的报错

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

这表示当前的 Python 环境是由操作系统或发行版严格管理的（例如 Debian/Ubuntu 等系统使用 apt 管理系统包），pip 默认在这种环境下禁止直接修改系统 Python 库，防止破坏系统的稳定性。

也就是说这个 python 其实是系统专用的，我们不能动它

## Python virtual environment

为了解决这个问题，可以使用 python virtual environment，创建一个独立的 Python 运行环境。

Python 3.3 以后内置了 `venv` 模块，可以直接使用该模块创建虚拟环境。常见的创建命令为：

```shell
python3 -m venv <path/to/venv>
```

- `-m venv`：使用 `venv` 模块来创建虚拟环境。
- `<path/to/venv-name>`：指定虚拟环境的路径

执行该命令后，会在对应路径下生成一个 `<venv-name>` 文件夹。

### 激活与退出

创建好虚拟环境后，需要激活它才能使用该环境内的 Python 和包管理工具（例如 pip）。

在 Linux/macOS 系统：

```javascript
source <venv-name>/bin/activate
```

激活后，你会在命令行提示符看到虚拟环境的名称（例如 `(venv)`），这表明你当前已经在虚拟环境中工作。要退出虚拟环境，只需在终端中输入命令：

```shell
deactivate
```

这会让你回到系统默认的 Python 环境。

### best practice

为了方便，可以将全局虚拟环境存放在的 home dir 下。使用 `~/.venv` 目录，然后在其中创建虚拟环境。

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

### vscode setting

vscode 可能无法主动搜索到这个 python virtual env, 需要手动添加路径，虚拟环境的 Python 解释器位于：

```shell
~/.venv/base/bin/python
```

