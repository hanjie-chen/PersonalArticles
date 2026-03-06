# GCP auth

要让 Terraform 操作你的 GCP (Google Cloud Platform) 资源，需通过以下任一种方式认证：

## 方式 1：gcloud CLI 登录（推荐）

[Install the Google Cloud CLI | Google Cloud](https://cloud.google.com/sdk/docs/install) 简单来说一个命令就可以搞定（以 Linux 环境为例）：

```shell
curl https://sdk.cloud.google.com | bash
```

安装完成后，重启终端，然后进行登陆。

注意： Terraform 需要的是应用默认凭据（ADC），所以登录命令与普通的 `gcloud auth login` 略有不同：

```bash
gcloud auth application-default login
```
执行后会弹出一个网页让你授权。成功之后就能看到这样子：

```shell
Credentials saved to file: [/home/plain/.config/gcloud/application_default_credentials.json]

These credentials will be used by any library that requests Application Default Credentials (ADC).
```

路径 `[/home/plain/.config/gcloud/application_default_credentials.json]` 已经生成，这意味着 Terraform 已经就绪了。

### 为什么这个 JSON 文件很重要？

在终端运行 `terraform plan` 时，Terraform 的 Google Provider 会按照以下逻辑寻找“通行证”：

1. 检查环境变量 `GOOGLE_APPLICATION_CREDENTIALS`。
2. （重点）检查你刚生成的这个 `application_default_credentials.json` 文件。
3. 如果是在 GCP 虚拟机内部，检查元数据服务器。

## 方式 2：服务账号认证（适合 CI/CD）

在 GCP 中，自动化流水线通常使用服务账号（Service Account）生成的 JSON 密钥文件进行认证。

```hcl
# 在 provider 块中直接配置 JSON 密钥文件的路径
# （强烈建议将 .json 文件加入 .gitignore，绝对不要提交到版本库！）
provider "google" {
  credentials = file("service-account-key.json")

  project = "your-gcp-project-id"
  region  = "us-central1"
  zone    = "us-central1-c"
}
```
(注：在 CI/CD 环境中，更好的最佳实践是不写 `credentials` 字段，而是将 JSON 密钥路径配置到环境变量 `GOOGLE_APPLICATION_CREDENTIALS` 中，Terraform 会自动读取。)

# GCP provider

terraform 需要 `google` provider 才能和 GCP 交互，使用 `terraform init` 命令，会自动分析 tf 代码中的插件并且下载。

比如说在 `provider.tf` 中：

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

# 配置 GCP 的核心参数
provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}
```

参考 [Get started with Terraform | Google Cloud](https://cloud.google.com/docs/terraform/get-started-with-terraform)

# GCP VS Azure 

1. 认证命令不同：Azure 用 `az login` 就能搞定一切；GCP 必须用带 `application-default` 的登录命令，否则 Terraform 依然会报找不到凭证。
2. 层级概念不同：Azure 强制要求建 `Resource Group`（资源组）；而 GCP 的顶级单位是 `Project`（项目），所以 GCP 的 Provider 里必须要填 `project = "xxx"`。