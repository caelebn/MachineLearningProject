import Review
import pickle
import gzip
import io
import os
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#  p(b|a) = p(a|b)*p(b)/p(a)
#  p(stars | reviewData) = p(reviewData | stars) * p(stars) / p(reviewData)


# guesses the review stars based off of the probabilities calculated from other functions
# returns the star number with the highest probability
def guess_stars(query, p_stars, p_review_from_stars, base_text_data):
    # p_text_of_query = get_p_text_of_query(query, base_text_data)
    p_text_of_query = base_text_data
    # print('P(text) = ', p_text_of_query)
    # print('P(stars) = ', p_stars)
    # print('P(reviewFromStars) = ', p_review_from_stars)
    overall_p = abs(p_text_of_query[0]) + abs(p_text_of_query[1]) + abs(p_text_of_query[2])
    p1 = float(float(abs(p_review_from_stars[0]) * p_stars[0]) / overall_p)
    p2 = float(float(abs(p_review_from_stars[1]) * p_stars[1]) / overall_p)
    p3 = float(float(abs(p_review_from_stars[2]) * p_stars[2]) / overall_p)
    p4 = float(float(abs(p_review_from_stars[3]) * p_stars[3]) / overall_p)
    p5 = float(float(abs(p_review_from_stars[4]) * p_stars[4]) / overall_p)

    # overall_p = (abs(p_text_of_query[0]) + abs(p_text_of_query[1]) + abs(p_text_of_query[2])) / 3
    # p1 = float(float(overall_p * p_stars[0]) / abs(p_review_from_stars[0]))
    # p2 = float(float(overall_p * p_stars[1]) / abs(p_review_from_stars[1]))
    # p3 = float(float(overall_p * p_stars[2]) / abs(p_review_from_stars[2]))
    # p4 = float(float(overall_p * p_stars[3]) / abs(p_review_from_stars[3]))
    # p5 = float(float(overall_p * p_stars[4]) / abs(p_review_from_stars[4]))

    guess_list = [p1, p2, p3, p4, p5]
    print(guess_list)
    guess_list = sorted(guess_list)
    return_val = 0
    if guess_list[4] == p1:
        return_val = 1
    elif guess_list[4] == p2:
        return_val = 2
    elif guess_list[4] == p3:
        return_val = 3
    elif guess_list[4] == p4:
        return_val = 4
    elif guess_list[4] == p5:
        return_val = 5

    return return_val


# finds the probability of each star review occurring
def find_base_star_probabilities(reviews):
    #  finds the base probability of any star occurring
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    tot = 0
    for r in reviews:
        if r.get_overall() == 1:
            num1 += 1
        elif r.get_overall() == 2:
            num2 += 1
        elif r.get_overall() == 3:
            num3 += 1
        elif r.get_overall() == 4:
            num4 += 1
        elif r.get_overall() == 5:
            num5 += 1
        tot += 1
    p1 = float(num1/tot)
    p2 = float(num2/tot)
    p3 = float(num3/tot)
    p4 = float(num4/tot)
    p5 = float(num5/tot)

    return p1, p2, p3, p4, p5  # p(stars)


# finds the probability of each review point given a set of reviews and a query
# accomplishes this by counting the total number of reviews (including query) with the same text points as the query
#   then divides this number by the total number of reviews
def find_base_text_probability(query, reviews):
    l_uppercase = []
    l_polarity = []
    l_richness = []
    for r in reviews:
        l_uppercase.append(r.get_raw_points()[0])
        l_polarity.append(r.get_raw_points()[1])
        l_richness.append(r.get_raw_points()[2])
        # print('TEST: ', r.get_raw_points()[0])

    l_uppercase.append(query.get_raw_points()[0])
    l_polarity.append(query.get_raw_points()[1])
    l_richness.append(query.get_raw_points()[2])

    unique_uppercase = Counter(l_uppercase)
    unique_polarity = Counter(l_polarity)
    unique_richness = Counter(l_richness)
    # print('UNIQUE_UPPER = ', unique_uppercase)
    # print('LENGTH UNIQUE_UPPERCASE_KEYS = ', len(unique_uppercase.keys()))
    # print('COUNTED UPPERCASE: ', unique_uppercase)

    p_upper = 0
    p_pol = 0
    p_rich = 0
    for k, v in unique_uppercase.items():
        if query.get_raw_points()[0] == k:
            p_upper = float(v / len(l_uppercase))
            # print('K = ', k)
            break

    for k, v in unique_polarity.items():
        if query.get_raw_points()[1] == k:
            p_pol = float(v / len(l_polarity))
            # print('K = ', k)
            break

    for k, v in unique_richness.items():
        if query.get_raw_points()[2] == k:
            p_rich = float(v / len(l_richness))
            # print('K = ', k)
            break

    return p_upper, p_pol, p_rich


