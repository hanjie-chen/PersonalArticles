# basic-concepts

CI/CD 不是单一的工具，而是一套流程和实践理念

- CI: continuous integration 持续集成
  - 每次提交代码后，自动执行检查：安装依赖、跑测试、构建镜像、静态检查等。
  - 目标：尽早发现问题。
- CD: continuous deployment 持续交付
  - CI 通过后，把新版本自动发布到目标环境（比如 Ubuntu 服务器）。
