# `~` VS `/home/username`

你的理解是对的！这两个路径在特定条件下确实指向相同的位置。让我来解释一下：

1. `/home/Plain/Personal_Project/Test_Articles_Data` 是绝对路径
2. `~/Personal_Project/Test_Articles_Data` 是使用了波浪号（~）的相对路径

这里的 `~` 符号是一个特殊符号，它代表当前用户的主目录（home directory）。在 Unix/Linux 系统中：

- 如果你的用户名是 "Plain"，那么 `~` 就会自动展开为 `/home/Plain`
- 所以 `~/Personal_Project/Test_Articles_Data` 实际上会被系统解释为 `/home/Plain/Personal_Project/Test_Articles_Data`

需要注意的是：
1. 这种等价关系只在你的用户名确实是 "Plain" 时才成立
2. `~` 符号的展开是由 shell 完成的
3. 在某些编程语言或应用程序中，可能需要手动展开 `~` 符号

这种使用 `~` 的方式很常用，因为：
- 更简短，便于输入
- 更通用，不同用户可以使用相同的路径表示
- 不需要硬编码完整的主目录路径