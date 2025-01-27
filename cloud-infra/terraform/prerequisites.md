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

# Reference

[^down-azure-cli]: [How to install the Azure CLI | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)