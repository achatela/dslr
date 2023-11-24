from describe import Describe
import matplotlib.pyplot as plt
import itertools
import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
    except:
        sys.exit("can't open file")

    normalized_data = d.numerical_data
    for row in normalized_data:
        row.pop("Index")
        for feature in row:
            row[feature] = abs(row[feature] / (d.stats["Max"][feature] - d.stats["Min"][feature]))

    losses = {}
    for row in normalized_data:
        for i, first_feature in enumerate(row):
            for second_feature in itertools.islice(row, i + 1, None):
                if first_feature not in losses:
                    losses[first_feature] = {}
                if second_feature not in losses[first_feature]:
                    losses[first_feature][second_feature] = 0
                losses[first_feature][second_feature] += abs(row[first_feature] - row[second_feature])
    
    min_loss_features = []
    for first_feature in losses:
        for second_feature in losses[first_feature]:
            if not min_loss_features:
                min_loss_features = [first_feature, second_feature]
            elif losses[first_feature][second_feature] < losses[min_loss_features[0]][min_loss_features[1]]:
                min_loss_features = [first_feature, second_feature]
    
    x = []
    y = []
    for row in normalized_data:
        if min_loss_features[0] in row and min_loss_features[1] in row:
            x.append(row[min_loss_features[0]])
            y.append(row[min_loss_features[1]])

    plt.xlabel(min_loss_features[0])
    plt.ylabel(min_loss_features[1])
    plt.scatter(x, y)
    plt.show()  

if __name__ == "__main__":
    main()