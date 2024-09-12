import numpy as np
import gzip
import matplotlib.pyplot as plt

def load_mnist(images_path, labels_path):
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(
            imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 784)

    return images, labels

if __name__ == "__main__":
    train_images_path = 'mnist_database/train-images-idx3-ubyte.gz'
    train_labels_path = 'mnist_database/train-labels-idx1-ubyte.gz'
    test_images_path = 'mnist_database/t10k-images-idx3-ubyte.gz'
    test_labels_path = 'mnist_database/t10k-labels-idx1-ubyte.gz'
    train_images, train_labels = load_mnist(train_images_path, train_labels_path)
    test_images, test_labels = load_mnist(test_images_path, test_labels_path)
    print("训练数据的矩阵 ->",train_images.shape, "训练数据的标签矩阵->",train_labels.shape)
    # 显示第一张训练图片
    # plt.imshow(train_images[0].reshape(28, 28), cmap='gray')
    # plt.show()
    print("the first train label", train_labels[0])
