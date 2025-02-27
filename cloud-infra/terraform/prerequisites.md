# 下载 terraform

在 terraform 的官网下载地址下载 terraform [Install | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/install)

可以使用命令 `terraform --version` 来验证是否下载完成

```shell
Plain@Linux-VM:~/Personal_Project/azure-vm-terraform$ terraform --version
Terraform v1.10.5
on linux_amd64
```



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
