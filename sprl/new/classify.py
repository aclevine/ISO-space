# -*- coding: utf-8 -*-

"""
Code to classify an SPRL tag to an ISO-Space one.
"""

import re
import os
import tagdoc as td
import wordsimilarity as ws
import stopwords as sw
from nltk.corpus import wordnet as wn

LABELS = ['SPATIAL_ENTITY', 'PLACE', 'PATH']
LABEL_DICT = td.TagDir(td.ISO_GOLD_DIR).tagDict
LABEL_TEXT = {key : list(set([w.attrib['text'] for w in LABEL_DICT[key]])) for key in LABEL_DICT.keys() if key in LABELS}
LABEL_PHRASES = {key : td.flatten([[sw.sub(x) for x in w.split()] for w in LABEL_TEXT[key]]) for key in LABEL_TEXT.keys()}

lm = td.TagDoc().tagDict['LANDMARK']

#this is not returning the same results as the original
#metric used in sprl_to_iso-space.py
#debug it if possible (the old one was good!)
def classify(tag, labels = ['SPATIAL_ENTITY', 'PLACE', 'PATH']):
    phrase = [sw.sub(word) for word in tag.attrib['text'].split()]
    scores = [(ws.avg_wup(phrase, LABEL_PHRASES[label]), label) for label in labels]
    return max(scores)
