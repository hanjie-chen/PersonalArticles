在 Linux 的 Bash（或 zsh）中，默认使用的是 Readline 的快捷键配置，而不是像 Windows Terminal 那样使用 Ctrl+Backspace。常用的删除单词快捷键有：

- **Ctrl+W**：删除光标前的一个单词。例如，在输入命令 `mkdir somefile` 时，如果光标位于 `somefile` 后面，按下 Ctrl+W 就能删除整个 `somefile` 单词，而不必一个字符一个字符删除。
- **Alt+D**：删除光标后面的一个单词，从光标当前位置删除到下一个空格为止。

如果你习惯 Windows 中的 Ctrl+Backspace，也可以尝试修改终端的键盘映射（例如编辑 ~/.inputrc 文件）来实现类似的效果，但默认情况下 Linux 不会将 Ctrl+Backspace 映射为删除单词。

citeturn0search0 citeturn0search6