# calculates the probability of text given the number of stars
#   calls the find_base_text_probability function on lists of reviews of a particular star
#   returns a list of probabilities of each star type
def get_ptext_given_stars(query, reviews):
    r1 = []
    r2 = []
    r3 = []
    r4 = []
    r5 = []

    for r in reviews:
        if r.get_overall() == 1:
            r1.append(r)
        elif r.get_overall() == 2:
            r2.append(r)
        elif r.get_overall() == 3:
            r3.append(r)
        elif r.get_overall() == 4:
            r4.append(r)
        else:
            r5.append(r)

    t1 = find_base_text_probability(query, r1)
    t2 = find_base_text_probability(query, r2)
    t3 = find_base_text_probability(query, r3)
    t4 = find_base_text_probability(query, r4)
    t5 = find_base_text_probability(query, r5)

    # p1 = t1[0] + t1[1] + t1[2]
    # p2 = t2[0] + t2[1] + t2[2]
    # p3 = t3[0] + t3[1] + t3[2]
    # p4 = t4[0] + t4[1] + t4[2]
    # p5 = t5[0] + t5[1] + t5[2]

    p1 = t1[0] * t1[1] * t1[2]
    p2 = t2[0] * t2[1] * t2[2]
    p3 = t3[0] * t3[1] * t3[2]
    p4 = t4[0] * t4[1] * t4[2]
    p5 = t5[0] * t5[1] * t5[2]

    return p1, p2, p3, p4, p5


path = 'Datasets/reviews_Automotive_5.json.gz'


# used to parse a gzip file
def parse(p):
    gz = gzip.open(p, 'rb')
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

    return review_points_list


def dump_tuple_data(data):
    with open('Datasets/tuple_dataNB.pkl', 'wb') as f:
        pickle.dump(data, f)
    f.close()


# used exclusively in classes that graph data
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


# def calculate_euclidean_distance(t1, t2):
#    sum_total = 0
#    for index in range(0, len(t1)):
#        difference = t1[index] - t2[index]
#        two_point_diffsq = difference * difference
#        sum_total += two_point_diffsq
#    return math.sqrt(sum_total)


# get_max_overall_allowed
# finds which overall number has the lowest amount of reviews, and
# returns the number of reviews with that overall
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


def read_list_to_reviews(org):
    reviews = []
    for r in org:
        print(r)
        curr = Review.Review(r[0], r[1])
        reviews.append(curr)
    return reviews


# returns a list of reviews with the same amount of each overall
def gen_even_list(reviews):
    nums = [0]*5

    for r in reviews:
        nums[r.get_overall()-1] += 1

    lowest = sorted(nums)[0]

    n_revs = []
    count = [0]*5
    for r in reviews:
        if count[0] < lowest and r.get_overall() == 1:
            n_revs.append(r)
            count[0] += 1
        elif count[1] < lowest and r.get_overall() == 2:
            n_revs.append(r)
            count[1] += 1
        elif count[2] < lowest and r.get_overall() == 3:
            n_revs.append(r)
            count[2] += 1
        elif count[3] < lowest and r.get_overall() == 4:
            n_revs.append(r)
            count[3] += 1
        elif count[4] < lowest and r.get_overall() == 5:
            n_revs.append(r)
            count[4] += 1

    # print('TOTAL COUNT: ', count)
    return n_revs


