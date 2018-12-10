import math
import gzip
import io
import Review
import pickle
import os.path
import bisect
import Selection
from operator import itemgetter

review_points_list = [[],[],[],[],[]]
reviews = [[],[],[],[],[]]

n = 751 #only if not using sqrt(n)
set_name = 'Video_Games'
path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_' + set_name + '_5.json.gz'

def parse(path):
    gz = gzip.open(path, 'rb')
    f = io.BufferedReader(gz)
    for l in f:
        yield eval(l)
    gz.close()

def load_tuple_data():
    global review_points_list
    with open('Datasets/' + set_name + '_tuple_data.pkl', 'rb') as f:
        review_points_list = pickle.load(f)
    f.close()
    if not review_points_list[0]:
        make_review_points_list()

def dump_tuple_data():
    global set_name
    with open('Datasets/' + set_name + '_tuple_data.pkl', 'wb') as f:
        pickle.dump(review_points_list, f)
    f.close()

#used exclusively in classes that graph data
def get_tuple_data():
    return review_points_list

#  make_review_list()
#  INPUTS: path- the path to the dataset
#  OUTPUTS: reviews- a list of Review objects
#  INFO:  Makes a list of Review objects from the given dataset
def make_review_list(location = path):
    global reviews
    for curr in parse(location):
        review = Review.Review(curr['reviewText'], curr['helpful'][0], curr['helpful'][1], curr['overall'])
        reviews[review.get_overall()-1].append(review)

#  get_most_occurring(vals)
#  Finds the overall rating that occurs most out of the nearest neighbors
def get_most_occurring(vals):
    starCount = [0] * 5
    for val in vals:
        starCount[val[1]] += 1
    return starCount.index(max(starCount)) + 1


#  calculate_manhattan_distance
# Calculates the manhattan distance between two lists
def calculate_manhattan_distance(t1, t2):
    sum_total = 0
    for i in range(len(t1)):
        sum_total += abs(t1[i] - t2[i])
    return sum_total

#def calculate_euclidean_distance(t1, t2):
#    sum_total = 0
#    for index in range(0, len(t1)):
#        difference = t1[index] - t2[index]
#        two_point_diffsq = difference * difference
#        sum_total += two_point_diffsq
#    return math.sqrt(sum_total)



#  find_nearest_neighbors(query, points_list, k)
#  INPUTS: query - the tuple to be compared to the list of tuples.
#          points_list - the pre-existing list of tuples that will be compared against.
#          k - the number of neighbors to grab
#  OUTPUTS: a list of tuples, each containing containing the distance and its rating
#  INFO: Goes through the tuples list and compares the distance to the query
def find_nearest_neighbors(query, points_list, k = n):
    distances = []
    for i in range(5):
        for j in range(len(points_list[i])):
            distances.append((calculate_manhattan_distance(query, points_list[i][j]), i))
    return Selection.select(distances, k)

#get_max_overall_allowed
#finds which overall number has the lowest amount of reviews, and
#returns the number of reviews with that overall
def get_max_overall_allowed(review_list):
    return min(len(x) for x in review_list)

#  make_review_points_list()
#  INPUTS: path- path to dataset
#  OUTPUTS: tuples_list - a list of tuples of the data points from the reviews list.
#           format = ((d1, d2, ... , dn), overall)
def make_review_points_list(location = path):
    global review_points_list, reviews
    print("Creating all review points. This may take a while")
    make_review_list(location)
    max_allowed = get_max_overall_allowed(reviews)
    for i in range(5):
        for j in range(max_allowed):
            review_points_list[i].append(reviews[i][j].get_points())
    dump_tuple_data()

#  make_review_points_list()
#  INPUTS: path- path to dataset
#  OUTPUTS: tuples_list - a list of tuples of the data points from the reviews list.
#           format = ((d1, d2, ... , dn), overall)
def update_review_points_list():
    global review_points_list, reviews
    for i in range(5):
        for j in range(get_max_overall_allowed(reviews)):
            review_points_list[i].append(reviews[i][j].get_points())
    dump_tuple_data()

def set_review_points_list(list):
    global review_points_list
    review_points_list = list

def guess_review(query):
    global review_points_list, n
    if not review_points_list[0]:
        load_tuple_data()
    query = Review.Query(query[0], query[1], query[2])
    query_points = query.get_points()
    output = find_nearest_neighbors(query_points, review_points_list, n)
    return get_most_occurring(output)

def guess_tuple(tuple):
    global review_points_list, n
    if not review_points_list[0]:
        load_tuple_data()
    output = find_nearest_neighbors(tuple, review_points_list, n)
    return get_most_occurring(output)

if(__name__ == '__main__'):
    text = input('Enter a text review: ')
    helpful = int(input('Enter helpful: '))
    not_helpful = int(input('Enter not helpful: '))
    load = str(input('Use existing review tuples? (Y/N) '))
    if load.upper()[0] == 'N' or not os.path.isfile('Datasets/tuple_data.pkl'):
        make_review_points_list()
    print(guess_review((text, helpful, not_helpful)))