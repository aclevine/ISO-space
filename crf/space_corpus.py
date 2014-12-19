# -*- coding: utf-8 -*-

"""WRapper for a corpus of ISO-Space annotated documents for machine learning.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""
import os
import xml.etree.ElementTree as ET

from crfsuite.instance import Instance
from crfsuite.sequence import Sequence
from space_document import Space_Document

train = '/users/sethmachine/desktop/Train++'
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
    def __init__(self, dirpath='', recursive=True):
        self.dirpath = dirpath
        self.xmls = getXmls(dirpath)
        self.documents = [Space_Document(xml) for xml in self.xmls]
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

c = Space_Corpus(train)
c.set_sequences()
b = Space_Corpus(test)
b.set_sequences()
        
w = open('train++.txt', 'w')
#for x in c.documents:
#    print>>w, str(x)
#    print>>w, 'FUCK U'
print>>w, str(c)
w.close()

w = open('test++.txt', 'w')
#for x in c.documents:
#    print>>w, str(x)
#    print>>w, 'FUCK U'
print>>w, str(b)
w.close()
