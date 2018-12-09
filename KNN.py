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

n = 101
path = 'Datasets/reviews_Automotive_5.json.gz'

def parse(path):
    gz = gzip.open(path, 'rb')
    f = io.BufferedReader(gz)
    for l in f:
        yield eval(l)
    gz.close()

def load_tuple_data():
    global review_points_list
    with open('Datasets/tuple_data.pkl', 'rb') as f:
        review_points_list = pickle.load(f)
    f.close()
    if not review_points_list[0]:
        make_review_points_list()

def dump_tuple_data():
    with open('Datasets/tuple_data.pkl', 'wb') as f:
        pickle.dump(review_points_list, f)
    f.close()

#used exclusively in classes that graph data
def get_tuple_data():
    return review_points_list

#  make_review_list()
#  INPUTS: path- the path to the dataset
#  OUTPUTS: reviews- a list of Review objects
#  INFO:  Makes a list of Review objects from the given dataset
def make_review_list(path):
    reviews = []
    for i in range(5):
        reviews.append([])
    for curr in parse(path):
        review = Review.Review(curr['reviewText'], curr['overall'])
        reviews[review.get_overall()-1].append(review)
    return reviews

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
    star_count = [0]*5
    for i in range(5):
        star_count[i] = len(review_list[i])
    return min(star_count, key=int)

#  make_review_points_list()
#  INPUTS: path- path to dataset
#  OUTPUTS: tuples_list - a list of tuples of the data points from the reviews list.
#           format = ((d1, d2, ... , dn), overall)
def make_review_points_list(location = path):
    print("Creating all review points. This may take a while")
    reviews = make_review_list(location)
    for i in range(5):
        for j in range(get_max_overall_allowed(reviews)):
            review_points_list[i].append(reviews[i][j].get_points())
    dump_tuple_data()
    return review_points_list

def guess_review(text):
    global review_points_list, n
    if not review_points_list[0]:
        load_tuple_data()
    query = Review.Query(text)
    query_points = query.get_points()
    output = find_nearest_neighbors(query_points, review_points_list, n)
    return get_most_occurring(output)

def main():
    text = input('Enter a text review: ')
    load = str(input('Use existing review tuples? (Y/N) '))
    if load.upper()[0] == 'N' or not os.path.isfile('Datasets/tuple_data.pkl'):
        make_review_points_list()
    print(guess_review(text))

#main()