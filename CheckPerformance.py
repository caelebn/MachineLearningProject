import KNN
import gzip
import pickle
import TestBase

def main():
    #path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Musical_Instruments_5.json.gz'
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Books_5.json.gz'
    num_tests = 2000
    queries = TestBase.get_query_list(path, num_tests)
    count = 0
    num_off = [0] * 5
    max_to_grab = TestBase.find_count(queries)
    for i in range(5):
        for j in range(max_to_grab):
            knn_val = KNN.guess_review(queries[i][j])
            #print(knn_val)
            curr_off = abs(i+1 - knn_val)  # actual - estimate
            num_off[curr_off] += 1
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


main()

