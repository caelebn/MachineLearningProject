import KNN
import Review
import gzip
import pickle
import TestBase

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
    queries = TestBase.get_query_list(path, num_tests*max_iterations)
    off = 0
    last_num_correct = 0
    num_off = [0] * 5
    learning_rate = 0.5
    last_weights = [0]*len(Review.weights)
    max_to_grab = TestBase.find_count(queries)
    for j in range(max_iterations):
        for l in range(5):
            for i in range(max_to_grab):
                knn_val = KNN.guess_review(queries[l][i])
                curr_off = abs(l+1 - knn_val)  # actual - estimate
                num_off[curr_off] += 1
                off += curr_off
                print("i:{} j:{}".format(i, j))
                if i > 0 and check_done(Review.weights, last_weights):
                    break;
                mid_step_weights = Review.weights
                for k in range(len(Review.weights)):
                    Review.weights[k] = Review.weights[k] + learning_rate*(num_off[0] - last_num_correct)*weight_slope(num_off[0], last_num_correct, Review.weights[k], last_weights[k])
        last_num_correct = num_off[0]
        last_weights = mid_step_weights
        print(Review.weights[k])
    print('Weight 0 = ', Review.weights[0])
    print('Weight 1 = ', Review.weights[1])
    print('Weight 2 = ', Review.weights[2])
    print('Weight 3 = ', Review.weights[3])
    print('Weight 4 = ', Review.weights[4])
    print('Weight 5 = ', Review.weights[5])
    print('Weight 6 = ', Review.weights[6])
    print('Weight 7 = ', Review.weights[7])

main()
