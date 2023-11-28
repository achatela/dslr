from describe import Describe
import sys
import numpy as np
import ast
from sklearn.metrics import accuracy_score


# Gryffindor 0
# Slytherin 1
# Ravenclaw 2
# Hufflepuff 3
precision = 0
overall_precision = 0
y_pred = []
y_true = []


def prediction(theta, grade):
    Z = theta * grade
    return float(1/(1 + np.exp(-Z)))

def check_prediction(theta, grades, houses, answer):
    global y_pred
    global y_true
    global precision
    global overall_precision

    y_true.append(answer)

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
                # print("Probabilities for", "Gryff = ", gryff_prob, "Raven =", raven_prob, "Sly =", sly_prob, "Puff =", puff_prob)
            if tmp > highest:
                highest = tmp
                result = houses[i]
        j += 1
        if result == answer:
            precision += 1
    if gryff_overall > sly_overall and gryff_overall > raven_overall and gryff_overall > puff_overall:
        y_pred.append("Gryffindor")
    elif sly_overall > gryff_overall and sly_overall > raven_overall and sly_overall > puff_overall:
        y_pred.append("Slytherin")
    elif raven_overall > sly_overall and raven_overall > gryff_overall and raven_overall > puff_overall:
        y_pred.append("Ravenclaw")
    elif puff_overall > sly_overall and puff_overall > raven_overall and puff_overall > gryff_overall:
        y_pred.append("Hufflepuff")

def isHouse(house, predictedHouse):
    if house == predictedHouse:
        return 0.5
    return 0

def calculate_theta(feature_values, house):
    theta = 0.0 
    L = 0.0000001 # Learning Rate
    epochs = 100
    
    for _ in range(epochs):
        sums = sum((prediction(theta, float(line[1])) - isHouse(line[0], house)) * float(line[1]) for line in feature_values)
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


# def get_house_value(str):
#     if str == "Gryffindor":
#         return 0.0
#     elif str == "Slytherin":
#         return 1.0
#     elif str == "Ravenclaw":
#         return 2.0
#     elif str == "Hufflepuff":
#         return 3.0


def main():
    if (len(sys.argv) != 2):
        sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
        with open("dataset_test.csv", "r") as file2:
            d_test = Describe(file2)
        with open("dataset_truth.csv", "r") as file3:
            d_truth = Describe(file3)
    except:
        sys.exit("can't open file")
    
    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    selected_features = ('Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Charms', 'Flying')
    
    features_value = {item: [] for item in selected_features}
    
    for line in d.data:
        for feature in line:
            if feature in selected_features and line[feature] != '':
                features_value[feature].append([line["Hogwarts House"], float(line[feature])])
    min_max_normalization(features_value)

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

    features_value2 = {item: [] for item in selected_features}

    for line in d_test.data:
        for feature in line:
            if feature in selected_features and line[feature] != '':
                features_value2[feature].append([line["Hogwarts House"], float(line[feature])])

    # print(features_value2)

    # print("Index, Hogwarts House")
    for i in range(400):
        tmp = []
        for feature in selected_features:
            try:
                value = features_value2[feature][i][1]
            except:
                value = 0
            tmp.append(float(value))
        check_prediction(theta_list, tmp, houses, d_truth.data[i]["Hogwarts House"])
        # check_prediction(theta_list, tmp, houses, d.data[i]["Hogwarts House"])

if __name__ == "__main__":
    main()
    # print("Precision =", precision, "Overall precison =", overall_precision)
    empty = 0
    while len(y_pred) < 400:
        y_pred.append(0)
        empty += 1
    print("Accuracy =", accuracy_score(y_true, y_pred) * 100, "%", "Empty = ", empty)


# 82
# ('Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Charms', 'Flying')
# 80
# ('Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Muggle Studies', 'Potions', 'Charms', 'Flying')
# 81
# ('Herbology', 'Transfiguration', 'Potions', 'Charms', 'Flying')
# 81
# ('Arithmancy', 'Astronomy', 'Herbology', 'Muggle Studies', 'Potions', 'Charms', 'Flying')