
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from describe import Describe


def main():
    with open("dataset_train.csv", "r") as file:
        d_train = Describe(file)
    X_train = pd.DataFrame(d_train.num_data)
    X_train = X_train.assign(house=[row["Hogwarts House"] for row in d_train.data]).rename(columns={"house": "Hogwarts House"})
    X_train = X_train.dropna()
    X_train['Hogwarts House'] = LabelEncoder().fit_transform(X_train['Hogwarts House'])
    y_train = X_train['Hogwarts House']

    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)

    with open("dataset_test.csv", "r") as file:
        d_test = Describe(file)
    X_test = pd.DataFrame(d_test.num_data)
    with open("dataset_truth.csv", "r") as file:
        d_truth = Describe(file)
    X_test = X_test.assign(house=[row["Hogwarts House"] for row in d_truth.data]).rename(columns={"house": "Hogwarts House"})
    X_test = X_test.dropna()
    X_test['Hogwarts House'] = LabelEncoder().fit_transform(X_test['Hogwarts House'])
    y_test = X_test['Hogwarts House']

    predictions = logistic_regression.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print('Accuracy: ', accuracy)


if __name__ == "__main__":
    main()