import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from describe import Describe


def main():
    d_train = Describe('dataset_train.csv')
    X_train = pd.DataFrame(d_train.num_data)
    X_train["Hogwarts House"] = [row["Hogwarts House"] for row in d_train.data]
    X_train = X_train.dropna()
    y_train = X_train["Hogwarts House"]
    X_train = X_train.drop(["Index", "Hogwarts House", "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Ancient Runes", "History of Magic", "Transfiguration", "Charms"], axis=1)

    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)

    d_test = Describe('dataset_test.csv')
    X_test = pd.DataFrame(d_test.num_data)
    d_truth = Describe('dataset_truth.csv')
    X_test["Hogwarts House"] = [row["Hogwarts House"] for row in d_truth.data]
    X_test = X_test.dropna()
    y_test = X_test["Hogwarts House"]
    X_test = X_test.drop(["Index", "Hogwarts House", "Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Ancient Runes", "History of Magic", "Transfiguration", "Charms"], axis=1)

    predictions = logistic_regression.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print('Accuracy: ', accuracy)


if __name__ == "__main__":
    main()