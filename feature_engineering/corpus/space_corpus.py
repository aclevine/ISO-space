# -*- coding: utf-8 -*-

"""Wrapper for a corpus of ISO-Space documents.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""
from __future__ import division
from collections import defaultdict
from itertools import chain, combinations
import re
import os
import xml.etree.ElementTree as ET

from space_document import Space_Document, link_dist
from qslink import qs
from util import *

train = '/users/sethmachine/desktop/Train++'
test = '/users/sethmachine/desktop/Test++'

#toId is the landmark/ground
#fromId is the trajector/figure

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
        
    """
    def __init__(self, dirpath='', recursive=True):
        self.dirpath = dirpath
        self.xmls = getXmls(dirpath)
        self.documents = [Space_Document(xml) for xml in self.xmls]
        self.tags = [tag for doc in self.documents for tag in doc.tags]
        self.lexes = [lex for doc in self.documents for lex in doc.lexes]
        self.sents = [sent for doc in self.documents for sent in doc.sents]
        self.links = [link for doc in self.documents for link in doc.links]

    def get_linkdict(self):
        link_types = {link.tag for link in self.links}
        linkdict = {link_type:[] for link_type in link_types}
        for link in self.links:
            linkdict[link.tag].append(link)
        return linkdict
    
id_pattern = re.compile(r'[0-9]+')

def get_type(ID):
	return id_pattern.sub('', ID)

"""
train_corpus = Space_Corpus(train)


qq = []
for doc in train_corpus.documents:
    qq += qs(doc)

training = qq

positives = [x for x in qq if x[0] != False]

qslinks = [link for link in train_corpus.get_linkdict()['QSLINK']
           if is_full_qslink(link)]
"""
#linkdict = train_corpus.get_linkdict()
#(types, d) = link_stats(linkdict)

