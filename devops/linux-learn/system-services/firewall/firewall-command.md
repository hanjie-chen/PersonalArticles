#### 可以使用 ufw 命令查看 Ubuntu Server 防火墙状态

Ubuntu 默认安装了 ufw (Uncomplicated Firewall) 防火墙。可以使用以下命令查看 ufw 防火墙的状态:

```javascript
sudo ufw status
```

如果显示 `Status: active`,则表示防火墙已开启;如果显示 `Status: inactive`,则表示防火墙未开启 

e.g.

```shell
Plain@Singapore-Linux-VM:~$ sudo ufw status
Status: inactive
```


