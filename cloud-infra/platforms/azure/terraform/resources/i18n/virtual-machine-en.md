<!-- source_blob: 58da4b17181341f7a552503d4d35d560d0af7cae -->

# VM OS disk setting

When we use Terraform to create a VM, we find that the `os_disk` block must be specified. In practice, this corresponds to the disk section in the Azure portal when creating a virtual machine.

![vm disk](./resources/images/vm-disk.png)

According to this Terraform article: [azurerm_linux_virtual_machine | Resources | hashicorp/azurerm | Terraform | Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_virtual_machine)

This `os_disk` block has 2 required options: `caching` and `storage_account_type`.

## caching

In the Azure portal, `caching` refers to Host caching.

![caching](./resources/images/caching.jpeg)

When creating an Azure VM in the portal, the OS disk caching cannot be specified, but the data disk caching can.

![create-vm-disk-caching](./resources/images/create-vm-disk-caching.jpeg)

For more details about Azure VM disks, see this [document](../native/virtual-machine/virtual-machine.md).

To summarize the differences between the 3 options in one sentence:

- **ReadOnly**: Caching accelerates reads only, not writes.
- **ReadWrite**: Caching accelerates both reads and writes, but it comes with risk.
- **None**: No caching, slower but more stable.

## storage account type

As for `stroage_account_type`, it is actually the OS disk type.

> [`storage_account_type`](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_virtual_machine#storage_account_type-1) - (Required) The Type of Storage Account which should back this the Internal OS Disk. Possible values are `Standard_LRS`, `StandardSSD_LRS`, `Premium_LRS`, `StandardSSD_ZRS` and `Premium_ZRS`. Changing this forces a new resource to be created.

Here, LRS means local redundant storage, and ZRS means zone redundant storage.

![disk type](./resources/images/disk-type.png)

# About the default disk size

Since we did not actually set the disk size with `disk_size_gb`, the default size will be used.

In Azure, when you create a virtual machine and do not specify the operating system disk (OS Disk) size, the **default size is**:

- **Linux virtual machine:** 30 GB
- **Windows virtual machine:** 127 GB

In practice, though, the default size feels sufficient for both Linux and Windows.

# VM image

In Azure Terraform, an image is identified by 4 properties.

```
source_image_reference {
    publisher = "Canonical"
    offer = "ubuntu-24_04-lts"
    sku = "server"
    version = "latest"
 }
```

To get these 4 properties, you can use the command `az vm image list --output table`, which shows some of the most commonly selected images.

[Find and use marketplace purchase plan information using the CLI - Azure Virtual Machines | Microsoft Learn](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/cli-ps-findimage)

![image list](./resources/images/image-list-less.png)

If you want to see all images, you need to add the `--all` parameter.

```shell
az vm image list --all
```

However, this command takes a very, very long time to run, far longer than a normal person would want to wait.

You can go to [Azure VM Image List](https://az-vm-image.info/) to view all images. Under the hood it is still running this command, but it is much faster.

There is also a reverse method: you can extract this information from an already created Azure VM.

Use the `az` command:

```
az vm show --resource-group <rg-name> --name <VM-name> --query "storageProfile.imageReference"
```

Output like:

```
{
    "communityGalleryImageId": null,
    "exactVersion": "19045.4529.240607",
    "id": null,
    "offer": "Windows-10",
    "publisher": "MicrosoftWindowsDesktop",
    "sharedGalleryImageId": null,
    "sku": "win10-22h2-pro-g2",
    "version": "latest"
  }
```

You can extract the relevant information from this output.

## Marketplace

You can also check Azure Marketplace to see some information, such as the publisher ID and product ID, though the capitalization of those two may not match exactly.

![marketplace image info](./resources/images/marketplace-image.png)

You can also search for some keywords on [Azure VM Image List](https://az-vm-image.info/) and combine that with Grok 3.

## ARM template

We do not need to actually create the VM. We only need to go as far as the review screen, where you can see `Download a template for automation` in the lower-right corner. Click it.

![arm-template](./resources/images/arm-template.png)

On that page, simply press Ctrl + F and search for `imagereference` to find it.

![arm tempalte image reference](./resources/images/arm-image-reference.png)

# VM size

You can refer to this [document](../native/virtual-machine/virtual-machine.md).

# Windows virtual machine

[azurerm_windows_virtual_machine | Resources | hashicorp/azurerm | Terraform | Terraform Registry](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/windows_virtual_machine)

One more thing to note about a Windows VM is `compute_name`. If you do not set it explicitly, it will default to the value provided in `name`.

> [`computer_name`](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/windows_virtual_machine#computer_name-1) - (Optional) Specifies the Hostname which should be used for this Virtual Machine. If unspecified this defaults to the value for the `name` field. If the value of the `name` field is not a valid `computer_name`, then you must specify `computer_name`. Changing this forces a new resource to be created.

However, because Windows has a 15-character limit for computer names (NetBIOS names), which is a historical convention inherited from NetBIOS and early Windows networking protocols, if you do not configure `compute_name` and your `name` exceeds 15 characters, you will get the following error:

```shell
│ Error: unable to assume default computer name "computer_name" can be at most 15 characters, got 20. Please adjust the "name", or specify an explicit "computer_name"
```
