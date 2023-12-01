from math import *
from copy import deepcopy
import pandas as pd
import csv
import sys
import re

class Describe:
	def __init__(self, file_name, percentiles=None):
		try:
			with open(file_name, "r" ) as file:
				csv_reader = csv.DictReader(file)
				self.data = []
				self.num_data = []
				for row in csv_reader:
					self.data.append(row)
					numerical_row = {}
					for feature in row:
						if re.fullmatch(r"[-+]?\d*\.?\d+", row[feature]):
							numerical_row[feature] = float(row[feature])
					self.num_data.append(numerical_row)
		except:
			sys.exit('wrong file')
		if percentiles:
			percentiles = set(percentiles)
			percentiles.add(50)
			percentiles = sorted(percentiles)
			for percentile in percentiles:
				if percentile < 0 or percentile > 100:
					sys.exit('percentiles should be values between 0 and 100')
		else:
			percentiles = [25, 50, 75]
		self.fields = {}
		self.fields["Count"] = self.calculate_features_count(self.num_data)
		self.fields["Mean"] = self.calculate_features_mean(self.num_data, self.fields["Count"])
		self.fields["Std"] = self.calculate_features_std(self.num_data, self.fields["Count"], self.fields["Mean"])
		self.fields["Min"] = self.calculate_features_min(self.num_data)
		for percentile in percentiles:
			self.fields[f"{percentile}%"] = self.calculate_features_percentile(self.num_data, self.fields["Count"], percentile)
		self.fields["Max"] = self.calculate_features_max(self.num_data)

		self.norm_data = deepcopy(self.num_data)
		for row in self.norm_data:
			for feature in row:
				row[feature] = (row[feature] - self.fields["Min"][feature]) / (self.fields["Max"][feature] - self.fields["Min"][feature])

	def display(self):
		description = {}
		max_field_len = 0
		max_features_len = {}
		for field in self.fields:
			description[field] = {}
			if len(field) > max_field_len:
				max_field_len = len(field)
			for feature in self.fields[field]:
				formatted_value = "{:.6f}".format(self.fields[field][feature])
				if feature not in max_features_len:
					max_features_len[feature] = len(feature)
				if len(formatted_value) > max_features_len[feature]:
					max_features_len[feature] = len(formatted_value)
				description[field][feature] = formatted_value
		featuresLine = " "*(max_field_len + 1)
		for feature in max_features_len:
			featuresLine += feature.rjust(max_features_len[feature] + 4)
		print(featuresLine)
		for field in description:
			valuesLine = field.ljust(max_field_len + 1)
			for feature in description[field]:
				valuesLine += description[field][feature].rjust(max_features_len[feature] + 4)
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
			if int(percentile_index) != percentile_index:
				index_offset = percentile_index - int(percentile_index)
				diff = (features_percentile[feature][int(percentile_index) + 1] - features_percentile[feature][int(percentile_index)]) / 100 * (index_offset * 100)
			else:
				diff = 0
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
	if not sys.argv:
		sys.exit("wrong number of arguments")
	if len(sys.argv) > 2:
		try:
			percentiles = [int(x) for x in sys.argv[2:]]
		except:
			sys.exit('wrong percentiles')
		d = Describe(sys.argv[1], percentiles=percentiles)
	else:
		d = Describe(sys.argv[1])
	d.display()

if __name__ == "__main__":
	main()
