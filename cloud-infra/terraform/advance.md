# Terraform 进阶：模块化重构与状态管理

当我们的 main.tf 写了几百行，拥有了多台 VM 和复杂的网络时，代码变得难以维护，这就需要引入模块化。

# Why Modules?

虽然我们可以把代码分拆成 compute.tf, network.tf 散落在根目录里，Terraform 并不强制要求必须使用特定的文件夹结构。

但是绝大多数现代项目（包括官方文档）都会推荐创建一个专属的 modules/ 文件夹，e.g.

```shell
terraform-projects/
├── main.tf                <- 调用模块
├── terraform.tfvars
├── outputs.tf
├── providers.tf
├── modules/
│   ├── virtual-machine/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── network/
│   └── ...
```

主要是出于以下几点：

- 清晰的结构：modules/ 这个名字一看就知道这些文件夹是 Terraform modules，而不是别的东西（比如脚本、配置文件等）。
- 可维护性：当项目变大以后，会有很多东西：CI/CD 脚本、文档、terraform plan 输出、backend config 等。用 modules/ 隔离模块，可以让目录结构保持整洁。
- 复用：如果未来你想把某些模块提取出来变成独立 module（比如上传到 Terraform Registry 或 GitHub reuse），modules/ 目录可以直接作为基础。

也就是说我们用 `modules/` 是一种 best practice。

# Module Design Strategy

既然决定了要使用模块，那么在动手写代码之前，我们要面临第一个架构问题：到底该怎么拆分模块？每个模块应该如何区分和设计？

以下面的这个没有模块化的 terraform project 为例（在 Azure 上分别创建 1 台 linux vm 和 1 台 windows vm）

```shell
$ tree
.
├── README.md
├── compute-linux-vm.tf
├── compute-windows-vm.tf
├── network-general.tf
├── network-linux.tf
├── network-windows.tf
├── outputs.tf
├── providers.tf
├── variables-general.tf
├── variables-linux.tf
└── variables-windows.tf
```

我们面临两种主流的拆分思路：

## Resource Type

按照资源类型划分，将所有相似的资源整理成一个模块，例如：

- compute module：`compute-linux-vm.tf` + `compute-windows-vm.tf`。
- network module：`network-general.tf` + `network-linux.tf` + `network-windows.tf`。

优点：逻辑符合云基础设施的分层，复用性极强。

缺点：如果 Linux 和 Windows 的网络需求差异极大，一个通用的网络模块需要写无数个参数去适配，导致模块极度臃肿，且模块间依赖复杂。

## Function Unit

按功能完整性划分，将一个完整的功能（比如一个 Linux VM 或 Windows VM）封装成一个模块，例如：

- linux-vm module：包含 `compute-linux-vm.tf`、`network-linux.tf` 和 `variables-linux.tf`。
- windows-vm module：包含 `compute-windows-vm.tf`、`network-windows.tf` 和 `variables-windows.tf`。

优点：高内聚，每个模块自包含。Linux 和 Windows 可以有完全独立的网络配置。

缺点：如果有共享资源（如它们同处一个 VNet），会在两个模块里产生代码冲突或重复。

## Hybrid Mode

针对这种“既有共享网络，又有独立机器”的常见架构，最佳实践是混合模式：

1. 提取通用基建：创建一个独立的 network 模块，包含共享的虚拟网络（VNet），并输出 VNet ID。
2. 按功能打包机器：创建 linux-vm 和 windows-vm 模块，里面包含机器自己的 Compute 资源以及专属的 Subnet 和 NSG。这样既消除了重复，又保留了极大的灵活性。

# Define & Use Modules

设计好架构后，我们终于可以开始写代码了。Terraform Module 就像编程语言中的“函数”，一次定义，到处调用。

既然说它类似于函数，那么我们就和理解函数一样，来讲讲看它如何定义，传参，以及如何返回值。

## Define module

定义一个 modules 非常简单，我们只需创建一个文件夹，并且放入下面的几个关键文件即可

