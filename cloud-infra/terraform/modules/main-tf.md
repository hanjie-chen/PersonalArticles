# `main.tf` in project root

项目根目录的 `main.tf` 是项目的入口点（entry point）它需要调用每一个 module（比如 network、linux-vm、windows-vm），给模块传入变量，并且相互调用模块之间的输出

## 如何在 `main.tf` 中调用其他模块的输出

假设你已经有以下 modules：

- modules/network：创建虚拟网络 + 子网
- modules/linux-vm：创建 Linux VM（需要 subnet_id）
- modules/windows-vm：创建 Windows VM（也需要 subnet_id）

你的 main.tf 可以这样写

```hcl
# 调用 network 模块
module "network" {
  source              = "./modules/network"
  # ...其他变量
}

# 调用 Linux VM 模块
module "linux_vm" {
  source              = "./modules/linux-vm"
  subnet_id           = module.network.subnet_id  # 来自 network 的 output
  # ...其他变量
}

# 调用 Windows VM 模块
module "windows_vm" {
  source              = "./modules/windows-vm"
  subnet_id           = module.network.subnet_id  # 来自 network 的 output
  # ...其他变量
}
```
