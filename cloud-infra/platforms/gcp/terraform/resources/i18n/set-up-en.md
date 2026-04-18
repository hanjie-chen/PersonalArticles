---
Title: Getting Started with GCP Terraform Setup
SourceBlob: e39a152905b908cca76154e04a1a5e049dce8c7d
---

```
BriefIntroduction: Introductory setup and preparation for managing GCP resources with Terraform
```

<!-- split -->

To let Terraform manage resources in GCP (Google Cloud Platform), we first need to configure the Provider in code, and then provide Terraform with credentials that identify it to operate on GCP.

# GCP Provider

In `provider.tf`, we need to declare that we are using the `google` plugin and configure the core parameters.

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

See [Get started with Terraform | Google Cloud](https://cloud.google.com/docs/terraform/get-started-with-terraform)

After writing the configuration, run `terraform init` to download the plugin. Next, Terraform will automatically look for credentials in the system environment. Different work scenarios call for different authentication methods:

# Authentication

## Local Development

When writing code on your own computer, the safest and simplest approach is to use the gcloud CLI to generate local Application Default Credentials (ADC).

1. Install the gcloud CLI (Linux example):

   ```shell
   curl https://sdk.cloud.google.com | bash
   ```

2. Run the ADC login command:

   Note: Terraform needs ADC credentials, so you must include the `application-default` parameter.

   ```bash
   gcloud auth application-default login
   ```

How it works:

After authorization, the terminal will tell you that a JSON file has been generated (for example, `~/.config/gcloud/application_default_credentials.json`).

When you run `terraform plan`, Terraform will automatically find this hidden file and use it to operate on GCP.

## CI/CD Pipeline

In “headless servers” such as GitHub Actions or GitLab CI, you cannot open a browser and log in interactively. In this case, you need to use a machine-level identity.

### :x: Traditional Approach: Service Account

The older approach was to go to the GCP console and download a static `.json` key file for a Service Account.

- Configuration method: store the JSON in CI/CD Secrets, and at runtime point the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to that file so Terraform can read it.
- Pain point: long-lived static keys carry a major leakage risk and need to be rotated regularly.

### :heavy_check_mark: Best Practice: Workload Identity Federation (WIF)

This is the passwordless authentication approach that Google currently recommends most strongly, completely eliminating the need for JSON key files.

- Core idea: through the OIDC protocol, GitHub Actions and GCP establish a trust relationship and dynamically exchange short-lived temporary tokens.

- CI/CD usage (GitHub Actions example):

  In the `.yml` pipeline, just include Google’s official auth action:

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

  After the `auth` step completes, it will automatically emulate an ADC environment in CI, so the following Terraform commands can run securely and seamlessly just like they do on your local machine.

# GCP vs Azure

If you are used to Azure, keep these two major differences in mind when switching to GCP:

1. The authentication commands are different:
   - Azure: `az login` handles everything.
   - GCP: you must use `gcloud auth application-default login`. Using only `gcloud auth login` will still cause Terraform to report that it cannot find credentials.
2. The hierarchy concepts are different:
   - Azure: the top-level resource container is a `Resource Group`, and you need to create one before creating anything else.
   - GCP: the top-level unit is a `Project`, which is roughly equivalent to an Azure Subscription. That is why the GCP `provider` block must globally specify `project = "xxx"`.
