import numpy as np
import matplotlib.pyplot as plt
import TestBase
import KNN
import Review

def get_average_sentence_length(text):
        total_words = 0
        sentences = text.split('.')
        for sent in sentences:
            total_words += len(sent.split())
        total_sentences = max(1, len(sentences))
        return total_words / total_sentences

reviews = [[],[],[],[],[]]
location_base = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\\'
datasets = ['reviews_Automotive_5.json.gz',
            'reviews_Musical_Instruments_5.json.gz',
            'reviews_Patio_Lawn_and_Garden_5.json.gz']
for d in datasets:
    for curr in TestBase.parse(location_base + d):
        reviews[int(curr['overall'])-1].append(get_average_sentence_length(curr['reviewText']))

min = 0
max = 36
num_bins = 12
tick_frequency = (max-min)/num_bins

for i in range(5):
    plt.hist(reviews[i], bins=num_bins, range=(min,max))
    plt.xticks(np.arange(min, max, tick_frequency))
    plt.title("{} Star Average Sentence Lengths".format(i+1))
    plt.xlabel('Sentence Length (# words)')
    plt.ylabel('Frequency')
    plt.show()