---
RolloutDate: 2024-09-19
---

# PowerShell Custom Commands

![cover](./resources/images/cover_image.webp)

## Profile Source of Truth

这些 custom commands 来自我的 PowerShell `$PROFILE`。

现在 `$PROFILE` 不再直接作为知识库文章维护，而是由 [personal-config](https://github.com/hanjie-chen/personal-config) 统一管理。实际代码维护在：

```text
personal-config/powershell/Microsoft.PowerShell_profile.ps1
```

本机的 PowerShell 7 profile 通过 symbolic link 指向这个文件：

```text
$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

因此，这篇文章只记录这些命令的用途和常见用法，不再复制完整实现。需要修改实现时，应修改 `personal-config` 中的 profile 文件。

## Command `open`

`open` 用来从 PowerShell 打开文件或目录。

打开目录时，它会使用 Windows Explorer；打开文件时，它会尽量模拟从 Explorer 双击文件的行为，避免某些 GUI app 因为仍然附着在 Windows Terminal session 上而在终端关闭后一起退出。

常见用法：

```powershell
open .
open .\notes.md
open .\some-folder
```

我通常用它来快速打开当前目录、Markdown 文件，或者需要用默认 app 查看和编辑的文件。

## Command `touch`

`touch` 模拟 Linux 中的 `touch` 命令。

如果文件不存在，它会创建一个新文件；如果文件已经存在，它会更新文件的 `LastWriteTime`。

常见用法：

```powershell
touch note.md
touch .env
touch a.txt b.txt
```

这个命令适合用在临时创建文件、初始化 Markdown 笔记、或者快速刷新文件时间戳的时候。

## Command `tree`

`tree` 用来显示当前目录下的文件树。

它会覆盖 PowerShell 原本的 `tree` command，并支持一些更适合日常使用的参数，例如只显示目录，或者忽略指定目录。

常见用法：

```powershell
tree
tree -DirectoriesOnly
tree -Ignore "resources", "images"
```

其中 `-DirectoriesOnly` 只显示目录，`-Ignore` 用来跳过不想看的目录或文件名。

这个命令还会配合 `$PSStyle.FileInfo` 给目录、symbolic link、executable file 和部分常见文件扩展名设置颜色，让目录结构更容易扫描。
