import KNN
import gzip
import pickle

def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)

def get_query_list(path, num_tests):
    queries = []
    for i in range(5):
        queries.append([])
    for curr in parse(path):
        queries[int(curr['overall'])-1].append(curr['reviewText'])
        if find_count(queries) * 5 >= num_tests:
            return queries
    return queries

def find_count(queries):
    star_count = [0]*5
    for i in range(5):
        star_count[i] = len(queries[i])
    smallest_number = min(star_count, key=int)
    return smallest_number