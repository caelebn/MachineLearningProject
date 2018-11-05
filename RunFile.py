import k_nearest_neighbor
import gzip
import pickle


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


def get_query_list(path, num_tests):
    queries = []
    count = 0
    for curr in parse(path):
        q = curr['reviewText'], curr['overall']
        queries.append(q)
        count += 1
        if count >= num_tests:
            break
    return queries


def main():
    #path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Musical_Instruments_5.json.gz'
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Books_5.json.gz'
    num_tests = 2000
    queries = get_query_list(path, num_tests)
    count = 0
    num_off = [0] * 5
    for i in range(num_tests):
        knn_val = k_nearest_neighbor.main_helper(queries[i][0])
        curr_off = int(abs(queries[i][1] - knn_val))  # actual - estimate
        num_off[curr_off] += 1
        print(i+1)
    off = num_off[1] + 2*num_off[2] + 3*num_off[3] + 4*num_off[4]
    print('NUM CORRECT = ', num_off[0])
    print('AVG OFFSET = ', float(off/num_tests))
    print('NUM 1 OFF = ', num_off[1])
    print('NUM 2 OFF = ', num_off[2])
    print('NUM 3 OFF = ', num_off[3])
    print('NUM 4 OFF = ', num_off[4])


main()

