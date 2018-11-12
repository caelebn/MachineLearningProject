import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

#0: net_compound_weight   # from -1 to 1
#1: uppercase_weight # from 0 to 1
#2: richness_weight #experimental
weights = [3, 3, 37]

class Query:

    #  Initializer
    def __init__(self, text):
        self.text = text
        self.find_polarity_scores()

    def find_polarity_scores(self):
        sid = SentimentIntensityAnalyzer()
        total_negative = 0
        total_neutral = 0
        total_compound = 0
        total_positive = 0
        sentences = self.text.split('.')
        for sentence in sentences:
            ps = sid.polarity_scores(sentence)
            total_negative += ps.get('neg')
            total_neutral += ps.get('neu')
            total_compound += ps.get('compound')
            total_positive += ps.get('pos')
        num_sentences = max(1, len(sentences))
        self.polarity_negative = total_negative / num_sentences
        self.polarity_neutral = total_neutral / num_sentences
        self.polarity_compound = total_compound / num_sentences
        self.polarity_positive = total_positive / num_sentences

    def get_text(self):
        return self.text

    def count_num_words(self):
        # Returns the total number of words in the text review
        return max(1, len(self.text.split()))

    def percent_uppercase(self):
        # Returns the percentage of uppercase words in the text review
        num_upper_words = 0
        for word in self.text.split():
            if word.isupper() and len(word) > 1:  # Checks length so words like 'A' and 'I' are excluded
                num_upper_words += 1
        return num_upper_words / self.count_num_words()

    def num_special_chars(self):
        # Returns the number of special characters in the text review
        special_chars_string = "!?"
        num_special_chars = 0
        for character in self.text:
            if character in special_chars_string:
                num_special_chars += 1
        return num_special_chars

    def get_average_sentence_length(self):
        total_words = 0
        sentences = self.text.split('.')
        for sent in sentences:
            total_words += len(sent.split())
        total_sentences = max(1, len(sentences))
        average_length = total_words / total_sentences
        if average_length > 35:
            return 6
        if average_length > 25:
            return 5
        if average_length > 15:
            return 4
        if average_length > 8:
            return 3
        if average_length > 3:
            return 2
        if average_length > 1:
            return 1
        return 0

    def get_richness(self):
        length = max(1, len(self.text))
        return len(set(self.text)) / length

    def get_points(self):
        return (self.percent_uppercase() * weights[1],
                self.polarity_compound * weights[0],
                self.get_richness() * weights[2])


class Review(Query):

    #  Initializer
    def __init__(self, text, overall):
        Query.__init__(self, text)
        self.overall = int(overall)

    def get_overall(self):
        return self.overall
