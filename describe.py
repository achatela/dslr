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
                try:
                    numerical_row[feature] = float(row[feature])
                except:
                    pass
            self.numerical_data.append(numerical_row)

    def describe(self):
        description = {}
        count_values = self.get_count_values()
        description["count"] = self.format_values(count_values)
        mean_values = self.get_mean_values(count_values)
        description["mean"] = self.format_values(mean_values)
        description["std"] = self.format_values(self.get_std_values(count_values, mean_values))
        description["min"] = self.format_values(self.get_min_values())
        description["25%"] = self.format_values(self.get_percentile_values(25, count_values)) # TODO handle bonuses as input with other value than 25/50/75
        description["50%"] = self.format_values(self.get_percentile_values(50, count_values)) # TODO handle bonuses as input 
        description["75%"] = self.format_values(self.get_percentile_values(75, count_values)) # TODO handle bonuses as input 
        description["max"] = self.format_values(self.get_max_values())

        longest_values = {}
        for statistic in description:
            for feature in description[statistic]:
                if feature not in longest_values:
                    longest_values[feature] = len(feature)
                if len(description[statistic][feature]) > longest_values[feature]:
                    longest_values[feature] = len(description[statistic][feature])

        featuresLine = " "*6
        for feature in longest_values:
            featuresLine += feature.rjust(longest_values[feature] + 1)
        print(featuresLine)
        for statistic in description:
            valuesLine = statistic.ljust(6)
            for feature in description[statistic]:
                valuesLine += description[statistic][feature].rjust(longest_values[feature] + 1)
            print(valuesLine)

    def format_values(self, values):
        return {feature : "{:.6f}".format(values[feature]) for feature in values}

    def get_count_values(self):
        count_values = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in count_values:
                    count_values[feature] = 0
                count_values[feature] += 1
        return count_values

    def get_mean_values(self, count_values):
        mean_values = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in mean_values:
                    mean_values[feature] = 0
                mean_values[feature] += row[feature]
        for features in mean_values:
            mean_values[features] = mean_values[features] / count_values[features]
        return mean_values

    def get_std_values(self, count_values, mean_values):
        std_values = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in std_values:
                    std_values[feature] = 0
                std_values[feature] += (row[feature] - mean_values[feature])**2
        for features in std_values:
            std_values[features] = sqrt(std_values[features] / (count_values[features] - 1))
        return std_values

    def get_min_values(self):
        min_values = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in min_values or row[feature] < min_values[feature]:
                    min_values[feature] = row[feature]
        return min_values

    def get_percentile_values(self, percentile, count_values):
        percentile_values = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in percentile_values:
                    percentile_values[feature] = []
                percentile_values[feature].append(row[feature])
        for feature in percentile_values:
            percentile_values[feature] = sorted(percentile_values[feature])
            percentile_index = percentile / 100 * (count_values[feature] - 1)
            index_offset = percentile_index - int(percentile_index)
            diff = (percentile_values[feature][int(percentile_index) + 1] - percentile_values[feature][int(percentile_index)]) / 100 * (index_offset * 100)
            percentile_values[feature] = percentile_values[feature][int(percentile_index)] + diff
        return percentile_values

    def get_max_values(self): 
        max_values = {}
        for row in self.numerical_data:
            for feature in row:
                if feature not in max_values or row[feature] > max_values[feature]:
                    max_values[feature] = row[feature]
        return max_values

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