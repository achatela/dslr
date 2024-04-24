## Project Overview

The project is divided into three main sections:

1. **Data Analysis**
2. **Data Visualization**
3. **Logistic Regression**

Each section has specific tasks that are detailed below. The aim is to manually implement statistical methods and machine learning techniques without relying on high-level library functions that would automate these tasks.

### V.1 Data Analysis

The `describe` script performs a detailed statistical analysis on numerical features of the dataset. This script computes the following statistics manually:

- Count
- Mean
- Standard Deviation
- Minimum
- 25th Percentile
- 50th Percentile (Median)
- 75th Percentile
- Maximum

### V.2 Data Visualization

This section includes scripts that generate various types of plots to explore the dataset visually:

- **Histogram:** Identifies which Hogwarts course has a homogeneous score distribution across all four houses.
- **Scatter Plot:** Determines the two features that are most similar.
- **Pair Plot:** Helps in selecting features that will be used for logistic regression modeling.

### V.3 Logistic Regression

The logistic regression section contains two scripts:

- `logreg_train`: Trains a multi-class logistic regression model using gradient descent to minimize the error and saves the model weights.
- `logreg_predict`: Uses the trained weights to predict the Hogwarts house for entries in a test dataset and outputs the predictions in a specified format.
