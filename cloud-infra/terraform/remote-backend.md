# remote backend

在 basic.md 中我们反复强调了一点：“terraform.tfstate 是命根子，包含密码，绝对不能提交到 Git”。那么问题来了：

1. 如果不提交 Git，你的同事拉取了代码，他本地没有 tfstate，怎么接着你的进度干活？
2. 刚才我们聊到的 CI/CD 流水线是一次性的虚拟机，跑完就销毁了，它产生的 tfstate 存到哪里去？

答案就是：把 tfstate 从本地电脑移走，存到云端的“对象存储桶”里！

在我们个人的练手项目中，运行 `terraform apply` 后，状态文件 `terraform.tfstate` 会保存在本地电脑的文件夹里。 

但在企业级项目、团队协作或 CI/CD 流水线中，把状态文件留在本地是灾难性的（无法共享进度，且极易丢失）。因此，生产环境的最佳实践是配置 Remote Backend（远程后端），将状态文件集中存储在云端。

在 providers.tf/foundation.tf 或者专门的 backend.tf 文件中，加入下面的代码

```hcl
terraform {
  backend "gcs" {
    bucket  = "my-web-tfstate"
    prefix  = "terraform/state"
  }
}
```

- bucket: 告诉 Terraform，去这个叫 my-web-tfstate 的云端对象存储“桶”里存东西。（注意：这个桶必须是你提前在 GCP 上手动创建好的）。

- prefix: 就像文件夹路径。它会在桶里自动创建一个 terraform/state 目录，并把状态文件放在下面。它的最终真实完整路径是：
  terraform/state/default.tfstate

  为什么叫做 default.tfstate?

  local：Terraform 认为这是一个单机、单环境的操作，所以给了一个固定的名字 `terraform.tfstate`。

  cloud (GCS)：Terraform 默认支持多工作空间协作。它会把状态文件存放在以 Workspace 命名的文件里。

  - 因为你现在处于默认状态，所以 Workspace 的名字是 `default`。
  - 最终在 GCS 里的文件名就会变成 **`default.tfstate`**。

## 优势：

1. 唯一事实来源 (Single Source of Truth)：
   团队里所有人、以及 CI/CD 流水线，运行 Terraform 时都会去这个 GCS 桶里读取同一个状态文件。无论谁修改了基础设施，状态都是实时同步的。
2. 状态锁定 (State Locking)：
   当开发者 A 正在运行 terraform apply 时，Terraform 会在云端给这个状态文件上一把“锁”。如果此时开发者 B（或者另一条 CI 流水线）也尝试部署，Terraform 会直接报错并拦截，完美防止了并发修改导致的云环境崩溃！

当你在代码里加上了 backend 块之后，你必须重新运行一次 terraform init。Terraform 会检测到后端的改变，并问你：“检测到你配置了云端存储，需要我把你本地的 tfstate 文件迁移到云端吗？”，输入 yes 即可完成无缝上云。