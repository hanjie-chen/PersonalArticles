因为在使用 Typora 的时候遇到一个问题，那就是我想要使用基于仓库根目录的绝对路径，为了兼容 github 上面的格式，因为我文章路径比较深，如果使用相对路径去引用其他地方的文章则不太合适，而且为了我正在开发的网站考虑，使用基于仓库根目录的绝对路径更适合我操作。

例如说我的这是我的 github 项目根目录

```perl
C:\Users\Plain\PersonalArticles
```

这是我的部分文章：

```perl
PS C:\Users\Plain\PersonalArticles
├───personal-growth
...
├───template
│   ├───images
│   │   └───cover_image.jpeg
│   └───Article_Template.md
├───tools-guide
│   ├───git-guide
│   │   ├───images
│   │   │   └───cover_image.png
│   │   └───Git使用指南.md
...
└───README.md
```

一般来说我引用图片的方式是使用相对路径，比如说我在Article_Template.md中使用`./images/cover_image.jpeg` 来引用图片

但是当我想要引用其他的文章的时候，我想要使用基于基于仓库根目录的绝对路径，比如说我引用Git使用指南这篇文章，则是 `/tools-guide/git-guide/Git使用指南.md` 

这2个方式在github上面是同时生效的

但是我阅读了 [Typora Links](https://support.typora.io/Links) 文章，其中并没有这个格式，只有如下格式

```markdown
[Readme1](Readme1.md)

[Readme2](../Docs/Readme2.markdown)

[Readme3](Readme3)

[Readme4](/User/root/Docs/Readme1.md)

[Readme4](C:/Develop/Docs/Readme1.md)

[Readme4](file:///User/root/Docs/Readme1.md)

```

后来我发现了这个 issue: [兼容 obsidian 的基于库根目录的绝对路径 · Issue #259 · obgnail/typora_plugin](https://github.com/obgnail/typora_plugin/issues/259) 似乎存在一个 typora-plugin 的解决方案，于是打开了 typora plugin 的新大陆

[obgnail/typora_plugin: Typora plugin. Feature enhancement tool | Typora 插件，功能增强工具](https://github.com/obgnail/typora_plugin)