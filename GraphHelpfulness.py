import numpy as np
import matplotlib.pyplot as plt
import TestBase
import KNN
import Review 
	



reviews = [[],[],[],[],[]]
location_base = r'C:\Users\mdhal\Desktop\Fall 2018\Machine Learning\Project\Compressed\\'
datasets = ['reviews_Automotive_5.json.gz',
            'reviews_Musical_Instruments_5.json.gz',
            'reviews_Patio_Lawn_and_Garden_5.json.gz',
            'reviews_Amazon_Instant_Video_5.json.gz']
for d in datasets:
    for curr in TestBase.parse(location_base + d):
        reviews[int(curr['overall'])-1].append(curr['helpful'][1])

min = 0
max = 15
num_bins = 15
tick_frequency = max/num_bins

for i in range(5):
    plt.hist(reviews[i], bins=num_bins, range=(min,max))
    plt.xticks(np.arange(0, max, tick_frequency))
    plt.title("{} Star Unhelpfulness".format(i+1))
    plt.xlabel('Number of People Who Found It Unhelpful')
    plt.ylabel('Frequency')
    plt.show()