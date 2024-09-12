from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

def Data_Normalization(Input):
    """
    normalize the data, help the neuro network learn the data fast and perfect
    use the max-min sacling: Input = (Input - input_min) / (input_max - input_min)
    """
    Normal_Input = (Input - Input.min()) / (Input.max() - Input.min())

    return Normal_Input


digits = load_digits()

Input_Data = Data_Normalization(digits.data)
Target_Data = digits.target

# 分割数据 数据集的3/4为训练集 1/4为测试集
Input_Train, Input_Test, Target_Train, Target_Test = train_test_split(Input_Data, Target_Data, test_size=0.25)

# (100, 20) 表示2个隐藏层 神经元数量分别是100， 20
# max_iter 表示训练次数
mlp = MLPClassifier(hidden_layer_sizes=(100, 20), max_iter=500)
# 传入训练数据
mlp.fit(Input_Train, Target_Train)
# 使用测试数据测试模型准确率
predictions = mlp.predict(Input_Test)
print(classification_report(Target_Test, predictions))

