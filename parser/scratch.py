'''
Created on Sep 9, 2014

@author: Aaron Levine
'''

import Corpora.corpus as zach
import Corpora.tokenizer as mark
import operator
from bs4 import BeautifulSoup
from Corpora.tokenizer import TokenizedSentence
import nltk



if __name__ == "__main__":
    
    
    sentence = "also known as the Asakusa Kannon temple"
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)
    print [nltk.ne_chunk(pos_tags, binary=False)]


