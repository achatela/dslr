from describe import Describe
import sys
import numpy as np

# Gryffindor 0
# Slytherin 1
# Ravenclaw 2
# Hufflepuff 3

def prediction(theta, grade):
    Z = theta * grade
    return float(1/(1 + np.exp(-Z)))

def calculate_theta(feature_values):
    theta = 0.0
    L = 0.00001 # Learning Rate
    epochs = 100
    
    # for _ in range(epochs):
    #     sums = 0.0
    #     for line in feature_values:
    #         sums += prediction(theta, float(line[1])) - float(line[0]) * float(line[1])
        # theta = theta - (L / len(feature_values)) * sums
    for _ in range(epochs):
        sums = 0.0
        for line in feature_values:
            h = prediction(theta, float(line[1]))
            error = h - float(line[0])
            sums += error * float(line[1])
        theta = theta - L * sums
    return theta

def min_max_normalization(selected_features):
    for feature in selected_features: 
        mini = min(selected_features[feature])[1]
        maxi = max(selected_features[feature])[1]
        for i in range(len(selected_features[feature])):
            selected_features[feature][i][1] = (selected_features[feature][i][1] - mini) / (maxi - mini)

def write_to_txt(thetas, selected_features):
    f = open("thetas.csv", "w")
    for i in range(len(selected_features)):
        f.write(f"{selected_features[i]}")
        if i != (len(selected_features)) - 1:
            f.write(",")
    f.write("\n")
    for i in range(len(thetas)):
        f.write(f"{thetas[i]}")
        if i != (len(thetas)) - 1:
            f.write(",")
    f.write("\n")
    f.close()

def get_house_value(str):
    if str == "Gryffindor":
        return 0.0
    elif str == "Slytherin":
        return 1.0
    elif str == "Ravenclaw":
        return 2.0
    elif str == "Hufflepuff":
        return 3.0

def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
    except:
        sys.exit("can't open file")
    
    selected_features = ["Astronomy", "Defense Against the Dark Arts", "Divination"]
    features_value = {item: [] for item in selected_features}
    
    for line in d.data:
        for feature in line:
            if feature in selected_features and line[feature] != '':
                features_value[feature].append([float(get_house_value(line["Hogwarts House"])), float(line[feature])])
    min_max_normalization(features_value)
    # print(features_value)
    thetas = []

    for feature in selected_features:
        thetas.append(calculate_theta(features_value[feature]))
    print(thetas)
    write_to_txt(thetas, selected_features)

if __name__ == "__main__":
    main()