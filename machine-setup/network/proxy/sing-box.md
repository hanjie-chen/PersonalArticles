因为发现使用 hysteria 2 官方提供的 client 需要预热一段时间（大概10分钟）才能使用，于是打算 sing-box

前往 [Releases · SagerNet/sing-box](https://github.com/SagerNet/sing-box/releases) 下载 `windows-amd64` 的最新版本

特别注意，有一个名字特别相似的就在他的下方，叫做 `arm64` tmd 就差了一个字母，我看了好半天也没有看出来

正确区别如下：

| filename                            | architecture         | system                                                       | size    |
| ----------------------------------- | -------------------- | ------------------------------------------------------------ | ------- |
| `sing-box-1.11.7-windows-amd64.zip` | AMD64（也叫 x86_64） | 大多数现代 Windows PC（包括 Intel 和 AMD 处理器）            | 11.9 MB |
| `sing-box-1.11.7-windows-arm64.zip` | ARM64                | 仅适用于 ARM 架构 Windows（如 Surface Pro X 或其他 ARM 芯片设备） | 10.6 MB |

这里顺便讲下如何检查 Windows 系统架构：

1. 按下 `Win + R`，输入 `msinfo32` 回车。
2. 查看系统摘要中的系统类型：
   - `x64-based PC` → 你应该下载 `amd64`
   - `ARM-based PC` → 你才需要 `arm64`

