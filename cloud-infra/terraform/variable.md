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

# Sensitive varialbes

当我们使用 git 这样子的版本控制的时候，对于某些特别的变量，比如说密码等敏感信息，不能上传和暴露，那么我们应该怎么办呢？

## 方法一：使用 Terraform 的 `-var` 命令行参数传递密码

你可以在运行 `terraform apply` 或 `terraform plan` 时，通过命令行传递密码变量。**步骤：**

1. **在 `variables.tf` 中，声明 `admin_password` 变量，但不要设置默认值。并将变量标记为敏感的。**

   ```cpp
   variable "admin_password" {
     description = "Admin password for the Linux VM"
     type        = string
     sensitive   = true
   }
   ```

   **注意：** `sensitive = true` 标记这个变量为敏感的，Terraform 在输出日志时将不会显示其值。

2. **在运行 Terraform 命令时，通过命令行参数传递密码。**

   ```bash
terraform apply -var "admin_password=YourSecurePassword123!"
   ```


## 方法二：使用 `terraform.tfvars` 文件

你可以创建一个名为 `terraform.tfvars` 的文件，其中包含你的密码变量。然后，将该文件添加到 `.gitignore` 中，防止其被提交到 GitHub。**步骤：**

1. **创建 `terraform.tfvars` 文件：**

   ```cpp
admin_password = "YourSecurePassword123!"
   ```

2. **在 `.gitignore` 文件中，添加 `terraform.tfvars`：**

   ```
   # .gitignore
   terraform.tfvars
   ```
   
3. 在 `variables.tf` 中，声明 `admin_password` 变量，不设置默认值，并标记为敏感的。

   ```cpp
   variable "admin_password" {
     description = "Admin password for the Linux VM"
     type        = string
     sensitive   = true
   }
   ```
   
4. Terraform 会自动读取 `terraform.tfvars` 中的变量值。

## 方法三：使用环境变量

Terraform 允许你通过环境变量来传递变量值。环境变量的命名格式为：`TF_VAR_变量名`。**步骤：**

1. **在 `variables.tf` 中，声明 `admin_password` 变量，不设置默认值，并标记为敏感的。**

   ```cpp
   variable "admin_password" {
     description = "Admin password for the Linux VM"
     type        = string
     sensitive   = true
   }
   ```
   
2. **在运行 Terraform 命令的终端中，设置环境变量：**

   ```bash
export TF_VAR_admin_password="YourSecurePassword123!"
   ```

3. **运行 Terraform 命令：**

   ```bash
   terraform apply
   ```

## 方法四：使用输入提示（交互式输入）

你可以让 Terraform 在运行时提示输入密码。**步骤：**

1. **在 `variables.tf` 中，声明变量，并设置 `description`，不设置默认值，并标记为敏感的。**

   ```cpp
   variable "admin_password" {
     description = "Admin password for the Linux VM (will be prompted)"
     type        = string
     sensitive   = true
   }
   ```
   
2. **运行 Terraform 命令时，添加 `-var` 参数，但不指定值。Terraform 将提示你输入变量值。**

   ```bash
   terraform apply -var="admin_password"
   ```

   **Terraform 输出：**
   
   ```javascript
   var.admin_password
     Admin password for the Linux VM (will be prompted):
   
     Enter a value:
   ```
   
3. **在提示时，输入密码。**

注意： 这种方法在某些 Terraform 版本中可能会提示输入，具体取决于 Terraform 版本和设置。
