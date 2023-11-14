import csv

class Describe:
    def __init__(self):
        self.data = [] # csv file stored as an array of dicts
        self.features_name = [] # list of str containing all the features name
        self.numerical_features = [] # list of str contraining all the features name with numerical values
    
    def parse(self, file_name):
        with open(file_name) as csv_file: # store the csv file in self.data
            reader = csv.DictReader(csv_file)
            for line in reader:
                self.data.append(line)
        with open(file_name) as csv_file: # get the column names
            self.features_name = str(list(csv_file)[0]).strip('\n').split(',')
        
        self.find_numerical_columns()

    def find_numerical_columns(self): # function to get the names of the columns that contains numerical values
        for tmp in self.features_name:
            try:
                float(self.data[0][tmp])
                self.numerical_features.append(tmp)
            except:
                ()

def main():
    d = Describe()
    d.parse("dataset_test.csv")

if __name__:
    main()