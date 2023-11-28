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


def prediction(z):
    return 1/(1 + np.exp(-z))

def normalize_probas(overall):
    # Print the probabilities normalized
    total = sum(overall)
    overall = [float(i)/total for i in overall]
    print(overall)

def determine_house(overall): # "Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"

    normalize_probas(overall)

    if overall[0] > overall[1] and overall[0] > overall[2] and overall[0] > overall[3]:
        return("Gryffindor")
    elif overall[1] > overall[0] and overall[1] > overall[2] and overall[1] > overall[3]:
        return("Slytherin")
    elif overall[2] > overall[1] and overall[2] > overall[0] and overall[2] > overall[3]:
        return("Ravenclaw")
    elif overall[3] > overall[1] and overall[3] > overall[2] and overall[3] > overall[0]:
        return("Hufflepuff")

def check_prediction(theta, grades, houses, answer):
    global y_pred
    global y_true

    y_true.append(answer)
    overall = [0,0,0,0] # "Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"

    gryff_thetas = []
    sly_thetas = []
    raven_thetas = []
    huff_thetas = []
    for i in range(len(theta)):
        gryff_thetas.append(theta[i][0])
        sly_thetas.append(theta[i][1])
        raven_thetas.append(theta[i][2])
        huff_thetas.append(theta[i][3])

    thetas = []
    thetas.append(gryff_thetas)
    thetas.append(sly_thetas)
    thetas.append(raven_thetas)
    thetas.append(huff_thetas)

    for i in range(len(houses)):
        z = np.dot(thetas[i], grades)
        overall[i] = prediction(z)
    y_pred.append(determine_house(overall))

def isHouse(house, predictedHouse):
    if house == predictedHouse:
        return 1
    return 0

def calculate_theta(feature_values, house):
    theta = 0.001
    L = 0.00001 # Learning Rate
    epochs = 200

    x = []
    y = []
    for line in feature_values:
        x.append(float(line[1]))
        if line[0] == house:
            y.append(1)
        else:
            y.append(0)

    for i in np.unique(y):
        y_copy = np.where(y == i, 1, 0)

    X = np.array(x)

    for _ in range(epochs):
        output = X.dot(theta)
        error = y_copy - prediction(output)
        gradient = np.dot(X.T, error)
        # sums = sum((prediction(theta, float(line[1])) - isHouse(line[0], house)) * float(line[1]) for line in feature_values) # line format: (str: House, float: Grade)
        theta = theta + L * gradient
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
    selected_features = ('Divination', 'Muggle Studies', 'Potions', 'Care of Magical Creatures', 'Flying')
    # selected_features = ('Herbology','Defense Against the Dark Arts','Divination','Muggle Studies','Ancient Runes','History of Magic','Transfiguration','Potions','Charms','Flying')
    
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

    min_max_normalization(features_value2)
    # print(features_value2)

    # print("Index, Hogwarts House")
    print(thetas)
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
        y_pred.append("Gryffindor")
        empty += 1
    print("Accuracy =", accuracy_score(y_true, y_pred) * 100, "%", "Empty = ", empty)

# ('Divination', 'Muggle Studies', 'Potions', 'Care of Magical Creatures', 'Flying')