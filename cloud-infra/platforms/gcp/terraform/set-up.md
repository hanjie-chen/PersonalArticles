---
Title: GCP Terraform 入门设置
Author: 陈翰杰
Instructor: gemini-3.1-pro-preview
CoverImage: ./resources/images/tf-gcp-cover.avif
RolloutDate: 2026-03-08
---

```
BriefIntroduction: 
使用 terraform 操纵 GCP resoruce 的入门设置和一些准备工作
```

<!-- split -->

![tf gcp cover](./resources/images/tf-gcp-cover.avif)

要让 Terraform 操作 GCP (Google Cloud Platform) 的资源，我们首先需要在代码中配置 Provider，然后为 Terraform 提供操作 GCP 的身份凭证。

# GCP Provider

在 `provider.tf` 中，我们需要声明使用 `google` 插件，并配置核心参数。

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# 最佳实践：这里只写项目和区域，不要把 credentials (密钥) 写死在这里
provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}
```

参考 [Get started with Terraform | Google Cloud](https://cloud.google.com/docs/terraform/get-started-with-terraform)

代码写好后，使用 `terraform init` 下载插件。接下来，Terraform 会自动去系统环境中寻找身份凭证（通行证）。针对不同的工作场景，我们有不同的认证方式：

# Authentication

## Local Development

在自己的电脑上写代码时，最安全、最简单的方式是使用 gcloud CLI 生成本地应用默认凭据 (ADC)。

1. 安装 gcloud CLI（以 Linux 为例）：

   ```shell
   curl https://sdk.cloud.google.com | bash
   ```

2. 执行 ADC 登录：

   注意：Terraform 需要的是 ADC 凭据，所以必须带 `application-default` 参数

   ```bash
   gcloud auth application-default login
   ```

原理解析：

执行授权后，终端会提示生成了一个 JSON 文件（如 `~/.config/gcloud/application_default_credentials.json`）。

当你敲下 `terraform plan` 时，Terraform 会自动找到这个隐藏文件并拿着它去操作 GCP。

## CI/CD Pipeline

在 GitHub Actions 或 GitLab CI 等“无头服务器”中，无法弹出浏览器扫码登录。此时我们需要使用机器级别的身份。

### :x: 传统方式：Service Account

过去的做法是去 GCP 控制台下载一个 Service Account 的 `.json` 静态密钥文件。

- 配置法：在 CI/CD 中把 JSON 存入 Secrets，并在运行时通过环境变量 `GOOGLE_APPLICATION_CREDENTIALS` 指向该文件供 Terraform 读取。
- 痛点：长期有效的静态密钥存在极大的泄露风险，且需要定期轮换。

### :heavy_check_mark: 最佳实践：Workload Identity Federation (WIF)

这是目前 Google 官方强烈推荐的无密钥认证方式，彻底告别了 JSON 文件。

- 核心逻辑：通过 OIDC 协议，让 GitHub Actions 与 GCP 建立信任关系，动态交换“短效临时 Token”。

- CI/CD 用法（以 GitHub Actions 为例）：

  在 `.yml` 流水线中，引入 Google 官方的 auth 动作即可：

  ```yaml
  - id: 'auth'
    uses: 'google-github-actions/auth@v2'
    with:
      # 填入在 GCP 预先配置好的 WIF 资源 ID 和绑定的服务账号
      workload_identity_provider: 'projects/123/locations/global/workloadIdentityPools/my-pool/providers/my-provider'
      service_account: 'terraform-sa@your-project.iam.gserviceaccount.com'
  
  - name: 'Terraform Plan'
    run: 'terraform plan'
  ```

  执行完 `auth` 步骤后，它会在 CI 环境里自动伪装成 ADC 环境变量，后续的 Terraform 命令会像在本地一样“无感”且安全地运行！

# GCP vs Azure

如果习惯了 Azure，切换到 GCP 时请牢记这两个最大区别：

1. 认证命令不同：
   - Azure：`az login` 就能搞定一切。
   - GCP：必须用 `gcloud auth application-default login`，只用普通的 `gcloud auth login` 会导致 Terraform 依然报找不到凭证。
2. 层级概念不同：
   - Azure：顶级资源容器是 `Resource Group`（资源组），建任何东西都要先建它。
   - GCP：顶级单位是 `Project`（项目），相当于 Azure 的 Subscription。所以 GCP 的 `provider` 块里必须要全局指定 `project = "xxx"`。