当我们将 terraform 项目重构为 modules 之后，然后运行 `terraform validate` 可能会发现如下的报错

```shell
$ terraform validate
│ Error: Module not installed
│
│ This module is not yet installed. Run "terraform init" to install all modules required by this configuration.
```

这个报错的意思是：Terraform 在 validate 阶段发现你使用了 module，但当前 module 还没有被“初始化（install）”。

这个错误的原因其实是 Terraform 的一个「机制问题」

哪怕你用的是本地模块（比如 source = "./modules/network"），Terraform 也会把它当成一个「待安装的 module source」。

而所有的 module（无论是远程的，还是本地的），都必须在运行 terraform init 时被扫描、复制到 .terraform/modules 目录下，这样 Terraform 才会认为它们是“已安装”的模块。

所以正确流程应该是：

每次你：

- 新增了 module 块（module "xxx" {...}）
- 修改了 module 的 source 路径
- 从 GitHub 或本地新引入模块
- 升级了 Terraform provider
- 增加了 backend 配置

都要运行：

```bash
terraform init
```

这个命令会：

- 下载/注册模块（本地或远程）
- 安装 provider 插件（比如 azurerm）
- 初始化 backend（比如 remote state）



为了保证每次干净运行建议使用这一套命令顺序：

```bash
terraform init           # 初始化 module / provider / backend
terraform validate       # 语法和配置检查
terraform plan           # 查看执行计划
terraform apply          # 真正部署
```

> [!tip]
>
> 可以在 .terraform/modules/ 目录中看到 Terraform 把 module 拷贝了进去（哪怕是本地的），这是 Terraform 的“内部模块缓存机制”