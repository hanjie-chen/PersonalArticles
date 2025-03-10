# terraform import

terraform import 用于 import 目前不是由当前 tfstate 管理的 Azure resource. 但是如果Azure portal 上面的reosurce 是由当前的 tfstate 管理的，那么 terraform import 便无法生效

比如说，我从 github repository 上面上下了



## import common resource

对于一般的 resoruce 而言 Terraform 的 import 命令格式是：

```shell
terraform import <resource-type>.<resource-name> <resource-id>
```

e.g.

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



## import association resource

对于 azurerm_subnet_network_security_group_association 这样的资源，它并不是一个独立的实体，而是表示子网（Subnet）和网络安全组（NSG）之间的关联关系。因此，它的资源 ID 并不是一个独立的 ID，而是直接使用子网的 ID 来标识这种关联。

```shell
terraform import azurerm_subnet_network_security_group_association.windows_subnet_nsg_association <subnet>
```

