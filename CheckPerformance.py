import KNN
import gzip
import pickle
import TestBase
import seaborn as sn
from pandas import DataFrame
import matplotlib.pyplot as plt
import confusion_matrix_pretty_print as pp

def main():
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Books_5.json.gz'
    num_tests = 400
    queries = TestBase.get_query_list(path, num_tests)
    num_off = [0] * 5
    guesses = []
    for a in range(5):
        guesses.append([0, 0, 0, 0, 0])
    max_to_grab = TestBase.find_count(queries)
    for i in range(5):
        for j in range(max_to_grab):
            knn_val = KNN.guess_review(queries[i][j])
            #print(knn_val)
            curr_off = abs(i+1 - knn_val)  # actual - estimate
            num_off[curr_off] += 1
            guesses[i][knn_val-1] += 1
            print("i:{} j:{}".format(i, j))
    off = num_off[1] + 2*num_off[2] + 3*num_off[3] + 4*num_off[4]
    percent_correct = num_off[0]/len(queries[0])*20
    print('NUM CORRECT = ', num_off[0])
    print('PERCENT CORRECT = ', percent_correct)
    print('AVG OFFSET = ', float(off/len(queries[0])/5))
    print('NUM 1 OFF = ', num_off[1])
    print('NUM 2 OFF = ', num_off[2])
    print('NUM 3 OFF = ', num_off[3])
    print('NUM 4 OFF = ', num_off[4])

    df_cm = DataFrame(guesses, index=range(1,6), columns=range(1,6))
    pp.pretty_plot_confusion_matrix(df_cm)


main()

