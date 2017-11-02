# Challenge Description
The goal of the task is to extract browser familiy and major version from user agents. 

# Installation:
This tool is based on sklearn. Before running the code, make sure install the requirement libraries.
pip install -r lib_reqmt.txt

# How to use it:
This executable script can be running with the following input parameters:
1) filename of training data
2) filename of test data
3) filename of prediction results from test data
python run.py --training path_of_training_data.txt --test path_of_test_data.txt --prediction-results path_of_output_data.txt


# Machine Learning Model
It's obvious that this challenge is a classification problem. So firstly I'm trying to build feature vectors to describe the browser family categories. After observing the training dataset and online reference, I build a 25-fearture vector for each browser data. Then in the model part, I use a random forest classifier by putting the feature vectors into the sklearn-randomforest api to predict the browser-family. Also we can easily find the major version in the User-Agent format according to its matching model. Reason for choosing this model: Random forest classifier is a common classifier I used in Kaggle competition. The most advantage of this model I think is increasing the number of trees tends to decrease the variance of the model, without increasing the bias. Compared with other classifier, it performs much better on overfitting issue. 

# Result
Temporay accuracy is 100%.
