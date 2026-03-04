# security-scan

在做 ci 的时候常常需要做安全性扫描，对此常用的是 pip-audit(python project) 和 trivy

在 GitHub Actions 或 GitLab CI 中，它们的作用通常是：“发现漏洞就中止构建”。



## pip-audit

pip-audit 是一个专门针对 Python 生态系统的安全扫描工具。

- 核心功能：扫描 Python 环境或 `requirements.txt`、`pyproject.toml` 等文件，检查是否存在已知的漏洞。
- 数据来源：它主要通过 [PyPI 漏洞数据库](https://www.google.com/search?q=https://pypi.org/advisory-database/) 或 [OSV (Open Source Vulnerabilities)](https://osv.dev/) 来获取最新的安全威胁信息。
- 为什么用它？
  - 专注性：对 Python 包的解析非常精准。
  - 原生支持：如果你只做 Python 项目，它是最轻量、最容易上手的选择。

如果你在开发代码，想看看当前的虚拟环境安不安全：

```shell
# 安装
pip install pip-audit

# 扫描当前环境（最快的方式）
pip-audit

# 扫描指定的需求文件
pip-audit -r requirements.txt
```

在 CI (GitHub Actions) 中的操作

pip-audit 有官方维护的 Action，配置起来非常直观：

```yaml
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      # 1. 拉取代码
      - uses: actions/checkout@v4

      # 2. 安装 Python (这是关键一步)
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      # 3. 运行 pip-audit
      - name: Pip audit
        uses: pypa/pip-audit@v1
        with:
          inputs: requirements.txt
```

如果发现漏洞，CI 会直接报错（Exit Code 1），阻止代码合并。

## Trivy

Trivy 是目前 DevOps 领域最流行的开源安全扫描器之一，它不仅仅局限于某种编程语言。

- 核心功能：
  - 软件包扫描：支持 Python, JS, Go, Java, Rust 等几乎所有主流语言。
  - 容器镜像扫描：扫描 Docker 镜像里的操作系统层（如 Debian, Alpine）是否有漏洞。
  - IaC 配置扫描：检查你的 Terraform 或 Kubernetes 配置文件是否存在安全隐患（比如忘了关掉某个公网端口）。
  - 机密检测：检查代码里是否不小心硬编码了密码或 API Key。
- 数据来源：整合了各大主流操作系统的漏洞库（RedHat, Debian, Ubuntu 等）以及 GitHub Advisory。
- 为什么用它？
  - 一站式：如果你用 Docker 部署，或者项目是多语言的，Trivy 一个顶五个。
  - 速度快：扫描效率极高，非常适合放在 CI 流程的各个环节。

Trivy 的命令结构非常统一：`trivy [扫描对象] [目标]`。虽然它功能多，但你只需要记住下面这三个最常用的场景。

场景 A：扫描文件系统（类似 pip-audit）

如果你只想让 Trivy 像 pip-audit 一样扫一下 Python 依赖：

```shell
# 扫描当前文件夹下的所有依赖（它会自动识别 requirements.txt, Pipfile 等）
trivy fs .
```

场景 B：扫描 Docker 镜像（这是它的王牌）

这是 Trivy 最常用的地方。它不仅看你的 Python 包，还会看你的 Linux 基础镜像（比如 Python:3.9-slim）有没有系统级漏洞。

```shell
trivy image my-app:latest
```

场景 C：在 CI 中只拦截“高危”漏洞

Trivy 默认会报出一大堆微小的漏洞（可能有几百个），这会让 CI 频繁挂掉。实战中我们通常会加过滤条件：

```shell
# 只在发现“严重(CRITICAL)”或“高危(HIGH)”漏洞时才让 CI 报错退出
trivy fs --severity HIGH,CRITICAL --exit-code 1 .
```

### GitHub Actions

在 CI 流程里，不需要自己写 `sudo apt install`。官方已经做好了现成的组件（Action），直接调用

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'my-app:latest' # 扫描镜像
    format: 'table'
    exit-code: '1'             # 发现漏洞就让 CI 挂掉
    severity: 'CRITICAL,HIGH'  # 只关注严重和高危漏洞
```

