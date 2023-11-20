from describe import Describe
import sys
import matplotlib.pyplot as plt

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
    for stat in d.stats:
            
    plt.legend()
    plt.show()  

if __name__ == "__main__":
    main()