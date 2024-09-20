---
Title: Personal Windows PS Command
Author: 陈翰杰
Instructor: Sonnet 3.5
CoverImage: ./image/cover_image.jpg
RolloutDate: 2024-09-19
UltimateModifiedDate:
Category: windows/windows command/windows powershell

---

```
BriefIntroduction: 
personal windows powershell command, for my convinence
```

<!-- split -->



# Personal Windows `$PROFILE`

I write down some use command for my convinence, here is my `$PROFILE` source code

```powershell
oh-my-posh init pwsh --config $env:POSH_THEMES_PATH\robbyrussell.omp.json | Invoke-Expression
cls
# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
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
```



# Command `open`

it will open a file with maximized windows, but if it open a folder, it use default size.

```powershell
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
```

