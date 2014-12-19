# -*- coding: utf-8 -*-

"""WRapper for an ISO-Space annotated document for machine learning.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import xml.etree.ElementTree as ET

from crfsuite.instance import Instance
from crfsuite.sequence import Sequence

test = '/users/sethmachine/desktop/Train++/RFC/Bogota.xml'

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
        
    """
    def __init__(self, filepath=''):
        self.filepath = filepath
        self.sentences = []
        if filepath:
            self.sentences = [child for child in ET.parse(filepath).getroot().find('TOKENS')]
        self.sequences = []

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
            s = Sequence()
            for lex in sentence.getchildren():
                label = 'None'
                if 'label' in lex.attrib:
                    label = lex.attrib['label']
                    del lex.attrib['label']
                i = Instance(label, lex.attrib)
                i.add(('word', lex.text))
                s.add(i)
            self.sequences.append(s)
            #if not s.instances:
                #print self.filepath

    def __repr__(self):
        return '\n'.join([str(sequence) for sequence in self.sequences if sequence.instances])
            
            
"""            
t = Space_Document(test)
t.set_sequences()
s = t.sequences[0]
for x in s.instances:
    print x
"""
