我一开始的想法是把渲染完成的 html 文件直接一股脑的全部放到 rendered_articles 这个文件夹下面，然后为了防止同名文件，我打算使用数据库的主键 id 作为html 的文件名称，例如

```perl
➜ rendered_articles
├───1.html
├───2.html
├───3.html
├───4.html
└───5.html
```

但是这样子会遇到一个问题，那就是如果源文件需要使用 images 里面的资源，那么他又要去哪里找呢？所以我又想着需要把 images 文件夹拷贝过去

所以问题来了，把这个 images 文件夹放在哪里？

我的想法是，在 rendered_articles 中每一个分类都创建一个文件夹，然后把images文件夹 copy 进去即可，然后把属于这个 category 的文章都放在这个文件夹下，这样子就无需修改 html 中的图片引用方式，我都是使用相对路径来引用图片的，例如 `./images/cover_image.jpg`

而这个文件夹的命令，则是把 category 中的 `/` 更换为 `-` 例如

```perl
rendered_articles/
├── PythonLearn-PythonPackage-SQLAlchemy
│   ├── 2.html
│   └── images
│       └── cover_image.png
├── PythonLearn-PythonPackage-flask-sqlalchemy
│   ├── 3.html
│   └── images
│       └── cover_image.webp
└── ToolGuide-GitGuide
    ├── 1.html
    └── images
        └── cover_image.png
```



