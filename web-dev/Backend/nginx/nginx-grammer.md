# nginx location

Nginx location 匹配按以下优先级顺序处理（从高到低）：

1. **精确匹配** `=`：例如 `location = /50x.html`
2. **优先级前缀匹配** `^~`：例如 `location ^~ /images/`
3. **正则表达式匹配** `~` 或 `~*`：例如 `location ~ \.php$`
4. **普通前缀匹配**：例如 `location /` 或 `location /api/`

## `alias` vs `root` 的区别

在 Nginx 配置中，`alias` 和 `root` 都用于定义静态文件的存放路径，但它们的作用方式有所不同。

### `alias`

`alias` 用于指定一个确切的目录路径，直接替换 location 中的匹配部分。

##### **示例**

```nginx
location /rendered-articles/ {
    alias /usr/share/nginx/html/rendered-articles/;
}
```

如果用户访问 

```
http://example.com/rendered-articles/test.html
```

Nginx 会查找文件：

```
/usr/share/nginx/html/rendered-articles/test.html
```

`location` 中 `/rendered-articles/` 这部分不会拼接到 `alias` 后面。



### `root`

`root` 用于 定义一个基础目录，然后 Nginx 拼接 location 匹配到的路径 来查找文件。

##### **示例**

```nginx
location /rendered-articles/ {
    root /usr/share/nginx/html/;
}
```

访问 

```
http://example.com/rendered-articles/test.html
```

Nginx 会查找：

```
/usr/share/nginx/html/rendered-articles/test.html
```

- `location` 中 `/rendered-articles/` 这部分会被拼接到 `root` 之后。





## `autoindex off`

`autoindex` 用于控制是否 显示目录列表（当用户访问的是一个目录，而不是具体文件时）。

- `off`（默认值）表示 如果访问目录但没有 `index.html`，则返回 403 Forbidden，而不是列出目录内容。
- `on` 表示 如果访问目录但没有 `index.html`，则列出目录中的文件。