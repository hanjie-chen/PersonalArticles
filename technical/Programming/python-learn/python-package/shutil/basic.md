#### shutil模块

**shutil**是Python标准库中的一个高级文件操作模块,提供了一些用于文件和目录管理的实用功能。它的名字是"shell utilities"的缩写,意为shell工具。shutil模块提供的主要功能包括:

1. **文件复制和移动**:使用`shutil.copy()`, `shutil.copy2()`, `shutil.copyfile()`, `shutil.move()`等函数可以复制或移动文件和目录。
2. **目录树操作**:使用`shutil.copytree()`可以递归复制目录树,`shutil.rmtree()`可以删除整个目录树。
3. **文件权限管理**:使用`shutil.copymode()`, `shutil.copystat()`可以复制文件的权限和元数据信息。
4. **文件和目录的高级操作**:使用`shutil.disk_usage()`可以获取磁盘使用情况,`shutil.which()`可以在系统PATH中查找可执行文件。
5. **打包和压缩**:shutil提供了创建和读取压缩包(zip, tar等)的功能,如`shutil.make_archive()`, `shutil.unpack_archive()`等。

下面是一些使用shutil的代码示例:复制文件:

```python
import shutil

shutil.copy("src.txt", "dest.txt")  # 复制文件
shutil.copy2("src.txt", "dest.txt")  # 复制文件,同时复制元数据
```

移动文件或目录:

```python
import shutil

shutil.move("src.txt", "dst_dir/")  # 移动文件到另一个目录
```

删除目录树:

```python
import shutil

shutil.rmtree("dir_to_remove")  # 删除整个目录树
```

总的来说,shutil提供了方便的高级文件操作功能,使得在Python中处理文件和目录变得更加简单。它是Python标准库的一部分,无需额外安装即可使用。希望这个介绍对你有所帮助!如果你还有任何问题,欢迎随时问我。



# `shutil.rmtree()` function

#### shutil.rmtree()函数

`shutil.rmtree()`函数的功能与Linux/Unix系统中的`rm -rf`命令非常相似,它会递归地删除指定目录下的所有文件和子目录,最后删除目录本身。函数语法:

python



```python
shutil.rmtree(path, ignore_errors=False, onerror=None)
```

参数说明:

- `path`:要删除的目录路径。
- `ignore_errors`(可选):如果设为True,删除失败时会忽略错误继续删除。默认为False,遇到错误时会引发异常。
- `onerror`(可选):指定错误处理函数,当`ignore_errors`参数为False时,你可以提供此回调函数来处理删除操作中遇到的错误。

使用示例:

```python
import shutil

shutil.rmtree("dir_to_remove")  # 删除"dir_to_remove"目录及其所有内容
```

#### 注意事项

- `shutil.rmtree()`是一个非常强大的函数,使用时需要格外小心,因为它会永久删除文件和目录,删除后无法恢复。
- 在删除重要数据之前,请务必仔细检查路径是否正确,以免误删。
- 如果要删除的目录非常大或包含大量文件,删除操作可能会花费一些时间。
- 在某些情况下,如果文件或目录正在被其他程序使用,删除操作可能会失败并引发异常。可以使用`ignore_errors`或`onerror`参数来处理这种情况。

总之,`shutil.rmtree()`函数的功能与`rm -rf`命令非常相似,都是递归删除目录及其所有内容。使用时需要格外小心,以免误删重要数据。