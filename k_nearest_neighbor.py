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
            dist = calculate_manhattan_distance(tuples[i], tuples[j])
            t_to_add = (tuples[i], tuples[j], dist)
            distances.append(t_to_add)
    return distances

#  get_most_occurring(vals)
#  Finds the overall rating that occurs most out of the nearest neighbors


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


def calculate_manhattan_distance(t1, t2):
    for i in range(len(t1)):
        sum_total = t1[i] - t2[i]
    return sum_total

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
            distances.append((calculate_manhattan_distance(query, points_list[i][j]), i))
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
        review = Query.Review(curr['reviewText'], curr['overall'])
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

def main_helper(text, make_reviews = False):
    query = Query.Query(text)
    query_points = query.get_points()
    #path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Toys_and_Games_5.json.gz' #37% 1.1 (not sure why it's lower
    path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Automotive_5.json.gz' #41% 1.01 offset with 500
    n = 101 #101
    if make_reviews:
        review_points_list = make_review_points_list(path)
    else:
        with open('Datasets/tuple_data.pkl', 'rb') as f:
            review_points_list = pickle.load(f)
        f.close()
    output = find_nearest_neighbors(query_points, review_points_list, n)
    #print(output)
    #print(get_most_occurring(output))
    return get_most_occurring(output)

def main():
    text = input('Enter a text review: ')
    load = str(input('Use existing review tuples? (Y/N) '))
    if load.upper()[0] == 'N' or not os.path.isfile('Datasets/tuple_data.pkl'):
        make_reviews = True
    else:
        make_reviews = False
    print(main_helper(text, make_reviews))

#main()