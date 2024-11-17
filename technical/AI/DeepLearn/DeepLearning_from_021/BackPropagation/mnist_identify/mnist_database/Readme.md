# Mnist Database illustration

the url of the mnist is : [MNIST handwritten digit database, Yann LeCun, Corinna Cortes and Chris Burges](http://yann.lecun.com/exdb/mnist/)

the mnist have 4 file :

```python
'train_img':'train-images-idx3-ubyte.gz',
'train_label':'train-labels-idx1-ubyte.gz',
'test_img':'t10k-images-idx3-ubyte.gz',
'test_label':'t10k-labels-idx1-ubyte.gz'
```

MNIST数据集中的文件名称是根据它们的数据类型、用途和格式来命名的。下面是对每个文件名称的解释：

- train-images-idx3-ubyte.gz: 这个文件包含了MNIST训练集的图像数据。其中，"train"表示这是训练集，"images"表示这是图像数据，"idx3"表示这个文件使用了IDX3格式来存储数据，"ubyte"表示这个文件中的数据类型是无符号字节。
- train-labels-idx1-ubyte.gz: 这个文件包含了MNIST训练集的标签数据。其中，"train"表示这是训练集，"labels"表示这是标签数据，"idx1"表示这个文件使用了IDX1格式来存储数据，"ubyte"表示这个文件中的数据类型是无符号字节。
- t10k-images-idx3-ubyte.gz: 这个文件包含了MNIST测试集的图像数据。其中，"t10k"表示测试集中包含的10,000个样本，"images"表示这是图像数据，"idx3"表示这个文件使用了IDX3格式来存储数据，"ubyte"表示这个文件中的数据类型是无符号字节。
- t10k-labels-idx1-ubyte.gz: 这个文件包含了MNIST测试集的标签数据。其中，"t10k"表示测试集中包含的10,000个样本，"labels"表示这是标签数据，"idx1"表示这个文件使用了IDX1格式来存储数据，"ubyte"表示这个文件中的数据类型是无符号字节。

