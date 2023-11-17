from describe import Describe
import sys
import matplotlib.pyplot as plt

def normalize_data(datas, categories, numerical_features):
    for category in categories:
        for feature in numerical_features:
            datas[category][feature] = (datas[category][feature] - datas['Min'][feature]) / (datas['Max'][feature] - datas['Min'][feature])

def main():
    categories = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"] # list of all the categories that will be described
    d = Describe()
    d.parse(sys.argv[1])
    features = d.get_features()
    values = d.get_values()
    datas = {category: {feature: 0 for feature in numerical_features} for category in categories}
    for features in numerical_features:
        for category in categories:
            datas[category][features] = values[category][features]
    normalize_data(datas, categories, numerical_features)
    for category, features in datas.items():
        x = list(features.keys())
        y = list(features.values())
        plt.scatter(x, y, label=category)

    plt.xlabel('Features')
    plt.ylabel('Values')
    plt.title('Scatter Plot of datas')
    plt.legend()
    plt.show()  

if __name__ == "__main__":
    main()