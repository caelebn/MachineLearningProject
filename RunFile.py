import k_nearest_neighbor
import gzip
import pickle


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


def get_query_list(path):
    queries = []
    for curr in parse(path):
        q = curr['reviewText'], curr['overall']
        queries.append(q)
    return queries


def main():
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Musical_Instruments_5.json.gz'
    queries = get_query_list(path)
    off = 0
    count = 0
    num_correct = 0
    num_1_off = 0
    num_2_off = 0
    num_3_off = 0
    num_4_off = 0
    for i in range(0, 2000):
        knn_val = k_nearest_neighbor.main_helper(queries[i][0], 0, 0, 'Y')
        curr_off = abs(queries[i][1] - knn_val)  # actual - estimate
        if curr_off == 0:
            num_correct += 1
        elif curr_off == 1:
            num_1_off += 1
        elif curr_off == 2:
            num_2_off += 1
        elif curr_off == 3:
            num_3_off += 1
        else:
            num_4_off += 1
        off += curr_off
        count += 1
        print(count)
    print('NUM CORRECT = ', num_correct)
    print('AVG OFFSET = ', float(off/count))
    print('NUM 1 OFF = ', num_1_off)
    print('NUM 2 OFF = ', num_2_off)
    print('NUM 3 OFF = ', num_3_off)
    print('NUM 4 OFF = ', num_4_off)


main()

