# -*- coding: utf-8 -*-

"""WRapper for an ISO-Space annotated document for machine learning.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import xml.etree.ElementTree as ET

from crfsuite.instance import Instance
from crfsuite.sequence import Sequence
#from space_corpus import stopwords

test = '/users/sethmachine/desktop/Train++/RFC/Bogota.xml'

#print stopwords
    

class Space_Document(object):
    """Wrapper for an ISO-Space annotated document.

    Opens an ISO-Space annotated xml, retrieving all of its sentence tags
    in <TOKENS>...</TOKENS>.  Each sentence tag has a series of <lex>...</lex>
    children, which has each instance's true class label and features.

    Args:
        filepath: An absolute filepath to the ISO-Space annotated xml.

    Attributes:
        filepath: An absolute filepath to the ISO-Space annotated xml.
        sentences: A list of ElementTree Element tags, each representing
            a series of tokens for a sentence.
        window_features: An exhaustive list of functions taking a list of
            Instances and adding in window based features.  These are called
            right before printing the formatted string to output.
        extra_features: An exhaustive list of functions taking a Lex token
            and Instance as input, adding in features to that Instance.
        filter_features: An exhaustive list of features to be only used
            for training and testing.  If empty, all available features are
            used.  
        
    """
    def __init__(self, filepath='', root='TOKENS', filter_features=[], window_features=[], extra_features=[], stopwords=[]):
        self.filepath = filepath
        self.sentences = []
        if filepath:
            self.sentences = [child for child in ET.parse(filepath).getroot().find(root)]
        self.sequences = []
        self.filter_features = filter_features
        self.window_features = window_features
        self.extra_features = extra_features
        self.stopwords = stopwords

    def _reset(self):
        if filepath:
            self.sentences = [child for child in ET.parse(filepath).getroot().find('TOKENS')]
        
    def set_sequences(self):
        if not self.sentences:
            raise ValueError, "No sentences to make sequences from."
        if self.sequences:
            self._reset()
            self.sequences = []
        for sentence in self.sentences:
            s = Sequence(self.window_features)
            for lex in sentence.getchildren():
                if lex.text in self.stopwords:
                    continue
                label = 'None'
                if 'label' in lex.attrib:
                    label = lex.attrib['label']
                    del lex.attrib['label']
                if self.filter_features:
                    for key in lex.attrib.keys():
                        if key not in self.filter_features:
                            del lex.attrib[key]
                i = Instance(label, lex.attrib)
                i.add(('word', lex.text))
                for function in self.extra_features:
                    function(lex, i)
                s.add(i)
            self.sequences.append(s)
            #if not s.instances:
                #print self.filepath

    def sequence_list(self):
        return [sequence.feature_list() for sequence in self.sequences]
    
    def __repr__(self):
        return '\n'.join([str(sequence) for sequence in self.sequences if sequence.instances])
            
            
"""
t = Space_Document(test)
t.set_sequences()
s = t.sequences[0]
for x in s.instances:
    print x
w = open('tiny_test.txt', 'w')
print>>w, str(t)
w.close()
"""
