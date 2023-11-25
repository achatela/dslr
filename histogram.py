from describe import Describe
import matplotlib.pyplot as plt
import sys

def main():
	if (len(sys.argv) != 2):
		sys.exit("wrong number of arguments")
	file_name = sys.argv[1]
	try:
		with open(file_name, "r") as file:
			d = Describe(file)
	except:
		sys.exit("can't open file")
	
	plt.xlabel("grading")
	plt.ylabel("students count")

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
			houses[house].append(d.norm_data[i][min_std_course])

	for house in houses:
		plt.hist(sorted(houses[house]), label=house, alpha=0.75)

	plt.legend()
	plt.show()

if __name__ == "__main__":
	main()