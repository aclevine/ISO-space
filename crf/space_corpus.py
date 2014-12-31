# -*- coding: utf-8 -*-

"""Wrapper for a corpus of ISO-Space annotated documents for machine learning.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""
import os, re
import xml.etree.ElementTree as ET

from crfsuite.instance import Instance
from crfsuite.sequence import Sequence
import pycrfsuite
from space_document import Space_Document

train = '/users/sethmachine/desktop/Tokenized++'
test = '/users/sethmachine/desktop/Test++'

class Space_Corpus(object):
    """Wrapper for a corpus of ISO-Space annotated documents.

    Args:
        dirpath: An absolute filepath to the top level directory
            containing valid and annotated ISO-Space xmls.
        recursive: If True, the class will search all subdirectories
            exhaustively, collecting all ISO-Space xmls.

    Attributes:
        dirpath: An absolute filepath to the top level directory
            containing valid and annotated ISO-Space xmls.
        xmls: A list of the absolute filepaths of all ISO-Space xmls
            in the corpus.
        documents: A list of all ISO-Space documents in the corpus.
        sequences: A global list of all CRFSuite sequences from the documents.
        
    """
    def __init__(self, dirpath='', recursive=True, extra_features=[], window_features=[], filter_features=[], stopwords=[]):
        self.dirpath = dirpath
        self.xmls = getXmls(dirpath)
        self.documents = [Space_Document(xml, extra_features=extra_features, window_features=window_features, filter_features=filter_features, stopwords=stopwords) for xml in self.xmls]
        self.sequences = []

    def set_sequences(self):
        if not self.documents:
            raise ValueError, "Must contain at least one ISO-Space document."
        #reset sequences
        self.sequences = []
        for document in self.documents:
            document.set_sequences()
            self.sequences += document.sequences

    def __repr__(self):
        return '\n'.join([str(document) for document in self.documents])
        s = ''
        for x in self.documents:
            s += str(x)
            s += '\n'
            s += '\n'
        return s
            
def getXmls(dirpath, recursive=True):
    files = []
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            if f.endswith('.xml'):
                files.append(fpath)
        if recursive:
            if os.path.isdir(fpath):
                files += getXmls(fpath, recursive)
    return files

def begins_capitalized(lex, instance):
    instance.add(('isupper', str(lex.text[0].isupper())))

def word_len(lex, instance):
    thresholds = [5,10]
    length = len(lex.text)
    lengthValue = '-1' #longest word
    for (i, threshold) in enumerate(thresholds):
        if length <= threshold:
            lengthValue = str(i)
            break
    instance.add(('wordlen', lengthValue))


window_pattern = re.compile(r'\[[\+\-][1-9]+\]')
def n_window(window=[1,1]):
    def window_func(instances):
        LEFT = 0
        RIGHT = -1
        for (i, instance) in enumerate(instances):
            #left context
            j = i - 1
            counter = 1
            while j >= (i - window[LEFT]) and j >= 0:
                left_instance = instances[j]
                left_dict = {''.join([key, '[-', str(counter), ']']):left_instance.features[key] for key in left_instance.features if not window_pattern.search(key)}
                instance.addDict(left_dict)
                counter += 1
                j -= 1
            counter = 1                                 
            j = i + 1
            while j <= (i + window[RIGHT]) and j < len(instances):
                right_instance = instances[j]
                right_dict = {''.join([key, '[+', str(counter), ']']):right_instance.features[key] for key in right_instance.features if not window_pattern.search(key)}
                instance.addDict(right_dict)
                counter += 1
                j += 1
    return window_func
            
        
        
    

windows = [n_window(window=[1,1])]
extras = [begins_capitalized, word_len]
filters = []
filters = ['pos', 'ner', 'word', 'FORM',
           'CATEGORY', 'LCATEGORY', 'LFORM']

w = open('/users/sethmachine/desktop/nops.txt')
t = w.read()
w.close()
#ignore N most frequent words from training which aren't spatial mentions
stopwords = {line.decode('utf-8') for line in t.split('\n')[0:0]}

c = Space_Corpus(train, extra_features=extras,
                 window_features=windows, filter_features=filters,
                 stopwords=stopwords)
c.set_sequences()
b = Space_Corpus(test, extra_features=extras, window_features=windows,
                 filter_features=filters, stopwords=stopwords)
b.set_sequences()
        
w = open('train++.txt', 'w')
print>>w, str(c)
w.close()

w = open('test++.txt', 'w')
print>>w, str(b)
w.close()

train = c
test = b

tagger = pycrfsuite.Tagger()
tagger.open('m.model')
