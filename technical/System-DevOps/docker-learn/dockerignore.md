# `.dockerignore`

.dockerignore 文件的主要作用是在构建 Docker 镜像时，告诉 Docker 引擎哪些文件和目录应该被忽略，不要被复制到镜像中。这与 .gitignore 文件的概念类似。

主要优点和作用：

1. **提高构建效率**
   - 减少构建上下文的大小
   - 加快镜像构建速度
   - 减少不必要的缓存失效

2. **减小镜像体积**
   - 排除不需要的文件和目录
   - 避免将敏感信息打包进镜像

3. **增加安全性**
   - 防止敏感文件（如 .env、密钥文件等）被意外包含
   - 避免将开发环境的文件打包到生产环境

常见的 .dockerignore 配置示例：

```plaintext
# 版本控制相关
.git
.gitignore
.svn

# 开发环境文件
node_modules
npm-debug.log
yarn-debug.log
yarn-error.log

# 编辑器配置文件
.vscode
.idea
*.swp
*.swo

# 环境配置文件
.env
.env.local
.env.*

# 文档和测试文件
README.md
docs
test
tests

# 日志文件
*.log
logs

# 临时文件
tmp
temp
```

使用注意事项：

1. **语法规则**：

   - 支持通配符 * 和 ?
   - 支持 ! 来否定之前的规则
   - 每行一个规则
   - 规则匹配是相对于构建上下文的根目录

2. **常见模式**：

   ```plaintext
   # 忽略所有 .txt 文件
   *.txt
   
   # 但是保留 important.txt
   !important.txt
   
   # 忽略根目录下的 temp 文件夹
   /temp
   
   # 忽略所有目录下的 temp 文件夹
   **/temp
   ```

3. **最佳实践**：

   - 将 .dockerignore 文件放在 Dockerfile 所在的目录
   - 定期审查和更新忽略规则
   - 确保不会意外排除必要的文件
   - 在构建前检查构建上下文大小

使用 .dockerignore 文件可以让你的 Docker 镜像构建过程更加高效、安全，并且生成的镜像更加精简。建议在所有 Docker 项目中都使用这个文件来管理构建上下文。