# 项目文件命名规范

在软件开发中，特别是处理文件系统时，命名规范显得尤为重要。全小写命名已经成为现代开发中的最佳实践之一。

## 为什么使用全小写？

### 1. 跨平台兼容性

- **Windows vs Unix-like系统**
  - Windows：大小写不敏感
  - Linux/Unix/macOS：大小写敏感
  - 示例：`Images/` 和 `images/` 在 Linux 上是不同目录，而在 Windows 上是相同的

### 2. URL友好性

- 网址通常使用小写是一种默认约定
- 更易读和记忆
- 示例：
  ```
  # 推荐
  example.com/my-project/docs
  
  # 不推荐
  example.com/My-Project/Docs
  ```

### 3. 命令行操作便利性

- 无需使用Shift键
- 减少输入错误
- 提高操作效率

### 4. Git版本控制考虑

- Git默认大小写敏感
- Windows上的Git可能出现大小写重命名问题
- 示例：
  ```bash
  # 这种重命名在Windows上可能产生问题
  git mv Images images
  ```

## 命名规范建议

### 1. 目录命名

```
# 推荐的命名方式
my-project/
  ├─ docs/
  ├─ images/
  ├─ src/
  └─ README.md

# 不推荐的命名方式
My-Project/
  ├─ Docs/
  ├─ Images/
  ├─ Src/
  └─ README.md
```

### 2. 特殊情况例外

某些特定文件可以使用大写：

- `README.md`
- `LICENSE`
- `Dockerfile`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

## 最佳实践

1. **使用连字符分隔单词**
   ```
   # 推荐
   user-guide/
   system-setup/
   
   # 不推荐
   userGuide/
   SystemSetup/
   ```

2. **避免使用空格和特殊字符**
   ```
   # 推荐
   project-docs/
   
   # 不推荐
   project docs/
   project_docs/
   ```

3. **使用有意义的描述性名称**
   ```
   # 推荐
   user-authentication/
   
   # 不推荐
   auth/
   ```

## 实际应用示例

将现有项目结构规范化：

```
# 原始结构
MyProject/
  ├─ SourceCode/
  ├─ Documentation/
  └─ TestFiles/

# 规范化后
my-project/
  ├─ src/
  ├─ docs/
  └─ tests/
```

## 结论

采用全小写命名不仅是一种编码规范，更是一种防御性编程实践。它能帮助我们避免跨平台开发中的各种潜在问题，提高代码的可维护性和可移植性。

## 参考资料

- [Google Style Guide](https://google.github.io/styleguide/)
- [npm naming guidelines](https://docs.npmjs.com/cli/v8/configuring-npm/package-json#name)
- [Git documentation](https://git-scm.com/docs)