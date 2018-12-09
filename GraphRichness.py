import numpy as np
import matplotlib.pyplot as plt
import TestBase
import KNN
import Review

def get_richness(text):
        length = max(1, len(text))
        return len(set(text)) / length

reviews = [[],[],[],[],[]]
location_base = 'Datasets/'
datasets = ['reviews_Automotive_5.json.gz',
            'reviews_Musical_Instruments_5.json.gz',
            'reviews_Patio_Lawn_and_Garden_5.json.gz',
            'reviews_Amazon_Instant_Video_5.json.gz']
for d in datasets:
    for curr in TestBase.parse(location_base + d):
        reviews[int(curr['overall'])-1].append(get_richness(curr['reviewText']))

min = 0
max = 0.4
num_bins = 16
tick_frequency = (max-min)/num_bins

for i in range(5):
    plt.hist(reviews[i], bins=num_bins, range=(min,max))
    plt.xticks(np.arange(min, max, tick_frequency))
    plt.title("{} Star Richness".format(i+1))
    plt.xlabel('Richness (%)')
    plt.ylabel('Frequency')
    plt.show()