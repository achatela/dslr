import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

def main():
    try:
        truth2 = pd.read_csv("dataset_truth.csv")
        predictions2 = pd.read_csv("houses.csv")
        truth = pd.DataFrame(truth2)
        predictions = pd.DataFrame(predictions2)
    except:
        print("Cannot open file\nYou must be in the root to execute the script")
        exit()

    plt.xlabel("House")
    plt.ylabel("Frequency")

    X_truth = []
    X_predictions = []
    
    for row in truth.iterrows():
        X_truth.append(row[1][1])
    for row in predictions.iterrows():
        X_predictions.append(row[1][1])
    
    plt.hist(X_truth, bins=4, alpha=0.8)
    plt.hist(X_predictions, bins=4, alpha=0.8)
    plt.show()

main()
    