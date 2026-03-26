`chown` 命令的全称是 change owner，用于更改文件或目录的所有者（Owner）和所属组（Group）

## `chown` 命令详解

`chown` 主要用于修改文件或目录的所有者和所属组，常见语法如下：

```bash
chown [option] [user]:[group] file/dir
```

其中：

- `user` 指定新的文件所有者，可以是用户名或 UID。
- `group` 指定新的用户组，可以是组名或 GID（可以省略）。
- `file/dir` 指定要修改的文件或目录。

### 常见用法

#### **（1）更改文件的所有者**

```bash
chown user1 myfile.txt
```

将 `myfile.txt` 的所有者更改为 `user1`，组不变。

#### **（2）更改文件的所有者和组**

```bash
chown user1:group1 myfile.txt
```

将 `myfile.txt` 的所有者更改为 `user1`，并将组更改为 `group1`。

#### **（3）只更改文件的组**

```bash
chown :group1 myfile.txt
```

将 `myfile.txt` 的组更改为 `group1`，所有者保持不变。

#### **（4）递归更改目录及其子文件的所有者**

```bash
chown -R user1:group1 /home/user1/projects
```

更改 `/home/user1/projects` 目录及其中所有文件的所有者为 `user1`，组为 `group1`。

#### **（5）使用 `--reference` 选项**

```bash
chown --reference=otherfile myfile.txt
```

将 `myfile.txt` 的所有者和组更改为 `otherfile` 的所有者和组。





## linux file 默认权限

通常，当我们在 Linux 中创建文件时，默认权限是 `rw-r--r--` (`chmod 644`)，也就是说会让所有者拥有 `rw-` 权限，这样所有者就可以读写

```bash
touch file2
ls -l file2
# -rw-r--r-- 1 user1 group1 0 Apr 3 12:00 file2
```

这时，如果运行：

```bash
chown user2:group2 file2
```

然后切换到 `user2`，你会发现 `user2` 仍然可以读写文件（因为 `644` 允许所有者读写）。

