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
        queries[int(curr['overall'])-1].append((curr['reviewText'], curr['helpful'][0], curr['helpful'][1]))
        if find_count(queries) >= num_tests:
            return queries
    return queries

def find_count(queries):
    return min(len(x) for x in queries)