# Powershell 7 downlaod and setting

下载参考这篇文章[快速提高生产力——Power Shell也能命令提示并自动补全_安装最新的powershell,了解新功能和改进-CSDN博客](https://blog.csdn.net/m0_63230155/article/details/134685660)

首先powershell 7的启动速度比windows powershell快上不少

安装完毕之后会存在几个问题，逐一解决

# 加载Python 环境

如果使用anaconda 3创建的python环境，还需要使用命令`conda init powershell`来激活一些设定，否则anaconda 3的某些路径无法正确的载入Powershell 7的环境变量中，可以使用`echo $env:PATH` 来查看powershell 7的环境变量。可以拿来和正常的windows powershell进行对比。

或许某些conda命令可以运行，比如说`conda env list`，当然最重要的是能否运行激活python环境的命令`conda activate xxx`如果不行的话，那么就按照以上的步骤进行

# 颜色加载问题

当第一次使用powershell 7的时候，文件夹会有蓝色的背景颜色，有人已经提过了github issue: https://github.com/PowerShell/PowerShell/issues/18550

解决方案是自定义颜色在`$PROFILE`中

```powershell
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

效果如下：

![powershell-file-display-color](./images/file-color-example.png)



