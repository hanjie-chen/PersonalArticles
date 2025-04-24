当我们将一个普通的 terraform 项目重构为使用 modules 之后，并且使用 terraform validate 确定语法没有问题。

然后使用 terraform plan 的时候，就有可能会发现：

```shell
...
Plan: 13 to add, 0 to change, 13 to destroy.
...
```

也就是 Terraform 想「删除所有现有资源再重建一遍」，而不是简单地 update

这是为什么呢？

## 🔍 原因分析：为什么 Terraform 要 destroy & recreate？

简而言之：你重构了模块（文件结构变了），但 Terraform 的状态文件（.tfstate）中，旧的资源定义还保留着「老位置路径」，现在 Terraform 认为这些资源“不在代码中”了。

举个例子：

之前你创建 VM 的路径是：

terraform 识别旧 VM 的位置为：

```hcl
azurerm_linux_virtual_machine.linux_vm
```

现在你用了模块，变成了：

```hcl
module.linux_vm.azurerm_linux_virtual_machine.linux_vm
```

两个路径完全不同，对 Terraform 来说，这等于「老资源不见了，出现了一个新资源」，所以就触发 destroy + create。

这种变化对 Terraform 来说叫做：

> ❗资源地址（address）改变 ≠ 资源内容改变
>  Terraform 会重新创建它，而不是“移动”它。



## 合理吗？

技术上是合理的，但在生产环境或你已经部署了重要资源时，这是不可接受的。你需要的是保留已有资源，并让 Terraform 继续追踪它们，而不是重建它们。



## 解决方案：terraform state mv

如果你想要「保留资源不被删重建」，你要做的是手动告诉 Terraform：

> “这些旧资源，其实对应的是模块里面的新资源路径。”

你可以使用 terraform state mv 命令来「迁移状态」：

比如：

```bash
terraform state mv \
  azurerm_linux_virtual_machine.linux_vm \
  module.linux_vm.azurerm_linux_virtual_machine.linux_vm
```

再比如：

```bash
terraform state mv \
  azurerm_network_interface.linux_vm_nic \
  module.linux_vm.azurerm_network_interface.linux_vm_nic
```

⚠️ 注意：你要一个一个手动迁移，确保地址是对的。

📌 你可以运行 terraform state list 来查看当前状态里的资源地址



## 推荐做法总结

| 目的                    | 方法                                         |
| ----------------------- | -------------------------------------------- |
| 避免 destroy & recreate | 手动使用 terraform state mv 命令迁移资源地址 |
| 一次性检查状态资源      | terraform state list                         |
| 实验项目                | destroy + apply 是可以接受的                 |
| 生产环境                | 强烈建议手动迁移 tfstate                     |



# 如何迁移

使用 terraform state list 命令查看资源状态

```shell
$ terraform state list
azurerm_linux_virtual_machine.linux_vm
azurerm_network_interface.linux_vm_nic
azurerm_network_interface.windows_vm_nic
azurerm_network_security_group.linux_subnet_nsg
azurerm_network_security_group.windows_subnet_nsg
azurerm_public_ip.linux_vm_public_ip
azurerm_public_ip.windows_vm_public_ip
azurerm_resource_group.main
azurerm_subnet.linux_subnet
azurerm_subnet.windows_subnet
azurerm_subnet_network_security_group_association.linux_subnet_nsg_association
azurerm_subnet_network_security_group_association.windows_subnet_nsg_association
azurerm_virtual_network.main
azurerm_windows_virtual_machine.windows_vm
```

Terraform 现在的资源地址（state list 中）是：

- azurerm_linux_virtual_machine.linux_vm
- azurerm_virtual_network.main
- azurerm_subnet.windows_subnet

而在模块化结构中，它们应该变成：

- module.linux_vm.azurerm_linux_virtual_machine.linux_vm
- module.network.azurerm_virtual_network.main
- module.windows_vm.azurerm_subnet.windows_subnet
   等等…

可以从之前的

## terraform state mv 脚本

你可以将下面这些命令复制粘贴运行，每行迁移一个资源：