# used to plot the final confusion matrix
def plot_confusion_matrix(con_mat, title='NB Confusion Matrix', cmap=plt.cm.gray_r):
    plt.matshow(con_mat, cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(con_mat.columns))
    plt.xticks(tick_marks, con_mat.columns, rotation=45)
    plt.yticks(tick_marks, con_mat.index)
    plt.tight_layout()
    plt.ylabel(con_mat.index.name)
    plt.xlabel(con_mat.columns.name)
    plt.show()


# runs a number of reviews (num_data_points) from a query list using base data list (datapath)
def main(qPath, datapath, num_data_points):
    load = input('Load review data? [y/n]')
    if load.upper()[0] == 'N' or not os.path.isfile('Datasets/tuple_dataNB.pkl'):
        reviews = []
        for curr in parse(datapath):
            review = Review.Review(curr['reviewText'], curr['overall'])
            reviews.append(review)
        with open('Datasets/tuple_dataNB.pkl', 'wb') as f:
            pickle.dump(reviews, f)
        f.close()
    with open('Datasets/tuple_dataNB.pkl', 'rb') as f:
        reviews = pickle.load(f)
    f.close()

    p_stars = find_base_star_probabilities(reviews)

    reviews = gen_even_list(reviews) # makes reviews even number of each star

    correctness = [0, 0, 0, 0, 0]
    guesses = [0, 0, 0, 0, 0]
    g_list = []
    a_list = []
    counter = 0
    for q in parse(qPath):
        print('Guessing query #', counter)
        query = Review.Query(q['reviewText'])
        p_text = find_base_text_probability(query, reviews)
        # p_review_from_stars = find_p_reviewdata_given_star(query, reviews)
        p_review_from_stars = get_ptext_given_stars(query, reviews)
        print('P(Review | Stars) = ', p_review_from_stars)
        guess = guess_stars(query, p_stars, p_review_from_stars, p_text)
        print('GUESS: ', guess)

        guesses[int(guess-1)] += 1

        actual = int(q['overall'])

        g_list.append(guess)
        a_list.append(actual)

        index = abs(int(guess) - int(actual))
        correctness[index] += 1

        counter += 1
        if counter >= num_data_points:
            break

    print('Correctness List: 0 off, 1 off, 2 off, 3 off, 4 off = ')
    print('\t', correctness)

    print('Guesses List: 1, 2, 3, 4, 5')
    print('\t', guesses)

    pred = pd.Series(g_list, name='Predicted')
    actu = pd.Series(a_list, name='Actual')

    df_confusion = pd.crosstab(actu, pred, rownames=['Actual'], colnames=['Predicted'], margins=True)

    print(df_confusion)
    plot_confusion_matrix(df_confusion)


# used to test a single inputted query
def enter_one_query(datapath):
    load = input('Load data? [y/n]')
    if load.upper() == 'N':
        reviews = []
        for curr in parse(datapath):
            review = Review.Review(curr['reviewText'], curr['overall'])
            reviews.append(review)
        with open('Datasets/tuple_dataNB.pkl', 'wb') as f:
            pickle.dump(reviews, f)
        f.close()
    with open('Datasets/tuple_dataNB.pkl', 'rb') as f:
        reviews = pickle.load(f)
    f.close()

    reviews = gen_even_list(reviews)

    query = Review.Query((input('Enter text review: ')))

    p_stars = find_base_star_probabilities(reviews)
    p_text_data = find_base_text_probability(query, reviews)
    p_review_from_stars = get_ptext_given_stars(query, reviews)
    print(p_review_from_stars)
    guess = guess_stars(query, p_stars, p_review_from_stars, p_text_data)

    print('GUESS: ', str(guess))


q_Path = 'Datasets/reviews_Musical_Instruments_5.json.gz'
d = 'Datasets/reviews_Toys_and_Games_5.json.gz'
max_num = 1500
# enter_one_query(d)
main(q_Path, d, max_num)
