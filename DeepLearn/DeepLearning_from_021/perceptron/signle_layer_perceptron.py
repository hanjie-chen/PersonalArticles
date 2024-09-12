import numpy as np
# 定义学习率
learning_rate = 1
target = 1
# 定义输出和初始随机权值
x0, x1, x2 = 1, 0, -1
w0, w1, w2 = -5, 0, 0
input = np.array([x0, x1, x2])
weight = np.array([w0, w1, w2])
# 权值调整公式
def adjust_weight(learning_rate, target, output, input):
    return learning_rate * (target - output) * input

def activate_function(x):
    # 使用sign函数
    if x > 0 :
        return 1
    elif x == 0:
        return 0
    elif x < 0:
        return -1

for i in range(100):
    print("iterative ",i," weight is :", weight)
    # 计算输出
    output = activate_function(np.dot(input, weight.T))
    # 如果输出和目标不相等 那么调整权值
    if output != target:
        weight += adjust_weight(learning_rate, target, output, input)
    else:
        print("train done.")
        break