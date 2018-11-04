import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

class Query:
    positive_words = []
    negative_words = []
    emphasis_words = []

    #  Initializer
    def __init__(self, text):
        self.text = text
        self.net_negative_weight = 200  # from 0 to 1
        self.net_neutral_weight = 30    # from 0 to 1
        self.net_compound_weight = 20   # from 0 to 1
        self.net_positive_weight = 200  # from 0 to 1
        self.uppercase_weight = 70 # from 0 to 1
        self.spec_char_weight = 2
        self.sentence_length_weight = 20 # from 0 to 6
        self.richness_weight = 50 #experimental
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

    def get_net_negativity(self):
        return self.polarity_negative

    def get_net_neutrality(self):
        return self.polarity_neutral

    def get_net_compound(self):
        return self.polarity_compound

    def get_net_positivity(self):
        return self.polarity_positive

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

    @staticmethod
    def get_emphasis_words():
        if len(Query.emphasis_words) == 0:
            with open('Datasets/negative_words.txt', 'r') as emp_file:
                Query.emphasis_words = emp_file.read().upper().splitlines()
            emp_file.close()
        return Query.emphasis_words

    def get_points(self):
        return (self.percent_uppercase() * self.uppercase_weight,
                self.num_special_chars() * self.spec_char_weight,
                self.get_net_negativity() * self.net_negative_weight,
                self.get_net_neutrality() * self.net_neutral_weight,
                self.get_net_compound() * self.net_compound_weight,
                self.get_net_positivity() * self.net_positive_weight,
                self.get_average_sentence_length() * self.sentence_length_weight,
                self.get_richness() * self.richness_weight)


class Review(Query):

    #  Initializer
    def __init__(self, text, overall):
        Query.__init__(self, text)
        self.overall = overall

    def get_overall(self):
        return self.overall
