<!-- source_blob: 724501b7210f3ae1d638743e5e2bee4d9d29ff9b -->

# Terraform Beginner's Guide

The pain of cloud-native work: imagine clicking through a cloud console to create 10 servers, configure networking, and set up firewalls. It takes half a day. Then the next day you realize you need to build the same test environment again in another region. Wouldn't that be maddening?

Infrastructure as Code (IaC): what if you could write all of that configuration down like code, and every time you clicked "run," the environment would be created automatically? That is exactly what Terraform is for.

In simple terms, Terraform uses code to manage components on the cloud (`azure`, `gcp`, `aws`). This means you no longer have to keep clicking around in the portal. It is much easier to manage, and when creating many resources, it can do so in parallel to speed things up.

Download it from the official site: [Install | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/install). You can use the command `terraform --version` to verify that the installation is complete.

```shell
$ terraform --version
Terraform v1.10.5
on linux_amd64
```

If you use VS Code, you can also install the official extension: HashiCorp Terraform.

# Minimal Terraform Project

A minimal runnable Terraform project usually contains the following four core files:

  - `providers.tf`: declares the provider (which cloud you want to operate on)
  - `main.tf`: defines cloud resources (`resource`)
  - `variables.tf` & `terraform.tfvars`: reusable parameters (such as region/name) and sensitive passwords
  - `outputs.tf`: information you want printed in the terminal after deployment (such as an IP address)

## Syntax (main.tf)

In Terraform, the syntax of a resource block is:

```cpp
resource "<resource-type>" "<local-resource-name>" {
  # 资源配置
}
```

For example, to create an Azure resource group:

```cpp
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.resource_region
}
```

Here:

- `"azurerm_resource_group"` is the resource type, meaning it creates an Azure resource group.

- `"main"` is the local resource name. It is only used inside Terraform code, making it easier for other resources to reference it. For example:

  ```cpp
  resource "azurerm_virtual_network" "main" {
    name                = var.vnet_name
    resource_group_name = azurerm_resource_group.main.name
    # 这里的azurerm_resource_group.main.name就是引用之前定义的资源组
  }
  ```

  > [!note]
  >
  > - This name must be unique within the scope of the Terraform configuration, but it is not used as the actual resource name in the cloud provider.
  > - You can choose any name that fits your preference and project needs, such as `"main"`, `"resource_group"`, or `"rg"`.

## Variables (variables.tf & terraform.tfvars)

We write reusable variables in the `variables.tf` file, such as the resource location.

```yaml
variable "resource_region" {
  description = "Azure resource location: Singapore"
  default = "southeastasia"
}
```

> [!note]
>
> Azure uses two ways to represent location names:
>
> 1. Human-readable names (Display Name), such as `"Southeast Asia"` and `"East US"`, which are commonly shown in the Azure portal.
> 2. Location codes (Location Name or Location Code), such as `"southeastasia"` and `"eastus"`, which are commonly used in API calls and scripts.
>
> In Terraform, the AzureRM provider (Azure Resource Manager Provider) accepts both forms.
>
> It is recommended to use canonical location names, which are lowercase and contain no spaces, such as `"southeastasia"`.
>
> This is because canonical location names keep your configuration consistent with Azure APIs, CLI tools, and SDKs, which typically use that format to specify locations.

### Using Variables

In other `.tf` files, such as `network.tf`, we can use variables defined in `variables.tf` through the `var.<variable-name>` syntax. For example:

```yaml
# variables.tf
variable "resource_region" {
  description = "Azure resource location: Singapore"
  default = "southeastasia"
}

variable "resource_group_name" {
    description = "resource group name"
    default = "Singapore-RG"
}
---
# network.tf
# create resource group
resource "azurerm_resource_group" "main" {
  name = var.resource_group_name
  location = var.resource_region
}
```

### Sensitive variables

Because the code will be pushed to GitHub, passwords must never be written in `variables.tf`. The best practice is to use a `terraform.tfvars` file instead.

Create a file named `terraform.tfvars` that contains the password variable. Then add that file to `.gitignore` so it will not be committed to GitHub.

1. Create the `terraform.tfvars` file:

   ```cpp
   admin_password = "YourSecurePassword"
   ```

2. Add `terraform.tfvars` to the `.gitignore` file.

3. In `variables.tf`, declare the `admin_password` variable without a default value, and mark it as sensitive.

   ```cpp
   variable "admin_password" {
     description = "Admin password for the Linux VM"
     type        = string
     sensitive   = true
   }
   ```

4. Terraform will automatically read the variable value from `terraform.tfvars`.

## Outputs

After deployment, we usually need to retrieve some key information, such as the public IP of the VM we just created. This is defined in `outputs.tf`:

```hcl
# outputs.tf
output "vm_public_ip" {
  value = azurerm_public_ip.main.ip_address
}
```

# Terraform Workflow

Before we begin, Terraform still needs cloud authentication in order to operate on cloud resources: [Azure](../azure/terraform/auth.md) [GCP](../gcp/terraform/auth.md)

