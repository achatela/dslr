import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from describe import Describe


def hypothesis(X, thetas):
    Z = np.dot(X, thetas)
    return 1 / (1 + np.exp(-Z))

def gradient_descent(X, y, thetas, alpha, iterations):
    m = len(y)
    for _ in range(iterations):
        h = hypothesis(X, thetas)
        gradient = np.dot(X.T, (h - y)) / m
        thetas = thetas - alpha * gradient
    return thetas

def main():
    with open("dataset_train.csv", "r") as file:
        d_train = Describe(file)
    X_train = pd.DataFrame(d_train.num_data)
    X_train["Hogwarts House"] =  LabelEncoder().fit_transform([row["Hogwarts House"] for row in d_train.data])
    X_train = X_train.dropna()
    y_train = X_train["Hogwarts House"]
    # X_train.drop("Hogwarts House", axis=1)
    X_train = X_train.drop(["Index", "Hogwarts House", "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Ancient Runes", "History of Magic", "Transfiguration", "Charms"], axis=1)

    num_classes = 4

    num_features = X_train.shape[1]

    alpha = 0.0001
    iterations = 10000

    classes_thetas = np.zeros((num_classes, num_features))

    for i in range(num_classes):
        y_bin = np.where(y_train == i, 1, 0)
        classes_thetas[i] = gradient_descent(X_train, y_bin, classes_thetas[i], alpha, iterations)
    
    with open("dataset_test.csv", "r") as file:
        d_test = Describe(file)
    X_test = pd.DataFrame(d_test.num_data)
    with open("dataset_truth.csv", "r") as file:
        d_truth = Describe(file)
    X_test["Hogwarts House"] =  LabelEncoder().fit_transform([row["Hogwarts House"] for row in d_truth.data])
    X_test = X_test.dropna()
    y_test = X_test["Hogwarts House"]
    # X_test.drop("Hogwarts House", axis=1)
    X_test = X_test.drop(["Index", "Hogwarts House", "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Ancient Runes", "History of Magic", "Transfiguration", "Charms"], axis=1)

    houses_hypotesis = [hypothesis(X_test, classes_thetas[i]) for i in range(num_classes)]
    final_predictions = np.argmax(houses_hypotesis, axis=0)
    # print(final_predictions)
    accuracy = accuracy_score(y_test, final_predictions)
    print('Accuracy: ', accuracy)


if __name__ == "__main__":
    main()