
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import HistGradientBoostingClassifier

from sklearn.metrics import accuracy_score
from describe import Describe
import sys


# Assume df is your DataFrame and it has columns 'house', 'grade1', 'grade2', 'grade3', ...

# Convert the 'house' column into numerical values



def main():
    with open("dataset_train.csv", "r") as file:
        d_train = Describe(file)
   
    df_train = pd.DataFrame(d_train.num_data)
    df_train = df_train.assign(house=[row["Hogwarts House"] for row in d_train.data]).rename(columns={"house": "Hogwarts House"})
    df_train = df_train.dropna()

    # df_train['Hogwarts House'] = LabelEncoder().fit_transform(df_train['Hogwarts House'])
    # X = df_train.drop('Hogwarts House', axis=1) # Features
    # y = df_train['Hogwarts House'] # Target variable

    # X_train, X_test, y_train, y_test = train_test_split(X, y)

    df_train['Hogwarts House'] = LabelEncoder().fit_transform(df_train['Hogwarts House'])
    y_train = df_train['Hogwarts House']
    print(y_train)
    # df_train.drop('Hogwarts House')
    X_train = df_train
    # y_train = LabelEncoder().fit_transform(pd.DataFrame([{"Hogwarts House": row["Hogwarts House"] for row in d_train.data}]))

    print(X_train, y_train)

    logistic_regression = LogisticRegression()
    logistic_regression.fit(X_train, y_train)

    # clf = HistGradientBoostingClassifier()
    # clf.fit(X_train, y_train)

    with open("dataset_test.csv", "r") as file:
        d_test = Describe(file)
    df_test = pd.DataFrame(d_test.num_data)
    X_test = df_test.assign(house=[row["Hogwarts House"] for row in d_train.data]).rename(columns={"house": "Hogwarts House"})

    predictions = logistic_regression.predict(X_test)

    with open("dataset_truth.csv", "r") as file:
        d_truth = Describe(file)
    y_test = pd.DataFrame(d_truth.data)

    accuracy = accuracy_score(y_test, predictions)
    print('Accuracy: ', accuracy)


if __name__ == "__main__":
    main()