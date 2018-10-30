class Query:
    positive_words = []
    negative_words = []
    emphasis_words = []

    #  Initializer
    def __init__(self, helpful, text):
        self.helpful = helpful
        self.text = text
        self.net_pos_weight = 20  # 1000
        self.help_weight = 0  # 100
        self.help_votes_weight = 0  # 20
        self.uppercase_weight = 40
        self.spec_char_weight = 3  # 10
        self.sentence_length_weight = 5

    #  Accessor Methods
    def get_helpful_percent(self):
        if self.helpful[1] == 0:
            return 0
        return self.helpful[0] / self.helpful[1]

    def get_help_votes(self):
        return self.helpful[1]

    def get_text(self):
        return self.text

    def count_num_words(self):
        # Returns the total number of words in the text review
        return len(self.text.split())

    def num_uppercase_words(self):
        # Returns the number of uppercase words in the text review
        num_upper_words = 0
        for word in self.text.split():
            if word.isupper() and len(word) > 1:  # Checks length so words like 'A' and 'I' are excluded
                num_upper_words += 1
        return num_upper_words

    def num_special_chars(self):
        # Returns the number of special characters in the text review
        special_chars_string = """ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
        num_special_chars = 0
        for character in self.text:
            if character in special_chars_string:
                num_special_chars += 1
        return num_special_chars

    def get_net_positivity(self):
        # Calculates the net positivity of a text review. Negates all words in a sentences
        # preceded by the word 'not', and adds more weight to words followed by adjectives that
        # emphasize
        # https://gist.githubusercontent.com/mkulakowski2/4289437/raw/1bb4d7f9ee82150f339f09b5b1a0e6823d633958/positive-words.txt
        # https://gist.githubusercontent.com/mkulakowski2/4289441/raw/dad8b64b307cd6df8068a379079becbb3f91101a/negative-words.txt
        value = 0
        sentences = self.text.split('.')
        for sent in sentences:
            words = sent.split()
            not_occured = 1
            for word in words:
                current_word = word.upper()
                if current_word in Query.get_emphasis_words():
                    emphasis_multiplier = 3
                else:
                    emphasis_multiplier = 1
                if current_word in Query.get_positive_words():
                    value += not_occured * emphasis_multiplier
                elif current_word in Query.get_negative_words():
                    value += -not_occured * emphasis_multiplier
                if current_word == 'NOT':
                    not_occured = -1
                else:
                    not_occured = 1
        return int(value)

    def get_average_sentence_length(self):
        total_words = 0
        sentences = self.text.split('.')
        for sent in sentences:
            total_words += len(sent.split())
        total_sentences = len(sentences)
        if total_sentences == 0:
            return 0;
        return total_words / total_sentences

    @staticmethod
    def get_positive_words():
        if len(Query.positive_words) == 0:
            with open('Datasets/positive_words.txt', 'r') as pos_file:
                Query.positive_words = pos_file.read().upper().splitlines()
            pos_file.close()
        return Query.positive_words

    @staticmethod
    def get_negative_words():
        if len(Query.negative_words) == 0:
            with open('Datasets/negative_words.txt', 'r') as neg_file:
                Query.negative_words = neg_file.read().upper().splitlines()
            neg_file.close()
        return Query.negative_words

    @staticmethod
    def get_emphasis_words():
        if len(Query.emphasis_words) == 0:
            with open('Datasets/negative_words.txt', 'r') as emp_file:
                Query.emphasis_words = emp_file.read().upper().splitlines()
            emp_file.close()
        return Query.emphasis_words

    def get_points(self):
        return (
            # self.get_helpful_percent() * self.help_weight,
            # self.get_help_votes() * self.help_votes_weight,
            self.num_uppercase_words() * self.uppercase_weight,
            self.num_special_chars() * self.spec_char_weight,
            # self.count_num_words(),
            self.get_net_positivity() * self.net_pos_weight,
            self.get_average_sentence_length() * self.sentence_length_weight)


class Review(Query):

    #  Initializer
    def __init__(self, helpful, text, overall):
        Query.__init__(self, helpful, text)
        self.overall = overall

    def get_overall(self):
        return self.overall
