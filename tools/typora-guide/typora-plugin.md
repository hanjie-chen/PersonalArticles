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

一般来说我引用图片的方式是使用相对路径，比如说我在 Article_Template.md 中使用 `./images/cover_image.jpeg` 来引用图片

但是当我想要引用其他的文章的时候，我想要使用基于基于仓库根目录的绝对路径，比如说我引用 Git 使用指南这篇文章，则是 `/tools-guide/git-guide/Git使用.md` 

这 2 个方式在 github 上面是同时生效的 [test](/tools-guide/git-guide/git-usage.md)

但是我阅读了 [Typora Links](https://support.typora.io/Links) 文章，其中这个格式含义则实际上是去找了系统根路径，而不是项目根路径，例如在这篇文档提供的示例中

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

于是直接乐不思蜀，抛下这个问题，开始研究 typora plugin 一顿操作狠狠的配置，结果发现大部分我似乎都用不上，不过少部分还是有点意思的

在我配置 plugin 的过程中遇到了一个问题，那就是 vscode 似乎会自动对比 default.toml 文件和 user.toml 文件然后自动删除 user.toml 文件中重复的部分，这浪费我大量的时间，结果也没有找到解决方案，遂放弃

回到正题，我在配置插件的过程中尝试了这个插件，效果让我并不满意，因为这个插件的作用仅仅针对 image 有效，和在 YAML 中添加 `typora-root-url` 的效果是相同

[Images in Typora - Typora Support](https://support.typora.io/Images/#display-images-in-relative-path)

已经提了这个 issue 了：[[Feature\] consider file link start with `/` as absolute path base on repository dir like github · Issue #6194 · typora/typora-issues](https://github.com/typora/typora-issues/issues/6194)

蹲一手吧