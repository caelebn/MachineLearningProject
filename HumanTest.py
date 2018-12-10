import KNN
import gzip
import pickle
import TestBase
import seaborn as sn
from pandas import DataFrame
import matplotlib.pyplot as plt
import confusion_matrix_pretty_print as pp
from random import shuffle

def get_randomized_reviews(path, num_tests):
    reviews = []
    joined_list = []
    for i in range(5):
        reviews.append([])
    for curr in TestBase.parse(path):
        reviews[int(curr['overall'])-1].append((curr['reviewText'], curr['helpful'][0], curr['helpful'][1], int(curr['overall'])))
        if TestBase.find_count(reviews)*5 >= num_tests:
            for i in range(5):
                for j in range(TestBase.find_count(reviews)):
                    joined_list.append(reviews[i][j])
            shuffle(joined_list)
            return joined_list

def main():
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Video_Games_5.json.gz'
    num_tests = 200
    reviews = get_randomized_reviews(path, num_tests)
    reviewsGuessed = 0
    guesses = []
    for a in range(5):
        guesses.append([0, 0, 0, 0, 0])
    for i in range(len(reviews)):
        currentOverall = reviews[i][3]
        currentText = reviews[i][0]
        currentHelpful = reviews[i][1]
        currentNotHelpful = reviews[i][2]
        currentGuess = int(input("Text: {}\nHelpful: {}\nNot Helpful: {}\n".format(currentText, currentHelpful, currentNotHelpful)))
        reviewsGuessed += 1
        guesses[currentOverall-1][currentGuess-1] += 1
        #print("{} reviews left".format())

    df_cm = DataFrame(guesses, index=range(1,6), columns=range(1,6))
    pp.pretty_plot_confusion_matrix(df_cm)


main()

