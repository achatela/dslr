import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from describe import Describe

def hypothesis(X, thetas):
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

    X_test = pd.DataFrame(d_test.norm_data)

    X_test = X_test.fillna(0)
    X_test = X_test.drop(["Index"], axis=1)

    houses_hypotesis = [hypothesis(X_test, classes_thetas[house]) for house in houses]
    final_predictions = np.argmax(houses_hypotesis, axis=0)

    f = open("houses.csv", "w")
    f.write("Index,Hogwarts House\n")
    for i in range(len(final_predictions)):
        f.write(f"{i},{houses[final_predictions[i]]}\n")
    f.close()

if __name__ == "__main__":
    main()