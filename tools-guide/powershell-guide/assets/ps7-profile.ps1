
# 基础系统文件
$PSStyle.FileInfo.Directory = "`e[34;1m"     # 蓝色加粗 - 目录
$PSStyle.FileInfo.SymbolicLink = "`e[36;1m"  # 青色加粗 - 符号链接
$PSStyle.FileInfo.Executable = "`e[32;1m"    # 绿色加粗 - 可执行文件

# 文件扩展名颜色配置
$colors = @{
    # 文本和文档
    ".txt" = "`e[33m"      # 黄色 - 普通文本
    ".md" = "`e[33m"       # 黄色 - Markdown
    ".log" = "`e[31m"      # 红色 - 日志文件
    ".pdf" = "`e[31;1m"    # 红色加粗 - PDF文档
    ".doc" = "`e[31;1m"    # 红色加粗 - Word文档
    ".docx" = "`e[31;1m"   # 红色加粗 - Word文档
    
    # 代码文件
    ".py" = "`e[36m"       # 青色 - Python
    ".ps1" = "`e[36m"      # 青色 - PowerShell
    ".sh" = "`e[32m"       # 绿色 - Shell脚本
    ".cpp" = "`e[32m"      # 绿色 - C++
    ".c" = "`e[32m"        # 绿色 - C
    ".h" = "`e[32m"        # 绿色 - 头文件
    ".java" = "`e[31m"     # 红色 - Java
    ".js" = "`e[33m"       # 黄色 - JavaScript
    ".css" = "`e[36m"      # 青色 - CSS
    ".html" = "`e[33m"     # 黄色 - HTML
    ".ipynb" = "`e[36m"    # 青色 - Jupyter Notebook
    
    # 配置文件
    ".json" = "`e[32m"     # 绿色 - JSON
    ".yml" = "`e[32m"      # 绿色 - YAML
    ".yaml" = "`e[32m"     # 绿色 - YAML
    ".xml" = "`e[32m"      # 绿色 - XML
    ".ini" = "`e[32m"      # 绿色 - INI配置
    ".conf" = "`e[32m"     # 绿色 - 配置文件
    
    # 图片文件
    ".jpg" = "`e[32;1m"    # 绿色加粗 - 图片
    ".jpeg" = "`e[32;1m"   # 绿色加粗 - 图片
    ".png" = "`e[32;1m"    # 绿色加粗 - 图片
    ".gif" = "`e[32;1m"    # 绿色加粗 - 图片
    ".bmp" = "`e[32;1m"    # 绿色加粗 - 图片
    ".webp" = "`e[32;1m"   # 绿色加粗 - 图片
    
    # 压缩文件
    ".zip" = "`e[31m"      # 红色 - 压缩文件
    ".tar" = "`e[31m"      # 红色 - 压缩文件
    ".gz" = "`e[31m"       # 红色 - 压缩文件
    ".7z" = "`e[31m"       # 红色 - 压缩文件
    ".rar" = "`e[31m"      # 红色 - 压缩文件
    
    # 系统和库文件
    ".dll" = "`e[32m"      # 绿色 - 动态链接库
    ".sys" = "`e[32m"      # 绿色 - 系统文件
    ".msi" = "`e[32m"      # 绿色 - 安装包
}
# apply it to color
foreach ($extension in $colors.Keys) {
    $PSStyle.FileInfo.Extension[$extension] = $colors[$extension]
}

# Custom aliases add by Plain 2024-09-19
function Open-Smart {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Path
    )

    $Path = Resolve-Path $Path

    if (Test-Path -Path $Path -PathType Container) {
        # It's a folder, open with normal size
        Start-Process -FilePath "explorer.exe" -ArgumentList $Path
    } else {
        # It's a file, open maximized
        Start-Process -FilePath $Path -WindowStyle Maximized
    }
}

# Set alias 'open' for the custom function
Set-Alias -Name open -Value Open-Smart

# custom command add by Plain 2024-09-23
function Touch-File {
    param(
        [Parameter(Mandatory=$true, Position=0, ValueFromPipeline=$true)]
        [string[]]$Path
    )

    foreach ($file in $Path) {
        if (Test-Path -Path $file) {
            # File exists, update its timestamp
            (Get-Item $file).LastWriteTime = Get-Date
            Write-Host "Updated timestamp: $file"
        }
        else {
            # File doesn't exist, create it
            New-Item -ItemType File -Path $file | Out-Null
            Write-Host "Created new file: $file"
        }
    }
}

Set-Alias -Name touch -Value Touch-File

# Linux-like tree command, added by Plain in 2024-11-15
function Show-TreeWithFiles {
    param (
        [string]$Path = ".",
        [string]$Indent = "",
        [bool]$IsLast = $true,
        [switch]$DirectoriesOnly # 新增参数，使用 switch 类型便于命令行使用
    )

    # 根据 DirectoriesOnly 参数决定是否只获取目录
    $items = if ($DirectoriesOnly) {
        Get-ChildItem -Path $Path | Where-Object { $_.PSIsContainer }
    } else {
        Get-ChildItem -Path $Path
    }
    
    $count = $items.Count
    $current = 0

    foreach ($item in $items) {
        $current++
        $isLastItem = ($current -eq $count)
        $prefix = if ($Indent -eq "") {
            if ($isLastItem) { "└───" } else { "├───" }
        } else {
            if ($isLastItem) { "$Indent└───" } else { "$Indent├───" }
        }

        # 使用 Write-Host 的 -NoNewline 参数来分段输出
        Write-Host "$prefix" -NoNewline

        # 使用 $PSStyle.FileInfo 的颜色设置
        if ($item.PSIsContainer) {
            # 目录使用 Directory 的颜色设置
            Write-Host ($PSStyle.FileInfo.Directory + $item.Name + $PSStyle.Reset)
        } else {
            # 文件使用对应扩展名的颜色设置
            $extension = $item.Extension.ToLower()
            $colorCode = $PSStyle.FileInfo.Extension[$extension]
            if ($colorCode) {
                Write-Host ($colorCode + $item.Name + $PSStyle.Reset)
            } else {
                # 如果没有定义颜色，使用默认颜色
                Write-Host $item.Name
            }
        }

        if ($item.PSIsContainer) {
            $newIndent = if ($Indent -eq "") {
                if ($isLastItem) { "    " } else { "│   " }
            } else {
                if ($isLastItem) { "$Indent    " } else { "$Indent│   " }
            }
            Show-TreeWithFiles -Path $item.FullName -Indent $newIndent -IsLast $isLastItem -DirectoriesOnly:$DirectoriesOnly
        }
    }
}

# 创建别名，使用 -Force 参数覆盖原有的 tree 命令
Set-Alias -Name tree -Value Show-TreeWithFiles -Force