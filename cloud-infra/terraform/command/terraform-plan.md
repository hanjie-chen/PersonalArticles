# `terraform plan`

`terraform plan` 会生成一个执行计划，显示 Terraform 将创建、修改或销毁哪些资源，以及具体的变更内容。仔细查看输出的计划，确保所有操作都符合您的预期。

## terraform plan output

一般来说如果 resource block 有变动，然后使用 terraform plan 的输出就会类似于

```
  ~ resource "azurerm_network_security_group" "linux_subnet_nsg" {
      ~ security_rule       = [
          - { ... } # 旧的 allow-ssh 规则
          - { ... } # 旧的 AllowAnyCustom443Inbound 规则
          + { ... } # 新的 allow-ssh 规则
          + { ... } # 新的 AllowAnyCustom443Inbound 规则
        ]
    }
```

这种 `-` 和 `+` 的表示方式确实让人觉得 Terraform 要“删除所有规则然后重建”，但实际情况并非如此。这是 Terraform 的表达方式和实际执行之间的一个“表现差异”

Terraform 是声明式的，它的目标是让实际状态（Azure 中的 NSG）与你定义的配置（.tf 文件）完全一致。terraform plan 的输出是用来描述“当前状态”到“期望状态”的变化。

对于像 security_rule 这样的列表属性，Terraform 会将整个列表作为一个整体进行比较。如果列表中的任何部分（哪怕只是一条规则的 description）与当前状态不一致，Terraform 会在输出中显示整个列表的“变化”：

- 用 `-` 表示当前状态中的规则。
- 用 `+` 表示期望状态中的规则。

即使只有一条规则的某个字段（例如 description）不同，整个列表都会被标记为“更新”

这种输出是 Terraform 的 diff（差异）算法的结果。它并不是说真的要删除所有规则然后重建，而是表示“当前列表”会被“替换”为“新列表”。但具体如何替换，取决于提供者（azurerm）的实现。

## terraform apply

当你运行 terraform apply 时，Terraform 不会直接执行 plan 输出中的“删除并添加”逻辑，而是将你的配置传递给 azurerm provider 然后azurerm provider 会调用 Azure 的 API，智能地判断：

- 如果只是某个字段（例如 description）变了，它会只更新那条规则的字段。
- 如果规则的 name 或 priority（关键标识字段）变了，可能需要删除并重建那条规则。
- 如果整个列表的结构没变（规则数量和顺序一致），它通常只会增量更新差异的部分。



# `-out` option

当我们直接使用 `terraform plan` 命令查看我们的执行计划时，会在底部看到这样子一个 note

```shell
Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

这是因为 `terraform apply` 会重新评估状态并生成一个新的计划。如果在这段时间内某些东西发生了变化（比如远程状态被修改，或者你工作目录中的代码被调整），`terraform apply` 执行的动作可能与你之前看到的 `terraform plan` 输出不完全一致。

但如果我们使用 `-out` 参数

```shell
terraform plan -out myplan.tfplan
```

那么 Terraform 会把这个计划保存到 `myplan.tfplan` 中，然后，你可以用这个保存的计划文件运行

```shell
terraform apply myplan.tfplan
```

确保 Terraform 严格按照你之前审查的计划执行，而不会重新计算或引入意外的更改

如果你在生产环境或者团队协作中，想要确保一致性和可审查性，那就听从建议，用 `--out` 保存计划，然后用保存的文件运行 `apply`

