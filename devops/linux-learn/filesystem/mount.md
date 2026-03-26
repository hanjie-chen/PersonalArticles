# `mount` & `/mnt`



## `/mnt` directory

在 Linux 文件系统层次结构（FHS - Filesystem Hierarchy Standard）中：

**/mnt**：

专门用于临时挂载文件系统，通常是外部存储设备或网络文件系统



## `mount` usage

#### 基本语法
```bash
mount [-t 文件系统类型] [-o 特殊选项] 设备源 挂载点
```

查看当前所有挂载 `mount -l`

#### 重要参数说明

**-t 文件系统类型**：

```bash
# 常见的文件系统类型
-t ext4      # Linux 标准文件系统
-t ntfs      # Windows NTFS 文件系统
-t vfat      # FAT32 文件系统
-t cifs      # Windows 网络共享
-t nfs       # Network File System
-t iso9660   # CD-ROM 文件系统
```

**-o 挂载选项**：

```bash
# 常用选项
ro          # 只读挂载
rw          # 读写挂载
user        # 允许普通用户挂载
noexec      # 禁止执行文件
sync        # 同步写入
async       # 异步写入
auto        # 允许自动挂载
noauto      # 禁止自动挂载
defaults    # 默认选项（rw,suid,dev,exec,auto,nouser,async）
```

**特殊用法**：

```bash
# 重新挂载为只读
sudo mount -o remount,ro /

# 绑定挂载（将一个目录挂载到另一个位置）
sudo mount --bind /source /destination
```

> ![note] 常见挂载点位置
>
> 除了 /mnt，Linux 系统还有其他特定用途的目录：
>
> ```plaintext
> /           # 根目录
> ├── /mnt    # 临时挂载点
> ├── /media  # 可移动设备自动挂载点
> ├── /dev    # 设备文件
> └── /proc   # 进程信息（虚拟文件系统）
> ```
>

## mount nature

```plaintext
用户空间（User Space）
    │
    ▼
系统调用接口（System Call Interface）
    │
    ▼
虚拟文件系统（VFS）层
    │
    ▼
具体文件系统驱动（ext4, ntfs, cifs等）
    │
    ▼
设备驱动层（Device Driver）
    │
    ▼
硬件层（Hardware）
```

# Practice

使用 mount 命令实现 Linux host 命令行实时访问 Windows host 文件夹

> [!note]
>
> 这里的linux host 和 windows host 在网络可以互通，而且网络环境稳定

首先在 Windows 10 上：

1. 右键要共享的文件夹
2. 选择"属性" -> "共享" -> "高级共享"
3. 勾选"共享此文件夹"
4. 设置权限，建议给予读取权限
5. 记住你的 Windows 用户名和密码

然后在 Linux 服务器上：

```bash
# 1. 首先创建一个挂载点
sudo mkdir /mnt/windows_share

# 2. 安装 cifs-utils（如果没有安装）
# 对于 Ubuntu/Debian：
sudo apt-get install cifs-utils
# 对于 CentOS/RHEL：
sudo yum install cifs-utils

# 3. 挂载共享文件夹
sudo mount -t cifs //WINDOWS_IP/共享文件夹名 /mnt/windows_share -o username=Windows用户名,password=密码

# 4. 复制文件
cp -r /mnt/windows_share/* /你想要存放的目标路径/
```

## mount 命令详解

```bash
sudo mount -t cifs //10.0.1.4/PersonalArticles /mnt/windows-share -o username=Plain,password=xxx
```

**mount**：Linux 的挂载命令

- 用于将文件系统附加到目录树
- 可以挂载本地设备或网络文件系统

**-t cifs**：

- `-t`：指定文件系统类型
- `cifs`：表示使用 CIFS/SMB 协议
- 其他常见的 -t 选项如：
  - `-t ext4`（本地 Linux 文件系统）
  - `-t ntfs`（Windows NTFS 文件系统）
  - `-t nfs`（Network File System）

**//10.0.1.4/PersonalArticles**：

- `//`：网络路径的标准前缀
- `10.0.1.4`：Windows 主机的 IP 地址
- `PersonalArticles`：共享文件夹名称

**/mnt/windows-share**：

- 本地挂载点
- 必须是一个空目录

**-o 选项**：

- `username=Plain`：Windows 用户名
- `password=xxx`：Windows 密码
- 其他常用选项：
  - `vers=3.0`：指定 SMB 协议版本
  - `uid=1000`：指定本地用户 ID
  - `gid=1000`：指定本地组 ID
  - `dir_mode=0755`：设置目录权限
  - `file_mode=0644`：设置文件权限

## 工作原理详解

这个机制的工作原理涉及几个层面：

1. **挂载机制**：
   - 挂载点（/mnt/windows-share）实际上是一个"窗口"或"入口"
   - 它不存储实际数据，而是提供了一个访问远程文件系统的接口
   - 所有对挂载点的操作都会被重定向到远程 Windows 共享

2. **CIFS/SMB 协议**：
   - CIFS (Common Internet File System) 是 SMB (Server Message Block) 协议的一个实现
   - 这是一个网络文件共享协议，允许不同操作系统之间共享文件
   - 当你访问挂载点时，Linux 系统会通过网络向 Windows 发送 CIFS/SMB 请求

3. **网络层面**：
   - 所有文件操作都会转换为网络请求
   - 读取文件时：数据从 Windows 通过网络传输到 Linux
   - 写入文件时：数据从 Linux 通过网络传输到 Windows

实时同步机制

挂载点会实时反映原始文件夹的变化。这是因为挂载点实际上不是在进行文件复制，而是创建了一个直接访问通道。当你：

- 在 Windows 上添加文件 → Linux 挂载点立即可见
- 在 Windows 上删除文件 → Linux 挂载点立即反映
- 在 Windows 上修改文件 → Linux 挂载点立即更新

## 如何持久化挂载

使用mount命令挂载完成之后是临时挂载，只在当前系统运行期间有效，可以通过编辑 `/etc/fstab` 可以实现持久化挂在

### `/etc/fstab` 文件详解

```bash
# 文件格式：
# <file system>        <mount point>      <type>      <options>       						<dump>  <pass>
UUID=xxxxx            /                   ext4        defaults        						 0       1
//10.0.1.4/share      /mnt/windows-share  cifs        credentials=/etc/samba/cred,vers=3.0   0   	 0
```

各字段说明：

`file system`：设备标识（设备名、UUID、网络共享地址等）

`mount point`：挂载点目录

`type`：文件系统类型（ext4, ntfs, cifs 等）

`options`：挂载选项

`dump`：是否备份（0表示不备份）

`pass`：开机时是否检查磁盘（0不检查，1为根目录，2为其他）

### 安全的持久化配置方法

对于网络共享，建议这样配置：

1. **创建凭据文件**：

```bash
sudo mkdir /etc/samba
sudo nano /etc/samba/credentials
```

2. **在凭据文件中添加**：

```
username=Plain
password=your_password
```

3. **设置凭据文件权限**：

```bash
sudo chmod 600 /etc/samba/credentials
```

4. **在 /etc/fstab 中添加**：

```bash
//10.0.1.4/PersonalArticles /mnt/windows-share cifs credentials=/etc/samba/credentials,vers=3.0,iocharset=utf8,file_mode=0777,dir_mode=0777 0 0
```

### 测试和验证

在修改 /etc/fstab 后，建议：

1. **测试配置是否正确**：

```bash
# 测试 fstab 中的配置
sudo mount -a
```

2. **检查挂载状态**：

```bash
# 查看挂载情况
df -h
# 或
mount | grep windows-share
```

