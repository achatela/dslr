import csv
import sys
from math import *

class Describe:
    def __init__(self, file):
        try:
            csv_reader = csv.DictReader(file)
        except:
            sys.exit("file is not csv")
        self.data = [] # csv file stored as an array of dicts
        self.numerical_data = []
        for row in csv_reader:
            self.data.append(row)
            numerical_row = {}
            for feature in row:
                if feature == "First Name":
                    continue
                try:
                    numerical_row[feature] = float(row[feature])
                except:
                    pass
            self.numerical_data.append(numerical_row)

    def describe(self):
        values = {}
        values["Count"] = self.get_count_data()
        values["Mean"] = self.get_mean_data(values["Count"])
        values["Std"] = self.get_std_data(values["Count"], values["Mean"])
        values["Min"] = self.get_min_data()
        values["25%"] = self.get_percentile_data(25, values["Count"]) # TODO handle bonuses as input with other value than 25/50/75
        values["50%"] = self.get_percentile_data(50, values["Count"]) # TODO handle bonuses as input 
        values["75%"] = self.get_percentile_data(75, values["Count"]) # TODO handle bonuses as input 
        values["Max"] = self.get_max_data()
        # First, print the header row
        header = "{:<15}".format("")  # Empty cell at the top left corner
        for category in values["Count"].keys():
            header += "{:<15}".format(category)
        print(header)

        # Then, print the rows for each statistic
        for stat in values.keys():
            row = "{:<15}".format(stat)  # Start with the statistic name
            for category in values[stat].keys():
                row += "{:<15.6f}".format(values[stat][category])  # Add each value
            print(row)
        # print(values)
        # column_names = []
        # print("{:<12}".format(""), end="")
        # for column_name in self.numerical_features:
        #     column_names.append(column_name)
        #     # length = len(column_name) + 3
        #     # print ("{:<{}}".format(column_name, length), end="")
        #     # spacing.append(length)
        # print("%s" %(column_names), end="")
        # print()
        # for category in categories:
        #     print(category, end="")
        #     for column in self.numerical_features:
        #             ()
        #         # print("{:<{}}".format("", 5), "{:.6f}".format(values[category][column]), end="")
        #         # print("{:<{}}".rjust(5), "{:.6f}".format(values[category][column]).rjust(len(category)), end="")
        #     print()

    def get_count_data(self):
        count_data = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in count_data:
                    count_data[feature] = 0
                count_data[feature] += 1
        return count_data

    def get_mean_data(self, count_data):
        mean_data = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in mean_data:
                    mean_data[feature] = 0
                mean_data[feature] += row[feature]
        for features in mean_data:
            mean_data[features] = mean_data[features] / count_data[features]
        return mean_data

    def get_std_data(self, count_data, mean_data):
        std_data = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in std_data:
                    std_data[feature] = 0
                std_data[feature] += (row[feature] - mean_data[feature])**2
        for features in std_data:
            std_data[features] = sqrt(std_data[features] / (count_data[features] - 1))
        return std_data

    def get_min_data(self):
        min_data = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in min_data or row[feature] < min_data[feature]:
                    min_data[feature] = row[feature]
        return min_data

    def get_percentile_data(self, percentile, count_data):
        percentile_data = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in percentile_data:
                    percentile_data[feature] = []
                percentile_data[feature].append(row[feature])
        for feature in percentile_data:
            percentile_data[feature] = sorted(percentile_data[feature])
            percentile_index = (percentile) / 100 * (count_data[feature] - 1)
            index_offset = percentile_index - int(percentile_index)
            diff = 0
            if index_offset != 0:
                diff = (percentile_data[feature][int(percentile_index) + 1] - percentile_data[feature][int(percentile_index)]) / 100 * (index_offset * 100) 
            percentile_data[feature] = percentile_data[feature][int(percentile_index)] + diff
        return percentile_data

    def get_max_data(self): 
        max_data = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in max_data or row[feature] > max_data[feature]:
                    max_data[feature] = row[feature]
        return max_data

def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
    except:
        sys.exit("can't open file")
    d.describe()

if __name__ == "__main__":
    main()