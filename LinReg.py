import Review
from numpy import *
import gzip
import io
import pickle
from sympy import *
import os.path
import nltk

nltk.download('vader_lexicon')

review_points_list = [[], [], [], [], []]

n = 101
path = r'C:\Users\reynoldsz2\Downloads\reviews_Automotive_5.json.gz'



def parse(path):
    gz = gzip.open(path, 'rb')
    f = io.BufferedReader(gz)
    for l in f:
        yield eval(l)
    gz.close()


def dump_tuple_data():
    with open('Datasets/tuple_data.pkl', 'wb') as f:
        pickle.dump(review_points_list, f)
    f.close()


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
        reviews[review.get_overall() - 1].append(review)
    return reviews


#  get_most_occurring(vals)
#  Finds the overall rating that occurs most out of the nearest neighbors


# get_max_overall_allowed
# finds which overall number has the lowest amount of reviews, and
# returns the number of reviews with that overall
def get_max_overall_allowed(review_list):
    star_count = [0] * 5
    for i in range(5):
        star_count[i] = len(review_list[i])
    return min(star_count, key=int)


#  make_review_points_list()
#  INPUTS: path- path to dataset
#  OUTPUTS: tuples_list - a list of tuples of the data points from the reviews list.
#           format = ((d1, d2, ... , dn), overall)
def make_review_points_list(location=path):
    print("Creating all review points. This may take a while")
    reviews = make_review_list(location)
    for i in range(5):
        for j in range(get_max_overall_allowed(reviews)):
            review_points_list[i].append(reviews[i][j].get_points())
    dump_tuple_data()
    return review_points_list


def error(b, m, points):
    total_error = 0
    for i in range(5):
        for j in range(len(points[i])):
            x = points[i][j][0]
            y = points[1][j][1]
            z = points[i][j][2]

            total_error += z - ((m * y ** 2) - (b * x))

    return total_error / float(len(points))


# This would change the size of the steps
def make_steps(b_current, m_current, points, learning_rate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    #for i in range(5):
    #    for j in range(len(points[i])):
    #        x = points[i][j][0]
    #        y = points[1][j][1]
    #        z = points[i][j][2]
    #        b_gradient += -(2 / N) * (y - ((m_current * .5 * x) + (b_current * .5 * z)))
    #        m_gradient += -(2 / N) * x * (y - ((m_current * .5) + (b_current * .5 * z)))
    #new_b = b_current - (learning_rate * b_gradient)
    #new_m = m_current - (learning_rate * m_gradient)
    new_b = 17
    new_m = 17
    return [new_b, new_m]


def gradient_descent(points, starting_b, starting_m, learning_rate, num_iterations):
    b = starting_b
    m = starting_m
    for i in range(num_iterations):
        b, m = make_steps(b, m, points, learning_rate)
        i += 1
    return [b, m]


def run():
    points = make_review_points_list()

    learning_rate = 0.0001
    iterations = 1000
    initial_b = 0  # initial y-intercept guess
    initial_m = 0  # initial slope guess
    print("Starting gradient descent at b = {0}, m = {1}, error = {2}".format(initial_b, initial_m, error(initial_b, initial_m, points)))
    print("Running...")
    [b, m] = gradient_descent(points, initial_b, initial_m, learning_rate, iterations)
    print("After {0} iterations b = {1}, m = {2}, error = {3}".format(iterations, b, m, error(b, m, points)))


if __name__ == '__main__':
    run()
