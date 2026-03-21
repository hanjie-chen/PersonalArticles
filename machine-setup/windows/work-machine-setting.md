

最近使用 terraform 创建 Azure windows vm, 想要将其设定为工作机器，但是创建出来的机器是一个空白的机器，所以需要给出一个标准的工作机器建设流程

# 工作用 windows machine 设置

软件

1. chrome 浏览器
2. markdown 笔记软件，例如 typora 或者其他
3. vscode 及其插件
4. windows terminal
5. powershell 7
6. python 3
7. git 版本控制
8. 简体中文输入法（microsoft 自带）

custom setting

powershell customerized command and profile

## git安装方法

使用winget 这个 windows 10  自带的包管理工具自动安装git 版本控制

```cmd
winget install --id Git.Git
```

或者

```cmd
winget install Git.Git
```

> [!note]
>
> 如果使用 cmd 安装完成之后，使用 `git --version` 命令显示没有找到，那么新开一个 cmd 或者 powershell 一般就能看到

## python3 安装方法

首先使用命令

```cmd
winget search Python.Python
```

输出如下：

```cmd
C:\Users\Plain>winget search Python.Python
Name        Id                 Version   Source
------------------------------------------------
Python 2    Python.Python.2    2.7.18150 winget
Python 3.0  Python.Python.3.0  3.0.1     winget
Python 3.1  Python.Python.3.1  3.1.4     winget
Python 3.10 Python.Python.3.10 3.10.11   winget
Python 3.11 Python.Python.3.11 3.11.9    winget
Python 3.12 Python.Python.3.12 3.12.9    winget
Python 3.13 Python.Python.3.13 3.13.2    winget
Python 3.2  Python.Python.3.2  3.2.5     winget
Python 3.3  Python.Python.3.3  3.3.5     winget
Python 3.4  Python.Python.3.4  3.4.4     winget
Python 3.5  Python.Python.3.5  3.5.4     winget
Python 3.6  Python.Python.3.6  3.6.8     winget
Python 3.7  Python.Python.3.7  3.7.9     winget
Python 3.8  Python.Python.3.8  3.8.10    winget
Python 3.9  Python.Python.3.9  3.9.13    winget
```

然后选择其中一个python 版本，例如 python 3.12 下载

```cmd
winget install --id Python.Python.3.12 -e
```

### python3 command

此时，只有使用 `python` 命令，可以生效，而 `python3` 命令则是会跳转到 MS store, 让你下载一个新的python 3

这是因为虽然winget 将python 路径添加到 path 中了，但是其中并没有一个可执行文件叫做 `python3` 所以，环境变量其实也不认识什么 python3

为此解决方案是，在 Python 安装目录下手动创建一个符号链接，让 `python3.exe` 指向 `python.exe`

```powershell
New-Item -ItemType SymbolicLink -Path "<python-path>\python3.exe" -Target "<python-path>\python.exe"
```

可以使用如下的命令拿到 `<python-path>`

```shell
PS C:\Users\Plain\articles> pip --version
pip 24.3.1 from C:\Users\Plain\AppData\Local\Programs\Python\Python312\Lib\site-packages\pip (python 3.12)
```

其中 `<python-path>` 就是 `C:\Users\Plain\AppData\Local\Programs\Python\Python312`

## windows terminal 下载方法

首先使用命令

```cmd
winget search "Windows Terminal"
```

输出如下

```cmd
C:\Users\Plain>winget search "Windows Terminal"
Name                     Id                                Version      Source
--------------------------------------------------------------------------------
Windows Terminal         9N0DX20HK701                      Unknown      msstore
Windows Terminal Preview 9N8G5RFZ9XK3                      Unknown      msstore
Windows Terminal         Microsoft.WindowsTerminal         1.22.10352.0 winget
Windows Terminal Preview Microsoft.WindowsTerminal.Preview 1.23.10353.0 winget
```

然后使用命令安装

```cmd
winget install --id Microsoft.WindowsTerminal -e
```



## vscode, chrome 安装方法

在 edge 中下载chrom, vscode