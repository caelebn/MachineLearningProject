import k_nearest_neighbor
import Query
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

def check_done(curr_weight, last_weight):
    for i in range(len(curr_weight)):
        if min(0.001, curr_weight[i] - last_weight[i]) != 0.001:
            return False
    return True

def weight_slope(num_correct, last_num_correct, curr_weight, last_weight):
    if curr_weight == last_weight:
        return 1
    return (num_correct - last_num_correct) / (curr_weight - last_weight)


#attempts to optimize weights, assuming that weights are independent of each other
def main():
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Books_5.json.gz'
    num_tests = 5
    max_iterations = 25
    queries = get_query_list(path, num_tests)
    off = 0
    last_num_correct = 0
    num_off = [0] * 5
    learning_rate = 0.5
    last_weights = [0]*len(Query.weights)
    for j in range(max_iterations):
        for i in range(num_tests):
            knn_val = k_nearest_neighbor.main_helper(queries[i][0], 'Y')
            curr_off = int(abs(queries[i][1] - knn_val))  # actual - estimate
            num_off[curr_off] += 1
            off += curr_off
            print("i:{} j:{}".format(i, j))
            if i > 0 and check_done(Query.weights, last_weights):
                break;
            mid_step_weights = Query.weights
            for k in range(len(Query.weights)):
                Query.weights[k] = Query.weights[k] + learning_rate*(num_off[0] - last_num_correct)*weight_slope(num_off[0], last_num_correct, Query.weights[k], last_weights[k])
        last_num_correct = num_off[0]
        last_weights = mid_step_weights
        print(Query.weights[k])
    print('Weight 0 = ', Query.weights[0])
    print('Weight 1 = ', Query.weights[1])
    print('Weight 2 = ', Query.weights[2])
    print('Weight 3 = ', Query.weights[3])
    print('Weight 4 = ', Query.weights[4])
    print('Weight 5 = ', Query.weights[5])
    print('Weight 6 = ', Query.weights[6])
    print('Weight 7 = ', Query.weights[7])

main()

