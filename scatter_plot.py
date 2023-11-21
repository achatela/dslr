from describe import Describe
import distinctipy
import matplotlib.pyplot as plt
import sys

def normalize_data(datas, categories, numerical_features):
    for category in categories:
        for feature in numerical_features:
            datas[category][feature] = (datas[category][feature] - datas['Min'][feature]) / (datas['Max'][feature] - datas['Min'][feature])

def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
    except:
        sys.exit("can't open file")
    x = []
    y_dict = {}
    for stat in d.stats:
        x.append(stat)
        for feature in d.stats[stat]:
            if feature not in y_dict:
                y_dict[feature] = []
            y_dict[feature].append(d.stats[stat][feature])
    plt.xticks(range(len(x)), x)
    colors = distinctipy.get_colors(len(y_dict))
    for i, feature in enumerate(y_dict):
        plt.scatter(x, y_dict[feature], color=colors[i], label=feature)
    plt.legend()
    plt.show()  

if __name__ == "__main__":
    main()