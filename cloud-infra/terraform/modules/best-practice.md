---
Title: terraform modules best practice
Author: 陈翰杰
Instructor: chatGPT 4o
CoverImage: 
RolloutDate: 
---

```
BriefIntroduction: 
terraform modules best practice
```

<!-- split -->

# background

对于大部分的项目结构都类似于如下所示

```shell
terraform-projects/
├── main.tf                <- 调用模块
├── terraform.tfvars
├── outputs.tf
├── providers.tf
├── modules/
│   ├── virtual-machine/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── network/
│   └── ...
```

那么我们是否可以省略 `modules` 文件夹，直接将里面的模块文件夹暴露在外呢？

答：

当然可以，我们可以直接把 linux-vm、windows-vm、network 等模块文件夹放在项目根目录里 —— Terraform 不强制你一定要用 modules/ 这个文件夹名。

但是，为什么大多数人（包括官方文档）都会用 modules/ 呢？主要是出于以下几点：



## 推荐用 modules/ 目录的原因

清晰的语义结构：modules/ 这个名字一看就知道“这些文件夹是 Terraform modules”，而不是别的东西（比如脚本、配置文件等）。

更好的可维护性：当你的项目变大以后，会有很多东西：CI/CD 脚本、文档、terraform plan 输出、backend config 等。用 modules/ 隔离模块，可以让目录结构保持整洁。

更容易复用：如果未来你想把某些模块提取出来变成独立 module（比如上传到 Terraform Registry 或 GitHub reuse），modules/ 目录可以直接作为基础。



## 可以不加 modules/ 的情况

- 项目规模小（比如只部署几台 VM）
- 是学习项目或练手 Demo
- 你就是想保持目录短一点，好 navigate

比如你完全可以这样：

```
my-terraform-project/
├── linux-vm/
├── windows-vm/
├── network/
├── main.tf
├── outputs.tf
├── variables.tf
```

然后：

```hcl
module "linux_vm" {
  source = "./linux-vm"
}
```

Terraform 是不会报错的。

总结一句话就是：

用 modules/ 是一种“最佳实践”，不是“强制规则”。如果你有更适合你风格的结构，也是完全 OK 的。
