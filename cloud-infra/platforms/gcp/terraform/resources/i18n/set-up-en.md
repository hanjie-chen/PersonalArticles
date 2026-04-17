<!-- source_blob: e39a152905b908cca76154e04a1a5e049dce8c7d -->

To let Terraform manage resources in GCP (Google Cloud Platform), we first need to configure the Provider in code, then provide Terraform with credentials that identify it to GCP.

# GCP Provider

In `provider.tf`, we need to declare the `google` plugin and configure the core parameters.

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Best practice: only set the project and region here; do not hardcode credentials (keys) here
provider "google" {
  project = "your-gcp-project-id"
  region  = "us-central1"
}
```

See [Get started with Terraform | Google Cloud](https://cloud.google.com/docs/terraform/get-started-with-terraform)

After writing the code, run `terraform init` to download the plugin. Next, Terraform will automatically look for credentials (your pass) in the system environment. Different working scenarios call for different authentication methods:

# Authentication

## Local Development

When writing code on your own computer, the safest and simplest approach is to use the gcloud CLI to generate local Application Default Credentials (ADC).

1. Install the gcloud CLI (Linux as an example):

   ```shell
   curl https://sdk.cloud.google.com | bash
   ```

2. Run ADC login:

   Note: Terraform needs ADC credentials, so you must include the `application-default` parameter.

   ```bash
   gcloud auth application-default login
   ```

How it works:

After authorization, the terminal will indicate that a JSON file has been generated (for example, `~/.config/gcloud/application_default_credentials.json`).

When you run `terraform plan`, Terraform will automatically find this hidden file and use it to operate on GCP.

## CI/CD Pipeline

In "headless servers" such as GitHub Actions or GitLab CI, you cannot pop up a browser and sign in interactively. In this case, you need to use a machine-level identity.

### :x: Traditional Approach: Service Account

In the past, the common approach was to download a static `.json` key file for a Service Account from the GCP console.

- Configuration method: store the JSON in CI/CD Secrets, then point the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to that file at runtime so Terraform can read it.
- Pain point: long-lived static keys carry a major leakage risk and must be rotated regularly.

### :heavy_check_mark: Best Practice: Workload Identity Federation (WIF)

This is the keyless authentication method currently strongly recommended by Google, and it completely eliminates the need for JSON files.

- Core idea: use the OIDC protocol to establish trust between GitHub Actions and GCP, then dynamically exchange it for a short-lived temporary token.

- CI/CD usage (GitHub Actions as an example):

  In the `.yml` pipeline, just use Google's official auth action:

  ```yaml
  - id: 'auth'
    uses: 'google-github-actions/auth@v2'
    with:
      # Fill in the preconfigured WIF resource ID in GCP and the bound service account
      workload_identity_provider: 'projects/123/locations/global/workloadIdentityPools/my-pool/providers/my-provider'
      service_account: 'terraform-sa@your-project.iam.gserviceaccount.com'
  
  - name: 'Terraform Plan'
    run: 'terraform plan'
  ```

  After the `auth` step runs, it will automatically emulate ADC environment variables in the CI environment, so subsequent Terraform commands can run just like they do locally, seamlessly and securely.

# GCP vs Azure

If you're used to Azure, keep these two major differences in mind when switching to GCP:

1. The authentication commands are different:
   - Azure: `az login` handles everything.
   - GCP: you must use `gcloud auth application-default login`; using only `gcloud auth login` will still cause Terraform to report that it cannot find credentials.
2. The hierarchy concepts are different:
   - Azure: the top-level resource container is a `Resource Group`, and you need to create one before creating anything else.
   - GCP: the top-level unit is a `Project`, which is roughly equivalent to an Azure Subscription. So in GCP, the `provider` block must globally specify `project = "xxx"`.
