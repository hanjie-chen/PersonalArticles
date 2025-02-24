# PersonalArticles

这个仓库用于存放我写的文章，打算在 github 中存储我的网站文章

我的个人网站会从这个 github repository 中获取所有文章

# file organize

然后再说一说文件组织形式，其中 assets 文件夹是我存放各种 resource 的地方，比如说 images 资源或者其他的一些配置文件等

# Special directory

`.<folder-name>` 格式的文件夹不会再出现在 Typora 的目录中，`__<folder-name>__` 格式的文件夹会出现在 Typora 的目录中

这正是我想要的，因为我需要查看 `__template__` 的文章模板，而 `.githooks` 只需要运行就可以了

## `__template__` folder

根路径下的  `__template__` 文件夹是存放文章模板的地方

## `.githooks` folder

这是我存放关于这个仓库的 git hooks, 目前只有 1 个，那就是在 git commit 之前检查是否存在后缀名是大写的图片文件，如果存在，那么将后缀名小写

# Repository config

enable case sensitive [Windows only]

```shell
git config core.ignorecase false
```

configure git hooks path [python3 environment require]

```shell
git config core.hooksPath .githooks
```

> 必须可以在命令行中可以运行 python3 –version 命令，而且输出不为空 e.g.
>
> ```clearshell
> PS > python3 --version
> Python 3.12.8
> ```
