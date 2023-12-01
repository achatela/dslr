# from pandas.plotting import scatter_matrix
import seaborn as sns
import pandas as pd
from describe import Describe
import matplotlib.pyplot as plt
import sys


def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    d = Describe(sys.argv[1])
    df = pd.DataFrame(d.num_data)
    df.columns = [col.split()[0] for col in df.columns]
    df = df.assign(house=[row["Hogwarts House"] for row in d.data]).rename(columns={"house": "Hogwarts House"})
    sns.pairplot(df, height=0.8, hue="Hogwarts House")
    plt.show()

if __name__ == "__main__":
    main()