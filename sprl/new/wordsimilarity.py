# -*- coding: utf-8 -*-

"""
Functions that compute the semantic similarity between sets of words.

"""

from nltk.corpus import wordnet as wn
import tagdoc as td

def _first_wup(word1, word2, pos=wn.NOUN):
    """
    Computes the Wu-Palmer similarity between two words.
    Compares the two most common synsets of each word.

    Args:
    word1: A string representing a word.
    word2: A string representing a word.
    pos: The part-of-speech of both words.

    Returns:
    score: A real number between [0, 1.0]
    """
    try:
        synset1 = wn.synsets(word1, pos)[0]
        synset2 = wn.synsets(word2, pos)[0]
        return wn.wup_similarity(synset1, synset2)
    except IndexError:
        return 0
        

def avg_wup(phrases1, phrases2, pos=wn.NOUN):
    """
    Computes the average Wu-Palmer similarity between two sets of words.
    Returns the average similarity of each word in phrases1 compared
    to every word in phrases2.  Scores of 0 are not factored into the
    final average.

    Args:
    phrases1: A list of strings representing a phrase.
    phrases2: A list of strings representing a phrase.
    pos: The part-of-speech of both phrases.

    Returns:
    avgscore: A real number between [0, 1.0].
    """
    score = 0
    count = 0
    for word1 in phrases1:
        word1_score = 0
        word1_count = 0
        for word2 in phrases2:
            curr_score = _first_wup(word1, word2)
            if curr_score != 0:
                word1_score += curr_score
                word1_count += 1
        if word1_count != 0:
            score += (word1_score / word1_count)
            count += 1
    if count != 0:
        return score / count
    return 0 #no pairs of words were in the thesaurus!
        
