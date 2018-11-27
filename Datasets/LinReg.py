import Review
from numpy import *
import gzip
import io
import pickle
from sympy import *
import os.path

review_points_list = [[],[],[],[],[]]

n = 101
path = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\reviews_Automotive_5.json.gz'

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
        reviews[review.get_overall()-1].append(review)
    return reviews

#  get_most_occurring(vals)
#  Finds the overall rating that occurs most out of the nearest neighbors


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



def error(points):
    total_error = 0
    for i in range(5):
        for j in range(len(points[i])):

            x = points[i][j][0]
            y = points[1][j][1]
            z = points [i][j][2]

            total_error += z - ((17 * y ** 2) - (17 * x))

    return total_error / float(len(points))


#This would change the size of the steps
#def make_steps(b_current, m_current, points, learningRate):
 #   b_gradient = 0
  #  m_gradient = 0
  #  N = float(len(points))
   # for i in range(5):
    #    for j in range(len(points[i])):
    #         x = points[i][j][0]
    #         y = points[1][j][1]
    #         z = points [i][j][2]
    #         b_gradient += -(2/N) * (y - ((m_current * .5 * x) + ((b_current * .5 * z))))
    #         m_gradient += -(2/N) * x * (y - ((m_current * .5) + ((b_current * .5 * z))))
    #new_b = b_current - (learningRate * b_gradient)
    #new_m = m_current - (learningRate * m_gradient)
#    return [new_b, new_m]



def run():

    points = make_review_points_list()


    iterations = 1000
    print("Starting gradient descent at error = {0}".format(error(points)))
    print ("Running...")
    print ("After {0} iterations, error = {1}".format(iterations, error(points)))





if __name__ == '__main__':
    run()