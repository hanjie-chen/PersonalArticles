---
Title: Windows Clash 与 Codex/OpenAI 连接问题排查笔记
Author: 陈翰杰
Instructor: Codex
RolloutDate: 2026-03-21
---

```
BriefIntroduction:
记录一次 Windows + Clash + Codex/OpenAI 的代理排查过程。
重点包括问题现象、根因分析、修复方法、长期自动修复方案，以及后续如何停用或排查。
```

<!-- split -->

# Windows Clash 与 Codex/OpenAI 连接问题排查笔记

## 问题现象

在 Windows 10 环境中使用 Codex 时，频繁出现 `reconnect`。

表面上看像是：

1. Codex 没有走代理
2. Clash 没有正确接管 OpenAI 请求
3. 系统代理开着，但应用仍然不稳定

后续检查发现，真正的问题不是 “完全没走代理”，而是 `chatgpt.com` / `chat.openai.com` 的部分连接被 Clash 规则误判成了直连。

## 根因

当前使用的 Clash 订阅规则里，存在：

```yaml
- GEOIP,CN,DIRECT
- MATCH,⚓️其他流量
```

问题在于：

1. `chatgpt.com` 或 `chat.openai.com` 的某些解析结果会被错误识别到 `CN`
2. 一旦命中 `GEOIP,CN,DIRECT`，请求会被直连
3. 直连超时之后，Codex 就会表现成反复 `reconnect`

也就是说，问题不是代理完全没开，而是分流规则不够精确。

## 一次性修复方案

在当前活动订阅文件中，把 OpenAI 相关域名规则放到 `GEOIP,CN,DIRECT` 前面。

核心规则如下：

```yaml
- DOMAIN-SUFFIX,chatgpt.com,⚓️其他流量
- DOMAIN-SUFFIX,openai.com,⚓️其他流量
- DOMAIN-SUFFIX,oaistatic.com,⚓️其他流量
- DOMAIN-SUFFIX,oaiusercontent.com,⚓️其他流量
```

这样可以确保：

1. `chatgpt.com`
2. `chat.openai.com`
3. `ab.chatgpt.com`
4. `oaistatic.com`
5. `oaiusercontent.com`

都优先走代理，而不是落到 `GEOIP,CN,DIRECT`。

## 长期方案

问题在于：订阅一更新，这些手工规则可能会被覆盖。

所以我额外做了一个长期自动修复方案。

### 1. 自动维护脚本

文件：

`C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules.ps1`

作用：

1. 找到当前活动的 Clash profile
2. 自动检查 OpenAI 规则是否存在
3. 如果缺失，则在 `GEOIP,CN,DIRECT` 前重新插入
4. 生成当前运行用的 runtime 配置
5. 热重载 Clash

### 2. 后台守护脚本

文件：

`C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules-daemon.ps1`

作用：

1. 后台常驻
2. 每 5 分钟执行一次维护脚本
3. 防止订阅更新后规则再次丢失

### 3. Windows 登录启动项

文件：

`C:\Users\Windows 10\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\codex-maintain-openai-rules.cmd`

作用：

1. 在登录 Windows 后自动启动后台守护脚本
2. 不是在打开 Codex 时才运行
3. 也不是只在打开 Clash 时才运行

也就是说：

只要登录 Windows，这个守护就会起来。

## 当前运行逻辑

当前逻辑可以理解成：

1. 登录 Windows
2. Startup 启动项触发
3. 后台守护脚本启动
4. 守护脚本每 5 分钟检查一次 Clash 当前活动配置
5. 如果 OpenAI 规则缺失，就自动补回并重载 Clash

## 可复现脚本

前面的说明解决了 “为什么这样做”，这一节解决 “如何完整复现”。

下面给出的是当前实际可工作的脚本版本。

### 1. 主维护脚本

文件：

`C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules.ps1`

