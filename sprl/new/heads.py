# -*- coding: utf-8 -*-

"""Code to grab heads of multiword tags in SPRL
"""

import re

import nltk
import tagdoc as td

is_noun = re.compile(r'^NN.*')

t = td.TagDir(td.SPRL_DIR)
l = list(set([x.attrib['text'] for x in t.get_multiwords('TRAJECTOR')]))

def last_NN(labeled_words):
    """Picks the last noun in a list of pos tagged words

    A word is a noun if its pos tag begins with NN, e.g.
    NN, NNS, NNP, etc.

    Args:
        labeled_words: a list of words appended with a pos tag

    Returns:
        the last (word, NN.*)

    """
    for i in xrange(len(labeled_words), -1, -1):
        if is_noun.match(labels[i][-1]):
            return labels[i]

def pos(multiword):
    """Returns a list of pos tagged words given a multiword

    A multiword is string containing at least two words separated by
    white space.  The list returned contains tuples of the form (word, pos).

    Args:
        multiword: A string where words are separated by white space

    Returns:
        A list of tuples of the form (word, pos)

    """
    tokens = nltk.word_tokenize(multiword)
    return nltk.pos_tag(tokens)

