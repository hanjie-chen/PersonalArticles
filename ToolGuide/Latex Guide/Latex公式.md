# Latex

## Pdftex编译中文方法：

首先载入CJKutf8的宏包，这个包仅支持四种字体，每一段中文段落必须包含`\begin{CJK*}{UTF8}{gbs}`

```latex
\documentclass{article}
\usepackage{CJKutf8}
	
\begin{document}
 
	\begin{CJK*}{UTF8}{gbsn}
		\section{支持简体中文宋体}
		这是一段宋体的简体中文的文字。
	\end{CJK*}
	\begin{CJK*}{UTF8}{gkai}
		\section{支持简体中文楷体}
		这是一段楷体的简体中文的文字。
	\end{CJK*}
	\begin{CJK*}{UTF8}{bsmi}
		\section{支持繁體中文宋體}
		這是一段宋體的繁體中文文字。
	\end{CJK*}
	\begin{CJK*}{UTF8}{bkai}
		\section{支持繁體中文楷體}
		這是一段楷體的繁體中文文字。
	\end{CJK*}
 
\end{document}
```

所以如果需要显示中文，只需要在头尾加上`\begin{CJK*}{UTF8}{gbs}`和`\end{CJK*}`即可，如下所示

```latex
\documentclass{article}
\usepackage{CJKutf8}
	
\begin{document}
 
\begin{CJK*}{UTF8}{gbsn}
% 添加任意代码——————————————————————————————————————————————————————————————————————————————————————
	\begin{table}[h!]
		\begin{center}
		  \caption{测试函数信息表格}
		  \begin{tabular}{l|c|r} 
			\textbf{Value 1} & \textbf{Value 2} & \textbf{Value 3}\\
			$\alpha$ & $\beta$ & $\gamma$ \\
			\hline
			1 & 1110.1 & a\\
			2 & 10.1 & b\\
			3 & 23.113231 & c\\
		  \end{tabular}
		\end{center}
	  \end{table}
% 中文显示区域结束———————————————————————————————————————————————————————————————————————————————————
\end{CJK*}

\end{document}
```



