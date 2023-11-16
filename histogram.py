from describe import Describe
import sys

def main():
    d = Describe()
    d.parse(sys.argv[1])
    # d.describe()
    values = d.get_values()
    print(values)

if __name__ == "__main__":
    main()