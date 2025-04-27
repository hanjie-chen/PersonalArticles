# Terraform Modules

Terraform Module 是 Terraform 中用来组织和管理基础设施代码的一种工具。简单来说，它就类似于编程语言中的函数，只需要定义一次，就可以在不同的项目或环境中调用这个模块，用时只需要调用和传递参数即可

既然说它类似于函数，那么我们就和理解函数一样，来讲讲看它如何定义，传参，以及如何返回值。

# Defining a Module

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

# Using Module & Passing Parameters

我们如何在 `main.tf` (project root) 中调用 module 并且令模块使用传递进来的参数呢？

我们只需要使用 module 关键字，然后在模块的 `variables.tf` 文件中定义对应的输入变量，然后在资源定义中使用这些变量即可

for example

我想要使用 `network` 模块，并且传递 `resource_group_name` 和 `resource_region` 参数，那么就应该

在 `main.tf` (project root) 中

```hcl
module "network" {								# 定义模块名
  source              = "./modules/network"		# 模块的路径
  resource_group_name = var.resource_group_name
  resource_region     = var.resource_region
}
```

在 `./modules/network/variables.tf` 中定义变量

```hcl
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "resource_region" {
  description = "Azure region"
  type        = string
}
```

在模块的资源定义中直接使用这些变量

```hcl
# create virtual network
resource "azurerm_virtual_network" "main" {
  name                = var.vnet_name
  address_space       = var.vnet_address_space
  location            = var.resource_region
  resource_group_name = var.resource_group_name
}
```

# Return Value

> terraform module 返回值其实叫做 outputs (详见下文) 这里之所以称之为返回值，是为了便于理解，拿编程语言中的函数返回值概念来类比

如何在一个 modules 定义返回值，并且在 project root 中调用这个返回值呢？

## define return value in module

为了定义返回值，我怕们需要在 modules 定义 `outputs.tf` 例如

在 `./network-module/outputs.tf` 中需要存在

```hcl
output "network_interface_id" {
  value = azurerm_network_interface.linux_vm_nic.id
}
```

## use the return value in project root

那么我们便可以在 project root 中使用如下的方式调用

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

# Module Sources

和函数类似，module 分为

本地模块：像上面例子中这样，模块文件就在你的项目文件夹里，适合个人学习或小项目。

远程模块：可以从 Git 仓库或 Terraform Registry 下载，适合大项目或团队协作。比如：

```hcl
module "linux_vm" {
  source = "git::https://example.com/modules.git?ref=v1.0.0"
  # ...
}
```

# Entry Point of Terraform Project

project root 中的 `main.tf` 是项目的入口点（entry point），类似于 C language 中的 main 函数，它会调用每一个 module（比如 network、linux-vm、windows-vm），给模块传入变量，并且相互调用模块之间的输出