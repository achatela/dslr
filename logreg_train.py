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
    f.write("Gryffindor, Hufflepuff, Ravenclaw, Slytherin\n")
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
    # Gryffindor 0, Hufflepuff 1, Ravenclaw 2, Slytherin 3
    X_train["Hogwarts House"] = LabelEncoder().fit_transform([row["Hogwarts House"] for row in d_train.data])
    X_data = pd.DataFrame(d_train.data)

    for column in X_data.columns:
        if column not in X_train.columns:
            X_train[column] = LabelEncoder().fit_transform(X_data[column])

    X_train = X_train.dropna()
    X_train = X_train.apply(lambda x: (x - x.min()) / (x.max() - x.min())) # Normalize the datas
    y_train = LabelEncoder().fit_transform(X_train["Hogwarts House"])
    X_train = X_train.drop(["Index", "Hogwarts House"], axis=1)

    num_classes = 4
    num_features = X_train.shape[1]
    alpha = 0.1
    iterations = 1000
    classes_thetas = np.zeros((num_classes, num_features))

    for i in range(num_classes):
        y_bin = np.where(y_train == i, 1, 0)
        classes_thetas[i] = gradient_descent(X_train, y_bin, classes_thetas[i], alpha, iterations)

    theta_to_csv(classes_thetas, 0, 0)
    # with open("dataset_test.csv", "r") as file:
    #     d_test = Describe(file)
    # X_test = pd.DataFrame(d_test.num_data)
    # with open("dataset_truth.csv", "r") as file:
    #     d_truth = Describe(file)
    # X_test["Hogwarts House"] = LabelEncoder().fit_transform([row["Hogwarts House"] for row in d_truth.data])
    # X_data = pd.DataFrame(d_test.data)
    # for column in X_data.columns:
    #     if column not in X_test.columns:
    #         X_test[column] = LabelEncoder().fit_transform(X_data[column])
    # X_test = X_test.dropna()
    # X_test = X_test.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    # y_test = LabelEncoder().fit_transform(X_test["Hogwarts House"])
    # X_test = X_test.drop(["Index", "Hogwarts House"], axis=1)

    # houses_hypotesis = [hypothesis(X_test, classes_thetas[i]) for i in range(num_classes)]
    # final_predictions = np.argmax(houses_hypotesis, axis=0)
    # accuracy = accuracy_score(y_test, final_predictions)
    # print("Accuracy:", accuracy)


if __name__ == "__main__":
    main()