import re


class RunningAverage:
    def __init__(self):
        self.values = []

    def add(self, val):
        self.values.append(val)

    def add_all(self, vals):
        self.values += vals

    def get(self):
        return sum(self.values) / len(self.values)

    def flush(self):
        self.values = []


def wordize_and_map(text):
    words = []
    index_map_from_text_to_word = []
    while len(text) > 0:
        match_space = re.match(r'^ +', text)
        if match_space:
            space_str = match_space.group(0)
            index_map_from_text_to_word += [None] * len(space_str)
            text = text[len(space_str):]
            continue

        match_en = re.match(r'^[a-zA-Z0-9]+', text)
        if match_en:
            en_word = match_en.group(0)
            index_map_from_text_to_word += [len(words)] * len(en_word)
            words.append(en_word)
            text = text[len(en_word):]
        else:
            index_map_from_text_to_word += [len(words)]
            words.append(text[0])
            text = text[1:]
    return words, index_map_from_text_to_word


def tokenize_and_map(tokenizer, text):
    words, index_map_from_word = wordize_and_map(text)

    tokens = []
    index_map_from_text_to_token = []
    while len(index_map_from_word) > 0:
        if index_map_from_word[0] is None:
            index_map_from_text_to_token.append(None)
            del index_map_from_word[0]
        else:
            word = words.pop(0)
            word_tokens = tokenizer.tokenize(word)
            if word_tokens == ['[UNK]']:
                index_map_from_text_to_token += [len(tokens)] * len(word)
                tokens.append('[UNK]')
                del index_map_from_word[:len(word)]
            else:
                for word_token in word_tokens:
                    word_token_len = len(re.sub(r'^##', '', word_token))
                    index_map_from_text_to_token += [len(tokens)] * word_token_len
                    tokens.append(word_token)
                    del index_map_from_word[:word_token_len]

    return tokens, index_map_from_text_to_token
