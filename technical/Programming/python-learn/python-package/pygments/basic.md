# Pygments 主题选择

使用命令 `pygmentize -L style` 可以看到 pygments 的主题

```shell
Plain@Linux-VM:~/Personal_Project/test-website$ pygmentize -L style
Pygments version 2.18.0, (c) 2006-2024 by Georg Brandl, Matthäus Chajdas and contributors.

Styles:
~~~~~~~
* abap:

* algol:

* algol_nu:

* arduino:
    The Arduino® language style. This style is designed to highlight the Arduino source code, so expect the best results with it.
* autumn:
    A colorful style, inspired by the terminal highlighting style.
* bw:

* borland:
    Style similar to the style used in the borland IDEs.
* coffee:
    A warm and cozy theme based off gruvbox
* colorful:
    A colorful style, inspired by CodeRay.
* default:
    The default style (inspired by Emacs 22).
* dracula:

* emacs:
    The default style (inspired by Emacs 22).
* friendly_grayscale:
    A modern grayscale style based on the friendly style.
* friendly:
    A modern style based on the VIM pyte theme.
* fruity:
    Pygments version of the "native" vim theme.
* github-dark:
    Github's Dark-Colorscheme based theme for Pygments
* gruvbox-dark:
    Pygments version of the "gruvbox" dark vim theme.
* gruvbox-light:
    Pygments version of the "gruvbox" Light vim theme.
* igor:
    Pygments version of the official colors for Igor Pro procedures.
* inkpot:

* lightbulb:
    A minimal dark theme based on the Lightbulb theme for VSCode.
* lilypond:
    Style for the LilyPond language.
* lovelace:
    The style used in Lovelace interactive learning environment. Tries to avoid the "angry fruit salad" effect with desaturated and dim colours.
* manni:
    A colorful style, inspired by the terminal highlighting style.
* material:
    This style mimics the Material Theme color scheme.
* monokai:
    This style mimics the Monokai color scheme.
* murphy:
    Murphy's style from CodeRay.
* native:
    Pygments version of the "native" vim theme.
* nord-darker:
    Pygments version of a darker "nord" theme by Arctic Ice Studio
* nord:
    Pygments version of the "nord" theme by Arctic Ice Studio.
* one-dark:
    Theme inspired by One Dark Pro for Atom.
* paraiso-dark:

* paraiso-light:

* pastie:
    Style similar to the pastie default style.
* perldoc:
    Style similar to the style used in the perldoc code blocks.
* rainbow_dash:
    A bright and colorful syntax highlighting theme.
* rrt:
    Minimalistic "rrt" theme, based on Zap and Emacs defaults.
* sas:
    Style inspired by SAS' enhanced program editor. Note This is not meant to be a complete style. It's merely meant to mimic SAS' program editor syntax highlighting.
* solarized-dark:
    The solarized style, dark.
* solarized-light:
    The solarized style, light.
* staroffice:
    Style similar to StarOffice style, also in OpenOffice and LibreOffice.
* stata-dark:

* stata-light:
    Light mode style inspired by Stata's do-file editor. This is not meant to be a complete style, just for use with Stata.
* tango:
    The Crunchy default Style inspired from the color palette from the Tango Icon Theme Guidelines.
* trac:
    Port of the default trac highlighter design.
* vim:
    Styles somewhat like vim 7.0
* vs:

* xcode:
    Style similar to the Xcode default colouring theme.
* zenburn:
    Low contrast Zenburn style.
```

在这个网站可以看到这些 theme 具体的样子 https://pygments.org/styles/

因为我的网站使用暗黑模式，所示考虑

Dracula, Monokai, One Dark, Github Dark

# export css file

为了导出这个 css 文件，我们可以使用命令

```shell
pygmentize -S default -f html -a .codehilite > styles.css
```

## 命令详解

`pygmentize` 是 **Pygments** 库的命令行接口（CLI）

`-S default`

指定要使用的配色方案， default 表示使用默认的 Pygments 样式 可以使用命令 `pygmentize -L style` 列出所有可用主题

- **参数**：`-S` 或 `--style`
- **用法**：`-S <style>`

`-f html`

指定输出格式为 HTML，生成适用于 HTML 页面使用的 CSS 样式表

- **参数**：`-f` 或 `--format`
- **用法**：`-f <format>`

`-a .codehilite`

指定 CSS 选择器，使用 `.codehilite` 作为选择器前缀。使生成的 CSS 规则只适用于具有 `.codehilite` 类的元素。防止样式污染其他元素。生成的 CSS 规则会形如：

```css
.codehilite .k { color: #008000; } /* 关键字 */
.codehilite .s { color: #BA2121; } /* 字符串 */
/* 其他规则 */
```

- **参数**：`-a` 或 `--prefix`
- **用法**：`-a <prefix>`

> [!note]
>
> 为什么要使用 `-a .codehilite`？
>
> - python-markdown 中使用 `CodeHilite` 扩展在渲染代码块时，默认会将代码包裹在一个具有 `.codehilite` 类的 `<div>` 或 `<pre>` 标签中。
> - 通过在 CSS 中指定前缀 `.codehilite`，可以确保这些样式只应用于代码高亮的部分，不会影响到页面中其他代码。

#### `> styles.css`

生成的 CSS 样式内容会被保存到 `styles.css`，以便您可以在 HTML 中引入。