# 创建用户

```shell
# 创建用户（系统会提示你设置密码和个人信息）
sudo adduser yourname
# 授予 Sudo 权限
sudo usermod -aG sudo yourname
```



# 查看当前用户权限

要查看当前用户是否具有 root 权限，您可以使用几种方法。我会为您解释最常用的几种方法：

1. 使用 `id` 命令：
   这个命令可以显示当前用户的 ID 信息，包括用户 ID (UID) 和组 ID (GID)。

   ```
   id
   ```

   如果输出中显示 `uid=0(root)`，那么当前用户就是 root 用户。

2. 使用 `whoami` 命令：
   这个命令会显示当前登录的用户名。

   ```
   whoami
   ```

   如果输出是 "root"，那么当前用户就是 root 用户。

3. 检查 `$UID` 变量：
   在 Bash shell 中，`$UID` 变量存储了当前用户的 ID。root 用户的 UID 始终为 0。

   ```
   echo $UID
   ```

   如果输出是 0，那么当前用户就是 root 用户。

4. 使用 `sudo` 命令测试：
   如果当前用户有 sudo 权限（可以使用 sudo 执行命令），那么他们就可以获得 root 权限。

   ```
   sudo -v
   ```

   如果命令执行成功（没有报错），那么当前用户有 sudo 权限。

5. 尝试访问只有 root 用户才能访问的目录：
   ```
   ls /root
   ```

   如果可以列出 /root 目录的内容，那么当前用户就是 root 用户或具有 root 权限。

请注意，即使当前用户不是 root 用户，他们也可能通过 sudo 或其他方式获得 root 权限。在进行需要 root 权限的操作时，建议使用 sudo 命令，而不是直接登录为 root 用户，这样可以提高系统的安全性。

如果您需要更多关于 Linux 权限管理的信息，请随时告诉我。

# Root 用户和root权限

在 Linux 系统中，严格意义上来说：

1. 真正的 root 用户只有一个：
   - UID (用户ID) 为 0 的用户就是 root 用户
   - 这个 root 账户是系统唯一的超级管理员账户
   - 用户名不一定非要叫 "root"，但 UID 为 0 的就是超级管理员

2. 但是可以有多个具有 root 权限的用户：
   有几种方式可以让普通用户获得 root 权限：

   a) 通过 sudo 权限：
   - 将用户添加到 sudo 组（Ubuntu）或 wheel 组（CentOS）
   - 编辑 `/etc/sudoers` 文件，授予特定用户 sudo 权限
   ```bash
   # 使用 visudo 命令编辑 sudoers 文件
   visudo
   
   # 或者将用户添加到 sudo 组
   usermod -aG sudo username
   ```

   b) 通过 SUID 权限：
   - 让特定程序以 root 权限运行
   - 普通用户执行这些程序时具有临时的 root 权限

3. 安全建议：
   - 不建议创建多个 UID 为 0 的账户
   - 推荐使用 sudo 机制来管理需要 root 权限的操作
   - 日常使用建议使用普通用户账户，需要时再通过 sudo 提升权限
   - 这样可以：
     * 保留操作记录
     * 更好地控制权限范围
     * 提高系统安全性

4. 查看具有 sudo 权限的用户：
   ```bash
   # 查看 sudo 组的成员
   getent group sudo
   
   # 或者查看 wheel 组的成员（在 CentOS 中）
   getent group wheel
   
   # 查看 sudoers 文件
   sudo cat /etc/sudoers
   ```

5. **实际应用示例**：
   ```bash
   # 创建新用户并授予 sudo 权限
   sudo useradd -m newuser           # 创建新用户
   sudo passwd newuser               # 设置密码
   sudo usermod -aG sudo newuser     # 将用户添加到 sudo 组
   ```

总结：
- 真正的 root 用户（UID=0）只有一个
- 但是可以有多个具有 root 权限的用户（通过 sudo）
- 从安全角度考虑，建议：
  * 使用 sudo 机制管理权限
  * 避免直接使用 root 账户
  * 严格控制具有 sudo 权限的用户数量

这种设计既保证了系统的安全性，又提供了足够的灵活性来进行系统管理。

# 切换用户

在 Linux 中，你可以通过 `su` 或 `sudo` 命令从 `root` 用户切换到普通用户。以下是几种常用方法

### 方法一：使用 `su` 命令（最常见）

```bash
su - username
```

- `-` 表示载入该用户的登录环境（和登录后一样的环境）。
- 如果你是 root，执行这条命令时**不会要求密码**（除非设置了额外限制）。
- 退出该用户可以输入 `exit`

