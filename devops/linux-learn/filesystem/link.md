# ln 命令

`ln -s` 全称是 link -symbolic，创建符号链接（Symbolic Link）。

简单来说，它的作用是为一个文件或文件夹创建一个“快捷方式”。

它的基本语法如下：

```bash
ln -s [源文件或目录] [链接名字]
```

- `ln`: link 的缩写。
- `-s`: symbolic 的缩写，代表创建的是“软链接”。如果不加 `-s`，默认创建的是“硬链接”（Hard Link）。
- 源文件: 已经存在的、你想要指向的文件。
- 链接名字: 你想要创建的新快捷方式的名字。

对于开发者和 DevOps 工程师来说，`ln -s` 有几个非常经典的使用场景：

1. 配置文件管理（Dotfiles）

   如果把所有的配置文件集中放在一个 Git 仓库里（比如 `~/dotfiles/zshrc`），但系统只会在根目录下找 `.zshrc`。

   这时可以用软链接：

   ```bash
   ln -s ~/dotfiles/zshrc ~/.zshrc
   ```

   这样，当修改 `~/dotfiles/zshrc` 时，系统的配置也会自动生效，而且还可以轻松用 Git 管理它。

2. 软件版本切换

   如果安装了两个版本的 Python：`python3.9` 和 `python3.11`。可以创建一个叫 `python` 的软链接：

   ```bash
   # 指向 3.11 版本
   ln -s /usr/bin/python3.11 /usr/local/bin/python
   ```

   如果想换回旧版本，只需要删掉这个链接，重新指向 3.9 即可，无需修改环境变量。

## 如何识别软链接？

当使用 `ls -l` 查看目录时，软链接会有非常明显的标志：

1. 权限位的第一位是 **`l`**（代表 link）。
2. 文件名后面会有一个箭头 **`->`** 指向源文件。

```text
lrwxrwxrwx 1 hanjie staff 12 Apr 19 13:00 .zshrc -> ~/dotfiles/zshrc
```

## 常用技巧

- 删除软链接: 使用 `rm` 命令即可，例如 `rm k8s-deploy`。注意：这只会删掉“快捷方式”，不会删掉原始文件。
- 强制覆盖: 如果链接名已经存在，可以使用 `ln -sf` (force) 来强制更新链接指向。