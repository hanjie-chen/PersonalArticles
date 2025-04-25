# terraform module

Terraform Module 是 Terraform 中用来组织和管理基础设施代码的一种工具。简单来说，它就像一个“模板”或“蓝图”，把一组相关的资源（比如虚拟机、网络、安全组等）打包成一个可以重复使用的单元。你可以在不同的项目或环境中调用这个模块，而不需要每次都重新写代码。

类似于编程语言中的函数，只需要定义一次，用时只需要调用和传递参数即可



## module example

一个 Terraform module 通常是一个文件夹，里面包含几个关键文件：
- **`main.tf`**：定义模块里的资源，比如虚拟机、数据库等。
- **`variables.tf`**：定义模块需要的输入变量（比如虚拟机名称、大小等）。
- **`outputs.tf`**：定义模块的输出值（比如虚拟机的 IP 地址、ID 等）。
- （可选）**`README.md`**：写一些说明，告诉别人这个模块是干嘛用的。

### 一个简单的例子
假设你要创建一个模块来部署一台 Linux VM。模块的文件夹结构可能是这样：
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

outputs.tf: 输出值





## 如何使用 Terraform Module？

使用模块分三步：创建模块、调用模块、使用输出。下面我一步步说明。

创建模块

就像上面例子中那样，写好 `main.tf`、`variables.tf` 和 `outputs.tf`，放在一个文件夹里（比如 `linux-vm-module`）。

在主配置中调用模块

假设你的主 Terraform 文件是 `main.tf`，你可以在里面调用这个模块：

```hcl
module "linux_vm" {
  source = "./linux-vm-module"  # 模块的路径

  vm_name             = "my-linux-vm"
  vm_size             = "Standard_B2s"
  network_interface_id = "your-network-interface-id"  # 假设你有这个值
}
```

- **`source`**：告诉 Terraform 去哪里找模块。这里是本地路径 `./linux-vm-module`。
- 输入变量：通过 `vm_name`、`vm_size` 等把值传给模块。



### 使用模块的输出
模块可以输出一些值，你可以在主配置或其他模块里用这些输出。比如：

```hcl
output "my_vm_ip" {
  value = module.linux_vm.vm_ip  # 获取 Linux VM 的 IP 地址
}
```

如果还有一个网络模块，你可以用它的输出作为 VM 模块的输入：

```hcl
module "network" {
  source = "./network-module"
  # 网络模块的配置...
}

module "linux_vm" {
  source = "./linux-vm-module"
  vm_name             = "my-linux-vm"
  vm_size             = "Standard_B2s"
  network_interface_id = module.network.network_interface_id  # 用网络模块的输出
}
```



## 模块的类型

**本地模块**：像上面这样，模块文件就在你的项目文件夹里，适合个人学习或小项目。

**远程模块**：可以从 Git 仓库或 Terraform Registry 下载，适合大项目或团队协作。比如：

```hcl
module "linux_vm" {
  source = "git::https://example.com/modules.git?ref=v1.0.0"
  # ...
}
```





# 在模块内使用从 root 目录 `main.tf` 传递进来的参数

在 `main.tf` 中，通过以下方式向 `network` 模块传递了 `resource_group_name` 和 `resource_region` 参数：

```hcl
module "network" {
  source              = "./modules/network"
  resource_group_name = var.resource_group_name
  resource_region     = var.resource_region
}
```

为了在 `network` 模块内部使用这些参数，你需要在模块的 `variables.tf` 文件中定义对应的输入变量，然后在资源定义中使用这些变量。

#### for example
在 `modules/network/variables.tf` 中添加变量定义，修改后的 `variables.tf` 如下：

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
# create resource group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.resource_region  # 改为 var.location，与 main.tf 保持一致
}

# create virtual network
resource "azurerm_virtual_network" "main" {
  name                = var.vnet_name
  address_space       = var.vnet_address_space
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}
```



