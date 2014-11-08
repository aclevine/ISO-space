# -*- coding: utf-8 -*-

"""
Uses word similarity metrics to classify words into a semantic type.

"""

import stopwords as sw
import word_similarity as ws

#indices for (labeln, [w1, ..., wn]) tuples
LABEL = 0
WORDS = 1

def classify(phrase, wordClasses, pos=ws.NOUN):
    """
    Classifies a phrase into a semantic class based on the
    maximized Wu-Palmer macro average similarity score between
    the word and each of the words in the given wordClasses.
    Returns the class label which maximizes this average.

    Args:
    phrase: A list of strings which linearlly denote a phrase/constituent.
    wordClasses: a list of (labeln, [p1, ..., pn]) tuples.
                 each pn is of the format [w1, ..., wn]

    Returns:
    classLabel: A string that denotes the most likely semantic class.
    """
    scores = []
    for (label, words) in wordClasses:
        scores.append((label, ws.wup_macro_average(phrase, words)))
    return max(scores)
        
