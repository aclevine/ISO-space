# -*- coding: utf-8 -*-

"""Stanford NLP's part-of-speech tagger

"""

import os, sys, inspect

from nltk.tag.stanford import POSTagger
from util.util import get_tokens

currdir = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
JAR = os.path.join(currdir, 'jars/stanford-postagger-3.5.0.jar')
MODEL = os.path.join(currdir, 'models/wsj-0-18-bidirectional-distsim.tagger')
TAGGER = POSTagger(MODEL, JAR)

def tag(text):
    """Tokenizes a string, then returns each token with its pos tag

    """
    return TAGGER.tag(get_tokens(text))
    

