from describe import Describe
import sys

def calculate_theta(feature_values):
    theta = 0
    L = 0.0000001 # Learning Rate

    

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
                features_value[feature].append((line["Hogwarts House"], float(line[feature])))
    print(features_value)
    thetas = []

    for feature in selected_features:
        thetas.append(calculate_theta(features_value[feature]))
    write_to_txt(thetas, selected_features)

if __name__ == "__main__":
    main()