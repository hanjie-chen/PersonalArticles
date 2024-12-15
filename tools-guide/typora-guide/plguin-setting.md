这是我的 typora plugin 使用设置，可以下载 toml 扩展（Even better toml）但是需要为了方式保存的时候自动帮你把注释删除了，需要在 setting.json 中把自动 format 关闭

`Crtil + Shit + P` 打开命令面板，输入 `Preferences: Open User Settings (JSON)` 然后加上

```json
{
    "[toml]": {
        "editor.formatOnSave": false,
        "editor.defaultFormatter": "tamasfe.even-better-toml"
    },
    "evenBetterToml.formatter.alignComments": true,
    "evenBetterToml.formatter.allowedBlankLines": 2,
    "evenBetterToml.formatter.columnWidth": 120
}
```

然后这是我的 `custom_plugin.user.toml` 配置文件 [plain custom file](./assets/toml-file/plain-custom_plugin.user.toml)