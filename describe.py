from math import *
from copy import deepcopy
import csv
import sys
import re

class Describe:
    def __init__(self, file):
        try:
            csv_reader = csv.DictReader(file)
        except:
            sys.exit("file is not csv")
        self.data = [] # csv file stored as an array of dicts
        self.num_data = []
        for row in csv_reader:
            self.data.append(row)
            numerical_row = {}
            for feature in row:
                if re.fullmatch(r"[-+]?\d*\.?\d+", row[feature]):
                    numerical_row[feature] = float(row[feature])
            self.num_data.append(numerical_row)
        self.stats = {}
        self.stats["Count"] = self.calculate_features_count(self.num_data)
        self.stats["Mean"] = self.calculate_features_mean(self.num_data, self.stats["Count"])
        self.stats["Std"] = self.calculate_features_std(self.num_data, self.stats["Count"], self.stats["Mean"])
        self.stats["Min"] = self.calculate_features_min(self.num_data)
        self.stats["25%"] = self.calculate_features_percentile(self.num_data, self.stats["Count"], 25)
        self.stats["50%"] = self.calculate_features_percentile(self.num_data, self.stats["Count"], 50)
        self.stats["75%"] = self.calculate_features_percentile(self.num_data, self.stats["Count"], 75)
        self.stats["Max"] = self.calculate_features_max(self.num_data)

        self.norm_data = deepcopy(self.num_data)
        for row in self.norm_data:
            for feature in row:
                row[feature] = (row[feature] - self.stats["Min"][feature]) / (self.stats["Max"][feature] - self.stats["Min"][feature])

    def describe(self):
        description = {}
        max_stat_len = 0
        max_features_len = {}
        for stat in self.stats:
            description[stat] = {}
            if len(stat) > max_stat_len:
                max_stat_len = len(stat)
            for feature in self.stats[stat]:
                formatted_value = "{:.6f}".format(self.stats[stat][feature])
                if feature not in max_features_len:
                    max_features_len[feature] = len(feature)
                if len(formatted_value) > max_features_len[feature]:
                    max_features_len[feature] = len(formatted_value)
                description[stat][feature] = formatted_value
        featuresLine = " "*(max_stat_len + 1)
        for feature in max_features_len:
            featuresLine += feature.rjust(max_features_len[feature] + 4)
        print(featuresLine)
        for stat in description:
            valuesLine = stat.ljust(max_stat_len + 1)
            for feature in description[stat]:
                valuesLine += description[stat][feature].rjust(max_features_len[feature] + 4)
            print(valuesLine)

    def calculate_features_count(self, num_data):
        features_count = {}
        for row in num_data:
            for feature in row:
                if feature not in features_count:
                    features_count[feature] = 0
                features_count[feature] += 1
        return features_count

    def calculate_features_mean(self, num_data, features_count):
        features_mean = {}
        for row in num_data:
            for feature in row:
                if feature not in features_mean:
                    features_mean[feature] = 0
                features_mean[feature] += row[feature]
        for features in features_mean:
            features_mean[features] = features_mean[features] / features_count[features]
        return features_mean

    def calculate_features_std(self, num_data, features_count, features_mean):
        features_std = {}
        for row in num_data:
            for feature in row:
                if feature not in features_std:
                    features_std[feature] = 0
                features_std[feature] += (row[feature] - features_mean[feature])**2
        for features in features_std:
            features_std[features] = sqrt(features_std[features] / (features_count[features] - 1))
        return features_std

    def calculate_features_min(self, num_data):
        features_min = {}
        for row in num_data:
            for feature in row:
                if feature not in features_min or row[feature] < features_min[feature]:
                    features_min[feature] = row[feature]
        return features_min

    def calculate_features_percentile(self, num_data, features_count, percentile):
        features_percentile = {}
        for row in num_data:
            for feature in row:
                if feature not in features_percentile:
                    features_percentile[feature] = []
                features_percentile[feature].append(row[feature])
        for feature in features_percentile:
            features_percentile[feature] = sorted(features_percentile[feature])
            percentile_index = percentile / 100 * (features_count[feature] - 1)
            index_offset = percentile_index - int(percentile_index)
            diff = (features_percentile[feature][int(percentile_index) + 1] - features_percentile[feature][int(percentile_index)]) / 100 * (index_offset * 100)
            features_percentile[feature] = features_percentile[feature][int(percentile_index)] + diff
        return features_percentile

    def calculate_features_max(self, num_data): 
        features_max = {}
        for row in num_data:
            for feature in row:
                if feature not in features_max or row[feature] > features_max[feature]:
                    features_max[feature] = row[feature]
        return features_max

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
