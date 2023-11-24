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
            row[feature] = (row[feature] - d.stats["Min"][feature]) / (d.stats["Max"][feature] - d.stats["Min"][feature])

    pairs_loss = {}
    for row in normalized_data:
        for i, first_feature in enumerate(row):
            for second_feature in itertools.islice(row, i + 1, None):
                if first_feature not in pairs_loss:
                    pairs_loss[first_feature] = {}
                if second_feature not in pairs_loss[first_feature]:
                    pairs_loss[first_feature][second_feature] = {"total": 0, "count": 0}
                pairs_loss[first_feature][second_feature]["total"] += abs(row[first_feature] - row[second_feature])
                pairs_loss[first_feature][second_feature]["count"] += 1
    
    closest_pair = ()
    min_avg_loss = float("inf")
    for first_feature in pairs_loss:
        for second_feature in pairs_loss[first_feature]:
            avg_loss = pairs_loss[first_feature][second_feature]["total"] / pairs_loss[first_feature][second_feature]["count"]
            if avg_loss < min_avg_loss:
                closest_pair = (first_feature, second_feature)
                min_avg_loss = avg_loss
    
    plt.xlabel(closest_pair[0])
    plt.ylabel(closest_pair[1])
    
    x = []
    y = []
    for row in normalized_data:
        if closest_pair[0] in row and closest_pair[1] in row:
            x.append(row[closest_pair[0]])
            y.append(row[closest_pair[1]])
    
    plt.scatter(x, y)
    plt.show()  

if __name__ == "__main__":
    main()