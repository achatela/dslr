import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from describe import Describe

def hypothesis(X, thetas):
    X = np.array(X)
    thetas = np.array(thetas)
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

    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    weights = pd.read_csv(sys.argv[2])
    classes_thetas = pd.DataFrame(weights)

    with open(sys.argv[1], "r") as file:
        d_test = Describe(file)
    X_test = pd.DataFrame(d_test.num_data)

    X_test = X_test.dropna()
    X_test = X_test.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    X_test = X_test.drop(["Index"], axis=1)

if __name__ == "__main__":
    main()