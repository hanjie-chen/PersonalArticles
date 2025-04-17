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