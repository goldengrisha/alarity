from absl import logging
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.backend import eval
import os
import re


class Encoder(object):
    model = None

    def __init__(self):
        logging.set_verbosity(logging.ERROR)
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.model = hub.load(module_url)

    def embed(self, input):
        '''
        Converting sentence or word or paragraph to vector
        '''
        return self.model(input)

    def eval_tensor(self, tensor):
        '''
        transform tensor to list
        '''
        return eval(tensor)

    def run_sts_benchmark(self, sent_1: str, sent_2: str):
        '''
        Take 2 strings and returns the similarity scores
        '''
        sts_encode1 = tf.nn.l2_normalize(self.embed([str(sent_1)]), axis=1)
        sts_encode2 = tf.nn.l2_normalize(self.embed([str(sent_2)]), axis=1)
        cosine_similarities = tf.reduce_sum(
            tf.multiply(sts_encode1, sts_encode2), axis=1)
        clip_cosine_similarities = tf.clip_by_value(
            cosine_similarities, -1.0, 1.0)
        scores = 1.0 - tf.acos(clip_cosine_similarities)

        return scores

