

# Before we begin

如果我们在 windows 环境中打开一个 Linux 脚本文件，并且将其复制到一个 Linux container 中，运行可能出现这样子的问题

```shell
exec /usr/local/bin/init.sh: no such file or directory
```

但是检查这个脚本文件也是存在的，这又是为什么呢？

这里存在一个windows 换行符和linux换行符的问题

# CRLF VS LF

虽然文件存在，并且 shebang 行是正确的 `#!/bin/sh`，但仍然出现错误：

```bash
exec /usr/local/bin/init.sh: no such file or directory
```

问题原因：

这个错误通常是由于脚本文件使用了 **Windows 风格的换行符（CRLF）**，而不是 **Unix/Linux 风格的换行符（LF）**。当脚本文件在 Unix/Linux 系统（如 Alpine Linux）中执行时，如果存在 Windows 的回车符（`\r`），shebang 行 `#!/bin/sh` 会被错误解析为 `#!/bin/sh\r`。系统会尝试寻找解释器 `/bin/sh\r`，但这个路径不存在，因此会报 "no such file or directory" 的错误。

解决方法：

您需要将所有脚本文件的换行符转换为 Unix/Linux 风格的换行符（LF）。以下是具体步骤：

1. **检查脚本文件的换行符：**

   Visual Studio Code (VSCode)：
   - 打开 `init.sh` 文件。
   - 在右下角可以看到当前文件的换行符格式，可能显示为 `CRLF` 或 `LF`
   - 如果是 `CRLF`，点击它并选择 `LF`
   - 保存文件

   

2. **重新构建 Docker 镜像：**

   由于您的 Docker 镜像是在构建时复制了这些脚本文件，您需要在更改文件后重新构建镜像：

   ```bash
   docker-compose build
   ```

   或者在启动容器时加上

   ```
   --build
   ```

   选项：

   ```bash
   docker-compose up --build
   ```

3. **重新启动容器：**

   重新启动您的 Docker 容器，问题应该得到解决。

   ```bash
   docker-compose up
   ```

**附加建议：**

- **配置 Git 处理换行符：**

为了防止将来再次出现此问题，您可以在项目中添加 `.gitattributes` 文件，强制指定脚本文件的换行符为 LF：

```javascript
*.sh text eol=lf
```

这样，当您检出代码时，Git 会自动将 `.sh` 文件的换行符设置为 LF。

- **在编辑器中设置默认换行符：**配置您的文本编辑器，使其默认使用 Unix/Linux 换行符（LF）创建新文件。

总结："no such file or directory" 错误在这种情况下通常不是指文件不存在，而是由于脚本中的换行符导致 shebang 行被错误解析。通过将脚本文件的换行符转换为 Unix/Linux 格式（LF），并重新构建 Docker 镜像，可以解决此问题。如果您还有其他问题或需要进一步的帮助，请随时告诉我。
