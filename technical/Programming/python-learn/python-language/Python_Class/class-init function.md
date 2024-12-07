# `__init__.py` 文件

1. **定义模块的公共接口**:

   ```
   __mixins__ = [BaseNestedSets]
   __all__ = ['BaseNestedSets', 'mptt_sessionmaker']
   ```

   - `__mixins__`：这是一个列表，包含了`BaseNestedSets`类，可能用于内部标识哪些类是mixin。
   - `__all__`：定义了模块的公共接口，指定导入时公开的名称。在使用`from sqlalchemy_mptt import *`时，只会导入这里列出的名称。



# 类方法和实例方法

在 Python 中，`@classmethod` 定义的类方法与普通在类中定义的实例方法有几个显著的不同：

### 1. 绑定对象不同

- **实例方法**：
  - 普通的实例方法是绑定到类的实例上的。调用时，第一个参数是 `self`，代表调用该方法的实例对象。
  - 实例方法可以访问和修改该实例的属性。

- **类方法**：
  - 类方法是绑定到类本身的，而不是实例。调用时，第一个参数是 `cls`，代表调用该方法的类。
  - 类方法可以访问和修改类级别的属性（类变量），但不能直接访问实例属性（除非通过某种方式传递实例）。

### 2. 调用方式不同

- **实例方法**：
  - 需要通过实例来调用。
  ```python
  class MyClass:
      def instance_method(self):
          print("This is an instance method.")
  
  obj = MyClass()
  obj.instance_method()  # 通过实例调用
  ```

- **类方法**：
  - 可以通过类本身或实例来调用。
  ```python
  class MyClass:
      @classmethod
      def class_method(cls):
          print("This is a class method.")
  
  MyClass.class_method()  # 通过类调用
  obj = MyClass()
  obj.class_method()      # 通过实例调用
  ```

### 3. 适用场景不同

- **实例方法**：
  - 适用于需要访问或修改实例状态的操作。
  - 需要对具体的对象进行操作时使用。

- **类方法**：
  - 适用于需要访问或修改类状态的操作。
  - 常用于实现工厂方法，或者当方法逻辑与特定实例无关，但需要与类相关时使用。

### 总结

实例方法和类方法主要在于它们的绑定对象不同，以及它们的适用场景不同。实例方法用于操作实例数据，而类方法用于操作类数据。选择使用哪种方法取决于你需要操作的数据是与具体实例相关还是与整个类相关。
