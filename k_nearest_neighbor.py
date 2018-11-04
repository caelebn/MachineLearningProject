import math
import gzip
import Query
import pickle
import os.path
from operator import itemgetter


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


#  calculate_distance_list(int tuple_size, tuples [])
#  INPUTS: int tuple_size- the size of each of the tuples
#          tuples[]- a list of all tuples that contain data points.
#  OUTPUTS: distances[tuple[t1, t2, d]] - a list of tuples that contain tuple 1, tuple 2, and the distance between them.
#  INFO: calculate_distance_list(...) goes through 0 to n tuples and calculates the distance between the points
#           contained.
#           It does this by calculating all distances between tuples 0 and 1, 0 and 2, ..., 0 and n-1, 1 and 2,
#           ..., 1 and n, ..., n-1, n. It saves each of these couple of points and their correlating distance into a
#           tuple, which is then stored into a list. This list of tuples is returned as the output.
#  FUNCTION STATUS: COMPLETE (NEEDS TESTING)


def calculate_distance_list(tuples):
    distances = []
    for i in range(0, len(tuples)-1):
        for j in range(i+1, len(tuples)):
            dist = calculate_2way_distance(tuples[i], tuples[j])
            t_to_add = (tuples[i], tuples[j], dist)
            distances.append(t_to_add)
    return distances

#  replace_largest_val(l)
#  TODO: Comment this


def replace_largest_val(lis, new_i, distance):
    m_val = max(lis, key=itemgetter(1))
    # print(m_val[1])
    if distance < m_val[1]:
        # print('Replacing ', m_val, ' with ', new_i, ', ', distance)
        lis[lis.index(m_val)] = (new_i, distance)
    return lis

#  get_most_occurring(vals)
#  TODO: Comment this


def get_most_occurring(vals):
    starCount = [0] * 5
    for val in vals:
        starCount[int(val[1])] += 1
    return starCount.index(max(starCount)) + 1


#  calculate_2way_distance(t1, t2)
#  INPUTS: tuple t1- a tuple of data points
#          tuple t2- a tuple of data points
#  OUTPUTS: Euclidean distance between t1 and t2
#  INFO: Calculates the euclidean distance between tuple t1 and tuple t2. Returns the final distance.
#        sqrt((x2-x1)^2 + (y2-y1)^2 + ... + (n2-n1)^2)
#  FUNCTION STATUS: WORKING AS INTENDED


def calculate_2way_distance(t1, t2):
    sum_total = 0
    for index in range(0, len(t1)):
        difference = t1[index] - t2[index]
        two_point_diffsq = difference * difference
        sum_total += two_point_diffsq
    return math.sqrt(sum_total)

#  find_nearest_neighbor(query, tuples)
#  INPUTS: query- the tuple to be compared to the list of tuples.
#          tuples- the pre-existing list of tuples that will be compared against.
#           max - the highest number allowed to calculate to make the number of reviews
#                the same for each overall
#  OUTPUTS: tuple(query, nearest_neighbor, distance, tuples[i][1])- a tuple containing the original query and its
#               nearest neighbor, along with the distance between them, and the overall of the knn tuple
#  INFO: Goes through the tuples list and compares the distance to the query, saving off the shortest distance and
#           tuple.
#  FUNCTION STATUS: NEEDS REVIEW


def find_nearest_neighbors(query, points_list, k):
    distances = []
    for i in range(5):
        for j in range(get_max_overall_allowed(points_list)):
            distances.append((calculate_2way_distance(query, points_list[i][j]), i))
    distances.sort(key=lambda l:l[0])
    return distances[0:k]    

#get_max_overall_allowed
#finds which overall number has the lowest amount of reviews, and
#returns the number of reviews with that overall

def get_max_overall_allowed(points_list):
    star_count = [0]*5
    for i in range(5):
        star_count[i] = len(points_list[i])
    smallest_number = min(star_count, key=int)
    return smallest_number

#  make_review_list()
#  INPUTS: path- the path to the dataset
#  OUTPUTS: reviews- a list of Review objects
#  INFO:  Makes a list of Review objects from the given dataset.


def make_review_list(path):
    reviews = []
    for i in range(5):
        reviews.append([])

    for curr in parse(path):
        review = Query.Review(curr['helpful'], curr['reviewText'], curr['overall'])
        reviews[int(review.get_overall()-1)].append(review)
    return reviews

#  make_review_points_list()
#  INPUTS: path- path to dataset
#  OUTPUTS: tuples_list - a list of tuples of the data points from the reviews list.
#           format = ((d1, d2, ... , dn), overall)


def make_review_points_list(path):
    reviews = make_review_list(path)
    review_points_list = []
    for i in range(5):
        review_points_list.append([])
        for index, curr in enumerate(reviews[i]):
            review_points_list[i].append(curr.get_points())
    with open('Datasets/tuple_data.pkl', 'wb') as f:
        pickle.dump(review_points_list, f)
    f.close()
    return review_points_list

#  count_review_words(base_tuples)
#  INPUTS: base_tuples - the list of base review tuples
#  OUTPUTS: num_review_words - a list of the number of review words for each review.
#  INFO: parses through the base_tuples and counts the number of words in each review, storing the result
#        in a separate list.
#  FUNCTION STATUS: INCOMPLETE


def count_review_words(base_tuples):
    num_review_words = []
    for curr_tuple in base_tuples:
        num_review_words.append(len(curr_tuple[1].split()))
    return num_review_words


def make_test_tuples():
    test_tuples = [((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3),
                   ((0, 0, 0, 0, 0, 0, 0, 0), 3)]
    return test_tuples


def main_helper(text, help1, help2, load):
    query = Query.Query([help1, help2], text)
    query_points = query.get_points()
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Automotive_5.json.gz'
    n = 101
    if load.upper()[0] == 'N' or not os.path.isfile('Datasets/tuple_data.pkl'):
        print('N')
        review_points_list = make_review_points_list(path)
    else:
        with open('Datasets/tuple_data.pkl', 'rb') as f:
            review_points_list = pickle.load(f)
        f.close()
    output = find_nearest_neighbors(query_points, review_points_list, n)
    print(output)
    print(get_most_occurring(output))

def main():
    text = input('Enter a text review: ')
    try:
        helpful = int(input('Enter helpful count: '))
    except:
        helpful = 0
    try:
        not_helpful = int(input('Enter not helpful count: '))
    except:
        not_helpful = 0
    load = str(input('Use existing review tuples? (Y/N) '))
    main_helper(text, helpful, not_helpful, load)

main()