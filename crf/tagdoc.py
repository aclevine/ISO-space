# -*- coding: utf-8 -*-

"""
Code to represent xml based annotation as Python objects.
"""
import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"baseline_classifier/Corpora")))
cmd_subfolder = cmd_subfolder.replace('/crf', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import xml.etree.ElementTree as ET
import tokenizer
import re

import stanford.taggers.pos as pos

                                      

SPRL_FILE = "/users/sethmachine/desktop//CP.gold/45 N 22 E.xml"
SPRL_DIR = "/users/sethmachine/desktop/CP.gold"
ISO_DIR = "/users/sethmachine/desktop/CP"
ISO_FILE = "/users/sethmachine/desktop/CP/45_N_22_E.xml"
ISO_GOLD_DIR = "/users/sethmachine/desktop/Tokenized"

TEXT = 'TEXT'
TAGS = 'TAGS'

#global list of ISO-Space tags which have extents, i.e. not relations.
ISO_CATEGORIES = ['PLACE', 'PATH', 'SPATIAL_ENTITY', 'NONMOTION_EVENT',
                  'MOTION', 'SPATIAL_SIGNAL', 'MOTION_SIGNAL', 'MEASURE', 'NONE']


def clean(word):
    #word = word.replace(u'\xad', '')
    return word

class Tag:
    """
    A wrapper around a tag.
    """
    def __init__(self, name, attrib, text, tokenizer2):
        self.name = name
        self.attrib = attrib
        self.attribNames = attrib.keys()
        self.text = text
        self.tokenizer = tokenizer2
        self.tokens = []
        self.sent = ''
        self.word = ''
        self.sentStart = 0
        self.sentEnd = 0
        if 'start' in self.attribNames:
            self.start = int(attrib['start'])
            self.end = int(attrib['end'])
        if 'text' in self.attribNames:
            self.sentIndex = self._get_sentence()
            self.word = self.attrib['text']
            if self.sentIndex:
                self.sent = self.text[self.sentIndex[0]:self.sentIndex[1]]
                self.sentStart = -1 * (self.sentIndex[0] - self.start)
                self.sentEnd = -1 * (self.sentIndex[0] - self.end)
                tk = tokenizer.Tokenizer(self.sent)
                tk.tokenize_text()
                self.tokens = [x[1][0] for x in tk.tokens]
    def _get_sentence(self):
        for sent in self.tokenizer.sentences:
            if int(self.attrib['start']) >= sent[0] and int(self.attrib['end']) <= sent[1]:
                return sent
        
        

    def __eq__(self, x):
        return self.name == x.name and self.attrib['text'] == x.attrib['text']

    def __ne__(self, x):
        return not self.__eq__(self, x)

    def __hash__(self):
        return hash(id(self))
    
    def __repr__(self):
        return self.name + " " + str(self.attrib)
    
class TagDoc:
    """
    A wrapper around an xml annotated document.
    """
    def __init__(self, filepath=SPRL_FILE):
        self.tree = ET.parse(filepath)
        self.categories = ISO_CATEGORIES
        self.root = self.tree.getroot()
        self.sentences = [child for child in self.root.find('TOKENS')]
        self.text = self.root.find(TEXT).text
        self.tokenizer = tokenizer.Tokenizer(self.text)
        self.tokenizer.tokenize_text()
        self.xmlTags = [child for child in self.root.find('TAGS') if child.tag in self.categories and child.attrib['text']]
        self.tags = [Tag(child.tag, child.attrib, self.text, self.tokenizer) for child in self.root.find(TAGS)]
        self.tagDict = getTagDict(self.tags)

    def _get_tags(self):
        for child in self.root.find(TAGS):
            tag = Tag(child.tag, child.attrib, self.text)
            
    def get_multiwords(self, name='TRAJECTOR'):
        """Returns a list of all tags with multiword extents
        """
        return [tag for tag in self.tagDict[name] if len(tag.attrib['text'].split()) > 1]
    
class TagDir:
    """
    A wrapper around a directory of xml annotated documents.
    """
    def __init__(self, dirpath=ISO_GOLD_DIR):
        self.files = getXML(dirpath)
        self.docs = [TagDoc(f) for f in self.files]
        self.texts = [doc.text for doc in self.docs]
        self.tags = flatten([doc.tags for doc in self.docs])
        self.tagDict = getTagDict(self.tags)

    def get_multiwords(self, name='TRAJECTOR'):
        """Returns a list of all tags with multiword extents
        """
        return [tag for tag in self.tagDict[name] if len(tag.attrib['text'].split()) > 1]
    
def getXML(dirpath=ISO_GOLD_DIR):
    files = []
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            if f.endswith('.xml'):
                files.append(fpath)
        elif os.path.isdir(fpath):
            files += getXML(fpath)
    return files
                
def getTagDict(tags):
    d = {tag.name: [] for tag in tags}
    for tag in tags:
        d[tag.name].append(tag)
    return d

def flatten(l):
    return [item for sublist in l for item in sublist]


gold = TagDir(ISO_GOLD_DIR)
#nineteen examples get the wrong text spans for the tokens
#something very weird going on
#some problematic unicode, e.g. u'South\xadeast of'
sp = [x for x in gold.tagDict['SPATIAL_SIGNAL'] if x.word == x.sent[x.sentStart:x.sentEnd]]
#z = t.docs[0]
#tr = t.tagDict['TRAJECTOR']
