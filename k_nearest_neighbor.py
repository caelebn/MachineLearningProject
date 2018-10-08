import math
import gzip


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
#  OUTPUTS: tuple(query, nearest_neighbor, distance)- a tuple containing the original query and its nearest neighbor,
#               along with the distance between them
#  INFO: Goes through the tuples list and compares the distance to the query, saving off the shortest distance and
#           tuple.
#  FUNCTION STATUS: NEEDS REVIEW


def find_nearest_neighbor(query, tuples):
    shortest_distance = 99999999
    closest_tuple = tuples[0]
    for i in range(0, len(tuples)):
        curr_distance = calculate_2way_distance(query, tuples[i])
        print('', query, ' ', tuples[i], ' distance = ', curr_distance)
        if curr_distance < shortest_distance:
            shortest_distance = curr_distance
            closest_tuple = tuples[i]
    return query, closest_tuple, shortest_distance

#  define_base_review_tuples()
#  INPUTS: path - the relative path to the dataset
#  OUTPUTS: review_tuples- a list of all base review tuples
#  INFO: goes through the dataset and puts all data into a list of tuples
#        including final stars given (overall), review text (reviewText), and helpfulness (helpful)
#  FUNCTION STATUS: INCOMPLETE


def define_base_review_tuples(path):
    review_tuples = []
    count = 0
    for review in parse(path):
        review_tuples.append((review['overall'], review['reviewText'], review['helpful']))
        count += 1
    print(sum(review_tuples[i][0] for i in range(0, count)) / len(review_tuples))
    print('Review at index 1 = ', review_tuples[1][1])
    print('\tHelpfulness: ', review_tuples[1][2])
    print('Count: ', count)
    return review_tuples

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


def main():
    t1 = (5, 10, 15)
    t2 = (10, 15, 20)
    t3 = (50, 100, 150)
    distance = calculate_2way_distance(t1, t2)
    print('distance', distance)
    distances = calculate_distance_list([t1, t2, t3])
    print('distance tuples', distances)

    print('Enter query tuple[0]: ')
    p1 = input('INT: ')
    print('Enter query tuple[1]: ')
    p2 = input('INT: ')
    print('Enter query tuple[2]: ')
    p3 = input('INT: ')
    query = (int(p1), int(p2), int(p3))

    knn = find_nearest_neighbor(query, [t1, t2, t3])
    print('KNN: ', knn)

    path = 'Datasets/reviews_Musical_Instruments_5.json.gz'
    review_tuples = define_base_review_tuples(path)
    num_review_words = count_review_words(review_tuples)
    print('WORD COUNT OF INDEX 10260 = ', num_review_words[10260])


main()
