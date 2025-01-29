当我们使用 terraform 创建一台 vm 的时候，会发现 `os_disk` block 是必须要选择的，实际上对对应的就是 Azure portal 创建 virutal machine 界面的 disk 部分

![vm disk](./images/vm-disk.png)

根据这篇terraform 的文章 [azurerm_linux_virtual_machine | Resources | hashicorp/azurerm | Terraform | Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_virtual_machine)

这个 os_disk block 存在2个必选项 `caching` `storage_account_type`

其中 对应这篇vm的文章，但是我没有看明白，得去问
