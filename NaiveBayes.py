import Review
import pickle
import gzip
import io
import os
from collections import Counter

#  p(b|a) = p(a|b)*p(b)/p(a)
#  p(stars | reviewData) = p(reviewData | stars) * p(stars) / p(reviewData)


# guesses the review stars
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
    # print(guess_list)
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


# finds the probability of each review point
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


    # probs_uppercase = []
    # probs_polarity = []
    # probs_richness = []

    # for k, v in unique_uppercase.items():
    #     prob_elem = float(v / len(l_uppercase))
    #     print(k, ' ', prob_elem)
    #     probs_uppercase.append((k, prob_elem))
    #
    # for k, v in unique_polarity.items():
    #     prob_elem = float(v / len(l_polarity))
    #     print(k, ' ', prob_elem)
    #     probs_polarity.append((k, prob_elem))
    #
    # for k, v in unique_richness.items():
    #     prob_elem = float(v / len(l_richness))
    #     print(k, ' ', prob_elem)
    #     probs_richness.append((k, prob_elem))

    # return probs_uppercase, probs_polarity, probs_richness
    return p_upper, p_pol, p_rich

# finds the probability of query text data points
def get_p_text_of_query(query, base_text_data):
    probs_uppercase = base_text_data[0]
    probs_polarity = base_text_data[1]
    probs_richness = base_text_data[2]

    q_uppercase = query.get_raw_points()[0]
    q_polarity = query.get_raw_points()[1]
    q_richness = query.get_raw_points()[2]

    shortest_dist = 999999
    closest_index = 0
    for i in range(0, len(probs_uppercase)):
        current_val = abs(q_uppercase - probs_uppercase[i][0]) + abs(q_polarity - probs_polarity[i][0]) + \
                      abs(q_richness - probs_richness[i][0])
        if current_val < shortest_dist:
            closest_index = i
            shortest_dist = current_val
    # print('SHORTEST DISTANCE = ', shortest_dist)
    return probs_uppercase[closest_index][1], probs_polarity[closest_index][1], probs_richness[closest_index][1]


# finds the probability of review data occurring given the number of stars
def find_p_reviewdata_given_star(query, reviews):
    tot_uppercase = [0, 0, 0, 0, 0]  # one, two, three, four, five star
    tot_polarity = [0, 0, 0, 0, 0]
    tot_richness = [0, 0, 0, 0, 0]
    tots = [0, 0, 0, 0, 0]  # number of each review

    for r in reviews:
        index = r.get_overall() - 1
        up = r.get_raw_points()[0]
        pol = r.get_raw_points()[1]
        rich = r.get_raw_points()[2]
        tot_uppercase[index] += up
        tot_polarity[index] += pol
        tot_richness[index] += rich
        tots[index] += up + abs(pol) + rich

    q_points = query.get_raw_points()
    q_tot = q_points[0] + q_points[1] + q_points[2]

    p1 = float(float(tot_uppercase[0] / tots[0]) *
               float(tot_polarity[0] / tots[0]) * float(tot_richness[0] / tots[0])) * q_tot

    p2 = float(float(tot_uppercase[1] / tots[1]) *
               float(tot_polarity[1] / tots[1]) * float(tot_richness[1] / tots[1])) * q_tot

    p3 = float(float(tot_uppercase[2] / tots[2]) *
               float(tot_polarity[2] / tots[2]) * float(tot_richness[2] / tots[2])) * q_tot

    p4 = float(float(tot_uppercase[3] / tots[3]) *
               float(tot_polarity[3] / tots[3]) * float(tot_richness[3] / tots[3])) * q_tot

    p5 = float(float(tot_uppercase[4] / tots[4]) *
               float(tot_polarity[4] / tots[4]) * float(tot_richness[4] / tots[4])) * q_tot

    return p1, p2, p3, p4, p5


path = 'Datasets/reviews_Automotive_5.json.gz'


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

    correctness = [0, 0, 0, 0, 0]
    counter = 0
    for q in parse(qPath):
        print('Guessing query #', counter)
        query = Review.Query(q['reviewText'])
        p_text = find_base_text_probability(query, reviews)
        p_review_from_stars = find_p_reviewdata_given_star(query, reviews)
        guess = guess_stars(query, p_stars, p_review_from_stars, p_text)

        actual = int(q['overall'])

        index = abs(int(guess) - int(actual))
        correctness[index] += 1

        counter += 1
        if counter >= num_data_points:
            break

    print('Correctness List: (0 off, 1 off, 2 off, 3 off, 4 off = ')
    print('\t', correctness)


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

    # reviews = gen_even_list(reviews)

    query = Review.Query((input('Enter text review: ')))

    p_stars = find_base_star_probabilities(reviews)
    p_text_data = find_base_text_probability(query, reviews)
    p_review_from_stars = find_p_reviewdata_given_star(query, reviews)
    print(p_review_from_stars)
    guess = guess_stars(query, p_stars, p_review_from_stars, p_text_data)

    print('GUESS: ', str(guess))


q_Path = 'Datasets/reviews_Amazon_Instant_Video_5.json.gz'
datapath = 'Datasets/reviews_Patio_Lawn_and_Garden_5.json.gz'
max_num = 400
# enter_one_query(datapath)
main(q_Path, datapath, max_num)