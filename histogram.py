from describe import Describe
import matplotlib.pyplot as plt
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
    homogeneity = []
    courses = []
    for feature in d.stats["Std"]:
        if feature != "Index":
            homogeneity.append(1 - (d.stats["Std"][feature] / (d.stats["Max"][feature] - d.stats["Min"][feature])))
            courses.append(feature)
    plt.bar(range(len(courses)), homogeneity)
    plt.xticks(range(len(courses)), courses)
    plt.ylabel("Homogeneity")
    plt.show()

if __name__ == "__main__":
    main()