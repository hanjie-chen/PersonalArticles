---
Title: A Brief Introduction to Using Docker Volumes
SourceBlob: 4fd23d5630644fb4c01a1a257388a85d4c3d316c
---

```
BriefIntroduction: Some thoughts and questions I have about using Docker volumes
```

<!-- split -->

# Docker Volume

A Docker volume is actually a storage space independent of a container, and its lifecycle is also independent of the container. In other words:

- Volume data still exists after the container is restarted
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

This configuration declares a volume named `articles_data`, and that volume is then mounted to:

- the `/articles-data` directory in the `articles-data` container
- the `/articles-data` directory in the `web-app` container

> [!note]
>
> By default, `[volume name]:[container path]` gives the container read-write (`rw`) access to the mounted path, unless it is explicitly specified as read-only (`ro`)
>
> Here, `rw` means that processes inside the container have read and write access to this volume.

This volume is actually stored at:

```bash
# Docker volumes are stored by default in
/var/lib/docker/volumes/[volume-name]/_data
```

## docker volume command

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

Delete a volume. You can also delete volumes with `docker compose down -v`.

# When Is a Volume Mounted?

If we define in `compose.yml` that a container mounts a volume, then when does that mount actually happen?

In Docker Compose, volume mounting happens when the container starts, that is, when `docker-compose up` is executed.

For the `compose.yml` in the previous example, when you run `docker-compose up`, Compose mounts the volume in the following order:

1. Check the `volumes:` key

   Under `volumes:`, `articles_data` is defined, so Docker Compose checks whether this volume already exists.

   - If it does not exist, Docker Compose creates it automatically
   - If it already exists, Docker Compose mounts it directly

2. Create and start the containers in `services`

   Create the `web-app` and `articles-data` containers, and mount `articles_data` to the corresponding paths

   - If the target path inside the container does not exist: Docker automatically creates that directory and then mounts the volume
   - If the target path inside the container already exists: the original files at that path inside the container are hidden (the original files still exist inside the container; they are just covered by the volume mount. If we stop the container and remove the volume mount, the original directory contents still exist), but they are not deleted

3. When the container starts, Docker mounts the volume to the specified path in the container

   `web-app` and `articles-data` share the same volume, so they can both access the `/articles-data` directory, and files stored there are accessible to each other.



## CMD first? or volume mount first?

A Docker volume is mounted when the container starts. At the same time, the `CMD`/`ENTRYPOINT` commands defined in the Dockerfile are also executed when the container starts. That leads to a question: which one happens first?

Here is the conclusion first:

Docker mounts the volume first, and only then executes `CMD` or `ENTRYPOINT`.

The execution order is as follows (assuming `docker run my_image`):

1. Create the container (based on the image)
2. Mount the volume (if a volume is specified with the `-v` parameter, it is mounted into the container filesystem)
3. Execute `ENTRYPOINT` or `CMD` (as the container's main process)

This is because the container filesystem (including all mounted volumes) must be fully set up before commands can be executed inside the container. The `CMD`/`ENTRYPOINT` instructions define the command or script the container runs, but those commands depend on a fully prepared container environment (including the mounted volumes).



## next action

It seems I still cannot find corresponding Docker documentation to support this point.

I found a [Stack Overflow post](https://stackoverflow.com/questions/69308389/docker-is-volume-mounted-before-running-cmd), but I really could not find the relevant explanation in the documentation linked in the answer either: https://github.com/opencontainers/runtime-spec/blob/master/config.md#createruntime-hooks

If there is documentation stating that the container environment includes the filesystem, and documentation stating that `CMD`/`ENTRYPOINT` instructions can only be executed after the container environment is fully set up, that would also prove this point.



# Docker volume VS. bind mount

Like a bind mount, when a Docker volume is mounted, the path it is mounted to will be covered. Even permission management is similar: a bind mount is determined by the host filesystem, while a Docker volume is determined by the volume's initial creator and subsequent operations.
