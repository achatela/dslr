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

def theta_to_csv(classes_thetas, i, j):
    f = open("weights.csv", "w")
    f.write("Gryffindor,Hufflepuff,Ravenclaw,Slytherin\n")
    while j < len(classes_thetas[i]):
        while i < len(classes_thetas):
            f.write(f"{classes_thetas[i][j]}")
            i += 1
            if i < len(classes_thetas):
                f.write(",")
        i = 0
        f.write("\n")
        j += 1
    f.close()

def main():
    with open("dataset_train.csv", "r") as file:
        d_train = Describe(file)

    X_train = pd.DataFrame(d_train.num_data)
    X_train["Hogwarts House"] = LabelEncoder().fit_transform([row["Hogwarts House"] for row in d_train.data])
    X_data = pd.DataFrame(d_train.data)

    for column in X_data.columns:
        if column not in X_train.columns:
            X_train[column] = LabelEncoder().fit_transform(X_data[column])

    X_train = X_train.dropna()
    X_train = X_train.apply(lambda x: (x - x.min()) / (x.max() - x.min())) # Normalize the datas
    y_train = LabelEncoder().fit_transform(X_train["Hogwarts House"])
    X_train = X_train.drop(["Index", "Hogwarts House", "Best Hand", "First Name", "Last Name", "Birthday"], axis=1)

    num_classes = 4
    num_features = X_train.shape[1]
    alpha = 0.2
    iterations = 1000
    classes_thetas = np.zeros((num_classes, num_features))

    for i in range(num_classes):
        y_bin = np.where(y_train == i, 1, 0)
        classes_thetas[i] = gradient_descent(X_train, y_bin, classes_thetas[i], alpha, iterations)

    theta_to_csv(classes_thetas, 0, 0)

if __name__ == "__main__":
    main()