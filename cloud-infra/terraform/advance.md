# Terraform 进阶：模块化重构与状态管理

当我们的 main.tf 写了几百行，拥有了多台 VM 和复杂的网络时，代码变得难以维护，这就需要引入模块化。



# why modules?

对于大部分的项目结构都类似于如下所示

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

那么我们是否可以省略 `modules` 文件夹，直接将里面的模块文件夹暴露在外呢？

当然可以，我们可以直接把 linux-vm、windows-vm、network 等模块文件夹放在项目根目录里 —— Terraform 不强制你一定要用 modules/ 这个文件夹名。

但是，为什么大多数人（包括官方文档）都会用 `modules/` 呢？主要是出于以下几点：

## why add `modules/` folder

### 清晰的语义结构：

modules/ 这个名字一看就知道“这些文件夹是 Terraform modules”，而不是别的东西（比如脚本、配置文件等）。

### 更好的可维护性：

当你的项目变大以后，会有很多东西：CI/CD 脚本、文档、terraform plan 输出、backend config 等。用 modules/ 隔离模块，可以让目录结构保持整洁。

### 更容易复用：

如果未来你想把某些模块提取出来变成独立 module（比如上传到 Terraform Registry 或 GitHub reuse），modules/ 目录可以直接作为基础。

总结一句话就是：用 `modules/` 是一种“最佳实践”，不是“强制规则”。如果你有更适合你风格的结构，也是完全 OK 的。

## don't want to use `modules/`

可以不加 modules/ 的情况

- 项目规模小（比如只部署几台 VM）
- 是学习项目或练手 Demo
- 你就是想保持目录短一点，好 navigate

比如可以这样：

```
my-terraform-project/
├── linux-vm/
├── windows-vm/
├── network/
├── main.tf
├── outputs.tf
├── variables.tf
```

然后：

```hcl
module "linux_vm" {
  source = "./linux-vm"
}
```

Terraform 是不会报错的。

# define and use module

Terraform Module 类似于编程语言中的函数，只需要定义一次，就可以在不同的项目或环境中调用这个模块，用时只需要调用和传递参数即可

既然说它类似于函数，那么我们就和理解函数一样，来讲讲看它如何定义，传参，以及如何返回值。

## Define

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

## Using & Passing Parameters

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

## Return Value

> terraform module 返回值其实叫做 outputs (详见下文) 这里之所以称之为返回值，是为了便于理解，拿编程语言中的函数返回值概念来类比

如何在一个 modules 定义返回值，并且在 project root 中调用这个返回值呢？

### define return value in module

为了定义返回值，我怕们需要在 modules 定义 `outputs.tf` 例如

在 `./network-module/outputs.tf` 中需要存在

```hcl
output "network_interface_id" {
  value = azurerm_network_interface.linux_vm_nic.id
}
```

### use the return value in project root

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

## Entry Point of Terraform Project

project root 中的 `main.tf` 是项目的入口点（entry point），类似于 C language 中的 main 函数，它会调用每一个 module（比如 network、linux-vm、windows-vm），给模块传入变量，并且相互调用模块之间的输出

# modele design strategy

当我们打算写 terraform 模块的时候，往往会遇到这样子的问题：每个模块应该如何区分和设计？

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

是应该把和 compute, network 相关的都整理位一个 modules, 比如说 compute module, network module

还是说按照 compute-linux-vm.tf + network-linux.tf + varialbes-linux.tf = linux-vm module 作为一个完成的 module 呢？

这涉及到 Terraform 模块划分的核心问题：到底是按照资源类型（如 compute、network）来划分模块，还是按照功能完整性（如 Linux VM 或 Windows VM 的完整配置）来划分模块。

针对这个项目，接下来分析这两种方式的优缺点，并给出建议。

## 项目结构分析

先来看一下项目相关文件：

```
.
├── compute-linux-vm.tf
├── compute-windows-vm.tf
├── network-general.tf
├── network-linux.tf
├── network-windows.tf
├── variables-general.tf
├── variables-linux.tf
├── variables-windows.tf
└── ...
```

