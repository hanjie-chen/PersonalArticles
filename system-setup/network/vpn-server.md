在Azure上创建一台Linux Ubuntu虚拟机来充当VPN服务器，你可以按照以下步骤进行设置：

#### 1. 在Azure门户中创建一个Ubuntu虚拟机

#### 2. 配置虚拟机的网络设置

- 将虚拟机放置在一个合适的虚拟网络和子网中。
- 配置一个公共IP地址，以便从Internet访问该虚拟机。
- 配置网络安全组（NSG）规则，允许必要的端口，如PPTP（TCP 1723）、L2TP（UDP 500、UDP 4500）等。

#### 3. 在Ubuntu虚拟机上安装和配置VPN服务器

- 通过SSH连接到Ubuntu虚拟机。

- 更新系统软件包：`sudo apt update && sudo apt upgrade -y`

- 安装PPTP服务器：`sudo apt install pptpd -y`

- 编辑PPTP服务器配置文件：

  ```
  sudo nano /etc/pptpd.conf
  ```

  - 取消注释并修改`localip`和`remoteip`行，指定VPN隧道的IP地址范围。

- 配置PPTP用户名和密码：

  ```
  sudo nano /etc/ppp/chap-secrets
  ```

  - 添加一行，格式为：`username pptpd password *`

- 启用IP转发：

  ```
  sudo nano /etc/sysctl.conf
  ```

  - 取消注释`net.ipv4.ip_forward=1`行

- 应用更改：`sudo sysctl -p`

- 配置iptables规则，启用NAT：

  ```javascript
  sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
  sudo iptables -A FORWARD -i eth0 -o ppp0 -m state --state RELATED,ESTABLISHED -j ACCEPT
  sudo iptables -A FORWARD -i ppp0 -o eth0 -j ACCEPT
  ```

- 重启PPTP服务：`sudo systemctl restart pptpd`

#### 4. 在小米路由器上配置VPN客户端

- 在小米路由器的管理界面中，找到VPN设置。
- 选择PPTP协议，输入Azure Ubuntu虚拟机的公共IP地址作为服务器地址。
- 输入在Ubuntu虚拟机上配置的VPN用户名和密码。
- 保存设置并启用VPN连接。

完成以上步骤后，小米路由器应该就可以通过PPTP协议与Azure上的Ubuntu虚拟机建立VPN连接了。如果遇到任何问题，请仔细检查配置，并查看虚拟机和路由器的日志信息以定位问题。

不行

ubuntu已经无支持pptp了

还需要考虑别的方案。

# 方案一：路由器连接上

需要考虑可以运行相关协议的，比如说openVPN



# 方案二：host 连接上

对于么个单独的host 需要单独的设置和下载