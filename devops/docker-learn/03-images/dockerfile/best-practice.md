# Dockerfile best practice

这里记录一些关于 dockerfile 的 best practice



# Run Container Processes as Non-Root

有时候我们会遇到这样子的问题，那就是 contianer 中的使用 root user 运行的 process 读写了一些文件，而这些文件是 bind mount 到 host 中，导致 host 中的 nonuser 无法操作这些文件。

而如果我们不在 Dockerfile 中专门的指定某个 user 来运行 process 的话，默认情况下，Docker 容器中的进程是以 `root` 用户运行的，这可能会带来安全风险。

为了降低安全风险，我们就需要避免 container 使用 root 权限运行 process

e.g.

```dockerfile
FROM alpine:3.19

# Define args for user/group IDs - you can pass these during build
ARG USER_ID=1000
ARG GROUP_ID=1000

# install git and dcron
RUN apk add --no-cache git dcron logrotate shadow # Add shadow for groupadd/useradd

# Create a group and user with specific IDs (match your host user if possible)
RUN addgroup -g ${GROUP_ID} -S appgroup && \
    adduser -u ${USER_ID} -S appuser -G appgroup

# Create log directory, set ownership to the new user/group
RUN mkdir -p /var/log/personal-website && \
    touch /var/log/personal-website/{articles-sync,crond}.log && \
    chown -R appuser:appgroup /var/log/personal-website

# create logrotate dir and copy file
COPY logrotate.conf /etc/logrotate.d/personal-website

# Set ownership for the data directory mount point as well
RUN mkdir -p /articles-data && chown appuser:appgroup /articles-data
WORKDIR /articles-data

# copy the scripts, provide the permission
COPY --chown=appuser:appgroup update-articles.sh init.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/update-articles.sh && \
    chmod +x /usr/local/bin/init.sh

# --- CRITICAL PART ---
# Switch to the non-root user BEFORE running the entrypoint/cmd
USER appuser

ENTRYPOINT [ "/usr/local/bin/init.sh" ]
```





