# ansible

Ansible 是一款 配置管理（Configuration Management） 工具。

想象一下：如果你有 100 台服务器，老板要求你在所有服务器上安装 Nginx 并修改一个小小的配置。

- 传统做法： 你得登录 100 次，敲 100 次命令。
- Ansible 做法： 你写一个名为 `playbook.yml` 的文本文件，告诉 Ansible “去把这 100 台机器装上 Nginx”，然后按一下回车，它就自动帮你搞定了。

Terraform = 基础建设（打地基、盖楼房）

它负责向阿里云、AWS 等云厂商申请资源。比如：我要 3 台虚拟机、1 个数据库、1 个负载均衡。

Ansible = 装修（刷漆、拉电线、买家具）

当 Terraform 把虚拟机开好后，Ansible 进场。它负责：安装 Docker、部署你的 Java 代码、设置防火墙规则。

## 基础

Ansible 的核心思想是“声明式”：你不需要告诉它“怎么做”（比如先敲什么命令，再敲什么命令），你只需要描述“最终状态是什么”（比如：Nginx 必须是安装好且启动的状态）。

要把 Ansible 跑起来，通常只需要这三个核心文件：

### 1. Inventory（清单）

告诉 Ansible “去哪儿”，这是一个简单的文本文件（通常叫 `hosts`），列出你要管理的服务器 IP 或域名。你可以把它们分组，比如“开发机”和“生产机”。

```toml
[web_servers]
192.168.1.10
192.168.1.11

[db_servers]
192.168.1.20
```

### 2. Playbook（剧本）

告诉 Ansible “做什么”，这是最核心的部分，用 YAML 格式编写。它规定了在哪些机器上执行什么任务。

**举个例子：一个简单的部署 Nginx 的剧本 `deploy_nginx.yml`**

```yaml
---
- name: 配置 Web 服务器并安装 Nginx
  hosts: web_servers  # 对应 Inventory 里的组名
  become: yes         # 使用 sudo 权限执行
  
  tasks:
    - name: 确保 Nginx 已经安装
      apt:            # 调用 apt 模块（适用于 Ubuntu/Debian）
        name: nginx
        state: present

    - name: 启动 Nginx 服务并设置开机自启
      service:
        name: nginx
        state: started
        enabled: yes
```

### 3. Modules（模块）

Ansible 的“工具箱”，你看到的 `apt`、`service`、`copy`、`shell` 都是 Module。Ansible 自带了上千个模块，几乎涵盖了所有运维操作。你不需要写复杂的脚本，只需要调用对应的模块并传入参数。

### 实际操作流程

1. 准备环境： 在你的控制节点（比如你的电脑或跳板机）上安装 Ansible。被管理端只要有 Python 和 SSH 就行。

2. 测试连接： 使用 `ping` 模块看看能不能通（这不是网络 ping，而是测试 Ansible 能否连接并执行 Python）：

   ```bash
   ansible all -m ping -i hosts
   ```

3. **运行剧本：**

   直接执行你写好的 Playbook：

   ```bash
   ansible-playbook -i hosts deploy_nginx.yml
   ```

### 进阶用法：Roles（角色）

当你管理的项目变大时，把所有代码写在一个 YAML 里会很乱。这时候你会用到 **Roles**。

它就像是代码的模块化封装。你可以把“安装 Docker”写成一个 Role，把“配置数据库”写成一个 Role。以后新项目需要 Docker，直接一行代码引用这个 Role 即可，非常适合大型 DevOps 项目的维护。

## 安装 ansible

ansible 只需要安装在你的“控制机”上，不需要安装在“被管理的服务器”上。

这也是 Ansible 最迷人的地方（Agentless / 无代理）。你只需要在你的笔记本电脑，或者一台专门用来发号施令的“跳板机”上安装即可。

### 1. 哪里需要安装？哪里不需要？

- 控制节点 (Control Node)： 你的工作电脑（Linux 或 macOS）。Ansible 运行在这里。
  - 注：Windows 目前不能直接作为控制节点，但可以通过 WSL2 (Windows Subsystem for Linux) 完美运行。
- 受控节点 (Managed Nodes)： 你的那些云服务器、虚拟机或树莓派。
  - 不需要安装 Ansible。
  - 只需要有：1. SSH 服务；2. Python (现在的 Linux 镜像基本自带)。

### 2. 怎么安装？（以 Linux 环境为例）

因为你之后可能会在 Ubuntu 环境下实操，安装过程非常简单：

#### 在 Ubuntu / Debian 上：

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

#### 在 macOS 上（使用 Homebrew）：

```bash
brew install ansible
```

### 3. 安装完后怎么验证？

装完之后，敲一下这个命令看看有没有反应：

Bash

```
ansible --version
```

你会看到版本号、配置文件路径以及它使用的 Python 版本。

------

### 4. 关键：如何让“控制机”控制“受控机”？

既然不需要在服务器上装软件，Ansible 怎么控制它们呢？**靠 SSH 免密登录。**

1. **生成密钥：** 在你的控制机上执行 `ssh-keygen`。

2. **分发密钥：** 把公钥传给你的服务器：

   Bash

   ```
   ssh-copy-id user@your_server_ip
   ```

3. **大功告成：** 只要你能不用密码直接 SSH 连上服务器，Ansible 就能替你接管它。