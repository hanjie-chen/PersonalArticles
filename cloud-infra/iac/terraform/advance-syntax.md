# advance-syntax

以一个自动获取 cloudflare ipv4 地址的 firewall.tf 为例

```c
data "http" "cloudflare_ipv4" {
  # Pull the current Cloudflare IPv4 list from the official endpoint.
  url = var.cloudflare_ipv4_source_url
}

locals {
  # Convert the plaintext response body into a clean CIDR list.
  cloudflare_ipv4_cidrs = [
    for cidr in split("\n", trimspace(data.http.cloudflare_ipv4.response_body)) : trimspace(cidr)
    if trimspace(cidr) != ""
  ]
}

check "cloudflare_ipv4_not_empty" {
  assert {
    # Fail fast if the upstream list could not be fetched or parsed.
    condition     = length(local.cloudflare_ipv4_cidrs) > 0
    error_message = "Failed to load Cloudflare IPv4 ranges from the configured source URL."
  }
}

resource "google_compute_firewall" "allow_cf_https" {
  # Model the existing rule that only allows Cloudflare to reach the origin on HTTPS.
  name        = var.firewall_allow_cf_https_rule_name
  description = var.firewall_allow_cf_https_description
  network     = var.vm_network

  direction     = "INGRESS"
  priority      = 100
  source_ranges = local.cloudflare_ipv4_cidrs

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
}

```



### `data`

- 它的任务： 联网访问 Cloudflare 的官网，把那一串长长的 IP 地址列表抓取下来。
- 关键点： 它不会改变任何云端资源，它只是把远程的一段文本（`response_body`）拉取到 Terraform 的内存里供后续使用。

### `locals`

由于 `data` 抓取回来的通常是一整块乱糟糟的文本（带换行符、可能有空格），直接给防火墙用会报错。这时 `locals` 就上场了。

- 它的任务： 数据清洗。
  - `split("\n", ...)`：把一整块文本按行切开，变成列表。
  - `trimspace(...)`：去掉每行前后的空格。
  - `if ... != ""`：剔除掉空行。
- 为什么这么做： 提高代码的可读性和复用性。你在 `google_compute_firewall` 里只需要引用简洁的 `local.cloudflare_ipv4_cidrs`，而不需要把这一大串复杂的清洗逻辑写在防火墙资源里。

### `check`

这是最精彩的部分。万一 Cloudflare 的服务器挂了，或者返回了一个空文件，怎么办？

- 它的任务： 断言（Assert）。它检查清洗后的列表长度是否大于 0。
- 它的作用： 如果没抓到 IP（长度为 0），`check` 会发出警告。
- 为什么重要： 防火墙的 `source_ranges` 如果为空，可能会导致意想不到的安全风险（有些云厂商可能会默认禁止所有，有些则可能报错导致部署中断）。`check` 让你在基础设施运行期间，能确切知道“数据源”是否健康。