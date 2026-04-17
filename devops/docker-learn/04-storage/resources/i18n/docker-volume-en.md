<!-- source_blob: 4fd23d5630644fb4c01a1a257388a85d4c3d316c -->

# Docker Volume

A Docker volume is actually a storage space independent of a container. Its lifecycle is separate from the container, which means:

- Volume data still exists after the container restarts
- Deleting a container does not delete the volume

You can think of it as a "shared folder."

In `compose.yml`, we can define and use a volume like this:

```yaml
services:
  web-app:
    volumes:
      - articles_data:/articles-data  # [volume name]:[container path]
    
  articles-sync:
    volumes:
      - articles_data:/articles-data

volumes:
  articles_data:
```

This configuration declares a volume named `articles_data`, and then mounts that volume to:

- the `/articles-data` directory in the `articles-data` container
- the `/articles-data` directory in the `web-app` container

> [!note]
>
> By default, `[volume name]:[container path]` gives the container read-write (`rw`) access to the mounted path, unless it is explicitly set to read-only (`ro`)
>
> Here, `rw` means that processes inside the container have read and write access to this volume.

This volume is actually stored at:

```bash
# Docker volumes are stored by default in
/var/lib/docker/volumes/[volume-name]/_data
```

## Docker Volume Commands

You can use the following commands to inspect Docker volume details.

### `docker volume ls`

List all volumes.

```shell
$ docker volume ls
DRIVER    VOLUME NAME
local     website_articles_data
```

### `docker volume inspect <volume-name>`

View detailed information about a volume.

```bash
$ docker volume inspect website_articles_data
[
    {
        "CreatedAt": "2025-03-07T08:57:39Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "bbb456a7f8812f1aa7fe3fa10a7a34c76dfb2b1ad60eadbae23a2f386992e456",
            "com.docker.compose.project": "website",
            "com.docker.compose.version": "2.33.1",
            "com.docker.compose.volume": "articles_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/website_articles_data/_data",
        "Name": "website_articles_data",
        "Options": null,
        "Scope": "local"
    }
]
```

Here, `Mountpoint` is the storage location of the volume on the host machine.

### `docker volume rm <volume-name>`

Delete a volume. You can also remove volumes by using `docker compose down -v`.

# When Is a Volume Mounted?

If we define a volume mount for a container in `compose.yml`, when does that mount actually happen?

In Docker Compose, volume mounting happens when the container starts, that is, when `docker-compose up` is executed.

For the earlier `compose.yml` example, when you run `docker-compose up`, Compose performs the mount in the following order:

1. Check the `volumes:` keyword

   Since `articles_data` is defined under `volumes:`, Docker Compose checks whether this volume already exists.

   - If it does not exist, Docker Compose creates it automatically
   - If it already exists, Docker Compose mounts it directly

2. Create and start the containers in `services`

   Create the `web-app` and `articles-data` containers, and mount `articles_data` to the corresponding paths

   - If the target path inside the container does not exist: Docker automatically creates the directory and then mounts the volume
   - If the target path inside the container already exists: the original files at that path inside the container are hidden (the original files still exist inside the container; they are just covered by the volume mount. If we stop the container and remove the volume mount, the contents of the original directory still exist), but they are not deleted

3. When the container starts, Docker mounts the volume to the specified path in the container

   `web-app` and `articles-data` share the same volume, so they can both access the `/articles-data` directory, and the files stored there are accessible to each other.

## CMD First, or Volume Mount First?

A Docker volume is mounted when the container starts. At the same time, the `CMD`/`ENTRYPOINT` command defined in the Dockerfile is also executed when the container starts. That leads to a question: which happens first?

Conclusion first:

Docker mounts the volume first, and only then executes `CMD` or `ENTRYPOINT`.

The execution order is as follows (assuming `docker run my_image`):

1. Create the container (based on the image)
2. Mount the volume (if a volume is specified with the `-v` option, mount it into the container filesystem)
3. Execute `ENTRYPOINT` or `CMD` (as the main process of the container)

This is because the container filesystem (including all mounted volumes) must be fully set up before commands can run inside the container. The `CMD`/`ENTRYPOINT` instruction defines the command or script the container runs, but those commands depend on a fully prepared container environment, which includes mounted volumes.

## Next Step

It seems I still cannot find the corresponding Docker documentation to support my argument.

I found a [Stack Overflow post](https://stackoverflow.com/questions/69308389/docker-is-volume-mounted-before-running-cmd), but I really could not find this in the document referenced by the answer: https://github.com/opencontainers/runtime-spec/blob/master/config.md#createruntime-hooks

If there is documentation stating that the container environment includes the filesystem, and documentation stating that the `CMD`/`ENTRYPOINT` instruction can only be executed after the container environment is fully set up, that would also prove this point.

# Docker Volume VS. Bind Mount

Like a bind mount, when a Docker volume is mounted, the target path is covered. Even permission management is similar: a bind mount is determined by the host filesystem, while a Docker volume is determined by the initial creator of the volume and subsequent operations.
