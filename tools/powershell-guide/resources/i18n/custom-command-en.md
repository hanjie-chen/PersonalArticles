---
Title: Personal Windows PowerShell Commands
SourceBlob: a329c20dabea9c6457525ab576c464632f7da097
---

```
BriefIntroduction: Personal Windows PowerShell commands for convenience.
```

<!-- split -->

# How to use these custom commands

Add these commands to the PowerShell `$PROFILE`, and then run `. $PROFILR` to reload the file. After that, you can use these commands.

# Command `open`

It opens a file in a maximized window, but if it opens a folder, it uses the default size.

```powershell
# Custom aliases created by Plain 2024-09-19
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
```

# Command `touch`

It works like the Linux command `touch`. If the file does not exist, it will create one. If the file already exists, it will update the timestamp.

```powershell
# custom command created by Plain 2024-09-23
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
```

# Command `tree`

A Linux-like `tree` command, used to replace PowerShell's native `tree`.

Use `tree -DirectoriesOnly` to show directories only.

Use `tree -Ignore "images", "image"` to ignore some folders.

```powershell
# Linux-like tree command, added by Plain in 2024-11-15
# modified in 2025-04-24, add Ingore parameter
function Show-TreeWithFiles {
    param (
        [string]$Path = ".",
        [string]$Indent = "",
        [bool]$IsLast = $true,
        [switch]$DirectoriesOnly, # 新增参数，使用 switch 类型便于命令行使用
        [string[]]$Ignore  # 新增 Ignore 参数
    )

    # 根据 DirectoriesOnly 参数决定是否只获取目录
    $items = if ($DirectoriesOnly) {
        Get-ChildItem -Path $Path | Where-Object { $_.PSIsContainer }
    } else {
        Get-ChildItem -Path $Path
    }
    # 如果指定 Ignore，过滤掉匹配的文件夹
    if ($Ignore) {
        $items = $items | Where-Object { $Ignore -notcontains $_.Name }
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
            Show-TreeWithFiles -Path $item.FullName -Indent $newIndent -IsLast $isLastItem -DirectoriesOnly:$DirectoriesOnly -Ignore:$Ignore
        }
    }
}

# 创建别名，使用 -Force 参数覆盖原有的 tree 命令
Set-Alias -Name tree -Value Show-TreeWithFiles -Force
```

The colors for the `tree` output:

```powershell
# add by Plain in 2024-10-05
$PSStyle.FileInfo.Directory = "`e[34;1m"  # bule bold for directory
$PSStyle.FileInfo.SymbolicLink = "`e[36;1m" 
$PSStyle.FileInfo.Executable = "`e[32;1m"  # green boldfor exe file

# seeting color for differnet file
$colors = @{
    ".txt" = "`e[33m"  # yellow
    ".log" = "`e[31m"  # red
    ".ps1" = "`e[36m"  
    ".exe" = "`e[32m"  # green
    ".json" = "`e[35m"  
    ".yml" = "`e[35m"  
    ".md" = "`e[33m"   # yellow
}
# apply it to color
foreach ($extension in $colors.Keys) {
    $PSStyle.FileInfo.Extension[$extension] = $colors[$extension]
}
```
