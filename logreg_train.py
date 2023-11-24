from describe import Describe
import sys
import numpy as np

# Gryffindor 0
# Slytherin 1
# Ravenclaw 2
# Hufflepuff 3
precision = 0
overall_precision = 0

def prediction(theta, grade):
    Z = theta * grade
    return float(1/(1 + np.exp(-Z)))

def check_prediction(theta, grades, houses, answer):
    global precision
    global overall_precision

    highest = 0
    result  = str()
    j = 0

    gryff_prob = 0
    raven_prob = 0
    sly_prob = 0
    puff_prob = 0

    gryff_overall = 0
    raven_overall = 0
    sly_overall = 0
    puff_overall = 0

    for grade in grades:
        for i in range(len(houses)):
            tmp = prediction(theta[j][i], grade)
            if i == 0:
                gryff_prob = tmp
            elif i == 1:
                sly_prob = tmp
            elif i == 2:
                raven_prob = tmp
            elif i == 3:
                puff_prob = tmp
                gryff_overall += gryff_prob
                sly_overall += sly_prob
                raven_overall += raven_prob
                puff_overall += puff_prob
                print("Probabilities for", "Gryff = ", gryff_prob, "Raven =", raven_prob, "Sly =", sly_prob, "Puff =", puff_prob)
            if tmp > highest:
                highest = tmp
                result = houses[i]
        j += 1
        if result == answer:
            precision += 1
        print("Student is from", result)
    if gryff_overall > sly_overall and gryff_overall > raven_overall and gryff_overall > puff_overall and result == "Gryffindor":
        overall_precision += 1
    if sly_overall > gryff_overall and sly_overall > raven_overall and sly_overall > puff_overall and result == "Slytherin":
        overall_precision += 1
    if raven_overall > sly_overall and raven_overall > gryff_overall and raven_overall > puff_overall and result == "Ravenclaw":
        overall_precision += 1
    if puff_overall > sly_overall and puff_overall > raven_overall and puff_overall > gryff_overall and result == "Hufflepuff":
        overall_precision += 1
    # print("Overall probabilities Gryff =", gryff_overall, "Sly =", sly_overall, "Raven =", raven_overall, "Puff =", puff_overall)

def calculate_theta(feature_values, house):
    theta = 1
    L = 0.00000001 # Learning Rate
    epochs = 10
    
    for _ in range(epochs):
        sums = 0.0
        for line in feature_values:
            h = prediction(theta, float(line[1]))
            if house != line[0]:
                error = h + 1
            else:
                error = h
            # error = h - float(line[0])
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
    
    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    selected_features = ["Astronomy", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Charms"] # Muggle Studie, Charms
    features_value = {item: [] for item in selected_features}
    
    for line in d.data:
        for feature in line:
            if feature in selected_features and line[feature] != '':
                features_value[feature].append([line["Hogwarts House"], float(line[feature])])
    min_max_normalization(features_value)
    # print(features_value)
    thetas = {item: {} for item in houses}

    for feature in selected_features:
        for house in houses:
            thetas[house][feature] = calculate_theta(features_value[feature], house)
    # write_to_txt(thetas, selected_features)
    theta_list = []
    i = 0
    for feature in selected_features:
        theta_list.append([])
        for house in houses:
            theta_list[i].append(thetas[house][feature])
        i += 1

    print(theta_list)
    for i in range(200):
        print(features_value["Astronomy"][i])
        check_prediction(theta_list, [float(features_value["Astronomy"][i][1]), float(features_value["Defense Against the Dark Arts"][i][1]), float(features_value["Divination"][i][1]), float(features_value["Muggle Studies"][i][1]), float(features_value["Charms"][i][1])], houses, d.data[i]["Hogwarts House"])

if __name__ == "__main__":
    main()
    print("Precision =", precision, "Overall precison =", overall_precision)