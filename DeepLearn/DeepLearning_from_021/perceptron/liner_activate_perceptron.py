import numpy as np
import matplotlib.pyplot as plt
# 分类4个坐标 (3, 3) (4, 3) (1, 1) (2, 1) 前2个为1 后2个为-1
Input = np.array([
    [1, 3, 3],
    [1, 4, 3],
    [1, 1, 1],
    [1, 2, 1]
])
Target = np.array([
    [1],
    [1],
    [-1],
    [-1]
])
Weight = np.random.random([3, 1])
# 记录目标和删除的误差
loss = []
# 学习率0.1
learning_rate = 0.1

def adjust_weight(lr, Target, Output, Input):
    delta_E = Target - Output
    # 使用平方差计算损失函数
    loss.append((np.sum(np.square(delta_E)))/2)
    # 使用权值调整公式计算出4个输出需要调整的大小取其和的算术平均值
    return ((Input.T).dot(lr * (delta_E))) / Input.shape[0]


for i in range(1000):
    print("iterative ", i, "time's weight : ", Weight)
    # 计算输出
    Output = np.dot(Input, Weight)
    Weight += adjust_weight(learning_rate, Target, Output, Input)


# 画2张图
fig, (ax1, ax2) = plt.subplots(1, 2)
# 样本坐标
x1 = [3, 4]
y1 = [3, 3]
x2 = [1, 2]
y2 = [1, 1]

xdata = [0, 5]
k = -Weight[1] / Weight[2]
d = -Weight[0] / Weight[2]

ax1.plot(xdata, xdata*k + d, 'r')
ax1.scatter(x1, y1, c='b')
ax1.scatter(x2, y2, c='y')
ax1.set_title('result')

ax2.plot(range(len(loss)), loss)
ax2.set_xlabel('iteration')
ax2.set_ylabel('loss')
ax2.set_title("loss change")


# 调整子图之间的间距
plt.subplots_adjust(wspace=0.5)

plt.show()