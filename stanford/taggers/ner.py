# -*- coding: utf-8 -*-

"""Stanford NLP's part-of-speech tagger

"""

import os, sys, inspect

from nltk.tag.stanford import NERTagger
from util.util import get_tokens

currdir = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
JAR = os.path.join(currdir, 'jars/stanford-ner-3.5.0.jar')
MODEL = os.path.join(currdir, 'models/english.all.3class.distsim.crf.ser.gz')
TAGGER = NERTagger(MODEL, JAR)

def ner(text):
    """Tokenizes a string, then returns each token with its NER tag.

    """
    return TAGGER.tag(get_tokens(text))
    