- `main.tf`：定义模块里的资源，比如虚拟机、数据库等。
- `variables.tf`：定义模块需要的输入变量（比如虚拟机名称、大小等）。
- `outputs.tf`：定义模块的输出值（比如虚拟机的 IP 地址、ID 等）。
- `README.md` (optional)：写一些说明，告诉别人这个模块是干嘛用的。

for example

假设我们需要创建一个模块来部署一台 Linux VM。模块的文件夹结构可能是这样：

```
linux-vm-module/
├── compute.tf
├── variables.tf
├── outputs.tf
└── network.tf
```

variables.tf: 定义变量

compute.tf: linux vm 定义

network.tf: linux vm 网络相关设置（nic, nsg, subnet 等）

outputs.tf: 输出值，类似于函数返回值

## Call module & Pass Parameters

在项目根目录（Project Root）的 main.tf 中，它就像 C 语言里的 main 函数（Entry Point），负责调用各个模块并传参：

```hcl
module "network" {
  source              = "./modules/network"     # 模块的本地路径
  resource_group_name = var.resource_group_name # 传递参数
  resource_region     = var.resource_region
}
```

而在 modules/network 中我们需要先定义这些变量

```hcl
# ./modules/network/variables.tf
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "resource_region" {
  description = "Azure region"
  type        = string
}
---
# ./modules/network/network-general.tf
# create virtual network
resource "azurerm_virtual_network" "main" {
  name                = var.vnet_name
  address_space       = var.vnet_address_space
  location            = var.resource_region
  resource_group_name = var.resource_group_name
}
```

### sensitive variables

核心原则：绝对不要在模块（如 modules/linux-vm）内部创建 terraform.tfvars 文件！

terraform.tfvars 是为项目根目录提供变量值的。正确的传密码姿势是：

1. 根目录：将包含真实密码的 terraform.tfvars 保留在项目根目录，并加入 .gitignore。
2. 声明：在根目录的 variables.tf 中声明 admin_password。
3. 传递：在根目录调用模块时，通过参数把密码喂给模块

## Get Return Values

> terraform module 返回值其实叫做 outputs (详见下文) 这里之所以称之为返回值，是为了便于理解，拿编程语言中的函数返回值概念来类比

如何在一个 modules 定义返回值，并且在 project root 中调用这个返回值呢？

### define return value in module

为了定义返回值，我怕们需要在 modules 定义 `outputs.tf` 如果 linux_vm 模块需要用到 network 模块创建的网卡 ID，那么在 `./network-module/outputs.tf` 中需要存在

```hcl
output "network_interface_id" {
  value = azurerm_network_interface.linux_vm_nic.id
}
```

### use the return value in project root

然后在根目录中跨模块引用：

```hcl
module "network" {
  source = "./network-module"
  # ...
}

module "linux_vm" {
  source = "./linux-vm-module"
  network_interface_id = module.network.network_interface_id  # 调用网络模块的输出
  # ...
}
```

> [!note]
>
> project root 中的 `outputs.tf` 则是用于显示部署完成之后输出的信息

## Module Sources

和函数类似，module 分为

本地模块：像上面例子中这样，模块文件就在你的项目文件夹里，适合个人学习或小项目。

远程模块：可以从 Git 仓库或 Terraform Registry 下载，适合大项目或团队协作。比如：

```hcl
module "linux_vm" {
  source = "git::https://example.com/modules.git?ref=v1.0.0"
  # ...
}
```

# Refactor Crisis

## module not installed

当我们将 terraform 项目重构为 modules 之后，然后运行 `terraform validate` 可能会发现如下的报错

```shell
$ terraform validate
│ Error: Module not installed
│
│ This module is not yet installed. Run "terraform init" to install all modules required by this configuration.
```

这个报错的意思是：Terraform 在 validate 阶段发现你使用了 module，但当前 module 还没有被“初始化（install）”。

原因：哪怕你用的是本地路径（source = "./modules/xxx"），Terraform 的机制也要求必须将其扫描并注册到 .terraform/modules 缓存目录中。

只要你新增、修改了 module 的路径，必须重新运行一次 terraform init！

