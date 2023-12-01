import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from describe import Describe
import csv


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


def theta_to_csv(classes_thetas):
    with open('weights.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"])
        writer.writerows(zip(*classes_thetas))

def main():
    with open("dataset_train.csv", "r") as file:
        d_train = Describe(file)

    X_train = pd.DataFrame(d_train.norm_data)
    X_train["Hogwarts House"] = LabelEncoder().fit_transform([row["Hogwarts House"] for row in d_train.data])

    X_train = X_train.fillna(0)
    y_train = LabelEncoder().fit_transform(X_train["Hogwarts House"])
    X_train = X_train.drop(["Index", "Hogwarts House", "Arithmancy", "Care of Magical Creatures"], axis=1)

    num_classes = 4
    num_features = X_train.shape[1]
    alpha = 2
    iterations = 1000
    classes_thetas = np.zeros((num_classes, num_features))

    for i in range(num_classes):
        y_bin = np.where(y_train == i, 1, 0)
        classes_thetas[i] = gradient_descent(X_train, y_bin, classes_thetas[i], alpha, iterations)

    theta_to_csv(classes_thetas)

if __name__ == "__main__":
    main()