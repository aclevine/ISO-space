# -*- coding: utf-8 -*-

"""
Code to represent xml based annotation as Python objects.
"""
import os
import xml.etree.ElementTree as ET

SPRL_FILE = "/users/sethmachine/desktop//CP.gold/45 N 22 E.xml"
SPRL_DIR = "/users/sethmachine/desktop/CP.gold"
ISO_DIR = "/users/sethmachine/desktop/CP"
ISO_FILE = "/users/sethmachine/desktop/CP/45_N_22_E.xml"
ISO_GOLD_DIR = "/users/sethmachine/desktop/Tokenized"

TEXT = 'TEXT'
TAGS = 'TAGS'

class Tag:
    """
    A wrapper around a tag.
    """
    def __init__(self, name, attrib):
        self.name = name
        self.attrib = attrib
        self.attribNames = attrib.keys()

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
        self.root = self.tree.getroot()
        self.sentences = [child for child in self.root.find('TOKENS')]
        self.text = self.root.find(TEXT).text
        self.tags = [Tag(child.tag, child.attrib) for child in self.root.find(TAGS)]
        self.tagDict = getTagDict(self.tags)

    def get_multiwords(self, name='TRAJECTOR'):
        """Returns a list of all tags with multiword extents
        """
        return [tag for tag in self.tagDict[name] if len(tag.attrib['text'].split()) > 1]
    
class TagDir:
    """A wrapper around a directory of xml annotated documents.
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


t = TagDir(ISO_GOLD_DIR)
z = t.docs[0]
#tr = t.tagDict['TRAJECTOR']