> [!tip]
>
> 可以在 .terraform/modules/ 目录中看到 Terraform 把 module 拷贝了进去（哪怕是本地的），这是 Terraform 的“内部模块缓存机制”

## Destroy Panic

解决了初始化问题，敲下了 terraform plan，却看到了可怕的输出：

```shell
...
Plan: 13 to add, 0 to change, 13 to destroy.
...
```

也就是 Terraform 想「删除所有现有资源再重建一遍」，而不是简单地 update

为什么会这样子？

虽然在云上的资源根本没动，但在 Terraform 的“小本本”（terraform.tfstate）里，它记录的旧 VM 路径是

```hcl
azurerm_linux_virtual_machine.linux_vm
```

现在用了模块，代码里的路径变成了

```
module.linux_vm.azurerm_linux_virtual_machine.linux_vm
```

路径变了，Terraform 就认为老机器被你删了，要求新建一台！ 这在生产环境是绝对不可接受的。

### resolution: state mirgration

为了保住老资源，我们需要手动给 Terraform 的状态文件“改名”，告诉它：“老资源就是模块里的新资源”。这就是 terraform state mv 命令。

```bash
terraform state mv \
  azurerm_linux_virtual_machine.linux_vm \
  module.linux_vm.azurerm_linux_virtual_machine.linux_vm
```

我们可以通过 terraform state list 查出老的地址，然后对照模块写出新的地址，并执行迁移

```shell
$ terraform state list
azurerm_linux_virtual_machine.linux_vm
...
```

一般来说，如果资源直接定义在 main.tf，没有模块嵌套，那么地址就是 `<resource-type>.<resource-name>`

而如果资源在 module 里，地址就是 `module.<module-name>.<resource-type>.<resource-name>`

### best practice

在运行 terraform state mv 之前记得备份 tfstate 文件：

```bash
cp terraform.tfstate terraform.tfstate.bak.manual-mv
```

最后运行 terraform plan 验证是否显示「0 to add, 0 to destroy」，如果看到 plan 里只剩些小变更 like ~（update），那就说明迁移成功

因为资源多，建议把所有的 mv 命令写进一个 .sh 脚本一次性执行。

当我们运行完成 `terraform state mv` 命令之后，就会发现多出了很多的 tfstate backup 文件，他们是运行 terraform state mv 命令，自动生成的状态备份，格式为：`terraform.tfstate.<timestamp>.backup`

每执行一次 mv，就会在复制一份 tfstate，确保即使搞砸了 state，也有回滚的机会。

可以使用 `rm terraform.tfstate.*.backup` 批量删除这些临时文件（先确认当前的 terraform.tfstate 是稳定且有效的）

# Import Existing Resources

`terraform import` 用于纳管目前不是由当前 tfstate 管理的 Azure resource（比如别人在 Azure Portal 上手动点击创建的资源）。

注意：如果 Azure 上的资源已经由当前的 tfstate 管理了，那么执行 import 会报错或无效。

## Import Common Resource

对于一般的 resoruce 而言 Terraform 的 import 命令格式是：

```shell
terraform import <resource-type>.<resource-name> <resource-id>
```

例如，把云上已有的 Windows VM 拉取到本地代码中管理：

```shell
$ terraform import azurerm_windows_virtual_machine.windows_vm <resource-id>
azurerm_windows_virtual_machine.windows_vm: Importing from ID "<resource-id>"...
azurerm_windows_virtual_machine.windows_vm: Import prepared!
  Prepared azurerm_windows_virtual_machine for import
azurerm_windows_virtual_machine.windows_vm: Refreshing state... [id=<resource-id>]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
```

执行成功后，这个资源就进入了你的 Terraform state，以后就可以用代码来修改它了。

## import association resource

对于 azurerm_subnet_network_security_group_association 这样的资源，它并不是一个独立的实体，而是表示子网（Subnet）和网络安全组（NSG）之间的关联关系。因此，它的资源 ID 并不是一个独立的 ID，而是直接使用子网的 ID 来标识这种关联。

```shell
terraform import azurerm_subnet_network_security_group_association.windows_subnet_nsg_association <subnet>
```

