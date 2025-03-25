# 学习路径

## 为静态资源设置缓存
你的 `readme.md` 中提到未来想为图片等静态资源设置缓存，这可以显著提升网站性能。

- **目标**：让 Nginx 缓存 `rendered-articles` 中的静态文件（如 HTML 和图片）。
- **学习内容**：
  - **缓存配置**：学习 `expires` 和 `Cache-Control` 头的使用。
  - **挂载目录**：将 `rendered-articles` 目录挂载到 Nginx 容器。
- **实践**：
  - 修改 `web-app` 的 Dockerfile 或挂载方式，将 `rendered-articles` 输出到共享卷（比如 `articles_data`）。
  - 在 Nginx 配置文件中添加 `location` 块：

    ```nginx
    location /rendered-articles {
        alias /articles-data/rendered-articles;  # 假设 rendered-articles 在 articles_data 卷中
        expires 30d;  # 缓存 30 天
        add_header Cache-Control "public";
    }
    ```

  - 更新 `compose.yml`，为 Nginx 添加卷挂载：
    ```yaml
    nginx:
      volumes:
        - articles_data:/articles-data:ro  # 只读访问
    ```

## 配置 HTTPS
你的未来计划中提到配置 HTTPS，这是提升网站安全性和用户信任的关键一步。

- **目标**：为网站启用 HTTPS。
- **学习内容**：
  - **SSL/TLS 证书**：了解如何获取证书（推荐使用免费的 Let's Encrypt）。
  - **HTTPS 配置**：学习配置 `listen 443 ssl` 和证书路径。
- **实践**：
  - 使用 Certbot 获取证书（本地测试可以用自签名证书）。
  - 更新 Nginx 配置：

    ```nginx
    server {
        listen 443 ssl;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/certs/cert.pem;  # 证书路径
        ssl_certificate_key /etc/nginx/certs/key.pem;  # 密钥路径

        location / {
            proxy_pass http://web-app:5000;
            # 保留之前的 proxy_set_header 配置
        }
    }

    # 重定向 HTTP 到 HTTPS
    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$host$request_uri;
    }
    ```

  - 将证书挂载到 Nginx 容器，更新 `compose.yml`：
    ```yaml
    nginx:
      volumes:
        - ./certs:/etc/nginx/certs:ro
    ```

## 高级功能和优化
在掌握基础后，可以探索 Nginx 的高级功能，结合你的项目需求进行优化。

- **负载均衡**（可选）：如果未来有多个 `web-app` 实例，可以配置 Nginx 分配请求。
- **性能优化**：调整 `worker_processes` 和 `worker_connections`。
- **安全配置**：添加防 DDoS 设置（如 `limit_req`）和访问控制。
- **实践**：在你的项目中尝试配置日志（已挂载到 `./nginx/logs`）并分析访问情况。



## 具体步骤建议

1. **从反向代理开始**  
   先确保 Nginx 能正常代理到 `web-app`，这是你的核心需求。参考第 2 步的配置，调试直到成功。

2. **逐步添加缓存**  
   将 `rendered-articles` 挂载到 Nginx 并设置缓存。测试静态资源是否加载更快。

3. **实现 HTTPS**  
   获取证书并配置 HTTPS，确保网站可以通过 `https://localhost` 访问。

4. **优化和扩展**  
   根据需要添加日志分析、性能优化等功能。


