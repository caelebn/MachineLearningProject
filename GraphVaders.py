import numpy as np
import matplotlib.pyplot as plt
import TestBase
import KNN
import Review
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

sid = SentimentIntensityAnalyzer()

def get_net_positivity(text):
        total_negative = 0
        total_neutral = 0
        total_compound = 0
        total_positive = 0
        sentences = text.split('.')
        for sentence in sentences:
            ps = sid.polarity_scores(sentence)
            total_negative += ps.get('neg')
            total_neutral += ps.get('neu')
            total_compound += ps.get('compound')
            total_positive += ps.get('pos')
        num_sentences = max(1, len(sentences))
        polarity_negative = total_negative / num_sentences
        polarity_neutral = total_neutral / num_sentences
        polarity_compound = total_compound / num_sentences
        polarity_positive = total_positive / num_sentences
        return [polarity_negative, polarity_neutral, polarity_compound, polarity_positive]


reviews = [[],[],[],[],[]]
location_base = 'Datasets/'
datasets = ['reviews_Musical_Instruments_5.json.gz',
            'reviews_Automotive_5.json.gz',
            'reviews_Patio_Lawn_and_Garden_5.json.gz']
            #'reviews_Amazon_Instant_Video_5.json.gz']
for d in datasets:
    for curr in TestBase.parse(location_base + d):
        reviews[int(curr['overall'])-1].append(get_net_positivity(curr['reviewText']))

min = 0
max = 0.3
num_bins = 15
tick_frequency = (max-min)/num_bins


for i in range(5):
    plt.hist([x[0] for x in reviews[i]], bins=num_bins, range=(min,max))
    plt.xticks(np.arange(min, max, tick_frequency))
    plt.title("{} Star Sentence Negativity".format(i+1))
    plt.xlabel('Sentence Negativity')
    plt.show()

#plt.xlabel('Sentence Neutrality (%)')

#for i in range(5):
#    plt.hist([x[1] for x in reviews[i]], bins=num_bins)#, range=(min,max))
#    plt.xticks(np.arange(min, max, tick_frequency))
#    plt.title("{} Star Sentence Neutrality".format(i+1))
#    plt.show()

#plt.xlabel('Sentence Compounds (%)')

#for i in range(5):
#    plt.hist([x[2] for x in reviews[i]], bins=num_bins)#, range=(min,max))
#    plt.xticks(np.arange(min, max, tick_frequency))
#    plt.title("{} Star Sentence Compounds".format(i+1))
#    plt.show()

#plt.xlabel('Sentence Positivity (%)')

#for i in range(5):
#    plt.hist([x[3] for x in reviews[i]], bins=num_bins)#, range=(min,max))
#    plt.xticks(np.arange(min, max, tick_frequency))
#    plt.title("{} Star Sentence Positivity".format(i+1))
#    plt.show()