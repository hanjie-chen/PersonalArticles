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

# Reference

[^down-azure-cli]: [How to install the Azure CLI | Microsoft Learn](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)