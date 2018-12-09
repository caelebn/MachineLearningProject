import KNN
import Review
import TestBase
import Selection


def get_max_weight(tuple_list):
    max = (0, 0)
    for i in range(len(tuple_list)):
        if tuple_list[i][0] > max[0]:
            max = tuple_list[i]
    return max[1]


#  attempts to optimize weights, assuming that weights are independent of each other
def main():
    path = 'Datasets/reviews_Books_5.json.gz'
    weight_range = (0,150)
    queries = TestBase.get_query_list(path, 5*(weight_range[1] - weight_range[0]))
    max_to_grab = TestBase.find_count(queries)
    for i in range(len(Review.weights)):
        num_correct = []
        for j in range(weight_range[0], weight_range[1]):
            num_off = [0] * 5
            off = 0
            Review.weights[i] = j
            current_star = 0
            for k in range(200):
                knn_val = KNN.guess_review(queries[current_star][j])
                current_star = (current_star + 1)%5
                curr_off = abs(current_star+1 - knn_val)  # actual - estimate
                num_off[curr_off] += 1
                off += curr_off
            print("i:{} j:{}".format(i, j))
            num_correct.append((num_off[0], j))
        Review.weights[i] = get_max_weight(num_correct)
        print(Review.weights[i])
    for i in range(len(Review.weights)):
        print("Weight {} = {}".format(i, Review.weights[i]))


main()

