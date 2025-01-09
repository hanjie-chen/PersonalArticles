# Git Hooks

Git Hooks 是 Git 中的脚本机制，允许您在 Git 仓库中某些事件发生前后自动执行自定义脚本。它们可以帮助您自动化工作流程、执行代码质量检查、强制执行提交规范等。

Git Hooks 分为两类：

1. **Client-side Hooks**：在本地仓库中执行，响应诸如提交、合并、推送等操作。常用于代码格式化、代码检查、提交信息验证等。
2. **Server-side Hooks**：在远程仓库（服务器）上执行，响应诸如接收推送、更新引用等操作。常用于强制执行提交策略、触发持续集成等。

# `./git/hooks` dir

Git Hooks 存储在每个仓库的 `.git/hooks` 目录中。默认情况下，这个目录包含一些示例脚本，以 `.sample` 结尾

```powershell
PS C:\Users\Plain\PersonalArticles\.git\hooks> ls

    Directory: C:\Users\Plain\PersonalArticles\.git\hooks

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---            1/8/2025  2:33 AM            478 applypatch-msg.sample
-a---            1/8/2025  2:33 AM            896 commit-msg.sample
-a---            1/8/2025  2:33 AM           4726 fsmonitor-watchman.sample
-a---            1/8/2025  2:33 AM            189 post-update.sample
-a---            1/8/2025  2:33 AM            424 pre-applypatch.sample
-a---            1/8/2025  2:33 AM           1649 pre-commit.sample
-a---            1/8/2025  2:33 AM            416 pre-merge-commit.sample
-a---            1/8/2025  2:33 AM           1374 pre-push.sample
-a---            1/8/2025  2:33 AM           4898 pre-rebase.sample
-a---            1/8/2025  2:33 AM            544 pre-receive.sample
-a---            1/8/2025  2:33 AM           1492 prepare-commit-msg.sample
-a---            1/8/2025  2:33 AM           2783 push-to-checkout.sample
-a---            1/8/2025  2:33 AM           2308 sendemail-validate.sample
-a---            1/8/2025  2:33 AM           3650 update.sample
```

这些示例脚本都是可供参考的模板。如果您想要启用某个钩子，只需移除 `.sample` 扩展名，并确保脚本具有可执行权限

e.g.

我想要检查图片文件中后缀名均为小写，如果是大写的话，将其变为小写

### 服务器端钩子

如果您管理自己的 Git 服务器，可以使用服务器端钩子来强制执行更严格的策略。例如，禁止提交包含特定关键字的代码，或在接收到推送后自动部署代码。**注意**：如果您使用的是托管的 Git 平台（如 GitHub、GitLab 等），通常无法自定义服务器端钩子。但这些平台提供了 Webhooks、CI/CD 集成等功能，可以达到类似的目的。

# 在项目中共享 Git Hooks

默认情况下，Git Hooks 不会被添加到版本控制中，即其他克隆该仓库的用户不会自动获得您的钩子脚本。为了解决这个问题，我们可以将钩子脚本存储在仓库中并设置 hooksPath

在仓库中创建一个目录存放钩子脚本

```bash
mkdir .githooks
```

将您的钩子脚本移动到该目录：

```bash
mv .git/hooks/pre-commit .githooks/pre-commit
```

告诉 Git 使用自定义的 hooks 目录：

```bash
git config core.hooksPath .githooks
```

将钩子目录添加到版本控制：

```bash
git add .githooks
git commit -m "Add git hooks"
```

这样一来，其他开发者在克隆仓库后，也会获得钩子脚本。



