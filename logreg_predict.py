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
        sys.exit("The program should take 2 arguments: <dataset_test.csv> <weights.csv>")

def main():
    error_checking()

    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    try:
        weights = pd.read_csv(sys.argv[2])
    except:
        sys.exit('wrong file')
    classes_thetas = pd.DataFrame(weights)

    d_test = Describe(sys.argv[1])

    X_test = pd.DataFrame(d_test.norm_data)

    X_test = X_test.fillna(0)
    X_test = X_test.drop(["Index", "Arithmancy", "Care of Magical Creatures"], axis=1)

    houses_hypotesis = [hypothesis(X_test, classes_thetas[house]) for house in houses]
    final_predictions = np.argmax(houses_hypotesis, axis=0)

    f = open("houses.csv", "w")
    f.write("Index,Hogwarts House\n")
    for i in range(len(final_predictions)):
        f.write(f"{i},{houses[final_predictions[i]]}\n")
    f.close()

if __name__ == "__main__":
    main()