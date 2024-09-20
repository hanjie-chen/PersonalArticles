# Add alias for a command

## Temporary

use the command in the powershell `Set-Alias -Name open -Value start` 

the command `open` will have the same effect with `start`, but it only will be effective at this PS process.

## Permanent

add it to the `$PROFILE` and it will work permanently, for example:

```ps1
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
Set-Alias -Name open -Value start
```



