# Linux file permission

查看Linux 文件权限的常用命令，一般来说是 `ls -l` e.g.

```shell
$ ls -l
total 12
-rw-r--r-- 1 root root 1561 Jan 17 01:17  articles-sync.log
-rw-r--r-- 1 root root  743 Jan 17 01:17 'articles-sync.log 2>&1'
-rw------- 1 root root 1203 Jan 17 02:00  crond.log
```

输出分析如下

## 文件权限

```
-rw-r--r--
```

这个输出分为4各部分，最开始的第一个字符为第一部分，之后每3个字符为一个部分

`-` part 1 –> 表示文件类型

`rw-` part 2 –> 表示文件所有者权限

`r--` part 3 –> 表示文件所属组权限（文件所有者所在的组）

`r--` part 4 –> 其他用户权限

### 文件类型字符含义

- `-` 表示文件
- `d` 表示文件夹
- `l` 表示链接文件

### 文件权限字符含义

- `r` read permission
- `w` write permission
- `x` execute permission
- `-` none permission

## 其他部分

`1`：硬链接数，表示有多少个文件名指向这个文件。

`root`：文件所有者的用户名。

`root`：文件所属组的组名。

`1561`：文件大小，单位为字节。

`Jan 17 01:17`：文件的最后修改时间。

`articles-sync.log`：文件名。

## 权限判断

当一个进程尝试访问文件时，Linux 会检查该进程的 UID/GID：

- 如果进程的 UID 匹配文件的 UID，则使用 "所有者权限" 进行检查。
- 如果进程的 GID 匹配文件的 GID，则使用 "组权限" 进行检查。
- 否则，使用 "其他用户权限" 进行检查。



# change permision

好的，我看到你的环境是 Linux (Ubuntu)，目前 `logs/` 这个文件夹权限是：

```
drwxrwxr-x
```

- 第一位 `d`：说明是目录（directory）
- `rwxrwxr-x`：
  - `rwx` (owner=Plain)：读/写/执行
  - `rwx` (group=Plain)：读/写/执行
  - `r-x` (others)：读/执行，**没有写权限**

------

### 你的问题是：

> 想要给“其他用户（others）”也赋予读和写权限。

**很简单，用 `chmod` 命令：**

### 直接命令：

```bash
chmod o+rw logs
```

意思是：给 others (`o`) 添加 (`+`) 读(`r`) 和 写(`w`) 权限。

------

### 赋权后，再用 `ls -l` 查看，会变成：

```
drwxrwxrwx 2 Plain Plain 4096 Apr 17 14:26 logs
```

注意到：

- 最后变成了 `rwxrwxrwx`
- 也就是说，**所有人**（owner, group, others）都有读、写、执行权限了。

------

### 小补充（如果你想要递归赋权给里面的文件/子目录）

如果 `logs/` 下面还有很多文件或者子文件夹，而且你也希望它们都获得读写权限，需要加 `-R` 参数（recursive）：

```bash
chmod -R o+rw logs
```

不过要小心，**递归操作**风险更大一点，确认需要这么做才加 `-R`。

------

### 注意事项

- 目录赋 `w` 权限表示别人可以在目录里 **创建、删除** 文件。
- 目录赋 `x` 权限表示别人可以 **进入这个目录**。
- 所以，如果真的很讲究安全，可以考虑根据实际需要只给必要的权限。

------

要不要我顺便也给你讲一下如果想用 `ACL`（Access Control List）更细粒度控制哪些“特定用户”可以访问？
 （比如，只给某个用户写权限，不给所有人）
 👉 要的话告诉我！ACL 很适合生产环境使用。