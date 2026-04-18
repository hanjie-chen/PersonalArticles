---
Title: Codex App Reconnect Issue Caused by Clash Rules on Windows
SourceBlob: 024c979cdb05d71687774cd82327e81ed2f107db
---

```
BriefIntroduction: While using the Codex app on Windows 10, I kept running into a `reconnecting` issue. It would only start thinking after failing five times. I had Codex analyze it, and it finally got fixed after burning through half of the 128k context window. The conclusion was that the Clash rules were not written correctly and the traffic was falling through to `GEOIP` matching, so I’m documenting it here.
```

<!-- split -->

# Issue Description

When using Codex in a Windows 10 environment, it frequently gets stuck on `reconnect` before it can successfully start thinking.

# Root Cause

In the Clash subscription rules currently in use, there is:

```yaml
- GEOIP,CN,DIRECT
- MATCH,⚓️其他流量
```

The problem is:

1. Some DNS resolution results for `chatgpt.com` or `chat.openai.com` may be incorrectly identified as `CN`
2. Once they hit `GEOIP,CN,DIRECT`, the request is sent directly
3. After the direct connection times out, Codex starts behaving like it is repeatedly `reconnect`ing

In other words, the traffic-splitting rules are not precise enough.

# Resolution

In the currently active subscription file, place the OpenAI-related domain rules before `GEOIP,CN,DIRECT`. The core rules are as follows:

```yaml
- DOMAIN-SUFFIX,chatgpt.com,⚓️其他流量
- DOMAIN-SUFFIX,openai.com,⚓️其他流量
- DOMAIN-SUFFIX,oaistatic.com,⚓️其他流量
- DOMAIN-SUFFIX,oaiusercontent.com,⚓️其他流量
```

This ensures that `chatgpt.com`, `chat.openai.com`, `ab.chatgpt.com`, `oaistatic.com`, and `oaiusercontent.com` all go through the proxy first instead of falling through to `GEOIP,CN,DIRECT`.

However, if we manually update the subscription, those manual rules will be overwritten. So we added an extra manual auto-repair solution.

We wrote a PowerShell script and placed it at: `C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules.ps1`

Its purpose is to:

1. Find the currently active Clash profile
2. Automatically check whether the OpenAI rules exist
3. If they are missing, reinsert them before `GEOIP,CN,DIRECT`
4. Generate the runtime configuration currently used for execution
5. Hot-reload Clash

Then we added the following PowerShell command to the PowerShell profile:

```powershell
# manually repair Clash OpenAI rules after updating subscriptions
function Fix-ClashOpenAIRules {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.config\clash\codex-maintain-openai-rules.ps1"
}

Set-Alias -Name clash-fix-openai -Value Fix-ClashOpenAIRules
```

This way, after manually updating the Clash subscription, we can run the `clash-fix-openai` command to write those rules back in.

# Troubleshooting

If `reconnect` shows up again later, how do you check whether the OpenAI rules are still there and whether the script is working?

Check in the following order:

1. Whether Clash is running and the local port `127.0.0.1:7890` is still listening
2. Whether the OpenAI rules are still present in the current profile
3. Whether the Clash logs show that the DomainSuffix rules were matched

```powershell
$log = Get-ChildItem "$env:USERPROFILE\.config\clash\logs" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

Select-String -Path $log.FullName -Pattern "chatgpt.com|chat.openai.com|DomainSuffix\(chatgpt.com\)|DomainSuffix\(openai.com\)|GeoIP\(CN\)"
```

If you see:

```text
rule=DomainSuffix(chatgpt.com)
rule=DomainSuffix(openai.com)
```

that means OpenAI requests are going through the rules we added.

If you see:

```text
rAddr=chatgpt.com:443 ... rule=GeoIP(CN) proxy=DIRECT
```

then the old problem has returned.

# PowerShell Scripts

Main maintenance script PowerShell code

File: `C:\Users\Windows 10\.config\clash\codex-maintain-openai-rules.ps1`

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
