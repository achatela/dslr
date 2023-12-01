import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    pred = pd.read_csv("houses.csv", delimiter=",")
    true = pd.read_csv("dataset_truth.csv", delimiter=",")

    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    y_pred = pred['Hogwarts House']
    y_true = true['Hogwarts House']
    print(accuracy_score(y_true, y_pred))
    print(accuracy_score(y_true, y_pred, normalize=False))