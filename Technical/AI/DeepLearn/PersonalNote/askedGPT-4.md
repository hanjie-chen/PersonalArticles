# Data Normalization

> ## **数据归一化的概念**
>
> 数据归一化是一种预处理技术，用于将数据转换为统一的标准范围。在许多机器学习和深度学习应用中，数据归一化非常重要，因为它有助于模型更容易学习到数据中的规律。常见的归一化方法有：最小-最大缩放（Min-Max Scaling）和标准化（Standardization）。
>
> - 最小-最大缩放：将数据缩放到一个指定的范围，通常是[0, 1]。适用于数据集的分布未知，或者数据集的分布不规律的情况。计算公式为：
>
> $$
> x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}
> $$
>      
>
>    - 标准化：通过计算数据的均值和标准差，将数据转换成均值为0，标准差为1的数据,这种方法在数据分布近似正态分布时表现较好.计算公式为：
>      $$
>      x_{norm} = \frac{x - \mu}{\sigma}
>      $$
>
>    这种方法在数据分布近似正态分布时表现较好
>
>    其中，$x_{norm}$表示归一化后的数据，$x$表示原始数据，$x_{min}$和$x_{max}$分别表示数据的最小值和最大值，$\mu$表示均值，$\sigma$表示标准差。
>
> ## **在神经网络中实现数据归一化的方法**
>
> 在神经网络中实现数据归一化的方法通常分为两个步骤：首先，在训练数据集上计算归一化的参数（例如最小值、最大值、均值和标准差），然后使用这些参数对训练数据集和测试数据集进行归一化。这样做的目的是确保训练和测试数据集具有相同的分布。以下是实现数据归一化的一个简单示例（Python代码）：
>
> `````python
> import numpy as np
>    
> # 假设 X_train 和 X_test 是训练和测试数据集
> X_train, X_test = ...
>    
> # 计算归一化参数
> x_min, x_max = np.min(X_train), np.max(X_train)
> mean, std = np.mean(X_train), np.std(X_train)
>    
> # 最小-最大缩放
> X_train_normalized = (X_train - x_min) / (x_max - x_min)
> X_test_normalized = (X_test - x_min) / (x_max - x_min)
>    
> # 标准化
> X_train_standardized = (X_train - mean) / std
> X_test_standardized = (X_test - mean) / std
> ```
> `````
>
> ## **为什么需要数据归一化以及一个例子**
>
> 数据归一化的主要目的是消除数据中不同特征的量纲影响，使得模型能够更快地学习到数据中的规律。在许多情况下，数据的原始尺度可能相差很大，这可能导致模型在训练过程中收敛缓慢或者陷入局部最优解。
>
> 例如，在一个房价预测问题中，我们可能有两个特征：房子的面积（以平方米为单位）和房间的数量。假设面积的范围是[20, 200]，而房间数量的范围是[1, 5]。这两个特征的尺度差异很大，如果不进行归一化，模型可能会过分关注面积特征，因为它的数值相对较大。通过进行归一化，我们可以使得这两个特征具有相同的尺度，从而帮助神经网络更容易地找到合适的权重。
>
> 数据归一化还可以提高模型的泛化能力，防止过拟合。归一化后的数据具有相同的尺度，使得模型更容易学习到各个特征之间的相互关系，而不是只关注数值较大的特征。这有助于提高模型在未知数据上的预测性能。

# About affine transformation in forward propagation

> 1. 在神经网络中引入仿射变换的概念有以下好处：
>
> - **更广泛的表达能力**：仿射变换包括了线性变换（矩阵乘法）和平移（向量加法），这样的组合使得神经网络具有更强大的表达能力。这种非线性表达能力使神经网络能够更好地拟合复杂函数以解决实际问题。
>
> - **更直观的几何解释**：仿射变换在几何意义上表现为旋转、缩放、翻转和平移等操作，这种直观的几何理解有助于我们理解神经网络在处理数据时的变换过程。
>
> - **保留某些性质**：仿射变换能够保留原始数据的某些性质，例如，保留向量空间的平行性。这些性质有助于神经网络在处理数据时保持其结构特征。
>
> 2. 当然，你可以将仿射变换简单地理解为矩阵相乘再相加。然而，将其视为一个整体概念有一些优势：
>
> - **更加通用**：将仿射变换作为一个整体概念可以帮助我们更容易地理解和扩展到其他领域，例如计算机图形学、几何变换等。
>
> - **更清晰的理解**：将矩阵乘法和向量加法分开看可能会使我们忽略它们在神经网络中的结合作用。将它们作为一个整体的仿射变换有助于我们更好地理解神经网络中的变换过程。
>
> 总之，引入仿射变换的概念可以帮助我们更好地理解神经网络的工作原理，提升其表达能力，并在几何意义上更直观地描绘数据的变换。

# Mini-Batch : how to choose the size of mini-batch?

> 你提到的batch size选择的细节点很重要。我补充几点:
>
> 1. 一般来说,选择2的幂作为batch size会更高效:
>
> 原因是计算机内存和硬件都更喜欢2的幂。特别是GPU,它的计算能力是以2的幂为单位的,选择2的幂作为batch size可以更充分利用GPU。
>
> 2. 所以对于MNIST数据集,更好的batch size选择是:32、64、128。
>
> 这些都是2的幂,而且在MNIST数据集上效果都不错。
>
> 3. 选择77、72这种非2的幂的batch size效果可能不如2的幂。
>
> 原因如上,计算机和硬件不喜欢这些奇怪的数字。
>
> 4. batch size越大,训练速度越快,但可能带来过拟合。
>
> 所以一般来说,batch size在32到128之间是个好选择。
>
> 5. 对于不同的模型和数据集,合适的batch size也不同。
>
> MNIST这种简单数据集可以选择较大的batch size,而复杂数据集可能需要较小的batch size。
>
> 6. 你可以尝试不同的batch size,选择效果和训练速度最佳的。
>
> 所以总的来说,对于MNIST数据集,我建议你首先选择64或128作为batch size,这些数字效果最佳,而且训练速度也比较快。
> 如果效果不佳,你可以再尝试32作为batch size。
>
> 希望以上细节能帮助你选择一个合适的batch size!如果还有任何疑问,欢迎继续提,我会尽量回答。

# The Middle Layer neuro number

> 对于这个问题,没有一个确切的答案,中间层的神经元个数需要根据你的需求和经验来选择。一般来说,有以下几点可以参考:
>
> 1. 太少的神经元可能无法捕捉足够的信息,影响识别效果。
>
> 2. 太多的神经元可能会过拟合,降低泛化能力。
>
> 3. 通常情况下,输入层和输出层之间的神经元个数差不多在1-10倍之间。
>
> 4. 对于MNIST数据集来说,中间层的神经元个数一般在100-500之间。
>
> 5. 你可以从200开始尝试,如果效果不佳可以逐渐增加到500左右。
>
> 6. 另外,你可以使用多个中间层,每个层的神经元个数不同。
>
> 7. 选择中间层神经元个数需要根据你的识别效果来决定,需要一定的试错。
>
> 综上所述,我建议你:
>
> - 首先从200个神经元的单个中间层开始。
>
> - 如果识别效果不佳,逐渐增加到500个左右。
>
> - 如果还不理想,你可以试试两个中间层,第一个200个神经元,第二个500个神经元。
>
> - 根据你的实际效果来决定是否需要更多的中间层和更多的神经元。
>
> - 最后找到一个你满意的效果和结构。
>
> 希望以上参考能帮助你选择一个合适的中间层结构!如果还有任何疑问,欢迎继续提,我会尽量回答。

# The Activate Function in Neural Network

> Generally, we use the same activate function in hidden layer such as ReLU fucntion.
>
> And wu use another different activate function in output layer such as sigmod or softmax.
>
> 

# How to use test data

> After every epoch turn, use the test data to evaluate the model ability.