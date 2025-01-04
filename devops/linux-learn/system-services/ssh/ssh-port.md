#### 修改 SSH 配置文件

以 root 权限打开 SSH 配置文件:

```javascript
sudo vim /etc/ssh/sshd_config
```

在文件中找到包含 `#Port 22` 的行,去掉前面的 `#` 号,将 `22` 修改为 `10499`:

```javascript
Port 10499
```

保存并关闭文件。

#### 重启 SSH 服务

重启 SSH 服务以使更改生效:

```javascript
sudo systemctl restart ssh
```

#### 修改防火墙规则

1. 如果你使用了防火墙,需要允许新的端口通过防火墙。例如,如果你使用 UFW (Uncomplicated Firewall):

   javascript

   

   ```javascript
   sudo ufw allow 10499/tcp
   ```

2. 现在你可以使用新的端口连接 SSH 了:

   ```javascript
   ssh user@server_ip -p 10499
   ```

注意事项:

- 修改 SSH 端口后,必须使用 `-p` 选项指定新的端口号连接 SSH。
- 选择一个未被其他服务占用的端口号,建议使用 1024 以上的端口。
- 修改默认 SSH 端口可以提高安全性,但不是万无一失的方法,还需要采取其他安全措施。

希望这个步骤能够帮助你成功修改 SSH 端口号。如有任何其他问题,欢迎随时问我。

