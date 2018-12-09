import numpy as np
import matplotlib.pyplot as plt
import TestBase
import KNN
import Review

def get_num_special_chars(text):
    # Returns the number of special characters in the text review
    special_chars_string = "!?"
    num_special_chars = 0
    for character in text:
        if character in special_chars_string:
            num_special_chars += 1
    return num_special_chars

reviews = [[],[],[],[],[]]
location_base = 'Datasets/'
datasets = ['reviews_Automotive_5.json.gz',
            'reviews_Musical_Instruments_5.json.gz',
            'reviews_Patio_Lawn_and_Garden_5.json.gz',
            'reviews_Amazon_Instant_Video_5.json.gz']
for d in datasets:
    for curr in TestBase.parse(location_base + d):
        reviews[int(curr['overall'])-1].append(get_num_special_chars(curr['reviewText']))

min = 1
max = 20
num_bins = 19
tick_frequency = (max-min)/num_bins

for i in range(5):
    plt.hist(reviews[i], bins=num_bins, range=(min,max))
    plt.xticks(np.arange(min, max, tick_frequency))
    plt.title("{} Star Special Character Count".format(i+1))
    plt.xlabel('# Special Characters (? and !)')
    plt.ylabel('Frequency')
    plt.show()