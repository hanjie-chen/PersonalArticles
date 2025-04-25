---
Title:
Author: 陈翰杰
Instructor: grok3
CoverImage: 
RolloutDate: 
---

```
BriefIntroduction: 

```

<!-- split -->

# Modele design

当我们打算写 terraform 模块的时候，往往会遇到这样子的问题：每个模块应该如何区分和设计？

## background

当我们打算写 terraform 模块的时候，往往会遇到这样子的问题：每个模块应该如何区分和设计？

以下面的这个没有模块化的 terraform 项目为例（在 Azure 上分别创建 1 台 linux vm 和 1 台 windows vm）

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
有 **Linux VM** 和 **Windows VM** 相关的计算资源（`compute-linux-vm.tf` 和 `compute-windows-vm.tf`）。

网络资源分为通用的（`network-general.tf`）和专属的（`network-linux.tf` 和 `network-windows.tf`）。

变量文件也分为通用的（`variables-general.tf`）和专属的（`variables-linux.tf` 和 `variables-windows.tf`）。

项目既有共享资源（如通用的网络配置），又有独立配置（如 Linux 和 Windows VM 的专属网络和计算资源）。接下来，我会分析两种模块划分方式。



## 方式 1：按资源类型划分
这种方式是将所有相似的资源整理成一个模块，例如：
- **compute module**：主要包含 `compute-linux-vm.tf` 和 `compute-windows-vm.tf`。
- **network module**：主要包含 `network-general.tf`、`network-linux.tf` 和 `network-windows.tf`。

#### 优点
- **复用性强**：如果多个地方需要类似的计算或网络资源，可以直接调用同一个模块。例如，一个通用的 `network module` 可以被不同的 VM 使用。
- **逻辑清晰**：按资源类型划分（如计算、网络）符合基础设施的分层逻辑。

#### 缺点
- **依赖复杂**：`compute module` 可能需要依赖 `network module` 的输出（比如子网 ID），模块间的依赖关系可能变得复杂。
- **灵活性低**：如果 Linux VM 和 Windows VM 的网络需求差异很大，一个通用的 `network module` 可能需要大量参数来适配，导致模块臃肿。

#### 适用场景
- 当网络或计算资源是高度共享的，且不同 VM 的配置差异不大时。例如，所有 VM 都使用同一个虚拟网络（VNet）和子网。



## 方式 2：按功能完整性划分
这种方式是将一个完整的功能（比如一个 Linux VM 或 Windows VM）封装成一个模块，例如：
- **linux-vm module**：包含 `compute-linux-vm.tf`、`network-linux.tf` 和 `variables-linux.tf`。
- **windows-vm module**：包含 `compute-windows-vm.tf`、`network-windows.tf` 和 `variables-windows.tf`。

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
   - **linux-vm module**：包含 `compute-linux-vm.tf` 和 `network-linux.tf`，定义 Linux VM 及其专属的子网、安全组等。
   - **windows-vm module**：包含 `compute-windows-vm.tf` 和 `network-windows.tf`，定义 Windows VM 及其专属的网络配置。

#### 为什么推荐这种方式？
- **复用性**：通用的网络资源（如 VNet）放在 `network module` 中，避免重复定义。
- **灵活性**：Linux 和 Windows VM 的专属配置各自独立，适应不同的需求。
- **符合你的项目结构**：你的文件已经按功能分开（Linux vs Windows），混合模式可以直接利用这一点。
