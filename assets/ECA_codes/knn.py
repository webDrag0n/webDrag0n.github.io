import matplotlib.pyplot as plt
import numpy as np

A = 0
B = 0
k = 5

a_plot = [[],[]]
b_plot = [[],[]]

dataSet = [[1.0,2.0], [1.5, 3.0], [1.1, 0.1], [1.2,1.1], [0.1,1.4], [0.3,2.5]]
labels = ['A','A','B','B','B','A']

input = [1, 1.3]

plt.figure(figsize=(10,10))

def calculate_distant(input, dataSet, label):
    dist = []
    for i in range(len(dataSet)):
        x_square_dist = (dataSet[i][0] - input[0]) ** 2
        y_square_dist = (dataSet[i][1] - input[1]) ** 2
        dist.append(x_square_dist + y_square_dist)

    return np.array(dist)

dist = calculate_distant(input, dataSet, labels)

k_dist_sorted_index = dist.argsort()[:k]

for i in k_dist_sorted_index:
    if labels[i] == 'A':
        A += 1
        a_plot[0].append(dataSet[i][0])
        a_plot[1].append(dataSet[i][1])
    elif labels[i] == 'B':
        B += 1
        b_plot[0].append(dataSet[i][0])
        b_plot[1].append(dataSet[i][1])

if A > B:
    plt.scatter(input[0], input[1],s=100, c='b', marker='v', alpha=0.5)
else:
    plt.scatter(input[0], input[1],s=100, c='r', marker='v', alpha=0.5)

marker_a = None
marker_a = plt.scatter(a_plot[0], a_plot[1], s=100, c='b', alpha=0.5)
marker_b = None
marker_b = plt.scatter(b_plot[0], b_plot[1], s=100, c='r', alpha=0.5)

plt.legend([marker_a, marker_b], ["A", "B"])

plt.show()