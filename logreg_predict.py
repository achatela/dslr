import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from describe import Describe

def hypothesis(X, weights):
    Z = np.dot(X, weights)
    return 1 / (1 + np.exp(-Z))

def error_checking():
    if len(sys.argv) != 3:
        sys.exit("The program should take 2 arguments: <dataset_test.csv> <weights.csv>")

def main():
    error_checking()

    d_test = Describe(sys.argv[1])
    X_test = pd.DataFrame(d_test.norm_data)
    X_test = X_test.fillna(0)
    X_test = X_test.drop(["Index", "Arithmancy", "Care of Magical Creatures"], axis=1)

    try:
        weights = pd.read_csv(sys.argv[2])
    except:
        sys.exit('wrong file')
    classes_weights = pd.DataFrame(weights)
    classes = classes_weights.columns

    houses_hypotesis = [hypothesis(X_test, classes_weights[c]) for c in classes]
    indices_predictions = np.argmax(houses_hypotesis, axis=0)
    classes_predictions = np.array([classes[i] for i in indices_predictions])
    final_predictions = pd.DataFrame({"Hogwarts House": classes_predictions})

    final_predictions.to_csv("houses.csv", index_label="Index")

if __name__ == "__main__":
    main()