```powershell
$ErrorActionPreference = "Stop"

$clashRoot = Join-Path $env:USERPROFILE ".config\clash"
$profilesDir = Join-Path $clashRoot "profiles"
$generalConfig = Join-Path $clashRoot "config.yaml"
$profilesList = Join-Path $profilesDir "list.yml"
$runtimeConfig = Join-Path $profilesDir "codex-active-runtime.yml"
$utf8 = [System.Text.UTF8Encoding]::new($false)

$startMarker = "  # codex-openai-rules-start"
$endMarker = "  # codex-openai-rules-end"

function Get-GeneralValue {
    param(
        [string[]]$Lines,
        [string]$Key
    )

    foreach ($line in $Lines) {
        if ($line -match "^\s*$([regex]::Escape($Key)):\s*(.+?)\s*$") {
            return $Matches[1]
        }
    }

    return $null
}

function Get-MatchProxyName {
    param(
        [System.Collections.Generic.List[string]]$Lines
    )

    foreach ($line in $Lines) {
        if ($line -match '^\s*-\s*MATCH,(.+?)\s*$') {
            return $Matches[1]
        }
    }

    throw "Could not determine fallback proxy name from MATCH rule"
}

function Read-Utf8Text {
    param(
        [string]$Path
    )

    return [System.IO.File]::ReadAllText($Path, $utf8)
}

function Read-Utf8Lines {
    param(
        [string]$Path
    )

    return [System.IO.File]::ReadAllLines($Path, $utf8)
}

function Write-Utf8Lines {
    param(
        [string]$Path,
        [string[]]$Lines
    )

    [System.IO.File]::WriteAllLines($Path, $Lines, $utf8)
}

function Update-ProfileRules {
    param(
        [string]$Path
    )

    $lines = [System.Collections.Generic.List[string]]::new()
    foreach ($line in Read-Utf8Lines -Path $Path) {
        [void]$lines.Add($line)
    }

    $geoIndex = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^\s*-\s*GEOIP,CN,DIRECT\s*$') {
            $geoIndex = $i
            break
        }
    }

    if ($geoIndex -lt 0) {
        return $false
    }

    $startIndex = $lines.IndexOf($startMarker)
    if ($startIndex -ge 0) {
        $endIndex = $lines.IndexOf($endMarker)
        if ($endIndex -ge $startIndex) {
            $lines.RemoveRange($startIndex, $endIndex - $startIndex + 1)
            if ($startIndex -lt $geoIndex) {
                $geoIndex -= ($endIndex - $startIndex + 1)
            }
        }
    }

    $proxyName = Get-MatchProxyName -Lines $lines
    $managedBlock = @(
        $startMarker,
        "  - DOMAIN-SUFFIX,chatgpt.com,$proxyName",
        "  - DOMAIN-SUFFIX,openai.com,$proxyName",
        "  - DOMAIN-SUFFIX,oaistatic.com,$proxyName",
        "  - DOMAIN-SUFFIX,oaiusercontent.com,$proxyName",
        $endMarker
    )

    for ($i = 0; $i -lt $managedBlock.Count; $i++) {
        $lines.Insert($geoIndex + $i, $managedBlock[$i])
    }

    Write-Utf8Lines -Path $Path -Lines $lines
    return $true
}

function Get-ActiveProfilePath {
    param(
        [string]$ListPath,
        [string]$ProfilesRoot
    )

    $raw = Read-Utf8Text -Path $ListPath
    $indexMatch = [regex]::Match($raw, '(?m)^index:\s*(\d+)\s*$')
    if (-not $indexMatch.Success) {
        throw "Could not find active profile index in $ListPath"
    }

    $selectedIndex = [int]$indexMatch.Groups[1].Value
    $entries = [regex]::Matches($raw, '(?m)^\s*(?:-\s*)?time:\s*(.+?)\s*$') |
        ForEach-Object { $_.Groups[1].Value }

    if ($selectedIndex -ge $entries.Count) {
        throw "Active profile index $selectedIndex is out of range"
    }

    return Join-Path $ProfilesRoot $entries[$selectedIndex]
}

function Build-RuntimeConfig {
    param(
        [string]$SourcePath,
        [string]$DestinationPath,
        [string]$Controller,
        [string]$Secret
    )

    $lines = Read-Utf8Lines -Path $SourcePath
    $updated = foreach ($line in $lines) {
        if ($line -match '^log-level:') {
            "log-level: info"
        }
        elseif ($line -match '^external-controller:') {
            "external-controller: $Controller"
        }
        elseif ($line -match '^secret:') {
            "secret: $Secret"
        }
        else {
            $line
        }
    }

    Write-Utf8Lines -Path $DestinationPath -Lines $updated
}

function Reload-ActiveConfig {
    param(
        [string]$Controller,
        [string]$Secret,
        [string]$ConfigPath
    )

    $body = @{ path = $ConfigPath } | ConvertTo-Json
    Invoke-RestMethod `
        -Headers @{ Authorization = "Bearer $Secret" } `
        -Uri "http://$Controller/configs?force=true" `
        -Method Put `
        -ContentType "application/json" `
        -Body $body | Out-Null
}

if (-not (Test-Path $generalConfig)) {
    throw "Missing Clash general config: $generalConfig"
}

if (-not (Test-Path $profilesList)) {
    throw "Missing Clash profile list: $profilesList"
}

$generalLines = Read-Utf8Lines -Path $generalConfig
$controller = Get-GeneralValue -Lines $generalLines -Key "external-controller"
$secret = Get-GeneralValue -Lines $generalLines -Key "secret"

if (-not $controller) {
    throw "Missing external-controller in $generalConfig"
}

if ($null -eq $secret) {
    $secret = ""
}

