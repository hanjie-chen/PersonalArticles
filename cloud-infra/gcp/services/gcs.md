# Google Cloud Storage

在我们开始之前，我们先讲讲看云原生存储，简单来说，云原生存储（Cloud-Native Storage）不再仅仅是把文件存进硬盘，而是让存储像空气和电一样，能够自动伸缩、按需分配，契合容器化（如 Kubernetes）的应用环境。

在 google cloud storage 服务中，bucket (存储桶)：是在 GCS 中创建的容器。所有的文件（对象）都必须放在某个 Bucket 里。

听说 gcs bucket 有免费的额度，让我来看下如何白嫖，具体的文档：https://cloud.google.com/storage/pricing?hl=en#cloud-storage-always-free

具体来说就是在特定的 3 个区域 5 GB 以下是免费的，这里的 5 GB 是所有的 bucket 加起来的额度。

点击页面顶部的 “+ CREATE” (或者图中的 “Create bucket”)，然后按照以下步骤操作：

### 1. 命名你的存储桶 (Name your bucket)

- 输入名字：名字必须是全球唯一的。
- 点击 CONTINUE。

### 2. 选择存储位置 (Choose where to store your data)

> 这是免费的关键！

- Location type: 选择 Region。
- Location: 在下拉列表中选择以下三个之一（只有这三个有 5GB 免费额度）：
  - `us-east1` (South Carolina)
  - `us-central1` (Iowa)
  - `us-west1` (Oregon)
- 点击 CONTINUE。

### 3. 选择存储类型 (Choose a storage class)

- 选择 Standard。
- 勾选下方可能出现的 “Default class” 确认。
- 点击 CONTINUE。

### 4. 控制访问权限 (Choose how to control access)

- Enforce public access prevention on this bucket: 务必勾选（为了安全，不让别人乱看你的 tfstate）。
- Access control: 选择 Uniform (统一访问控制)，这对 Terraform 来说更简单、更推荐。
- 点击 CONTINUE。

### 5. 保护数据 (Choose how to protect object data)

- Object versioning: 强烈建议点击“开启” (Turn on)。这样万一你把 state 搞坏了，还能找回之前的版本。

  Max number of versions per object: 3

  Expire non-current versions after: 7 day

- Encryption: 保持默认的 Google-managed encryption key 即可。

------

### 6. 完成创建

点击底部的 **CREATE** 按钮。如果弹出关于“Public access”的警告，确认即可（因为我们已经选择了禁止公开访问）。

------

### 💡 接下来该做什么？

存储桶建好后，你就可以在你的 Terraform 代码中加入这段配置了：

Terraform

```
terraform {
  backend "gcs" {
    bucket  = "你刚才起的那个名字"
    prefix  = "terraform/state"
  }
}
```

**小贴士：** 因为你在图片里显示项目名是 `base-general`，请确保你在本地终端已经用 `gcloud auth application-default login` 登录过，这样 Terraform 才有权限往这个新桶里写东西。

需要我帮你写一段自动清理旧版本文件的 **Lifecycle (生命周期)** 配置吗？（这样可以防止版本存太多占用超过 5GB 的空间）。