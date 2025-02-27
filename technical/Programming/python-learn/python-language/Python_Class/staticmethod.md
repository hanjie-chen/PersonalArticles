`@staticmethod` 主要用于 类 (class) 中，但它本质上只是一个普通函数

它主要用于类内部，目的是让某些逻辑上属于类的方法不依赖 `self`（实例）或 `cls`（类）

## `staticmethod` 的特点：

1. **没有 `self` 或 `cls` 参数**
   - `self` 代表实例对象，`cls` 代表类本身，而 `staticmethod` 既不访问实例也不访问类。
2. **不能修改实例或类的状态**
   - 普通方法可以访问实例属性（`self.attribute`），类方法可以修改类属性（`cls.attribute`），但静态方法不能直接访问或修改它们。
3. **本质上是一个普通函数**
   - 它和类方法（`@classmethod`）的区别在于，类方法可以访问 `cls`，而静态方法只是一个普通函数，只是被归类到某个类里。

## 什么时候使用 `@staticmethod`？

1. **方法不需要访问实例或类**
   - 如果方法逻辑独立于实例和类，它就可以是 `@staticmethod`。
   - 例如，纯工具函数（utility function），比如数学计算、数据格式转换等。
2. **逻辑上属于类的一部分**
   - 如果一个方法在概念上属于类（而不是全局函数），但不需要访问类或实例的属性，使用 `@staticmethod` 可以让代码更清晰。