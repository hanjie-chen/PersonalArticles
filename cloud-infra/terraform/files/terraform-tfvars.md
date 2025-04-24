# `terraform.tfvars` 文件

当我们在 terraform 项目中需要用到某些 sensitive data 的时候（比如说密码，sub id 等）我们往往不能直接的写入 varialbes 文件，其中一个解决方案是使用 `terraform.tfvars` 文件

将这些 sensitive data 写入这个文件，并且不纳入版本控制（git）



# `terraform.tfvars`in modules

对于一个采用 modules 的 terraform 项目，应该如何使用 `terraform.tfvars` 文件呢？

现在你提到的问题是关于如何处理 `terraform.tfvars` 文件，特别是涉及到敏感数据（如 `linux_vm_admin_password` 和 `windows_vm_admin_password`）时，是否需要在 `modules/linux-vm` 和 `modules/windows-vm` 文件夹下分别创建 `terraform.tfvars` 文件。以下是详细的解答。

---

### 你需要做什么？
**你不需要在 `modules/linux-vm` 或 `modules/windows-vm` 文件夹下创建 `terraform.tfvars` 文件。** Terraform 的设计中，`terraform.tfvars` 文件是为根模块（即项目的主目录）提供变量值的，而不是为每个模块单独设置的。正确的做法是：

1. **保留根模块的 `terraform.tfvars` 文件**：继续在项目的主目录（`~/projects/azure-vm-terraform/`）中保留 `terraform.tfvars` 文件，并定义所有全局变量的值，包括敏感数据。
2. **通过根模块传递变量给子模块**：在根模块的 `main.tf` 文件中调用模块时，将这些变量的值传递给相应的模块。
3. **保护敏感数据**：确保敏感数据不会被上传到版本控制系统（如 Git）。

下面我会一步步解释如何实现。

---

### 具体步骤

#### 1. 保留根模块的 `terraform.tfvars` 文件
你的 `terraform.tfvars` 文件已经包含了全局变量的值，例如：
```hcl
subscription_id = "XXX"
linux_vm_admin_password = "XXX"
windows_vm_admin_password = "XXX"
```
- 这个文件应该保留在项目的主目录（即 `~/projects/azure-vm-terraform/terraform.tfvars`），不需要移动或复制到模块文件夹。
- 因为它包含敏感数据（如管理员密码），你需要确保它不会被上传到版本控制系统。可以在 `.gitignore` 文件中添加以下内容：
  ```
  terraform.tfvars
  ```

#### 2. 在根模块中定义全局变量
在根模块的 `variables-general.tf` 文件中，定义所有全局变量，包括敏感数据。例如：
```hcl
variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "linux_vm_admin_password" {
  description = "Admin password for Linux VM"
  type        = string
  sensitive   = true
}

variable "windows_vm_admin_password" {
  description = "Admin password for Windows VM"
  type        = string
  sensitive   = true
}
```
- 这些变量的值会从 `terraform.tfvars` 文件中读取。

#### 3. 在模块中定义输入变量
你的模块已经正确定义了输入变量。例如：
- 在 `modules/linux-vm/variables-linux.tf` 中：
  ```hcl
  variable "linux_vm_admin_password" {
    description = "Plain user password for the Linux VM"
    type        = string
    sensitive   = true
  }
  ```
- 在 `modules/windows-vm/variables-windows.tf` 中：
  ```hcl
  variable "windows_vm_admin_password" {
    description = "Admin password for the Windows VM"
    type        = string
    sensitive   = true
  }
  ```
  这些变量是模块的输入参数，它们不需要直接读取任何 `.tfvars` 文件，而是等待根模块传递具体的值。

#### 4. 在根模块的 `main.tf` 中调用模块并传递变量
在项目主目录的 `main.tf` 文件中（如果还没有这个文件，可以创建一个），调用模块并将根模块的变量传递给它们。例如：
```hcl
module "linux_vm" {
  source                  = "./modules/linux-vm"
  linux_vm_admin_password = var.linux_vm_admin_password
  # 其他参数...
}

module "windows_vm" {
  source                    = "./modules/windows-vm"
  windows_vm_admin_password = var.windows_vm_admin_password
  # 其他参数...
}
```
- 这里，`var.linux_vm_admin_password` 和 `var.windows_vm_admin_password` 是根模块的变量，它们的值来自 `terraform.tfvars` 文件。
- Terraform 会自动将这些值传递给模块使用。



### 为什么不需要在模块文件夹下创建 `terraform.tfvars`？

- **Terraform 的工作机制**：`terraform.tfvars` 文件是为根模块提供变量值的，Terraform 在运行时只会从根模块的目录读取这个文件。
- **模块的角色**：模块（如 `linux-vm` 和 `windows-vm`）是可重用的组件，它们的变量值是通过根模块调用时传递的，而不是直接从模块文件夹中的 `.tfvars` 文件读取。
- **避免冗余**：如果在每个模块文件夹下创建 `terraform.tfvars`，Terraform 不会自动识别这些文件，反而会导致管理混乱。
