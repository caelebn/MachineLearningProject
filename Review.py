class Review:

    #  Initializer
    def __init__(self, helpful, text, overall, review_time):
        self.helpful = helpful
        self.text = text
        self.overall = overall
        self.review_time = review_time
        self.net_pos_weight = 1000
        self.help_weight = 100
        self.help_votes_weight = 20
        self.spec_char_weight = 10

    #  Accessor Methods
    def get_helpful_percent(self):
        if self.helpful[1] == 0:
            return 0
        else:
            return self.helpful[0] / self.helpful[1]

    def get_help_votes(self):
        return self.helpful[1]

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

    #  Calculates the net positivity of a text review
    #  https://gist.githubusercontent.com/mkulakowski2/4289437/raw/1bb4d7f9ee82150f339f09b5b1a0e6823d633958/positive-words.txt
    #  https://gist.githubusercontent.com/mkulakowski2/4289441/raw/dad8b64b307cd6df8068a379079becbb3f91101a/negative-words.txt
    def get_net_positivity(self):
        with open('Datasets/positive_words.txt', 'r') as pos_file:
            pos_list = pos_file.read().upper().splitlines()
        with open('Datasets/negative_words.txt', 'r') as neg_file:
            neg_list = neg_file.read().upper().splitlines()

        pos_file.close()
        neg_file.close()

        # print(pos_list)

        net_pos_count = 0
        last_word_not = 1  # -1 for last word not, 1 for not last word not
        n_text = self.text.strip('.')
        for word in n_text.split():
            curr_val = 0
            if word.upper() in pos_list:
                curr_val = last_word_not
                last_word_not = 1
            elif word.upper() in neg_list:
                curr_val = last_word_not * -1
                last_word_not = 1
            if word.upper() == 'NOT':
                # print('word is not')
                last_word_not = -1 * last_word_not
            # print('Curr val: ', curr_val)
            net_pos_count += curr_val
            # print('Net pos count: ', net_pos_count)

        # print('POS COUNT: ', net_pos_count)
        return int(net_pos_count)

    #  Returns the number of special characters in the text review
    def num_special_chars(self):
        special_chars_string = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        num_special_chars = 0
        for character in self.text:
            if character in special_chars_string:
                num_special_chars += 1
        return num_special_chars

    def get_points(self):
        return (self.get_helpful_percent() * self.help_weight,
                self.get_help_votes() * self.help_votes_weight,
                self.num_uppercase_words(),
                self.num_special_chars() * self.spec_char_weight,
                self.count_num_words(),
                self.get_net_positivity() * self.net_pos_weight)
