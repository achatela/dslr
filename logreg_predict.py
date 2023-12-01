import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from describe import Describe

def hypothesis(X, thetas):
    # indexes = np.where(X == 3)[0]
    # for index in indexes:
        # X.remove(index)
        # thetas.pop(index)
    Z = np.dot(X, thetas)
    return 1 / (1 + np.exp(-Z))

def error_checking():
    if len(sys.argv) != 3:
        print("The program should take 2 arguments: <dataset_test.csv> <weights.csv>")
        return False
    
    try:
        if not open(sys.argv[1]) or not open(sys.argv[2]):
            pass
    except:
        print("One file is missing or cannot be opened!")
        return False
    


def main():
    if error_checking():
        exit()

    # features = ["Arithmancy","Astronomy","Herbology","Defense Against the Dark Arts","Divination","Muggle Studies","Ancient Runes","History of Magic","Transfiguration","Potions","Care of Magical Creatures","Charms","Flying"]
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    weights = pd.read_csv(sys.argv[2])
    classes_thetas = pd.DataFrame(weights)
    thetas_array = {}

    for house in houses:
        thetas_array[house] = np.array(classes_thetas[house])

    with open(sys.argv[1], "r") as file:
        d_test = Describe(file)
    X_test = pd.DataFrame(d_test.num_data)

    X_test = X_test.fillna(0)
    X_test = X_test.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    X_test = X_test.drop(["Index"], axis=1)

    test_set = []
    j = 0
    for row in X_test.iterrows():
        test_set.append([])
        for i in range(len(row[1])):
            test_set[j].append(row[1][i])
        j += 1

    f = open("houses.csv", "w")
    f.write("Index,Hogwarts House\n")
    for i in range(len(test_set)):
        # houses_hypotesis = [hypothesis(X_test, classes_thetas[i]) for i in range(num_classes)]
        tmp = [hypothesis(np.array(test_set[i]), classes_thetas[house]) for house in houses]
        result = tmp.index(max(tmp))
        f.write(f"{i},{houses[result]}\n")

if __name__ == "__main__":
    main()