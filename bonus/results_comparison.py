import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys

def main():
    if len(sys.argv) != 3:
        sys.exit('wrong number of arguments')
    try:
        expections = pd.read_csv(sys.argv[1])
        predictions = pd.read_csv(sys.argv[2])
    except:
        sys.exit("Cannot open file\nYou must be in the root to execute the script")

    plt.xlabel("House")
    plt.ylabel("Frequency")
    plt.hist(expections['Hogwarts House'], label='expections', bins=4, alpha=0.8)
    plt.hist(predictions['Hogwarts House'], label='predictions', bins=4, alpha=0.8)
    plt.legend()
    plt.show()

main()