# Latex编译产生的辅助文件

### 1、.aux文件

LaTeX 生成的主辅助文件，记录交叉引用、目录、参考文献的引用等。

### 2、.log文件

 排版引擎生成的日志文件，供排查错误使用。

### 3、.fls文件

### 4、.out文件

 hyperref 宏包生成的 PDF 书签记录文件。

### 5、.fdb_latexmk文件

### 6、.synctex.gz文件

7、删除每次编译之后产生的辅助文件，在setting.json里面加入

```json
"latex-workshop.latex.autoClean.run": "onBuilt",
    "latex-workshop.latex.clean.fileTypes": [
        "*.aux",
        "*.bbl",
        "*.blg",
        "*.idx",
        "*.ind",
        "*.lof",
        "*.lot",
        "*.out",
        "*.toc",
        "*.acn",
        "*.acr",
        "*.alg",
        "*.glg",
        "*.glo",
        "*.gls",
        "*.ist",
        "*.fls",
        "*.log",
        "*.fdb_latexmk",
        "*.gz"
    ]
```

即可

