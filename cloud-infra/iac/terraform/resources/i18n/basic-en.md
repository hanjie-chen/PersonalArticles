---
Title: Beginner's Guide to Terraform
SourceBlob: 724501b7210f3ae1d638743e5e2bee4d9d29ff9b
---

```
BriefIntroduction: A beginner's guide to Terraform
```

<!-- split -->

# Beginner's Guide to Terraform

The pain point of cloud-native: imagine spending half a day clicking around a cloud platform to create 10 servers, configure networking and firewalls, and finish everything manually. Then the next day, you realize you need to build the exact same test environment in another region. Wouldn't that be a nightmare?

Infrastructure as Code (IaC): if you could write all of that configuration down like code, and every time you just click "run" and the environment gets built automatically, wouldn't that be great? That's exactly what Terraform is meant to do.

Put simply, Terraform uses code to manage components on the cloud (`azure`, `gcp`, `aws`), so you no longer need to click around in the portal. It is also very convenient to manage, and when creating many resources, they can be provisioned in parallel to speed things up.

Download it from the official website: [Install | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/install). You can verify that the installation is complete with the command `terraform --version`.

```shell
$ terraform --version
Terraform v1.10.5
on linux_amd64
```

If you use VS Code, you can also install the official extension: HashiCorp Terraform.

# Minimal Terraform Project

A minimal runnable Terraform project usually contains the following four core files:

  - `providers.tf`: declares the provider (which cloud platform to operate on)
  - `main.tf`: defines cloud resources (`resource`)
  - `variables.tf` & `terraform.tfvars`: reusable parameters (such as `region` / `name`) and sensitive passwords
  - `outputs.tf`: information you want printed in the terminal after deployment (such as an IP address)

## Syntax (main.tf)

In Terraform, the syntax for a resource block is:

```cpp
resource "<resource-type>" "<local-resource-name>" {
  # 资源配置
}
```

For example, creating an Azure resource group:

```cpp
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.resource_region
}
```

Here:

- `"azurerm_resource_group"` is the resource type, which means creating an Azure resource group

- `"main"` is the local resource name. It is only used inside Terraform code so other resources can reference it conveniently. For example:

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
  > - You can choose any suitable name based on your own preference and project needs, such as `"main"`, `"resource_group"`, or `"rg"`.

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
> Azure has two ways to represent location names:
>
> 1. Human-readable names (Display Name): such as "Southeast Asia", "East US", and so on, which are usually shown in the Azure portal.
> 2. Location codes (Location Name or Location Code): such as "southeastasia", "eastus", and so on, which are usually used in API calls and scripts.
>
> In Terraform, the AzureRM provider (Azure Resource Manager Provider) accepts both formats for location names.
>
> It is recommended to use canonical location names, meaning all lowercase with no spaces, such as `"southeastasia"`.
>
> This is because canonical location names keep your configuration consistent with Azure APIs, CLI tools, and SDKs. These tools typically use canonical location names to specify locations.

### Using Variables

In other `.tf` files, such as `network.tf`, we can use variables defined in `variables.tf` with the format `var.<variable-name>`, e.g.

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

Because the code will be pushed to GitHub, passwords must never be written directly in `variables.tf`. The best practice is to use a `terraform.tfvars` file instead.

Create a file named `terraform.tfvars` containing the password variable, then add that file to `.gitignore` so it will not be committed to GitHub.

1. Create the `terraform.tfvars` file:

   ```cpp
   admin_password = "YourSecurePassword"
   ```

2. In the `.gitignore` file, add `terraform.tfvars`

3. In `variables.tf`, declare the `admin_password` variable without setting a default value, and mark it as sensitive.

   ```cpp
   variable "admin_password" {
     description = "Admin password for the Linux VM"
     type        = string
     sensitive   = true
   }
   ```

4. Terraform will automatically read variable values from `terraform.tfvars`.

## outputs

After deployment, we usually need to retrieve some key information, such as the public IP of the VM we just created. This is defined in `outputs.tf`:

```hcl
# outputs.tf
output "vm_public_ip" {
  value = azurerm_public_ip.main.ip_address
}
```

# Terraform Workflow

Before we begin, Terraform still needs cloud authentication in order to manage cloud resources: [Azure](../azure/terraform/auth.md) [GCP](../gcp/terraform/auth.md)

After writing the `.tf` files above, we can execute Terraform's four-step command workflow in order (`code --> cloud resource`). During this process, Terraform will automatically generate some extremely important files and folders.

## Step 1: initialize (`terraform init`)

This command initializes the Terraform project. It is similar to `git init`, but it can only run after `providers.tf` has been written. Terraform reads your configuration, sees that you want to use Azure, and then does the following:

