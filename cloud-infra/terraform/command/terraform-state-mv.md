# background

当我们将一个普通的 terraform 项目重构为使用 modules 之后，并且使用 terraform validate 确定语法没有问题。

然后使用 terraform plan 的时候，就有可能会发现：

```shell
...
Plan: 13 to add, 0 to change, 13 to destroy.
...
```

也就是 Terraform 想「删除所有现有资源再重建一遍」，而不是简单地 update

### 这是为什么呢？

当我们重构了模块（文件结构变了），而 Terraform 的状态文件（.tfstate）中，旧的资源定义还保留着「老位置路径」，现在 Terraform 认为这些资源“不在代码中”了。

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

### 这合理吗？

技术上是合理的，但在生产环境或你已经部署了重要资源时，这是不可接受的。我需要的是保留已有资源，并让 Terraform 继续追踪它们，而不是重建它们。



# resolution: terraform state mv

如果想要「保留资源不被删重建」，那么我们就需要手动告诉 Terraform：这些旧资源，其实对应的是模块里面的新资源路径

我们可以使用 terraform state mv 命令来「迁移状态」：

比如：

```bash
terraform state mv \
  azurerm_linux_virtual_machine.linux_vm \
  module.linux_vm.azurerm_linux_virtual_machine.linux_vm
```

这时，我们需要获取旧资源地址和新资源地址

### old resource address

我们可以使用 `terraform state list` 命令查看当前资源状态（也就是旧资源地址）

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

或者一般来说，如果资源直接定义在 main.tf，没有模块嵌套，那么地址就是 `<resource-type>.<resource-name>`

### new resource address

而如果资源在 module 里，地址就是 `module.<module-name>.<resource-type>.<resource-name>`

### for example

main.tf 中存在

```hcl
module "banana" {
  source = "./modules/linux-vm"  # 路径随便叫
}
```

Terraform 现在的资源地址（state list 中）是：`azurerm_linux_virtual_machine.linux_vm`

而在模块化结构中，它们应该变成：`module.banana.azurerm_linux_virtual_machine.linux_vm`



## migrate scripts

我们可以写一个脚本写上所有的 mv 命令，然后一次性运行完成，比如说类似于下面的脚本

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



> [!note]
>
> 在运行 terraform state mv 之前记得备份 tfstate 文件（很重要）：
>
> ```bash
> cp terraform.tfstate terraform.tfstate.bak.manual-mv
> ```
>
> 最后运行 terraform plan 验证是否只显示「0 to add, 0 to destroy」，如果你看到 plan 里只剩些小变更 like ~（update），那就说明迁移成功

## auto backup file after `mv`

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

这些多出来的文件是 Terraform 在你运行 terraform state mv 等命令时，自动生成的状态备份。

它们的命名规则是：`terraform.tfstate.<timestamp>.backup`

每一次你执行一次 mv，Terraform 会在 mv 之前复制一份 tfstate，确保你即使搞砸了 state，也有回滚的机会。

删除之前先确认当前的 terraform.tfstate 是稳定且有效的（比如你刚才 terraform plan 是 0 changes）

> [!tip]
>
> 可以这样批量删除这些临时文件：
>
> ```bash
> rm terraform.tfstate.*.backup
> ```
>

| file                                   | usage                    | delete?                          |
| -------------------------------------- | ------------------------ | -------------------------------- |
| `terraform.tfstate`                    | 当前使用的 state 文件    | 不要删                           |
| `terraform.tfstate.backup`             | apply 时自动备份         | 可留作一份安全备份               |
| `terraform.tfstate.<timestamp>.backup` | 每次 mv 操作时的中间备份 | 可以删除（建议 plan 后确认无误） |

