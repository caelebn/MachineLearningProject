import numpy as np
import matplotlib.pyplot as plt
import TestBase
import KNN
import Review 
	
	
def get_percent_uppercase(text):
    # Returns the percentage of uppercase words in the text review
    num_upper_words = 0
    for word in text.split():
        if word.isupper() and len(word) > 1:  # Checks length so words like 'A' and 'I' are excluded
            num_upper_words += 1
    return num_upper_words / max(1, len(text.split()))


reviews = [[],[],[],[],[]]
location_base = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\\'
datasets = ['reviews_Automotive_5.json.gz',
            'reviews_Musical_Instruments_5.json.gz',
            'reviews_Patio_Lawn_and_Garden_5.json.gz',
            'reviews_Amazon_Instant_Video_5.json.gz']
for d in datasets:
    for curr in TestBase.parse(location_base + d):
        reviews[int(curr['overall'])-1].append(get_percent_uppercase(curr['reviewText']))

min = .005
max = .05
num_bins = 10
tick_frequency = max/num_bins

for i in range(5):
    plt.hist(reviews[i], bins=num_bins, range=(min,max))
    plt.xticks(np.arange(0, max, tick_frequency))
    plt.title("{} Star Percent Uppercase".format(i+1))
    plt.xlabel('Uppercase Words (%)')
    plt.ylabel('Frequency')
    plt.show()