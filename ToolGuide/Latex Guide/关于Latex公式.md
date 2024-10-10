# Latex基本数学公式+符号

只需要两个$即可

1\极限
$$
{\lim_{x\to +\infty}}
$$
2\大括号
$$
\left\{\begin{array}{**lr**}  
             指针  \left\{\begin{array}{**lr**} 单链表\\双链表\end{array}\right.   \\
             数组  
\end{array}\right.
$$
3\箭头带文字
$$
a\stackrel{text}{\longrightarrow}b
$$
4\上下标省略号
$$
a_1,b^3,\cdot,\cdots
$$
5\向上取整 向下取整
$$
\lceil x \rceil \\
\lfloor x \rfloor
$$
6\表示正负号，约等于
$$
\pm \\
\approx
$$
7\求和符号
$$
\sum_{i=0}^{n}x_{i}^2
$$
8\绝对值
$$
\lvert C_{2} \rvert
$$

# Latex 公式推导 等号对齐

`{algin}` 和 `&=` 配合使用
$$
\begin{align}
Error &= \frac{1}{N}\times(Target-Output)^2\\
      &=\frac{1}{N}\times\sum_{i=1}^{N}(target_{i}-output_{i})^2
\end{align}
$$

# Latex 数学定义

使用符号`\triangleq` 来定义一个变量
$$
Net_{1\times m} \triangleq f_a(Input_{1\times n} \cdot Weights_{n\times m}^{hidden} + Bias_{1\times m}^{hidden})
$$


# Latex 增加变量之间空隙

使用`\quad` 可以增加公式之间空隙，从而达到美化效果
$$
Hidden_{1\times m} = f_a(Net_{1\times m}^{hidden}) \quad \Rightarrow \quad hidden_i = f_a(net_i^{hidden})
$$


# Latex 表示函数导数

直接暴力的在函数右上角加上`'`即可，例如：
$$
\frac{\partial (output_i)}{\partial (net_i^{output})} = \frac {\partial f_a(net_i^{output})} {\partial net_i^{output}}=f_a^{'}(net_i^{output})
$$


