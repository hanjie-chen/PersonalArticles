# `Terraform init`

`terraform init` 与 `git init` 类似，都是初始化项目环境的命令，但目的不同：

- `git init`：初始化一个 Git 仓库，用于版本控制。
- `terraform init`：初始化 Terraform 工作目录，为后续操作准备环境。

`terraform init` 的核心功能：

1. 下载 Provider 插件：
   根据配置文件（如 `provider.tf`）中声明的云平台（如 Azure），自动下载对应的 Provider（如 `azurerm`）。
2. 初始化后端（Backend）：
   配置状态文件（`.tfstate`）的存储位置（默认本地存储，生产环境可配置到 Azure Storage 等）。
3. 安装模块（Module）：
   如果代码中引用了外部模块（如网络模块），会从指定源下载。

何时执行 `terraform init`？

- 必要条件：
  在编写了至少一个 `.tf` 文件（如 `provider.tf`）之后执行。
  Terraform 需要根据配置文件中的内容来决定初始化哪些组件。
- 为什么需要先写配置文件？
  例如：如果 `provider.tf` 中声明了 `azurerm`，`terraform init` 会下载 Azure Provider 插件。

for example

```shell
Plain@Linux-VM:~/Personal_Project/azure-vm-terraform$ terraform init
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 4.16"...
- Installing hashicorp/azurerm v4.16.0...
- Installed hashicorp/azurerm v4.16.0 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

这个命令会生成 `.terraform.lock.hcl` 文件和 `.terraform` 文件夹