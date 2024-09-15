# Latex结构

## 1、Latex文档类

采用下述代码来指定工程要采用的文档类，其中options 和 class-name 均为可选参数。

```latex
\documentclass[options]{class-name}
```

class-name为文档类的名称，常用的文档类名称及对应说明如下表所示。

| 命令    | 说明                         |
| ------- | ---------------------------- |
| article | 短报告、程序文档、学术论文等 |

options 文档类的可选参数，用来设置排版的参数，如果想要写入多个命令，这些命令之间需要使用逗号隔开，参数的详细说明如下表所示。

| 命令                | 说明                                                         |
| ------------------- | ------------------------------------------------------------ |
| 10pt                | 指定文本的字号，默认为10pt，可选为10pt,11pt,12pt             |
| onecolumn\twocolumn | 指定单栏排版，默认为onecolumn，可选为onecolumn，twocolumn    |
| oneside\twoside     | 指定论文的单双面模式，默认是单面印刷oneside，可选为双面印刷twoside |
| fleqn               | 设置行间公式为左对齐， 而不是居中对齐。                      |
| a4paper\letterpaper | 定义纸张的尺寸。 默认设置为letterpaper。                     |

