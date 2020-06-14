import nltk
from nltk import sent_tokenize


def text_to_sentence(sentence: str):
    return sent_tokenize(sentence)
