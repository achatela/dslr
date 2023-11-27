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
        # print("Student is from", result)

    if gryff_overall > sly_overall and gryff_overall > raven_overall and gryff_overall > puff_overall:
        y_pred.append("Gryffindor")
    elif sly_overall > gryff_overall and sly_overall > raven_overall and sly_overall > puff_overall:
        y_pred.append("Slytherin")
    elif raven_overall > sly_overall and raven_overall > gryff_overall and raven_overall > puff_overall:
        y_pred.append("Ravenclaw")
    elif puff_overall > sly_overall and puff_overall > raven_overall and puff_overall > gryff_overall:
        y_pred.append("Hufflepuff")

    if gryff_overall > sly_overall and gryff_overall > raven_overall and gryff_overall > puff_overall and answer == "Gryffindor":
        # print("Gryff", answer)
        overall_precision += 1
    elif sly_overall > gryff_overall and sly_overall > raven_overall and sly_overall > puff_overall and answer == "Slytherin":
        # print("Sly", answer)
        overall_precision += 1
    elif raven_overall > sly_overall and raven_overall > gryff_overall and raven_overall > puff_overall and answer == "Ravenclaw":
        # print("Raven", answer)
        overall_precision += 1
    elif puff_overall > sly_overall and puff_overall > raven_overall and puff_overall > gryff_overall and answer == "Hufflepuff":
        # print("Puff", answer)
        overall_precision += 1

def calculate_theta(feature_values, house):
    theta = 1
    L = 0.00001 # Learning Rate
    epochs = 10
    
    for _ in range(epochs):
        sums = 0.0
        for line in feature_values:
            h = prediction(theta, float(line[1]))
            if house != line[0]:
                error = h
            else:
                error = h - 1
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
    # print(sys.argv[2])
    # if (len(sys.argv) != 2):
        # sys.exit("wrong number of arguments")
    file_name = sys.argv[1]
    try:
        with open(file_name, "r") as file:
            d = Describe(file)
    except:
        sys.exit("can't open file")
    
    houses = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    selected_features = ('Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Charms', 'Flying')
    # selected_features = ["Astronomy", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Charms"] # Muggle Studie, Charms
    
    # selected_features = sys.argv[2]
    # selected_features = ast.literal_eval(selected_features)

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

    # print(theta_list)

    for i in range(100):
        tmp = []
        for feature in selected_features:
            tmp.append(float(features_value[feature][i][1]))
        check_prediction(theta_list, tmp, houses, d.data[i]["Hogwarts House"])

if __name__ == "__main__":
    main()
    print("Precision =", precision, "Overall precison =", overall_precision)
    # print("Accuracy =", accuracy_score(y_true, y_pred) * 100, "%")


# 82
# ('Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Charms', 'Flying')
# 80
# ('Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Muggle Studies', 'Potions', 'Charms', 'Flying')
# 81
# ('Herbology', 'Transfiguration', 'Potions', 'Charms', 'Flying')
# 81
# ('Arithmancy', 'Astronomy', 'Herbology', 'Muggle Studies', 'Potions', 'Charms', 'Flying')