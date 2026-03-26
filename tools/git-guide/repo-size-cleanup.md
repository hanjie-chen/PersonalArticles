# git repo 瘦身问题

# background

我遇到这样子一个问题，因为我的 knowledge-base 是托管在 github 上面的，而我的这个 knowledge-base 有经过了不断的 git push, 所以可能会有这样子的问题，那就是 .git 文件夹中包含的历史记录，比真正的正文要大

因为 git 会记录整个提交的历史过程，使用 du 命令查看，结果发现

```shell
$ du -h --max-depth=1
2.5M    ./web-dev
125M    ./.git
5.8M    ./devops
2.9M    ./machine-setup
42M     ./personal-growth
8.8M    ./tools
2.9M    ./cloud-infra
700K    ./__template__
6.8M    ./code
8.0K    ./.githooks
197M    .
```

整个仓库 197 MB 光是 .git 文件夹就占据了 125 MB

# resolution

目前来说的方案是，如果想要 github repo 一起瘦身，那么就是删掉整个 knowlege-base 仓库，然后重建一个同样的名字的。并且删除本地仓库中的 .git 文件，然后重新使用 git init 流程走一遍，重新提交。

对于这种方案，其他地方已经clone的 github repo 来说，会出现问题，推荐删除，重新 git clone

如果仅仅是想要 git clone 下来的仓库小一些的话，那么使用 `git clone --depth 1`

默认的 `git clone` 会把仓库从“第一行代码”到“当前代码”的所有历史修改全部下载下来。

而 `--depth 1` 告诉 Git：“我只要最后一次提交（Commit）的状态，之前的历史记录我通通不要。”