1. Downloads provider plugins: automatically downloads Azure plugin code.
2. Initializes the backend: configures where the state file will be stored.

Files and folders generated after running it:

1. The `.terraform/` folder: a local cache directory that stores the plugins just downloaded. It must be added to `.gitignore`.

   - Plugins (Providers) `.terraform/providers/...`

     Terraform needs to know how to communicate with cloud platforms such as AWS, Azure, and GCP. It downloads binary plugins for these platforms.

   - Modules `.terraform/modules/`

     If your code references external modules, whether from a local path or a remote GitHub repository, `init` will copy or link the module code here.

   - Backend configuration `.terraform/terraform.tfstate`:

     This works like a "pointer." It does not record your resources. It only records: "Hey, Terraform, the real state file is in the remote S3 bucket, and its name is `network.tfstate`."

     This hidden file is generated only when a `backend` is configured (such as AWS S3, Azure Blob, etc.) so Terraform can record connection information.

2. `.terraform.lock.hcl`: the version lock file. It ensures everyone on the team downloads the same provider versions and avoids version conflicts. This file should be committed to Git.

   - If this file already exists, Terraform reads the existing `.terraform.lock.hcl` and initializes providers according to it.
   - If it does not exist, Terraform generates a new `.terraform.lock.hcl` during initialization.

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

## Step 2: validate syntax (`terraform validate`)

The `terraform validate` command checks whether the syntax and logic of your Terraform configuration files are correct. For example:

```shell
$ terraform validate
Success! The configuration is valid.
```

It checks:

1. Syntax, such as matching brackets and correct quote usage
2. Whether resource attributes match the Terraform provider schema, for example whether the `name` of `azurerm_network_interface` is a string
3. References, such as whether the variables or resources you reference actually exist

> [!note]
>
> It does not check whether cloud-side state or resources actually exist. As long as the syntax is correct and the configuration meets the resource requirements, `validate` will not report an error.

## Step 3: preview changes (`terraform plan`)

The `terraform plan` command does not modify anything. It only outputs a "plan" telling you what Terraform intends to do:

- `+` means a resource will be created
- `-` means a resource will be destroyed
- `~` means a resource attribute will be modified

### Core Concept: Where is the boundary?

Many beginners have a major misunderstanding about `terraform plan`: they think it is a "cloud vacuum cleaner" that will delete every resource in the cloud that exists remotely but not in local code. That is wrong.

Terraform only manages its own territory, and that territory is defined by its state file (`terraform.tfstate`, the ledger).

1. If a resource exists in the cloud, but not in the code or the ledger:
   (for example, a coworker manually created a VM in the web console), Terraform is effectively blind to it and will never delete it, because it is outside Terraform's scope.
2. If a resource exists in the ledger and in the cloud, but you remove it from the code:
   Terraform will detect it immediately and think: "This machine is under my management, but the latest code says it should be gone." At that point, `plan` will output `- destroy` and remove it from the cloud.
3. If someone manually changes a resource managed by Terraform:
   (for example, secretly opening port 80 in the console), Terraform will notice that the actual state no longer matches the code. `plan` will output `~ update`, and on the next deployment it will ruthlessly remove port 80 and force the resource back to the state defined in code.

> Summary: Terraform only compares and corrects resources that it created itself and has recorded in its ledger. Anything not in that ledger is outside its concern.

### Production best practice

At the bottom of this command, you may also see a note like this:

```shell
Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

That is because `terraform apply` will re-evaluate the state and generate a new plan. If anything changes during that time, such as remote state being modified or code in your working directory being updated, the actions performed by `terraform apply` may not exactly match the output you saw earlier from `terraform plan`.

You can use the `-out` option:

```shell
terraform plan -out myplan.tfplan
```

Then Terraform saves the plan to `myplan.tfplan`, and you can apply that exact saved plan with:

```shell
terraform apply myplan.tfplan
```

This ensures Terraform executes strictly according to the plan you reviewed earlier.

## Step 4: deploy resources (`terraform apply`)

After confirming the plan is correct, execute the deployment.

If you saved the plan file in the previous step, you can run `terraform apply myplan.tfplan` directly. Otherwise, use `terraform apply`, which will show the plan again and ask you to type `yes` to confirm (or you can use the `-auto-approve` option to skip confirmation).

File generated after running it:

`terraform.tfstate`: the state file. Terraform writes detailed information about the resources it just created in the cloud into this JSON file, including the password passed in from `tfvars`. This is the only basis Terraform uses to manage those resources later. It contains sensitive information and must never be committed to Git.

## Step 5: check output

If outputs are defined in `outputs.tf`, they will be printed automatically after a successful `apply`. You can also run `terraform output` at any time to view this key information again.