有 Linux VM 和 Windows VM 相关的计算资源（`compute-linux-vm.tf` 和 `compute-windows-vm.tf`）。

网络资源分为通用的（`network-general.tf`）和专属的（`network-linux.tf` 和 `network-windows.tf`）。

变量文件也分为通用的（`variables-general.tf`）和专属的（`variables-linux.tf` 和 `variables-windows.tf`）。

项目既有共享资源（如通用的网络配置），又有独立配置（如 Linux 和 Windows VM 的专属网络和计算资源）。接下来，我会分析两种模块划分方式。



## 方式 1：按资源类型划分

这种方式是将所有相似的资源整理成一个模块，例如：

- compute module：主要包含 `compute-linux-vm.tf` 和 `compute-windows-vm.tf`。
- network module：主要包含 `network-general.tf`、`network-linux.tf` 和 `network-windows.tf`。

#### 优点

- 复用性强：如果多个地方需要类似的计算或网络资源，可以直接调用同一个模块。例如，一个通用的 `network module` 可以被不同的 VM 使用。
- 逻辑清晰：按资源类型划分（如计算、网络）符合基础设施的分层逻辑。

#### 缺点

- 依赖复杂：`compute module` 可能需要依赖 `network module` 的输出（比如子网 ID），模块间的依赖关系可能变得复杂。
- 灵活性低：如果 Linux VM 和 Windows VM 的网络需求差异很大，一个通用的 `network module` 可能需要大量参数来适配，导致模块臃肿。

#### 适用场景

- 当网络或计算资源是高度共享的，且不同 VM 的配置差异不大时。例如，所有 VM 都使用同一个虚拟网络（VNet）和子网。

## 方式 2：按功能完整性划分

这种方式是将一个完整的功能（比如一个 Linux VM 或 Windows VM）封装成一个模块，例如：

- linux-vm module：包含 `compute-linux-vm.tf`、`network-linux.tf` 和 `variables-linux.tf`。
- windows-vm module：包含 `compute-windows-vm.tf`、`network-windows.tf` 和 `variables-windows.tf`。

#### 优点

- 自包含：每个模块包含了创建特定 VM 所需的所有资源（计算、网络等），逻辑简单，易于理解和维护。
- 灵活性高：Linux VM 和 Windows VM 可以有各自独立的网络配置，不需要强行统一。

#### 缺点

- 代码重复：如果多个 VM 需要类似的网络配置（比如都用同一个 VNet），可能会在不同模块中重复定义。
- 共享困难：如果有共享资源（如通用的 VNet），需要额外的协调。

#### 适用场景

- 当每个 VM 有独立的网络配置需求时。例如，Linux VM 在一个子网，Windows VM 在另一个子网，或者它们的安全组规则不同。

## 混合模式的建议

从项目的文件来看：

- `network-general.tf` 包含共享的网络资源（如 VNet）
- `network-linux.tf` 和 `network-windows.tf` 表示 Linux 和 Windows VM 有各自专属的网络配置（如 subnet, nsg）
- 计算资源（`compute-linux-vm.tf` 和 `compute-windows-vm.tf`）和变量（`variables-linux.tf` 和 `variables-windows.tf`）也是按功能分开。

在这种情况下，建议采用混合模式，兼顾复用性和灵活性：

1. 创建一个通用的 network module：
   - 包含 `network-general.tf` 中的资源，比如虚拟网络（VNet）。
   - 输出共享资源（如 VNet ID），供其他模块使用。

2. 为 Linux VM 和 Windows VM 分别创建模块：
   - linux-vm module：包含 `compute-linux-vm.tf` 和 `network-linux.tf`，定义 Linux VM 及其专属的子网、安全组等。
   - windows-vm module：包含 `compute-windows-vm.tf` 和 `network-windows.tf`，定义 Windows VM 及其专属的网络配置。

#### 为什么推荐这种方式？

- 复用性：通用的网络资源（如 VNet）放在 `network module` 中，避免重复定义。
- 灵活性：Linux 和 Windows VM 的专属配置各自独立，适应不同的需求。
- 符合你的项目结构：你的文件已经按功能分开（Linux vs Windows），混合模式可以直接利用这一点。
