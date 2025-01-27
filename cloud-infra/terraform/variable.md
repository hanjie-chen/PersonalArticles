我们往往在 variable.tf 这个文件中编写那些可以用来复用的变量，例如 resource location

```yaml
variable "resource_region" {
  description = "Azure resource location: Singapore"
  default = "southeastasia"
}
```

Azure 对于位置名称有两种表示方式：

1. 人类可读的名称（Display Name）：例如 "Southeast Asia"、"East US" 等，通常在 Azure 门户中显示。
2. 地点代码（Location Name 或 Location Code）：例如 "southeastasia"、"eastus" 等，通常用于 API 调用和脚本中。

在 Terraform 中，AzureRM 提供程序（Azure Resource Manager Provider）同时接受这两种形式的位置名称。

但是，推荐使用标准的区域代码（canonical location names），即全小写、无空格的形式，例如 `"southeastasia"`。这是因为：使用标准的区域代码可以确保您的配置与 Azure 的 API、CLI 和 SDK 保持一致。这些工具通常使用标准的区域代码来指定位置。

# 如何使用 varialbes.tf 中定义的变量

再其他的 tf 文件，比如说 network.tf 中我们可以使用 `var.<variable-name>` 的方式来使用再 variables.tf 中定义的变量

e.g.

```yaml
# varialbes.tf
variable "resource_region" {
  description = "Azure resource location: Singapore"
  default = "southeastasia"
}

variable "resource_group_name" {
    description = "resource group name"
    default = "Singapore-RG"
}
```

```yaml
# network.tf
# create resource group
resource "azurerm_resource_group" "main" {
  name = var.resource_group_name
  location = var.resource_region
}
```

