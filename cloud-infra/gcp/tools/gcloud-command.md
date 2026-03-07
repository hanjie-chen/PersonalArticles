# gcloud-command

gcloud init 命令登录你的 gcp 账号，这样子我们就可以进行各种其他的 gcloud 命令了

查看 gcs 中 bucket 的内容

```shell
gcloud storage ls gs://<bucket-name>
```

查看 project 信息

```shell
gcloud projects list
```

筛选 free tier region 的 zone

```shell
# 筛选这三个特定的 Free Tier 区域
gcloud compute zones list --filter="region:(us-west1 us-central1 us-east1)"
```

