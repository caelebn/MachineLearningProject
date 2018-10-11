class Review:

    #  Initializer
    def __init__(self, helpful, text, overall, review_time):
        self.helpful = helpful
        self.text = text
        self.overall = overall
        self.review_time = review_time

    #  Accessor Methods
    def get_helpful_percent(self):
        if self.helpful[1] == 0:
            return 0
        else:
            return self.helpful[0] / self.helpful[1]

    def get_text(self):
        return self.text

    def get_overall(self):
        return self.overall

    def get_date(self):
        return self.review_time

    #  Returns the total number of words in the text review
    def count_num_words(self):
        return len(self.text.split())

    #  Returns the number of uppercase words in the text review
    def num_uppercase_words(self):
        num_upper_words = 0
        for word in self.text.split():
            if word.isupper():
                num_upper_words += 1
        return num_upper_words

    #  Returns the number of special characters in the text review
    def num_special_chars(self):
        special_chars_string = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        num_special_chars = 0
        for character in self.text:
            if character in special_chars_string:
                num_special_chars += 1
        return num_special_chars

    def get_points(self):
        return (self.get_helpful_percent() * 100, self.num_uppercase_words(),
                self.num_special_chars(), self.count_num_words())
