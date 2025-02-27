# `terraform apply`

`terraform apply` 将根据执行计划，实际在 Azure 上创建和配置资源。命令执行过程中，Terraform 会再次显示执行计划，并提示您输入 `yes` 以确认执行。提示：如果您希望自动确认（在非交互式环境中使用时），可以使用 `-auto-approve` 参数：

```bash
terraform apply -auto-approve
```

