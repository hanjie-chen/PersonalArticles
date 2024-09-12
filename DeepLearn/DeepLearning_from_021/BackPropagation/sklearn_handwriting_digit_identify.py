# 导入搜写数据集
from sklearn.datasets import load_digits
import numpy as np
import os
import matplotlib.pyplot as plt
# use one-hot model
from sklearn.preprocessing import LabelBinarizer
# 拆分数据 训练集 数据集
from sklearn.model_selection import train_test_split


def activate_function(x):
    """
    use the sigmod function
    """
    return 1 / (1 + np.exp(-x))

def drivative_activate_function(function_result):
    """
    use the special of the sigmod
    f'(x) = f(x) * (1 - f(x))
    """
    return function_result * (1 - function_result)

def Initial_Weight(row, col):
    """
    it will generate the size of row * col matrix which the value between (-1, 1)
    the value will follow the uniform distribution
    """
    return ((np.random.random([row, col]) * 2) - 1)

def Initial_Bias(nuero_count):
    """
    use zero to initialize the bias
    """
    return np.zeros([nuero_count])


class NueroNetwork():
    # 初始化网络 定义网络结构
    # layers是一个数组 代表了网络每一个层的神经元个数 这个网络有3层
    # if layers = [64, 100, 10] -> 输入层64个神经元 中间层100个 输出层10个
    def __init__(self, layers) -> None:
        if os.path.exists("model/model.npy"):
          # 如果存在模型则加载
          print("Find the model file, trying to load the model !")
          load_model = np.load("model/model.npy", allow_pickle=True).item()
          self.Weight1 = load_model["Weight1"]
          self.Weight2 = load_model["Weight2"]
          self.Bias1 = load_model["Bias1"]
          self.Bias2 = load_model["Bias2"]
          self.learning_rate = load_model["learning_rate"]
          print("load the model successfully !")
        else:
          # 初始化权重
          self.Weight1 = Initial_Weight(layers[0], layers[1])
          self.Weight2 = Initial_Weight(layers[1], layers[2])
          # 初始化偏置值
          self.Bias1 = Initial_Bias(layers[1])
          self.Bias2 = Initial_Bias(layers[2])
          #  初始化学习率
          self.learning_rate = 0.1
        # 损失函数值列表
        self.loss = []
        # 识别精度表
        self.accuracy = []
        # 学习率变化
        self.learning_rate_change = []
    
    def Learning_Rate_exp_decay(self, current_trun):
        """
        指数衰减学习率
        """
        # 超参数 下降率
        decayed_rate = 0.99
        self.learning_rate = self.learning_rate * ( decayed_rate ** (current_trun / 100) )
        self.learning_rate_change.append(self.learning_rate)

    def Forward_Propagation(self, Input):
        # 前向传播计算
        # 这里使用了numpy broadcast 所以才能让维度不一致Bias1和矩阵相乘的结果相加
        # 中间层Y矩阵
        Y = activate_function(np.dot(Input, self.Weight1) + self.Bias1)
        # 结果Output矩阵
        Output = activate_function(np.dot(Y, self.Weight2) + self.Bias2)

        return Y, Output
    
    def Backward_Propagation(self, Input, Target, Y, Output, batch_size):
        # 计算学习信号
        learning_signal_2 = (Target - Output) * drivative_activate_function(Output)
        learning_signal_1 = learning_signal_2.dot(self.Weight2.T) * drivative_activate_function(Y)
        # 计算修改权重 不理解为什么需要求样本平均值
        self.Weight2 += self.learning_rate * Y.T.dot(learning_signal_2) / batch_size
        self.Weight1 += self.learning_rate * Input.T.dot(learning_signal_1) / batch_size
        # 计算偏置值权重
        self.Bias2 += self.learning_rate * np.mean(learning_signal_2, axis=0)
        self.Bias1 += self.learning_rate * np.mean(learning_signal_1, axis=0)

    def Record_Model_Capability(self, i, Input_Test, Target_Test):
        _, Test_Output = self.Forward_Propagation(Input_Test)
        # 取得最大值所在的index
        Predictions = np.argmax(Test_Output, axis=1)
        current_accuracy = np.mean(np.equal(Predictions, Target_Test))
        # 为什么需要 /2 不理解
        current_loss = np.mean(np.square(Target_Test - Predictions) / 2)
        self.accuracy.append(current_accuracy)
        self.loss.append(current_loss)
        # 每隔50次打印一次现在的精度
        if i % 50 == 0:
            print("epoch_trun: {:<6d} |  accuracy: {:.3f}  |  loss: {:.3f}  |  learning_rate: {: .6f}".format
                  (i, current_accuracy, current_loss, self.learning_rate))
            
    def Save_Model(self):
        print("Training Done. Try to save the model")
        # save the model parameter, load the parameter next time
        Model = {
            "Weight1" : self.Weight1,
            "Weight2" : self.Weight2,
            "Bias1"   : self.Bias1,
            "Bias2"   : self.Bias2,
            "learning_rate" : self.learning_rate
        }
        np.save("model/model.npy", Model)
        print("Save the model successuflly !")

    def Mini_Batch(self, Input_Train, Input_Target, batch_size):
        # 随机打算 训练数据和标签
        random_permutation = np.random.permutation(len(Input_Train))
        Input_Train = Input_Train[random_permutation]
        Input_Target = Input_Target[random_permutation]

        # 将数据集划分为完整的batch_size的mini-batch
        full_batches = len(Input_Train) // batch_size
        batch_input = np.array_split(Input_Train[:full_batches*batch_size], full_batches)
        batch_target = np.array_split(Input_Target[:full_batches*batch_size], full_batches)

        # 将剩余的数据放入最后一个 mini-batch 中
        if len(Input_Train) % batch_size != 0:
            batch_input.append(Input_Train[full_batches*batch_size:])
            batch_target.append(Input_Target[full_batches*batch_size:])

        # 返回 mini-batch
        return batch_input, batch_target

    def Train(self, *Data, batch_size, epoch_turn):
        # set data
        Input_Train, Input_Test, Target_Train, Target_Test = Data
        # set mini-batch
        batch_input, batch_target = self.Mini_Batch(Input_Train, Target_Train, batch_size)
        # train
        for i in range(1, epoch_turn + 1):
            for j in range(len(batch_input)):
                # 设置每次迭代的迷你批次
                Mini_Input, Mini_Target = batch_input[j], batch_target[j]
                batch_size = batch_input[j].shape[0]
                # Forward Propagation
                Mini_Y, Mini_Output = self.Forward_Propagation(Mini_Input)
                # Backward Propagation
                self.Backward_Propagation(Mini_Input, Mini_Target, Mini_Y, Mini_Output, batch_size)
            # 每次epoch_turn之后记录一次模型准确率
            self.Record_Model_Capability(i, Input_Test, Target_Test)
            # 动态调整学习率
            if i % 10 == 0:
                self.Learning_Rate_exp_decay(i)
        # save the model
        self.Save_Model()
        

