import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from describe import Describe
import csv
import sys

activation_function = "sigmoid"

def hypothesis(X, weights):
    Z = np.dot(X, weights)
    if activation_function == "sigmoid":
        return 1 / (1 + np.exp(-Z))
    else:
        return ((2 / (1 + np.exp(-2*Z)) - 1))

def batch_gradient_descent(X, y, m, weights, learning_rate, epochs, batch_size):
    for _ in range(epochs):
        indices = np.random.choice(m, batch_size)
        X_batch = X.iloc[indices]
        y_batch = y[indices]
        h = hypothesis(X_batch, weights)
        gradient = np.dot(X_batch.T, h - y_batch) / m
        weights = weights - learning_rate * gradient
    return weights

def stochastic_gradient_descent(X, y, m, weights, learning_rate, epochs, batch_size):
    for _ in range(epochs):
        indices = np.random.permutation(m)
        X = X.iloc[indices]
        y = y[indices]
        for i in range(0, m, batch_size):
            X_batch = X.iloc[i:i+batch_size]
            y_batch = y[i:i+batch_size]
            h = hypothesis(X_batch, weights)
            gradient = np.dot(X_batch.T, h - y_batch) / m
            weights = weights - learning_rate * gradient
    return weights

def gradient_descent(X, y, m, weights, learning_rate, epochs):
    for _ in range(epochs):
        h = hypothesis(X, weights)
        gradient = np.dot(X.T, h - y) / m
        weights = weights - learning_rate * gradient
    return weights

def main():
    global activation_function
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        sys.exit('wrong number of arguments')
    is_stochastic = False
    is_batch = False
    if len(sys.argv) == 3:
        if sys.argv[2] == 'stochastic':
            is_stochastic = True
        elif sys.argv[2] == 'batch':
            is_batch = True
        elif sys.argv[2] == 'tanh':
            activation_function = "hyperbolic_tangent"
        else:
            sys.exit('wrong algorithm')

    d_train = Describe(sys.argv[1])

    X_train = pd.DataFrame(d_train.norm_data)
    X_train = X_train.fillna(0)
    X_train = X_train.drop(["Index", "Arithmancy", "Care of Magical Creatures"], axis=1)
    num_samples, num_features = X_train.shape

    y_train = np.array([row["Hogwarts House"] for row in d_train.data])
    classes = np.unique(y_train)
    classes_weights = pd.DataFrame(columns=classes)
    
    learning_rate = 2
    epochs = 1000
    batch_size = num_samples // 10

    for c in classes:
        classes_weights[c] = np.zeros(num_features)
        y_bin = np.where(y_train == c, 1, 0)
        if is_stochastic:
            classes_weights[c] = stochastic_gradient_descent(X_train, y_bin, num_samples, classes_weights[c], learning_rate, epochs, batch_size)
        elif is_batch:
            classes_weights[c] = batch_gradient_descent(X_train, y_bin, num_samples, classes_weights[c], learning_rate, epochs, batch_size)
        else:
            classes_weights[c] = gradient_descent(X_train, y_bin, num_samples, classes_weights[c], learning_rate, epochs)

    classes_weights.to_csv('weights.csv', index=False)

if __name__ == "__main__":
    main()