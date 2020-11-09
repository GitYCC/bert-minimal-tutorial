from unittest.mock import Mock

import pytest

from utils import tokenize_and_map, wordize_and_map

@pytest.mark.parametrize(
    'text, expected_words, expected_index_map',
    [
        (
            '我 愛  喝  apple juice ',
            ['我', '愛', '喝', 'apple', 'juice'],
            [0, None, 1, None, None, 2, None, None, 3, 3, 3, 3, 3, None, 4, 4, 4, 4, 4, None]
        ),
        (
            'Rolling in the deep ! !',
            ['Rolling', 'in', 'the', 'deep', '!', '!'],
            [0, 0, 0, 0, 0, 0, 0, None, 1, 1, None, 2, 2, 2, None, 3, 3, 3, 3, None, 4, None, 5]
        ),
        (
            'I am YC.',
            ['I', 'am', 'YC', '.'],
            [0, None, 1, 1, None, 2, 2, 3]
        ),
        (
            '未知：? unknown: ?',
            ['未', '知', '：', '?', 'unknown', ':', '?'],
            [0, 1, 2, 3, None, 4, 4, 4, 4, 4, 4, 4, 5, None, 6]
        )
    ]
)
def test_wordize_and_map(text, expected_words, expected_index_map):
    words, index_map = wordize_and_map(text)
    assert words == expected_words
    assert index_map == expected_index_map


@pytest.mark.parametrize(
    'sentence, expected_tokens, expected_index_map',
    [
        (
            '我 愛  喝  apple juice ',
            ['我', '愛', '喝', 'apple', 'j', '##ui', '##ce'],
            [0, None, 1, None, None, 2, None, None, 3, 3, 3, 3, 3, None, 4, 5, 5, 6, 6, None]
        ),
        (
            'Rolling in the deep ! !',
            ['rolling', 'in', 'the', 'deep', '!', '!'],
            [0, 0, 0, 0, 0, 0, 0, None, 1, 1, None, 2, 2, 2, None, 3, 3, 3, 3, None, 4, None, 5]
        ),
        (
            'I am YC.',
            ['i', 'am', 'y', '##c', '.'],
            [0, None, 1, 1, None, 2, 3, 4]
        ),
        (
            '未知：? unknown: ?',
            ['未', '知', '：', '[UNK]', 'u', '##nk', '##now', '##n', ':', '[UNK]'],
            [0, 1, 2, 3, None, 4, 5, 5, 6, 6, 6, 7, 8, None, 9]
        )
    ]
)
def test_tokenize_and_map(sentence, expected_tokens, expected_index_map):
    def tokenize(word):
        mapping = {
            'juice': ['j', '##ui', '##ce'],
            'YC': ['y', '##c'],
            '?': ['[UNK]'],
            'unknown': ['u', '##nk', '##now', '##n']
        }
        if word in mapping:
            return mapping[word]
        else:
            return [word.lower()]

    mocked_tokenizer = Mock()
    mocked_tokenizer.tokenize = tokenize

    tokens, index_map = tokenize_and_map(mocked_tokenizer, sentence)

    assert tokens == expected_tokens
    assert index_map == expected_index_map
