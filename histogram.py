from describe import Describe
import matplotlib.pyplot as plt
import sys

def main():
	if len(sys.argv) != 2:
		sys.exit("wrong number of arguments")
	d = Describe(sys.argv[1])
	
	plt.xlabel("grade")
	plt.ylabel("frequency")

	features_norm_count = d.calculate_features_count(d.norm_data)
	features_norm_mean = d.calculate_features_mean(d.norm_data, features_norm_count)
	features_norm_std = d.calculate_features_std(d.norm_data, features_norm_count, features_norm_mean)

	min_std = float("inf")
	for feature in features_norm_std:
		if feature == "Index":
			continue
		if features_norm_std[feature] < min_std:
			min_std_course = feature
			min_std = features_norm_std[feature]

	houses = {}
	for i in range(len(d.data)):
		house = d.data[i]["Hogwarts House"]
		if house not in houses:
			houses[house] = []
		if min_std_course in d.num_data[i]:
			houses[house].append(d.num_data[i][min_std_course])

	plt.title(min_std_course)
	
	while houses:
		max_house_len = float("-inf")
		for house in houses:
			house_len = len(houses[house])
			if house_len > max_house_len:
				max_house = house
				max_house_len = house_len
		plt.hist(houses.pop(max_house), label=max_house, bins=15, alpha=0.8)

	plt.legend()
	plt.show()

if __name__ == "__main__":
	main()