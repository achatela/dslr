import csv
import sys
from math import *

class Describe:
    def __init__(self):
        self.data = [] # csv file stored as an array of dicts
        self.features_name = [] # list of str containing all the features name
        self.numerical_features = [] # list of str contraining all the features name with numerical values
        self.values = {}
    
    def get_values(self):
        return self.values

    def parse(self, file_name):
        with open(file_name) as csv_file: # store the csv file in self.data
            reader = csv.DictReader(csv_file)
            for line in reader:
                self.data.append(line)
        with open(file_name) as csv_file: # get the column names
            self.features_name = str(list(csv_file)[0]).strip('\n').split(',')
        self.find_numerical_columns()

    def find_numerical_columns(self): # function to get the names of the columns that contains numerical values
        for tmp in self.features_name:
            try:
                float(self.data[0][tmp])
                self.numerical_features.append(tmp)
            except:
                ()

    def get_describe_values(self, values):
        values = self.count(values)
        values = self.mean(values)
        values = self.std(values)
        values = self.min(values)
        values = self.percentile(values, 25) # TODO handle bonuses as input with other value than 25/50/75
        values = self.percentile(values, 50) # TODO handle bonuses as input 
        values = self.percentile(values, 75) # TODO handle bonuses as input 
        values = self.max(values)
        self.values = values
        return values

    def describe(self):
        categories = ["Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"] # list of all the categories that will be described
        spacing = [] # list of numbers
        values = { # dict of dict for every caterogy so when can find the Std of Herbology at values["Std"]["Herbology"]
            "Count":{item: 0.0 for item in self.numerical_features},
            "Mean":{item: 0.0 for item in self.numerical_features},
            "Std":{item: 0.0 for item in self.numerical_features},
            "Min":{item: 0.0 for item in self.numerical_features},
            "25%":{item: 0.0 for item in self.numerical_features},
            "50%":{item: 0.0 for item in self.numerical_features},
            "75%":{item: 0.0 for item in self.numerical_features},
            "Max":{item: 0.0 for item in self.numerical_features}
        }
        values = self.get_describe_values(values)
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

    def count(self, values):
        count_values = values["Count"]
        track_count = {
            item: 0 for item in self.numerical_features
        }
        for line in self.data:
            for features in self.numerical_features:
                try:
                    if line[features] != '':
                        track_count[features] += 1
                except:
                    ()
        for features in self.numerical_features:
            count_values[features] = track_count[features]
        values["Count"] = count_values
        return values

    def mean(self, values): 
        mean_values = values["Mean"]
        track_mean = {
            item: 0 for item in self.numerical_features
        }
        for line in self.data:
            for features in self.numerical_features:
                try:
                    if line[features] != '':
                        track_mean[features] += float(line[features])
                except:
                    ()
        for features in self.numerical_features:
            mean_values[features] = track_mean[features] / values["Count"][features]
        values["Mean"] = mean_values
        return values

    def std(self, values): 
        std_values = values["Std"]
        track_std = {
            item: 0 for item in self.numerical_features
        }
        for line in self.data:
            for features in self.numerical_features:
                try:
                    if line[features] != '':
                        track_std[features] += (float(line[features]) - values["Mean"][features])**2
                except:
                    ()
        for features in self.numerical_features:
            std_values[features] = sqrt((track_std[features] / (values["Count"][features] - 1)))
        values["Std"] = std_values
        return values

    def min(self, values): 
        min_values = values["Min"]
        track_min = {
            item: float('inf') for item in self.numerical_features
        }
        for line in self.data:
            for features in self.numerical_features:
                try:
                    if line[features] != '' and float(line[features]) < track_min[features]:
                        track_min[features] = float(line[features])
                except:
                    ()
        for features in self.numerical_features:
            min_values[features] = track_min[features]
        values["Min"] = min_values
        return values

    def percentile(self, values, percentile):
        percentile_values = values[str(percentile) + "%"]
        values_ascendenting = {
            item: [] for item in self.numerical_features
        }
        for line in self.data:
            for features in self.numerical_features:
                try:
                    if line[features] != '':
                        values_ascendenting[features].append(float(line[features]))
                except:
                    ()
        for features in self.numerical_features:
            values_ascendenting[features] = sorted(values_ascendenting[features])
            percentile_index = int(percentile) / 100 * (values["Count"][features] - 1)
            index_offset = percentile_index - int(percentile_index)
            diff = 0
            if index_offset != 0:
                diff = (values_ascendenting[features][int(percentile_index) + 1] - values_ascendenting[features][int(percentile_index)]) / 100 * (index_offset * 100) 
            percentile_values[features] = values_ascendenting[features][int(percentile_index)] + diff
        values[str(percentile) +"%"] = percentile_values
        return values

    def max(self, values): 
        max_values = values["Max"]
        track_max = {
            item: float('-inf') for item in self.numerical_features
        }
        for line in self.data:
            for features in self.numerical_features:
                try:
                    if line[features] != '' and float(line[features]) > track_max[features]:
                        track_max[features] = float(line[features])
                except:
                    ()
        for features in self.numerical_features:
            max_values[features] = track_max[features]
        values["Max"] = max_values
        return values



def main():
    d = Describe()
    d.parse(sys.argv[1])
    d.describe()

if __name__ == "__main__":
    main()