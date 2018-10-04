import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# import load_iris function from datasets module
from sklearn.datasets import load_iris
# load iris data set
iris = load_iris()
dataSet = iris.data
labels = iris.target

# according to iris dataset, the structure of input is [SepalLength, SepalWidth, PetalLength, PetalWidth]
# more details please refer to https://www.kaggle.com/uciml/iris
input = [3, 5, 4, 2]

# dataSet = [(1.0,2.0), (1.5, 3.0), (1.1, 0.1), (1.2,1.1), (0.1,1.4), (0.3,2.5)]
# labels = ['A','A','B','B','B','A']

# input = [1, 1.3]

# set the k value
# k = len(dataSet)
k = 1

# store different labels so they could be represented as index number
labelsTypes = []

# fill the labelsTypes list with different labels
for label in labels:
    # if the label found in labels is not in labelsTypes
    if not label in labelsTypes:
        # add the label to labelsTypes
        labelsTypes.append(label)

# list used to store the labels votes of the input
labelsVote = [0 for i in range(len(labelsTypes))]

# set up color scheme for the plot graph
# 3 classes -> 3 colors
colors = ['r', 'g', 'b']
# set the size of the matplotlib figure
plt.figure(figsize=(15,15))

def calculate_distance(input, dataSet, label):
    dist = []
    for i in range(len(dataSet)):
        d = 0
        for j in range(len(dataSet[i])):
            d += (dataSet[i][j] - input[j]) ** 2
        dist.append(d)

    return np.array(dist)

# dist is the array storing 150 points' distance
dist = calculate_distance(input, dataSet, labels)

# a sorted index list for 150 data points according to the distance to the input point
# cut the list and keep the first k elements
k_dist_sorted_index = dist.argsort()[:k]

# get the index of first k elements according to k_dist_sorted_index
for i in k_dist_sorted_index:
    # labels[i] is the label stored in index i
    # since labelsTypes and labelsVote are matched pairs(label index is same)
    # the nth element in labelsVote is labeled as labelsTypes[n]
    # therefore labelsVote[i] is the vote of label labelsTypes[n]
    labelsVote[labelsTypes.index(labels[i])] += 1

# find the index of input label in labelsVote
inputLabelIndex = labelsVote.index(max(labelsVote))
# since labelsVote is matched with labelsTypes, the index could be directly used
inputLabel = labelsTypes[inputLabelIndex]


# plot the input point
plt.subplot(221)
plt.scatter(input[0], input[1],s=50, c=colors[inputLabelIndex], marker='v', alpha=0.5)
plt.subplot(222)
plt.scatter(input[1], input[2],s=50, c=colors[inputLabelIndex], marker='v', alpha=0.5)
plt.subplot(223)
plt.scatter(input[2], input[3],s=50, c=colors[inputLabelIndex], marker='v', alpha=0.5)
plt.subplot(224)
plt.scatter(input[3], input[0],s=50, c=colors[inputLabelIndex], marker='v', alpha=0.5)

# plot the data set points
for pointIndex in range(len(dataSet)):
    colorIndex = labelsTypes.index(labels[pointIndex])
    plt.subplot(221)
    marker = plt.scatter(dataSet[pointIndex][0], dataSet[pointIndex][1], s=50, c=colors[colorIndex], alpha=0.5)
    plt.subplot(222)
    marker = plt.scatter(dataSet[pointIndex][1], dataSet[pointIndex][2], s=50, c=colors[colorIndex], alpha=0.5)
    plt.subplot(223)
    marker = plt.scatter(dataSet[pointIndex][2], dataSet[pointIndex][3], s=50, c=colors[colorIndex], alpha=0.5)
    plt.subplot(224)
    marker = plt.scatter(dataSet[pointIndex][3], dataSet[pointIndex][0], s=50, c=colors[colorIndex], alpha=0.5)

plt.show()