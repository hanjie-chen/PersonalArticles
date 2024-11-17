import numpy as np
import gzip

def load_mnist(images_path, labels_path):
    """
    load the mnist database
    """
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8, offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(
            imgpath.read(), dtype=np.uint8, offset=16).reshape(len(labels), 784)

    return images, labels

def Data_Normalization(Input):
    """
    normalize the Data, use the max-min scaleing
    """
    Normal_Input = (Input - Input.min()) / (Input.max() - Input.min())
    return Normal_Input

def Generate_Data():
    # load the database
    train_images_path = 'mnist_database/train-images-idx3-ubyte.gz'
    train_labels_path = 'mnist_database/train-labels-idx1-ubyte.gz'
    test_images_path = 'mnist_database/t10k-images-idx3-ubyte.gz'
    test_labels_path = 'mnist_database/t10k-labels-idx1-ubyte.gz'
    # train_images->(60000, 784) || train_labels->(60000, 1)
    train_images, train_labels = load_mnist(train_images_path, train_labels_path)
    # test_images->(10000, 784) || test_labels->(10000, 1)
    test_images, test_labels = load_mnist(test_images_path, test_labels_path)
    # normalized the train data
    train_input = Data_Normalization(train_images)
    test_input = Data_Normalization(test_images)
    # one-hot the labels data
    train_target = np.eye(10)[train_labels]
    test_target = np.eye(10)[test_labels]

    return (train_input, train_target), (test_input, test_target)

class Neuro_Network():
    """
    3 layer neural network
    """
    def __init__(self, layers) -> None:
        self.Network_Params = {}
        # init weight | normal distribution
        self.Network_Params['Weight1'] = np.random.randn(layers[0], layers[1]) * 0.1
        self.Network_Params['Weight2'] = np.random.randn(layers[1], layers[2]) * 0.1
        # init bias
        self.Network_Params['Bias1'] = np.zeros(layers[1])
        self.Network_Params['Bias2'] = np.zeros(layers[2])
        # init learning rate
        self.Network_Params['learning_rate'] = 0.1
                         
        self.loss = []
        
    def ReLU(self):
        pass

    def Sigmod(self):
        pass

    def Activate_Function(self):
        """
        activate function : use ReLU function
        """
        pass

    def Loss_Function(self):
        """
        use the loss function
        """
        pass
    
    def SDG(self):
        """
        stochastic gradient descent
        """
        pass

    def Mini_Batch(self, batch_size, Train_Input, Train_Target):
        """
        realize the mini-batch
        """
        # 随机打乱 训练数据&标签
        random_permutation = np.random.permutation(len(Train_Input))
        Train_Input = Train_Input[random_permutation]
        Train_Target = Train_Target[random_permutation]

        # 将数据集划分为完整的batch_size的mini-batch
        full_batches = len(Train_Input) // batch_size
        batch_input = np.array_split(Train_Input[:full_batches*batch_size], full_batches)
        batch_target = np.array_split(Train_Target[:full_batches*batch_size], full_batches)

        # 将剩余的数据放入最后一个 mini-batch 中
        if len(Train_Input) % batch_size != 0:
            batch_input.append(Train_Input[full_batches*batch_size:])
            batch_target.append(Train_Target[full_batches*batch_size:])

        # 返回 mini-batch
        return batch_input, batch_target

    
    def Forward_Propagation(self, Mini_Input):
        pass
    
    def Backward_Propagation(self):
        pass
    
    def Train_Network(self, *Mnist_Data, epoch_turn, batch_size):
        Train_Input, Train_Target, Test_Input, Test_Target = Mnist_Data
        # generate mini-batch
        Batch_Input, Batch_Target = self.Mini_Batch(batch_size, Train_Input, Train_Target)
        for i in range(epoch_turn):
            for j in range(len(Batch_Input)):
                # extra the mini batch
                Mini_Input, Mini_Target = Batch_Input[j], Batch_Target[j]
                real_batch_size = Mini_Input.shape[0]
            
                self.Forward_Propagation(Mini_Input)
            pass

        pass

if __name__ == "__main__":
    # 超参数设置
    epoch_turn = 100
    batch_size = 64
    # generate data
    (Train_Input, Train_Target), (Test_Input, Test_Target) = Generate_Data()
    Mnist_Data = [Train_Input, Train_Target, Test_Input, Test_Target]
    # start training the network
    network = Neuro_Network([728, 200, 10])
    print("Start training !")
    network.Train_Network(*Mnist_Data, epoch_turn=epoch_turn, batch_size=batch_size)
    