```bash
# network 模块
terraform state mv azurerm_virtual_network.main module.network.azurerm_virtual_network.main
terraform state mv azurerm_subnet.linux_subnet module.linux_vm.azurerm_subnet.linux_subnet
terraform state mv azurerm_subnet.windows_subnet module.windows_vm.azurerm_subnet.windows_subnet
terraform state mv azurerm_subnet_network_security_group_association.linux_subnet_nsg_association module.linux_vm.azurerm_subnet_network_security_group_association.linux_subnet_nsg_association
terraform state mv azurerm_subnet_network_security_group_association.windows_subnet_nsg_association module.windows_vm.azurerm_subnet_network_security_group_association.windows_subnet_nsg_association

# linux_vm 模块
terraform state mv azurerm_linux_virtual_machine.linux_vm module.linux_vm.azurerm_linux_virtual_machine.linux_vm
terraform state mv azurerm_network_interface.linux_vm_nic module.linux_vm.azurerm_network_interface.linux_vm_nic
terraform state mv azurerm_network_security_group.linux_subnet_nsg module.linux_vm.azurerm_network_security_group.linux_subnet_nsg
terraform state mv azurerm_public_ip.linux_vm_public_ip module.linux_vm.azurerm_public_ip.linux_vm_public_ip

# windows_vm 模块
terraform state mv azurerm_windows_virtual_machine.windows_vm module.windows_vm.azurerm_windows_virtual_machine.windows_vm
terraform state mv azurerm_network_interface.windows_vm_nic module.windows_vm.azurerm_network_interface.windows_vm_nic
terraform state mv azurerm_network_security_group.windows_subnet_nsg module.windows_vm.azurerm_network_security_group.windows_subnet_nsg
terraform state mv azurerm_public_ip.windows_vm_public_ip module.windows_vm.azurerm_public_ip.windows_vm_public_ip
```

可选但建议保留：

```bash
# 如果 resource group 没有模块化，也可以不动
terraform state mv azurerm_resource_group.main azurerm_resource_group.main
```

## 运行建议

1. 在运行 terraform state mv 之前备份 tfstate 文件（很重要）：

```bash
cp terraform.tfstate terraform.tfstate.bak.manual-mv
```

1. 然后一行行执行上面命令，或者保存成 shell 脚本 batch-mv.sh 执行。
2. 最后运行 terraform plan 验证是否只显示「0 to add, 0 to destroy」：

```bash
terraform plan
```

如果你看到 plan 里只剩些小变更 like ~（update），那就说明迁移成功

## backup file

当我们运行完成 `terraform state mv` 命令之后，就会发现多出了很多的 tfstate 文件

```shell
...
terraform.tfstate.1745482843.backup
terraform.tfstate.1745482846.backup
terraform.tfstate.1745482848.backup
terraform.tfstate.1745482851.backup
terraform.tfstate.1745482854.backup
terraform.tfstate.1745482857.backup
terraform.tfstate.1745482860.backup
terraform.tfstate.1745482863.backup
terraform.tfstate.1745482866.backup
terraform.tfstate.1745482869.backup
terraform.tfstate.1745482872.backup
terraform.tfstate.1745482875.backup
terraform.tfstate.1745482878.backup
...
```

这些多出来的文件是 Terraform 在你运行 terraform state mv 等命令时，为了「保护你」自动生成的状态备份。下面我来详细解释它们的作用、是否可以删除，以及最佳实践。

这些文件是做什么的？

都是 Terraform 每一次运行 terraform state mv 的时候自动生成的临时备份文件。它们的命名规则是：

terraform.tfstate..backup

每一次你执行一次 mv，Terraform 会在 mv 之前复制一份 tfstate，确保你即使搞砸了 state，也有回滚的机会。



## 可以删除吗？

可以删除，但建议这样做：

- 删除之前先确认当前的 terraform.tfstate 是稳定且有效的（比如你刚才 terraform plan 是 0 changes）
- 可以保留 terraform.tfstate.backup（没有时间戳的那个）作为额外备份
- 其他带时间戳的临时 backup（.17454xxxxx.backup）是安全删除的

你可以这样批量删除这些临时文件（保留最后一份 .backup）：

```bash
rm terraform.tfstate.*.backup
```

提示：你也可以打个压缩包保存在别处，比如：

```bash
tar czf tfstate-backups-20240424.tar.gz terraform.tfstate.*.backup
```

然后删除源文件。



## Terraform 的自动保护机制真的很贴心

实际上，每一次 terraform apply、state mv、state rm，都会自动生成 backup。你不小心 mv 错了，甚至删除了资源，手动替换 tfstate 还能救回来。

## 总结一下

| 文件名                    | 意义                     | 是否可以删除                       |
| ------------------------- | ------------------------ | ---------------------------------- |
| terraform.tfstate         | 当前使用的 state 文件    | ❌ 不要删                           |
| terraform.tfstate.backup  | apply 时自动备份         | ✅ 可留作一份安全备份               |
| terraform.tfstate..backup | 每次 mv 操作时的中间备份 | ✅ 可以删除（建议 plan 后确认无误） |

建议你把 terraform.tfstate 加入版本控制 .gitignore：

在 .gitignore 里加：

```
terraform.tfstate*
```

否则一不小心 push 到 GitHub 会很危险（包括资源 ID、密码、Public IP 等）