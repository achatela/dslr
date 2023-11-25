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

    pairs_loss = {}
    for row in d.norm_data:
        for i, first_feature in enumerate(row):
            for second_feature in itertools.islice(row, i + 1, None):
                pair = (first_feature, second_feature)
                if pair not in pairs_loss:
                    pairs_loss[pair] = {"total": 0, "count": 0}
                pairs_loss[pair]["total"] += abs(row[first_feature] - row[second_feature])
                pairs_loss[pair]["count"] += 1
    
    min_avg_loss = float("inf")
    for pair in pairs_loss:
        avg_loss = pairs_loss[pair]["total"] / pairs_loss[pair]["count"]
        if avg_loss < min_avg_loss:
            closest_pair = pair
            min_avg_loss = avg_loss
    
    plt.xlabel(closest_pair[0])
    plt.ylabel(closest_pair[1])
    
    x = []
    y = []
    for row in d.norm_data:
        if closest_pair[0] in row and closest_pair[1] in row:
            x.append(row[closest_pair[0]])
            y.append(row[closest_pair[1]])
    
    plt.scatter(x, y)
    plt.show()  

if __name__ == "__main__":
    main()