# terraform 语法基础

在 Terraform 中，资源块的语法格式是：

```cpp
resource "<resource-type>" "<local-resource-name>" {
  # 资源配置
}
```

e.g.

```cpp
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.resource_region
}
```

这里，`"azurerm_resource_group"` 是资源类型，表示你要创建一个 Azure 的资源组。而 `"main"` 是 **本地资源名称**（Local Name），在 Terraform 的文档和语法中，这部分被称为 资源名称 或 逻辑名称。作用：

- **标识资源实例：** 这个名称用于在 Terraform 配置中唯一标识这个资源实例，便于在其他地方引用。例如：

  ```cpp
  resource "azurerm_virtual_network" "main" {
    name                = var.vnet_name
    resource_group_name = azurerm_resource_group.main.name
    # 这里的azurerm_resource_group.main.name就是引用了你之前定义的资源组
  }
  ```

- **逻辑组织：** 通过赋予有意义的名称，可以提高配置文件的可读性和可维护性。

**注意：**

- 这个名称在 Terraform 配置的范围内必须是唯一的，但在 Azure 等云提供商的实际资源中，这个名称不会被使用。
- 你可以根据自己的喜好和项目需要，选择合适的名称。例如，有人喜欢用 `"main"`，也有人可能用更具体的名称，如 `"resource_group"` 或 `"rg"`。

因此，`main` 在这里是 Terraform 中资源的本地名称，用于在配置中引用该资源。