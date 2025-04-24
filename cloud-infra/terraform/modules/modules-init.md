当我们将 terraform 项目重构为 modules 之后，然后运行 `terraform validate` 发现会报错

```shell
$ terraform validate
╷
│ Error: Module not installed
│
│   on main.tf line 7:
│    7: module "network" {
│
│ This module is not yet installed. Run "terraform init" to install all modules required by this configuration.
╵
╷
│ Error: Module not installed
│
│   on main.tf line 14:
│   14: module "linux_vm" {
│
│ This module is not yet installed. Run "terraform init" to install all modules required by this configuration.
╵
╷
│ Error: Module not installed
│
│   on main.tf line 22:
│   22: module "windows_vm" {
│
│ This module is not yet installed. Run "terraform init" to install all modules required by this configuration.
```

这是 main.tf

```hcl
# create resource group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.resource_region
}

module "network" {
  source = "./modules/network"
  resource_group_name = var.resource_group_name
  resource_region = var.resource_region
  vnet_name = var.vnet_name
}

module "linux_vm" {
  source = "./modules/linux-vm"
  resource_group_name = var.resource_group_name
  resource_region = var.resource_region
  linux_vm_admin_password = var.linux_vm_admin_password
  vnet_name = var.vnet_name
}

module "windows_vm" {
  source = "./modules/windows-vm"
  resource_group_name = var.resource_group_name
  resource_region = var.resource_region
  windows_vm_admin_password = var.windows_vm_admin_password
  vnet_name = var.vnet_name
}
```

这是我的项目目录：
```
(base) Plain@Singapore-Linux-VM:~/projects/azure-vm-terraform$ tree
.
├── README.md
├── main.tf
├── modules
│   ├── linux-vm
│   │   ├── compute.tf
│   │   ├── network.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   ├── network
│   │   ├── network-general.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   └── windows-vm
│       ├── compute.tf
│       ├── network.tf
│       ├── outputs.tf
│       └── variables.tf
├── outputs.tf
├── providers.tf
├── terraform.tfstate
├── terraform.tfstate.backup
├── terraform.tfvars
└── variables-general.tf

5 directories, 19 files
```



这个错误的原因其实是 Terraform 的一个「机制问题」，不是写法错了。下面来详细解释原因和解决方案



## 报错原因解析：Module not installed

报错内容如下：

```
Error: Module not installed
This module is not yet installed. Run "terraform init" to install all modules required by this configuration.
```

🔍 这个报错的意思是：Terraform 在 validate 阶段发现你使用了 module，但当前 module 还没有被“初始化（install）”。

📌 哪怕你用的是本地模块（比如 source = "./modules/network"），Terraform 也会把它当成一个「待安装的 module source」。

👉 而所有的 module（无论是远程的，还是本地的），都必须在运行 terraform init 时被扫描、复制到 .terraform/modules 目录下，这样 Terraform 才会认为它们是“已安装”的模块。



## 正确流程应该是：

每次你：

- 新增了 module 块（module "xxx" {...}）
- 修改了 module 的 source 路径
- 从 GitHub 或本地新引入模块
- 升级了 Terraform provider
- 增加了 backend 配置

🛠️ 都要运行：

```bash
terraform init
```

这个命令会：

- 下载/注册模块（本地或远程）
- 安装 provider 插件（比如 azurerm）
- 初始化 backend（比如 remote state）



## 解决方案

你只需要在项目根目录运行：

```bash
terraform init
```

然后再运行：

```bash
terraform validate
```

问题就解决了



## ✅ 一次性命令流推荐：

为了保证每次干净运行建议使用这一套命令顺序：

```bash
terraform init           # 初始化 module / provider / backend
terraform validate       # 语法和配置检查
terraform plan           # 查看执行计划
terraform apply          # 真正部署
```

------

## 💡小提示：

你可以在 .terraform/modules/ 目录中看到 Terraform 把 module 拷贝了进去（哪怕是本地的），这是 Terraform 的“内部模块缓存机制”。

------

如果你还有其他报错（比如 module 输入输出参数错了），我也可以帮你看；但现在这个问题就是没运行 terraform init ～ 修一下就好了。要不要我顺便帮你检查一下 main.tf 的模块调用是否合理？