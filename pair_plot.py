from pandas.plotting import scatter_matrix
import pandas as pd
from describe import Describe
import matplotlib.pyplot as plt
import sys

def truncate_column_names(df, max_length=7):
   df.columns = [col[:max_length] for col in df.columns]
   return df

def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
    except:
        sys.exit("can't open file")
    df = pd.DataFrame(d.num_data)
    df = truncate_column_names(df)
    scatter_matrix(df, alpha = 0.2, figsize = (8, 8), diagonal = 'kde')
    plt.show()


if __name__ == "__main__":
    main()