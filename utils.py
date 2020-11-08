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


def tokenize_and_map(tokenizer, sentence):
    tokens = tokenizer.tokenize(sentence)
    index_map_from_sentence_to_token = []

    for i, token in enumerate(tokens):
        tail = re.sub(r'^##', '', token) if token != '[UNK]' else r'[^ ]'
        search_regex = r'^( *)(' + tail + r')'
        match_obj = re.match(search_regex, sentence, flags=re.IGNORECASE)
        if match_obj:
            blank_len = len(match_obj.group(1))
            tail_len = len(match_obj.group(2))
            sentence = sentence[blank_len + tail_len:]
            index_map_from_sentence_to_token += [None] * blank_len + [i] * tail_len
        else:
            raise ValueError
    index_map_from_sentence_to_token += [None] * len(sentence)

    return tokens, index_map_from_sentence_to_token
