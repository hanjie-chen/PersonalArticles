可以使用 `nc` / `ncat` 命令在 linux 上面测试 tcp connection

```bash
nc -zv <hostname> <port>
```

- `-z`：仅扫描不发送数据。
- `-v`：显示详细信息。

e.g.

```bash
Plain@Linux-VM:~$ nc -zv www.google.com 443
Connection to www.google.com 443 port [tcp/https] succeeded!
```

