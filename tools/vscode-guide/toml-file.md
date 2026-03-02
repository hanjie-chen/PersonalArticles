这是我的 typora plugin 使用设置，可以下载 toml 扩展（Even better toml）但是需要为了方式保存的时候自动帮你把注释删除了，需要在 setting.json 中把自动 format 关闭

`Crtil + Shit + P` 打开命令面板，输入 `Preferences: Open User Settings (JSON)` 然后加上

然后这是我的 `custom_plugin.user.toml` 配置文件 [plain custom file](./assets/toml-file/plain-custom_plugin.user.toml)

这里保留一份副本

他妈的，我发现 vscode 插件 even better toml 会自动对比 user.toml 和 default.toml 文件，发现一样的地方会直接删除，例如这个

我的 user.toml 文件

```toml
############### kanban ###############
[kanban]
# 是否启用此二级插件
enable = false
# 插件名称
name = "Kanban"
# 是否在右键菜单中隐藏
hide = false
# 在右键菜单中的出现顺序（越大越排到后面，允许负数）
order = 1
# 代码块语言
# 强烈建议不要修改。如果要修改，请跟着修改TEMPLATE选项里的语言
LANGUAGE = "kanban"
# 严格模式：不会忽略存在语法错误的代码行，直接在页面上报错（此选项用于控制所有看板，如果设置为true，那么会强制所有看板进入严格模式）
# 也可以在代码块首行添加use strict，使得此代码块进入严格模式
STRICT_MODE = false
# 开启交互模式（处于交互模式下，鼠标点击图表并不会展开代码块）
INTERACTIVE_MODE = true
# 当描述为空时隐藏描述框
HIDE_DESC_WHEN_EMPTY = true
# 看板最大高度（单位：px）（若<0，则显示全部）
KANBAN_MAX_HEIGHT = 700
# 看板的宽度（单位：px）
KANBAN_WIDTH = 250
# 看板任务描述框的最大高度（单位：em）（若<0，则显示全部）
KANBAN_TASK_DESC_MAX_HEIGHT = -1
# 当看板数量太多时是否换行显示
WRAP = false
# 当鼠标位于看板时，ctrl+wheel滚动看板
CTRL_WHEEL_TO_SCROLL = true
# 允许在描述框使用markdown内联样式（code、strong、em、del、link、img）
ALLOW_MARKDOWN_INLINE_STYLE = true
# 看板框的颜色（请保持 KANBAN_COLOR 和 TASK_COLOR 数量一致，否则颜色会乱套，就不好看了）
KANBAN_COLOR = ["#FFE0B2", "#DAE9F4", "#FEDCCC", "#C6E5D9", "#FFF1B9"]
# 任务框的颜色
TASK_COLOR = ["#FFFDE7", "#F8FAFF", "#FFFFF2", "#FFFCF0", "#FFFFF5"]
# 省略后续代码
...
```

直接给我删的只剩下

```toml
[kanban]
enable = false
KANBAN_COLOR = [ "#FFE0B2", "#DAE9F4", "#FEDCCC", "#C6E5D9", "#FFF1B9" ]
TASK_COLOR = [ "#FFFDE7", "#F8FAFF", "#FFFFF2", "#FFFCF0", "#FFFFF5" ]
```

奶奶的，没有注释我怎么看得懂啊，只能问下Sonnet 3.5 把这个功能禁用了，才能维持的了生活这个样子

~~这个功能做得很好，但是别做了~~

不过回头想想看，似乎也是有道理的，只保留修改过的值，可以保持配置文件简洁，只显示真正需要覆盖的值。关键在于我对配置文件不熟啊，下次再用吧dd

这似乎是 vsocde 行为，而不是even better toml 这个插件的行为，妈的，等一会我再来找你算账