# compose-merge

当你运行 `-f compose.yml -f compose.dev.yml` 时，Compose 会以第一个文件为基础，然后用第二个文件中的内容去**覆盖或补充**第一个文件。

### 合并的具体逻辑

合并规则通常遵循以下三个原则：

1. 新增（Add）： 如果 `compose.dev.yml` 中有 `compose.yml` 里没有的配置（例如新增了一个环境变量或一个新服务），它会被直接添加到最终配置中。
2. 覆盖（Override）： 对于单值字段（如 `image`, `container_name`, `restart`），后一个文件（dev）的值会直接取代前一个文件（base）的值。
3. 合并（Merge）： 对于多值列表或字典（如 `ports`, `volumes`, `environment`），两个文件的内容会结合在一起。

### 举个例子

假设你的两个文件内容如下：

`compose.yml` (基础文件)

```yaml
services:
  web:
    image: node:14
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
```

`compose.dev.yml` (覆盖文件)

```yaml
services:
  web:
    build: .        # 新增：开发环境改用本地构建
    ports:
      - "3000:3000" # 补充：现在同时映射了 80 和 3000 端口
    environment:
      - NODE_ENV=development # 覆盖：将生产环境改为开发环境
```

最终合并后的效果：

- image & build: 同时存在（虽然通常有了 build 会忽略 image，但逻辑上它们都合并进去了）。
- ports: 包含 `80:80` 和 `3000:3000`。
- environment: `NODE_ENV` 的值变为 `development`。

### 关键注意事项

- 顺序非常重要： 越靠后的文件优先级越高。如果你写反了（`-f dev.yml -f base.yml`），基础配置就会覆盖掉你的开发配置。

- 查看合并结果： 如果你不确定合并后到底长什么样，可以运行以下命令预览最终生成的完整 YAML 配置：

  ```shell
  docker compose -f compose.yml -f compose.dev.yml config
  ```

## override

有的时候，我们想要后面的配置覆盖而不仅仅是新增，比如说在 compose.yml 中存在

```yaml
ports:
  - "80:80"
  - "443:443"
```

但是这里的2个端口在 dev 环境中已经被占用了，所以我们需要换两个端口，但是如果在 compose.dev.yml 里再写：

```yaml
ports:
  - "8081:80"
  - "8444:443"
```

默认结果不是“改成 8081/8444”，而是变成：

```yaml
80:80 
443:443 
8081:80 
8444:443 
```

这是我们就需要用到

```yaml
ports: !override
      - "8081:80"
      - "8444:443"
```