After writing the `.tf` files above, we can execute Terraform's four-step workflow in order (`code --> cloud resource`). During this process, Terraform automatically generates several extremely important files and directories.

## Step 1: Initialize (`terraform init`)

This command initializes a Terraform project. It is similar to `git init`, but it can only run after `providers.tf` has been written. Terraform reads your configuration, sees that you want to use Azure, and then does the following:

1. Downloads the provider plugin: automatically downloads Azure plugin code.
2. Initializes the backend: configures where the state file is stored.

After running it, the following are created:

1. The `.terraform/` directory: a local cache directory that stores the plugins just downloaded. It must be added to `.gitignore`.

   - Plugins (Providers) `.terraform/providers/...`

     Terraform needs to know how to communicate with cloud platforms such as AWS, Azure, and GCP. It downloads binary plugins for these platforms.

   - Modules `.terraform/modules/`

     If your code references external modules, whether from a local path or a remote GitHub repository, `init` copies or links the module code here.

   - Backend configuration `.terraform/terraform.tfstate`:

     This is like a "pointer." It does not record your resources. It only records something like: "Hey Terraform, the real state file is in a remote S3 bucket, and its name is `network.tfstate`."

     Only when a `backend` is configured, such as AWS S3 or Azure Blob, will `init` generate this hidden file to record connection information.

2. `.terraform.lock.hcl`: the version lock file. It ensures everyone on the team downloads the same provider versions and avoids version conflicts. This file should be committed to Git.

   - If the file already exists, Terraform reads the existing `.terraform.lock.hcl` and initializes providers according to it.
   - If the file does not exist, Terraform generates a new `.terraform.lock.hcl` during initialization.

For example:

```shell
$ terraform init
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

## Step 2: Validate Syntax (`terraform validate`)

The `terraform validate` command checks whether the syntax and logic of your Terraform configuration files are correct. For example:

```shell
$ terraform validate
Success! The configuration is valid.
```

It checks:

1. Syntax, such as matching brackets and correct quote usage.
2. Whether resource attributes conform to the provider schema. For example, whether the `name` of `azurerm_network_interface` is a string.
3. References, such as whether the variables or resources you reference actually exist.

> [!note]
>
> It does not check whether the current cloud state or resources actually exist. As long as the syntax is correct and the resource definitions meet requirements, `validate` will not report an error.

## Step 3: Preview Changes (`terraform plan`)

The `terraform plan` command does not modify anything. It only outputs a "plan" that tells you what Terraform intends to do:

- `+` means a new resource will be created.
- `-` means a resource will be destroyed.
- `~` means a resource attribute will be modified.

### Core Concept: Where Is the Boundary?

Many beginners have a major misunderstanding about `terraform plan`. They think it is some kind of "cloud vacuum cleaner" that will delete every resource that exists in the cloud but is not in the local code. That is wrong.

Terraform actually only manages its own defined scope, and that scope is determined by its state file (`terraform.tfstate`), which acts like a ledger.

1. Exists in the cloud, but not in the code or the ledger:
   For example, a coworker manually created a VM in the web console. Terraform ignores it completely and will never delete it, because it is outside Terraform's scope.
2. Exists in the ledger and in the cloud, but you deleted it from the code:
   Terraform notices immediately: "This machine is mine to manage, but today's code says it should be removed." Only then will `plan` output `- destroy` and remove it from the cloud.
3. Someone manually changed a resource managed by Terraform:
   For example, someone secretly added port 80 in the web console. Terraform notices that the actual state does not match the code, and `plan` outputs `~ update`. On the next deployment, it will remove port 80 and force the resource back to the state defined in code.

> Summary: Terraform only compares and corrects resources that it created and recorded itself. If a resource is not in the ledger, Terraform does not care about it at all.

### Production Best Practice

At the bottom of this command's output, you may also see a note like this:

```shell
Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

This is because `terraform apply` re-evaluates the state and generates a new plan. If something changes during that time, such as the remote state being modified or the code in your working directory being updated, then the actions performed by `terraform apply` may not exactly match the `terraform plan` output you reviewed earlier.

You can use the `-out` option:

```shell
terraform plan -out myplan.tfplan
```

Terraform will then save the plan to `myplan.tfplan`, and you can run the saved plan file with:

```shell
terraform apply myplan.tfplan
```

This ensures Terraform executes exactly the plan you reviewed earlier.

## Step 4: Deploy Resources (`terraform apply`)

After confirming that the plan is correct, run the deployment.

If you saved a plan file in the previous step, you can run `terraform apply myplan.tfplan` directly. Otherwise, run `terraform apply`. Terraform will show the plan again and ask you to type `yes` to confirm, unless you use the `-auto-approve` option to skip confirmation.

Files generated after running it:

`terraform.tfstate`: the state file. Terraform writes all detailed information about the resources it just created in the cloud into this JSON file, including the password passed in from `tfvars`. This file is the only basis Terraform uses to manage these resources later. It contains sensitive information and must never be committed to Git.

## Step 5: Check Output

If outputs are defined in `outputs.tf`, they will be printed automatically after `apply` succeeds. You can also run `terraform output` at any time to view this key information again.
