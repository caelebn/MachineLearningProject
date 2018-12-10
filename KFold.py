import KNN
import gzip
import pickle
import TestBase
import Review
import seaborn as sn
from pandas import DataFrame
import matplotlib.pyplot as plt
import confusion_matrix_pretty_print as pp
import numpy as np

set_name = 'reviews_Video_Games_5'
path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Video_Games_5.json.gz'
num_folds = 10

def main():
    global set_name, num_folds
    with open('Folds/' + set_name + '_tuple_data.pkl', 'rb') as f:
        folds = pickle.load(f)
    guesses = []
    for i in range(5):
        guesses.append([0, 0, 0, 0, 0])
    for i in range(num_folds):
        training_set = np.array([])
        testing_set = np.array([])
        for j in range(num_folds):
            if j == i:
                testing_set = folds[j]
            elif len(training_set) == 0:
                training_set = folds[j]
            else:
                training_set = np.concatenate((training_set, folds[j]), axis=1)
        KNN.set_review_points_list(training_set.tolist())
        for j in range(5):
            for k in range(len(testing_set[j])):
                knn_val = KNN.guess_tuple(testing_set[j][k])
                guesses[j][knn_val-1] += 1
                print("i:{} j:{} k:{}".format(i, j, k))
    df_cm = DataFrame(guesses, index=range(1,6), columns=range(1,6))
    pp.pretty_plot_confusion_matrix(df_cm)

def make_folds():
    global set_name, num_folds, path
    tuples = [[],[],[],[],[]]
    for curr in TestBase.parse(path):
        review = Review.Review(curr['reviewText'], curr['helpful'][0], curr['helpful'][1], curr['overall'])
        tuples[review.get_overall()-1].append(review.get_points())
    max_allowed = min(len(x) for x in tuples)
    sanitized_tuples = [[],[],[],[],[]]
    for i in range(5):
        for j in range(max_allowed):
            sanitized_tuples[i].append(tuples[i][j])
    folds1 = np.array_split(np.array(sanitized_tuples[0]),num_folds)
    folds2 = np.array_split(np.array(sanitized_tuples[1]),num_folds)
    folds3 = np.array_split(np.array(sanitized_tuples[2]),num_folds)
    folds4 = np.array_split(np.array(sanitized_tuples[3]),num_folds)
    folds5 = np.array_split(np.array(sanitized_tuples[4]),num_folds)
    grouped_folds = []
    for i in range(num_folds):
        grouped_folds.append((folds1[i], folds2[i], folds3[i], folds4[i], folds5[i]))
    with open('Folds/' + set_name + '_tuple_data.pkl', 'wb') as f:
        pickle.dump(grouped_folds, f)
    f.close()

make_folds()


