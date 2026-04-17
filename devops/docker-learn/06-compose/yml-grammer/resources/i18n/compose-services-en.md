<!-- source_blob: db8034c621dc2085b8931eb6544b1a4781ffb9b7 -->

# `compose.yml` –> Detailed `services` Syntax Explanation

[Services top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/services/)



# `container name`

```
# 指定 contianer name
container_name: web-app
```

If you do not specify `container_name`, Docker Compose will automatically generate a default container name in the format `<project>_<service>_<number>`.

e.g. `test-website-articles-data-1 `



# `develop-watch`

[Use Compose Watch | Docker Docs](https://docs.docker.com/compose/how-tos/file-watch/)

During development, when some code changes, we often need to restart or rebuild the container so the changes take effect and we can see the result. But manually running `docker compose down` and then `docker compose up` is really too cumbersome.

In this case, we can use the `develop: watch` field.

## Grammar

```yaml
develp:
  watch:
    - path: project-source-path/
      target: container-destination-path
      action: 
      ignore:
        - ignore-path/
```

### `watch`

- Except for `ignore`, all paths are relative to the project path.
- `.dockerignore` rules apply automatically, and the `.git` folder is also ignored automatically.

### `action`

- `sync` copies changes from the project path to the container target path.
- `rebuild` rebuilds a new image and replaces the original container.
- `sync+restart` copies changes and then restarts.

`action` can only be one of these three values and cannot be split or combined arbitrarily. For example, you cannot use `restart` by itself.

### `path` and `target`

- `path`: the host project path
- `target`: the container path

If `target` is not specified, then the `sync` action will, by default, synchronize the host `path` to the same path inside the container.

### `ignore`

It must be an array (list), even if it contains only one element.

```yaml
ignore:
  - logs/
```

wrong config

```yaml
ignore: logs/
```

The paths in `ignore` are relative to the `path` parameter. For example, in my project:

```shell
website
├── Readme.md
├── articles-sync
│   ├── Dockerfile
│   ├── ...
│   ├── logs
├── compose.yml
└── web-app
    ├── Dockerfile
    ├── ...
    ├── ...
    └── templates
```

If I want to ignore all files under `website/articles-sync/logs`, then in YAML it would be:

```yaml
services:
  ...

  articles-sync:
    ...
    develop:
      watch:
        - path: ./articles-sync
          ignore:
            - logs/**
          action: rebuild

volumes:
  articles_data:
```

In fact, the Docker Compose watch documentation barely explains the `ignore` relative path part, so I created a PR to make it clearer.

PR: [Update file-watch.md: add ignore attribute path by hanjie-chen · Pull Request #21820 · docker/docs](https://github.com/docker/docs/pull/21820)

## `compose watch` VS. `bind mounts`

We can use a bind mount to share a host directory with a directory inside the container.

Likewise, we can use the `compose watch` field to detect source code changes and synchronize them into the container, while also using the `ignore` field and `.dockerignore` to control which files are watched.

However, the two can often coexist. For example, if I need to inspect all file changes in a directory inside the container in real time, I still need a bind mount, not just source code syncing.

## Start Watch

We can use the following command to enable watch mode:

```shell
docker compose up --watch
```

Or use:

```shell
docker compose watch
```

However, this command only outputs file-watch-related information and does not include detailed container runtime logs.

Note that the output of the first command is essentially still `docker logs`, so if your SSH connection drops unexpectedly, you can use the following command to view Docker logs in real time and get a similar effect:

```shell
docker compose logs -f
```

# `ports`

docker documents: [Services top-level elements | Docker Docs](https://docs.docker.com/reference/compose-file/services/#ports)

We may want to expose a process inside the container to the host machine. In that case, we need to use the `ports` field.

Grammar

```yaml
ports:
  - "8080:5000"  # "<host-machine port>":"<container port>"
```

# `image` & `build`

build: [Compose Build Specification | Docker Docs](https://docs.docker.com/reference/compose-file/build/)

## build

Used to specify how to build an image.

```yaml
build:
  context: ./articles-sync
  dockerfile: Dockerfile
```

- `context`: the location of the build context

- `dockerfile`: the location of the Dockerfile. If the default name `Dockerfile` is used, this field can also be omitted, and the whole configuration can be simplified to:

  ```yaml
  build: ./articles-sync
  ```

By default, Docker Compose automatically names the built image in the format `<project-name>_<service-name>` (the project name is usually the current directory name).

If you need a custom image name, you can combine it with the `image` field:

```yaml
build: ./articles-sync
image: articles-sync1.0
```

> [!tip]
>
> Although field order does not affect functionality, for readability and consistency, we usually place `build` before `image`: logically, building first and then naming feels more intuitive.

## image

Used to specify an existing image (which may be built locally or pulled from a remote registry). Docker Compose will use this image directly to start the container instead of building a new one.

```yaml
image: nginx
```

# `depends_on`

`depends_on` is used to define dependency relationships between services and can control startup order.

If service A specifies service B in `depends_on`, then Docker Compose will ensure that service B starts first, and then service A starts.

```yaml
nginx:
  depends_on:
    - web
```

# `healthcheck`

Used to define container health checks. It allows Docker to periodically check the runtime status inside the container and determine the container's health based on the result.

- Automatically detect whether the application is running normally  
   For example, a Flask app may have already crashed while the process is still running. By default, Docker will not detect this, but `healthcheck` can check proactively.
- **Ensure dependent services are available**  
   For example, if `web-app` depends on `articles-sync`, you can use `condition: service_healthy` in `web-app`'s `depends_on` configuration so it waits until `articles-sync` becomes healthy before starting.
- **Enable smarter container management in Swarm or Compose**  
   When a service is unhealthy, Swarm may reschedule the container.

## config

`healthcheck` mainly consists of the following parameters:

- **`test`**: specifies the health check command to execute, usually a shell command or `CMD` form.
- **`interval`**: the interval between checks (default `30s`).
- **`timeout`**: the timeout for the health check command (default `30s`).
- **`retries`**: how many failures before the container is considered unhealthy (default `3`).
- **`start_period`**: during this time after the container starts, health checks will not be triggered. This is suitable for slower-starting applications.

## example

Check whether a Flask application is running normally:

```yaml
services:
  web-app:
    image: my-flask-app
    ports:
      - "5000:5000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

- `test`: uses `curl` to access `http://localhost:5000/health`. If the HTTP request fails, the container is considered unhealthy.
- `interval: 30s`: checks every 30 seconds.
- `timeout: 10s`: if there is no response within 10 seconds, it counts as a failure.
- `retries: 3`: after 3 consecutive failures, the container is marked as `unhealthy`.
- `start_period: 10s`: after the container starts, no health check will run during the first 10 seconds, giving Flask time to start.

# `command`

In a `compose.yml` file, the `command` field overrides the `CMD` startup command in the Dockerfile. For example, suppose we have the following `compose.yml`:

```yaml
services:
  web-app:
    ...
    command: ["flask", "run", "--host=0.0.0.0", "--debug"]
```

And in `web-app`'s Dockerfile we write:

```dockerfile
...

# 启动命令 (production)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

Then in the end, `flask run` will actually be used as the startup command. This is useful for development environment setup. For example, you can create a `compose.dev.yml` to override the command in the Dockerfile.

# Custom fields

Fields beginning with `x-` are treated by Docker as "user-defined extensions." Compose completely ignores their contents, which makes them a great place to store YAML anchors.

For example, we can use `x-` and the `&` anchor to reuse a configuration, such as reusing Docker log settings:

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "1m"
    max-file: "5"

services:
  articles-sync:
    ...
    logging: *default-logging
  ...
...
```
