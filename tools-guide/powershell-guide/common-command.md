# mv command

在 PowerShell 中使用 `mv`（即 `Move-Item`）时，其参数传递方式与 Linux 的 `mv` 命令不同。你需要明确指定 `-Destination` 参数，并将多个源文件以**数组形式**传递给 `-Path`。以下是修复后的命令：

```powershell
mv -Path .\images\, .\apg-metric-explain.md, .\apg-multi-waf.md, .\network-watcher.md -Destination .\network\
```

### 分步说明：
1. **使用 `-Path` 指定多个源文件/目录**：将路径用逗号分隔，形成数组。
2. **明确指定 `-Destination` 参数**：确保目标目录 `.\\network\\` 存在。
3. **注意斜杠方向**：PowerShell 支持 `\` 或 `/`，但建议使用反斜杠 `\` 并转义（或直接使用单引号包裹路径）。

### 简化写法（省略参数名）：
```powershell
mv .\images\, .\apg-metric-explain.md, .\apg-multi-waf.md, .\network-watcher.md .\network\
```
此时第一个位置参数是 `-Path`，第二个是 `-Destination`。

### 错误原因：
- 你未将多个源文件作为数组传递，导致 PowerShell 将第二个文件（`.\\apg-metric-explain.md`）之后的参数误认为无效位置参数。
- PowerShell 的 `Move-Item` 默认只接受一个 `-Path` 和一个 `-Destination`，多源需显式用数组或逗号分隔。

### 验证目标目录：
确保目标目录 `.\\network\\` 存在。若不存在，先创建：
```powershell
New-Item -ItemType Directory -Path .\network\
```