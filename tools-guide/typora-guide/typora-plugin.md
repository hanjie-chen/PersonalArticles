因为在使用 Typora 的时候遇到一个问题，那就是我想要使用基于仓库根目录的绝对路径，为了兼容 github 上面的格式，因为我文章路径比较深，所以使用相对路径不太合适，而且为了我正在开发的网站考虑，使用基于仓库根目录的绝对路径更适合我操作。但是我阅读了 [Typora Links](https://support.typora.io/Links) 文章，其中并没有这个格式，只有如下格式

```markdown
[Readme1](Readme1.md)

[Readme2](../Docs/Readme2.markdown)

[Readme3](Readme3)

[Readme4](/User/root/Docs/Readme1.md)

[Readme4](C:/Develop/Docs/Readme1.md)

[Readme4](file:///User/root/Docs/Readme1.md)

```

后来我发现了这个 issue: [兼容obsidian的基于库根目录的绝对路径 · Issue #259 · obgnail/typora_plugin](https://github.com/obgnail/typora_plugin/issues/259) 似乎存在一个typora-plugin的解决方案，于是打开了 typora plugin 的新大陆

[obgnail/typora_plugin: Typora plugin. Feature enhancement tool | Typora 插件，功能增强工具](https://github.com/obgnail/typora_plugin)