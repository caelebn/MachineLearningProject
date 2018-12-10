import KNN
import Review
import gzip
import pickle
import TestBase
import matplotlib.pyplot as plt

#weight being trained
k = 2
weight_data = [[],[]]

def weight_slope(num_correct, last_num_correct, curr_weight, last_weight):
    if curr_weight == last_weight:
        return 1
    return (num_correct - last_num_correct) / (curr_weight - last_weight)


#attempts to optimize weights, assuming that weights are independent of each other
def main():
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Books_5.json.gz'
    num_tests = 50
    max_iterations = 50
    queries = TestBase.get_query_list(path, num_tests*max_iterations)
    last_num_correct = 0
    learning_rate = 15
    last_weight = 0
    delta = 5
    hasChanged = False
    stayFlatCount = 10
    max_to_grab = TestBase.find_count(queries)
    for j in range(max_iterations):
        num_off = [0] * 5
        off = 0
        for l in range(5):
            for i in range(max_to_grab):
                knn_val = KNN.guess_review(queries[l][i])
                curr_off = abs(l+1 - knn_val)  # actual - estimate
                num_off[curr_off] += 1
                off += curr_off
                print("i:{} j:{}".format(i, j))
        weight_data[0].append(Review.weights[k])
        weight_data[1].append(num_off[0]/off)
        Review.weights[k] = Review.weights[k] + delta
        if hasChanged:
            delta = learning_rate*(num_off[0] - last_num_correct) \
                    * weight_slope(num_off[0], last_num_correct, Review.weights[k], last_weight)
        KNN.update_review_points_list()
        if(max(.00001, abs(last_weight - Review.weights[k])) == 0.00001):
            if hasChanged:
                stayFlatCount = stayFlatCount - 1
                if stayFlatCount <= 0:
                    break
        else:
            stayFlatCount = 10
        if last_num_correct != num_off[0]:
            hasChanged = True
        last_num_correct = num_off[0]
        last_weight = Review.weights[k]
        print(Review.weights[k])
    print("Optimized weight: {}".format(Review.weights[k]))

    plt.plot(weight_data[0], weight_data[1])
    plt.title('Compound Weight vs. Accuracy')
    plt.xlabel('Weight')
    plt.ylabel('Accuracy (%)')
    plt.show()

main()
