# Key-based authentication

当我们使用ssh连接到一台远程服务器的时候，需要输出 username, passoword 来进行登录

但是这样子可能会遇到一些安全问题，比如说一台有 public ip 的 server 可能会遇到，密码爆破攻击这样子，为了安全考虑，我们可以使用 ssh key 验证

