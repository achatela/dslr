#!/bin/bash

while IFS= read -r line
do
 python3 logreg_train.py dataset_train.csv "$line"
done < "combinaisons.txt"
