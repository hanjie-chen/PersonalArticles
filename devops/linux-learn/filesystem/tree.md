# tree command



## tree 只显示第一级目录

要让 `tree` 命令只显示第一级目录，可以使用 `-L` 参数（Level的缩写）来指定要显示的目录层级深度。

具体命令如下：
```bash
tree -L 1
```

e.g.
```
Plain@Linux-VM:~/Personal_Project/test-website$ tree -L 1
.
├── Readme.md
├── articles-data
├── compose.yml
└── web-app

2 directories, 2 files
```

```
Plain@Linux-VM:~/Personal_Project/test-website$ tree -L 2
.
├── Readme.md
├── articles-data
│   ├── Dockerfile
│   ├── init.sh
│   ├── logrotate.conf
│   └── update-articles.sh
├── compose.yml
└── web-app
    ├── Dockerfile
    ├── app.py
    ├── config.py
    ├── import_articles_scripts.py
    ├── markdown_render_scripts.py
    ├── models.py
    ├── rendered_articles
    ├── requirements.in
    ├── requirements.txt
    ├── static
    └── templates

5 directories, 14 files
```



这样就只会显示当前目录下的第一层目录，而不会显示更深层次的子目录内容。

如果你还想要一些额外的选项，可以组合使用：
- `tree -L 1 -d`：只显示目录（不显示文件）
- `tree -L 1 -a`：显示所有文件，包括隐藏文件
- `tree -L 1 -h`：显示文件和目录的大小

## `tree -L <layer> -a`

显示所有的文件和目录，包括隐藏的文件

```
Plain@Linux-VM:~/Personal_Project/test-website$ tree -L 2 -a
.
├── .devcontainer
│   └── devcontainer.json
├── .git
│   ├── COMMIT_EDITMSG
│   ├── FETCH_HEAD
│   ├── HEAD
│   ├── ORIG_HEAD
│   ├── branches
│   ├── config
│   ├── description
│   ├── hooks
│   ├── index
│   ├── info
│   ├── logs
│   ├── objects
│   ├── packed-refs
│   └── refs
├── .gitignore
├── Readme.md
├── articles-data
│   ├── Dockerfile
│   ├── init.sh
│   ├── logrotate.conf
│   └── update-articles.sh
├── compose.yml
└── web-app
    ├── .dockerignore
    ├── Dockerfile
    ├── __pycache__
    ├── app.py
    ├── config.py
    ├── import_articles_scripts.py
    ├── instance
    ├── markdown_render_scripts.py
    ├── models.py
    ├── rendered_articles
    ├── requirements.in
    ├── requirements.txt
    ├── static
    └── templates

15 directories, 25 files
```



