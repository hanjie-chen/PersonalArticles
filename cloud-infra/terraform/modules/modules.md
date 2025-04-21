# terraform module

Terraform Module 是 Terraform 中用来组织和管理基础设施代码的一种工具。简单来说，它就像一个“模板”或“蓝图”，把一组相关的资源（比如虚拟机、网络、安全组等）打包成一个可以重复使用的单元。你可以在不同的项目或环境中调用这个模块，而不需要每次都重新写代码。

类似于编程语言中的函数，只需要定义一次，用时只需要调用和传递参数即可

## module consistent

一个 Terraform 模块通常是一个文件夹，里面包含几个关键文件：
- **`main.tf`**：定义模块里的资源，比如虚拟机、数据库等。
- **`variables.tf`**：定义模块需要的输入变量（比如虚拟机名称、大小等）。
- **`outputs.tf`**：定义模块的输出值（比如虚拟机的 IP 地址、ID 等）。
- （可选）**`README.md`**：写一些说明，告诉别人这个模块是干嘛用的。

### 一个简单的例子
假设你要创建一个模块来部署一台 Linux 虚拟机 (VM)。模块的文件夹结构可能是这样：
```
linux-vm-module/
├── main.tf
├── variables.tf
└── outputs.tf
```

#### **variables.tf**（输入变量）
```hcl
variable "vm_name" {
  description = "虚拟机的名称"
  type        = string
}

variable "vm_size" {
  description = "虚拟机的大小"
  type        = string
  default     = "Standard_B1s"  # 默认值
}

variable "network_interface_id" {
  description = "网络接口的 ID"
  type        = string
}
```

#### **main.tf**（资源定义）
```hcl
resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm_name
  resource_group_name = "your-resource-group"  # 通常也是变量
  location            = "East US"  # 通常也是变量
  size                = var.vm_size
  network_interface_ids = [var.network_interface_id]

  # 其他配置，比如操作系统、磁盘等...
}
```

#### **outputs.tf**（输出值）
```hcl
output "vm_id" {
  value = azurerm_linux_virtual_machine.vm.id
}

output "vm_ip" {
  value = azurerm_linux_virtual_machine.vm.public_ip_address
}
```

这个模块的功能是：根据你给的名称、大小和网络接口 ID，创建一台 Linux VM，并返回它的 ID 和 IP 地址。



## 如何使用 Terraform Module？

使用模块分三步：创建模块、调用模块、使用输出。下面我一步步说明。

### 创建模块
就像上面例子中那样，写好 `main.tf`、`variables.tf` 和 `outputs.tf`，放在一个文件夹里（比如 `linux-vm-module`）。

### 在主配置中调用模块
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
- **输入变量**：通过 `vm_name`、`vm_size` 等把值传给模块。

运行 `terraform init` 会下载模块（如果是本地模块就不需要下载），然后 `terraform apply` 就会创建资源。

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

- **本地模块**：像上面这样，模块文件就在你的项目文件夹里，适合个人学习或小项目。
- **远程模块**：可以从 Git 仓库或 Terraform Registry 下载，适合大项目或团队协作。比如：
  
  ```hcl
  module "linux_vm" {
    source = "git::https://example.com/modules.git?ref=v1.0.0"
    # ...
  }
  ```
  你现在可以先从本地模块开始练习。



## 动手实践建议

想真正学会 Terraform Module，最好动手试试。假设你有一个项目要部署网络和 VM，可以这样做：

1. **创建网络模块**  
   - 把网络相关的代码（比如虚拟网络、子网）放进一个模块。
   - 输出子网 ID 或网络接口 ID。

2. **创建 VM 模块**  
   - 像上面例子那样，写一个 Linux VM 模块。
   - 用网络模块的输出作为输入。

3. **在主文件调用**  
   - 在 `main.tf` 里调用这两个模块，确保它们能正确连接。

4. **测试**  
   - 运行 `terraform init` 和 `terraform apply`，看看能不能成功创建资源。



## 注意事项

- **路径要正确**：`source` 写错会导致模块找不到。
- **变量要传值**：没有默认值的变量必须在调用时赋值。
- **依赖关系**：模块之间的依赖（比如 VM 依赖网络）要通过输入和输出明确指定。



