# Python import 重复

我在文件 `single_perceptron_class.py` 中引入过了numpy, 然后我



## Import 作用域

在一个文件中导入的模块只在该文件的作用域内有效，例如在 `single_perceptron_class.py` 中导入 `numpy` 

然后在`perceptron_gate.py`中import single_perceptron_class， 不会使其在 `perceptron_gate.py` 中自动可用。

因为Python的导入机制很智能，多次导入同一库不会造成性能问题。实际上，库只会被加载一次到内存中，后续的导入只是创建新的引用。

## 记住 

在Python中，明确地在每个需要使用某个库的文件中导入该库是一个好习惯，不会造成实际的性能问题，反而会提高代码质量。