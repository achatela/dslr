from describe import Describe
import sys
import matplotlib.pyplot as plt

def main():
    d = Describe()
    numerical_features = d.parse(sys.argv[1])
    print(numerical_features)
    values = d.get_values()
    # plt.plot(values["Std"])

if __name__ == "__main__":
    main()