$profileFiles = Get-ChildItem $profilesDir -Filter *.yml |
    Where-Object {
        $_.Name -notin @("list.yml", "codex-active-runtime.yml") -and
        $_.Name -notlike "*.codex-merged.yml"
    }

foreach ($profile in $profileFiles) {
    $raw = Read-Utf8Text -Path $profile.FullName
    if ($raw -match '(?m)^rules:\s*$' -and $raw -match '(?m)^\s*-\s*GEOIP,CN,DIRECT\s*$') {
        Update-ProfileRules -Path $profile.FullName | Out-Null
    }
}

$activeProfile = Get-ActiveProfilePath -ListPath $profilesList -ProfilesRoot $profilesDir
Build-RuntimeConfig -SourcePath $activeProfile -DestinationPath $runtimeConfig -Controller $controller -Secret $secret
Reload-ActiveConfig -Controller $controller -Secret $secret -ConfigPath $runtimeConfig
```

### 2. 后台守护脚本

文件：

`C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules-daemon.ps1`

```powershell
$ErrorActionPreference = "Stop"

$mutex = New-Object System.Threading.Mutex($false, "Local\CodexClashOpenAIRulesDaemon")
$hasHandle = $false

try {
    $hasHandle = $mutex.WaitOne(0, $false)
    if (-not $hasHandle) {
        exit 0
    }

    $scriptPath = Join-Path $env:USERPROFILE ".config\clash\codex-maintain-openai-rules.ps1"
    $logPath = Join-Path $env:USERPROFILE ".config\clash\codex-maintain-openai-rules.log"

    while ($true) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        try {
            Add-Content -Path $logPath -Value "[$timestamp] start"
            & $scriptPath *>> $logPath
            Add-Content -Path $logPath -Value "[$timestamp] exit 0"
        }
        catch {
            Add-Content -Path $logPath -Value "[$timestamp] error: $($_.Exception.Message)"
        }

        Start-Sleep -Seconds 300
    }
}
finally {
    if ($hasHandle) {
        $mutex.ReleaseMutex() | Out-Null
    }

    $mutex.Dispose()
}
```

### 3. Windows 启动项

文件：

`C:\Users\Windows 10\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\codex-maintain-openai-rules.cmd`

```cmd
@echo off
start "" /min powershell.exe -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\.config\clash\codex-maintain-openai-rules-daemon.ps1"
```

### 4. 手工触发方式

如果不想等登录自动启动，也可以手工执行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.config\clash\codex-maintain-openai-rules.ps1"
```

或手工启动后台守护：

```powershell
powershell.exe -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.config\clash\codex-maintain-openai-rules-daemon.ps1"
```

## 额外代理环境变量

还设置了用户级环境变量：

```powershell
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=socks5://127.0.0.1:7891
NO_PROXY=localhost,127.0.0.1
```

作用：

1. 让命令行工具更容易继承代理
2. 降低某些 CLI 工具或子进程不走代理的概率

## 这次处理中踩到的坑

中间出现过一次 Clash 节点中文名乱码。

原因不是 Clash 本身坏掉，而是：

1. Windows PowerShell 对 UTF-8 脚本里的中文/emoji 字面量支持不稳定
2. 手工维护脚本里如果直接写 `⚓️其他流量` 这种分组名，可能被错误编码
3. 结果会把 profile 文件写成乱码

后面已经修正为：

1. 不再在脚本里硬编码中文/emoji 分组名
2. 改成从当前 profile 的 `MATCH,...` 规则里动态读取实际代理组名

这样稳定性会高很多。

## 如果以后想停用这个自动方案

最直接的方式是删除 Windows 启动项：

`C:\Users\Windows 10\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\codex-maintain-openai-rules.cmd`

如果想彻底清理，也可以一并删除：

1. `C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules.ps1`
2. `C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules-daemon.ps1`
3. `C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules.log`

## 如果以后又出现 reconnect

建议按下面顺序检查：

1. Clash 是否已启动，且本地端口 `127.0.0.1:7890` 仍在监听
2. 当前活动 profile 中是否还保留 OpenAI 规则
3. Clash 日志里是否出现：

```text
rule=DomainSuffix(chatgpt.com)
rule=DomainSuffix(openai.com)
```

如果看到的是：

```text
rule=GeoIP(CN) proxy=DIRECT
```

说明规则又被覆盖了，优先检查自动维护脚本是否还在运行。

## 结论

这次问题的本质，不是 “Codex 不支持代理”，而是：

1. Clash 分流规则对 OpenAI 域名不够精确
2. `GEOIP,CN,DIRECT` 误伤了 OpenAI 连接
3. 误判直连后引发超时和 `reconnect`

修复的核心就是：

给 OpenAI 域名单独加规则，并且保证这些规则优先于 `GEOIP,CN,DIRECT`。
