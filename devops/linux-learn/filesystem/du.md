# du command

如果我想要检查关于一个文件夹使用了多少存储空间，我们常常 du 命令

du 命令是 disk usage 命令的缩写

查看当前文件夹的大小

```shell
$ du -sh
197M    .
```

- -s (summary): 只显示总计，不列出每个子文件。
- -h (human-readable): 将字节数转换为我们熟悉的 KB、MB 或 GB。

查看当前文件夹下所有项目（文件+文件夹）的大小

```shell
$ du -sh *
4.0K    README.md
700K    __template__
2.9M    cloud-infra
6.8M    code
5.8M    devops
2.9M    machine-setup
42M     personal-growth
8.8M    tools
2.5M    web-dev
```

这里的 `*` 是 Shell 的通配符，它会在执行命令前先展开。

实际上，发送给系统的指令变成了： `du -sh README.md __template__ cloud-infra ...` 系统收到了一个列表，于是它会分别计算列表里每一个项的大小并逐行显示。

> [!note]
>
> 注意：`*` 不会展开 `.` 开头的隐藏文件或隐藏文件夹（比如 `.git` 或 `.env`）
>
> 这是因为在 Unix/Linux 的设计传统中，`*` 的定义就是“匹配当前目录下除隐藏文件外的所有内容”

查看当前文件夹下所有文件夹的大小

```shell
$ du -sh */
700K    __template__/
2.9M    cloud-infra/
6.8M    code/
5.8M    devops/
2.9M    machine-setup/
42M     personal-growth/
8.8M    tools/
2.5M    web-dev/
```

如果我们想要查看当前目录下所有的文件夹大小，包括隐藏的文件夹，那么可以使用 max-depth 参数

```shell
$ du -h --max-depth=1
2.5M    ./web-dev
125M    ./.git
5.8M    ./devops
2.9M    ./machine-setup
42M     ./personal-growth
8.8M    ./tools
2.9M    ./cloud-infra
700K    ./__template__
6.8M    ./code
8.0K    ./.githooks
197M    .
```

如果想要连同文件一起看，那么加一个 `-a` (all) 参数，用于强制显示所有项，包括文件。

```shell
$ du -ah --max-depth=1
2.5M    ./web-dev
125M    ./.git
5.8M    ./devops
4.0K    ./README.md
2.9M    ./machine-setup
42M     ./personal-growth
8.8M    ./tools
2.9M    ./cloud-infra
700K    ./__template__
6.8M    ./code
8.0K    ./.githooks
197M    .
```

