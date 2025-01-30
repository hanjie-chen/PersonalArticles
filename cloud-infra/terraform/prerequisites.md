# 下载 terraform

在 terraform 的官网下载地址下载 terraform [Install | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/install)

可以使用命令 `terraform --version` 来验证是否下载完成

```shell
Plain@Linux-VM:~/Personal_Project/azure-vm-terraform$ terraform --version
Terraform v1.10.5
on linux_amd64
```

# Azure auth

要让 Terraform 操作你的 Azure 资源，需通过以下任一种方式认证：

### 方式 1：Azure CLI 登录（推荐）

关于如何安装 Azure CLI [^down-azure-cli] 简单来说一个命令就可以搞定

```shell
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

然后登陆 并且选择 subscription

```bash
az login
```

登陆之后，可以使用下面的命令确认是否已经登陆

```shell
az account show
```

#### **方式 2：服务主体认证（适合 CI/CD）**

```hcl
# 在 provider 块中直接配置（不推荐提交到版本库）
provider "azurerm" {
  features {}

  subscription_id = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
  client_id       = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
  client_secret   = "xxxxxxxxxxxxxxxxxx"
  tenant_id       = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
}
```

# Azure provider

terraform 需要 azurerm provider 才能和 Azure 交互，使用 `terraform init` 命令，会自动分析 tf 代码中的插件并且下载

比如说在 `provider.tf` 中

```yaml
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
```

参考 [Quickstart: Create an Azure resource group using Terraform | Microsoft Learn](https://learn.microsoft.com/en-us/azure/developer/terraform/create-resource-group?tabs=azure-cli)



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

## `.terraform.lock.hcl` 文件

`.terraform.lock.hcl` 文件是 Terraform 的供应商锁定文件。它记录了当前 Terraform 配置所依赖的 提供者（providers） 的具体版本和源信息。为了确保团队中所有人在运行 Terraform 配置时都使用相同版本的提供者，避免因为提供者版本差异导致的问题。

我们需要将其纳入git repository中

> [!note]
>
> 当您在一个目录中运行 `terraform init` 时，Terraform 会根据以下情况处理 `.terraform.lock.hcl` 文件：
>
> 目录中已有 `.terraform.lock.hcl` 文件，Terraform 会读取现有的 `.terraform.lock.hcl` 文件，并按照其中指定的提供者版本进行初始化。
>
> 如果目录中不存在 `.terraform.lock.hcl` 文件，Terraform 会在初始化过程中 生成一个新的 `.terraform.lock.hcl` 文件。

## `.terraform/` 文件夹

`.terraform/` 文件夹是 Terraform 的本地工作目录，用于存储下载的提供者插件和模块等缓存数据。因为这个命令仅仅存放自动生成的缓存和二进制文件，所以我们应该在 `.gitignore` 中忽略这个目录。

运行 `terraform init` 命令时，Terraform 会在此目录中下载和存储所需的提供者和模块。





# `terraform validate`

`terraform validate` 用于验证 Terraform 配置文件的语法和逻辑是否正确。这一步可以帮助您尽早发现配置中的错误。

e.g.

```shell
Plain@Linux-VM:~/Personal_Project/azure-vm-terraform$ terraform validate
Success! The configuration is valid.
```

# `terraform plan`

`terraform plan` 会生成一个执行计划，显示 Terraform 将创建、修改或销毁哪些资源，以及具体的变更内容。仔细查看输出的计划，确保所有操作都符合您的预期。



# `terraform apply`

`terraform apply` 将根据执行计划，实际在 Azure 上创建和配置资源。命令执行过程中，Terraform 会再次显示执行计划，并提示您输入 `yes` 以确认执行。提示：如果您希望自动确认（在非交互式环境中使用时），可以使用 `-auto-approve` 参数：

```bash
terraform apply -auto-approve
```



## `.terraform.tfstate` 文件

#### 什么是 `terraform.tfstate` 文件？

`terraform.tfstate` 是 **Terraform 的状态文件**，用于跟踪和记录由 Terraform 创建和管理的资源的当前状态。

- Terraform 通过状态文件了解哪些资源已经被创建，以及它们的属性，以便在后续的 `plan` 和 `apply` 操作中正确地更新和管理资源。

- 状态文件以 JSON 格式存储，包含资源的详细信息，如资源 ID、属性值等。
- **注意**：状态文件中可能包含敏感信息，例如资源的连接信息。

#### **1.2. 是否需要将 `terraform.tfstate` 文件纳入版本控制（Git）？**

建议不要将 `terraform.tfstate` 文件提交到 Git 等版本控制系统

原因：

安全风险：

- 状态文件可能包含敏感信息，如 IP 地址、资源 ID，甚至可能包含密码或访问密钥等。
- 将状态文件提交到版本控制系统，可能导致敏感信息泄露。

合并冲突：

- 状态文件会在每次 `terraform apply` 后更新，如果多个团队成员同时修改并提交状态文件，容易产生合并冲突。

数据一致性：

- 本地状态文件适用于单人工作环境，在团队协作中，使用本地状态文件会导致状态不一致的问题。

# `terraform output`

部署完成后，Terraform 会显示您在 `outputs.tf` 中定义的输出变量。您也可以随时运行以下命令查看输出：

```bash
terraform output
```



# Reference

[^down-azure-cli]: [How to install the Azure CLI | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)