def Data_Normalization(Input):
    """
    normalize the data, help the neuro network learn the data fast and perfect
    use the max-min sacling: Input = (Input - input_min) / (input_max - input_min)
    """
    Normal_Input = (Input - Input.min()) / (Input.max() - Input.min())

    return Normal_Input

def Draw_Picture(loss, accuracy, learning_rate):
    """
    save the loss and accuracy picture in local
    """
    plt.figure()
    plt.plot(range(1, len(loss) + 1), loss)
    plt.xlabel("epoch_trun")
    plt.ylabel("loss")
    plt.savefig("loss.png")

    plt.figure()
    plt.plot(range(1, len(accuracy) + 1), accuracy)
    plt.xlabel("epoch_turn")
    plt.ylabel("accuracy")
    plt.savefig("model/accuracy.png")

    plt.figure()
    plt.plot(range(1, len(learning_rate) + 1), learning_rate)
    plt.xlabel("epoch_turn")
    plt.ylabel("learning_rate")
    plt.savefig("model/learning_rate.png")

if __name__ == "__main__":
    # set epoch, batch_size
    epoch_turn = 1000
    batch_size = 50
    # 加载数据 包括图片本身的标签
    digits = load_digits()
    Target = digits.target
    # 归一化数据
    All_Input = Data_Normalization(digits.data)
    # 分割数据 数据集的3/4为训练集 1/4为测试集
    Input_Train, Input_Test, Target_Train, Target_Test = train_test_split(All_Input, Target, test_size=0.25)
    # 将训练数据的标签转为one-hot模式
    Target_Train = LabelBinarizer().fit_transform(Target_Train)
    # 封装成数组
    Data = [Input_Train, Input_Test, Target_Train, Target_Test]
    # 创建三层神经网络
    network = NueroNetwork([64, 100, 10])
    # 开始训练
    print("Start Training:")
    network.Train(*Data, batch_size = batch_size, epoch_turn = epoch_turn)
    # 画图
    Draw_Picture(network.loss, network.accuracy, network.learning_rate_change)
    