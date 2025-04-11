`mkdir -p` 中的 `-p` 参数是 **`--parents`** 的缩写，意思是：在创建目录时，自动创建其父目录（如果不存在的话）；如果目录已经存在，也不会报错。



### 举个例子：

```bash
mkdir -p /home/user/projects/demo
```

如果你没有 `/home/user/projects` 这个路径，`-p` 就会先帮你创建 `/home/user/projects`，然后再创建 `demo`。而如果这些目录都已经存在，命令也不会出错。



### 如果不加 `-p`：

```bash
mkdir /home/user/projects/demo
```

- 如果 `projects` 目录不存在，这条命令会报错。
- 如果 `demo` 已经存在，这条命令也会报错。



所以 `-p` 非常常用，特别适合写脚本或自动化场景，能避免很多因为目录不存在而失败的情况。