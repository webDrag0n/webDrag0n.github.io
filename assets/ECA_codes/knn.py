import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(10,10))

def calculate_distant(input, dataSet, label):
    dist = []
    for i in range(len(dataSet)):
        x_square_dist = (dataSet[i][0] - input[0]) ** 2
        y_square_dist = (dataSet[i][1] - input[1]) ** 2
        dist.append(x_square_dist + y_square_dist)

    return np.array(dist)

dataSet = [[1.0,2.0], [1.5, 3.0], [1.1, 0.1], [1.2,1.1], [0.1,1.4], [0.3,2.5]]
labels = ['A','A','B','B','B','A']

input = [1, 1.3]
dist = calculate_distant(input, dataSet, labels)
Ad = 0
Bd = 0
k = 6

k_dist_sorted_index = dist.argsort()[:k]

for i in k_dist_sorted_index:
    if labels[i] == 'A':
        Ad += dist[i]
        plt.scatter(dataSet[i][0], dataSet[i][1],s=200, c='b', alpha=0.5)
    elif labels[i] == 'B':
        Bd += dist[i]
        plt.scatter(dataSet[i][0], dataSet[i][1],s=200, c='r', alpha=0.5)

if Ad < Bd:
    plt.scatter(input[0], input[1],s=200, c='b', marker='v', alpha=0.5)
else:
    plt.scatter(input[0], input[1],s=200, c='r', marker='v', alpha=0.5)

plt.show()