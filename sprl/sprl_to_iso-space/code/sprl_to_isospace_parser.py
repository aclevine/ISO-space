# -*- coding: utf-8 -*-

"""
Code to parse tags from SPRL and ISO-Space annotated .xml files.  This is home brewed,
requiring no outside libraries, and works irrespective of operating system.

"""

import re
import os
import stopwords as sw
import word_classify as wc
from nltk.corpus import wordnet as wn

TAGNAME = 0
ATTRS = 1
ATTR_NAME = 0
ATTR_VALUE = 1
TEXT = 'text'

SPRL_FILE = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP.gold/45 N 22 E.xml"
SPRL_DIR = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP.gold"
ISO_DIR = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP"
ISO_FILE = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP/45_N_22_E.xml"
ISO_GOLD_DIR = "/users/sethmachine/desktop/Tokenized"

GET_TAGS_TEXT = re.compile(r'(?<=TAGS>).*(?=</TAGS)', re.DOTALL)
GET_TAG_ATTRIBUTES = re.compile(r'(?<=<)(?P<tag_name>[_A-Z]+) (?P<attributes>.*)(?=/>)', re.IGNORECASE)
GET_ATTRIBUTES = re.compile(r'(?P<attr_name>[a-z0-9_]+)="(?P<attr_value>[^"]+)', re.IGNORECASE)

def getKey(item):
    return item[1]

class Tag:
    """
    A wrapper around an xml tag of the form <tagname, <attr1, attr2, ..., attrn>>
    """
    def __init__(self, rawtag):
        self.rawtag = rawtag
        self.tagname = rawtag[0]
        self.attributes = rawtag[1]
        self.attrDict = {x[0]: x[1] for x in self.attributes}
    def __repr__(self):
        attrStr = ""
        for x in self.attributes:
            attrStr += x[0] + "=" + x[1] + ", "
        attrStr = attrStr[:-2]
        return self.tagname + ": " + attrStr
        
class Tag_Doc:
    """
    A wrapper around the tags from an annotated xml file.
    """
    def __init__(self, path = SPRL_DIR):
        self.path = path
        self.tags = [Tag(x) for x in dir_to_list(path, False)]
    def getTagTokens(self, tagname):
        return [tag for tag in self.tags if tag.tagname == tagname]
    def getTagAttrFreq(self, tagname, attr):
        tokens = self.getTagTokens(tagname)
        attrs = [x.attrDict[attr] for x in tokens]
        d = {x: attrs.count(x) for x in attrs}
        l = [(x, d[x]) for x in d.keys()]
        l = sorted(l, key=getKey, reverse=True)
        return l
        
        
    
def xml_to_list(path = SPRL_FILE, debug = False):
    w = open(path, 'r')
    t = w.read()
    rawTags = GET_TAGS_TEXT.findall(t)[0].split('\n')
    tags = []
    bad = []
    for tag in rawTags:
        m = GET_TAG_ATTRIBUTES.search(tag)
        if m:
            tagName = m.group("tag_name")
            attributes = GET_ATTRIBUTES.findall(m.group("attributes"))
            tags.append((tagName, attributes))
        else:
            bad.append(tag)
    if debug:
        return (tags, bad)
    return tags


def _dir_to_list(dirpath = ISO_GOLD_DIR, debug = False):
    tags = []
    for f in os.listdir(dirpath):
        if os.path.isfile(os.path.join(dirpath, f)):
            if f.endswith('.xml'):
                tags += xml_to_list(os.path.join(dirpath, f))
        elif os.path.isdir(os.path.join(dirpath, f)):
            tags += _dir_to_list(os.path.join(dirpath, f))
    return tags
        
def tag_by_type(tagname, tags):
    return [tag for tag in tags if tag[0] == tagname]

def get_attr(attr, tag):
    for a in tag[1]:
        if a[0] == attr:
            return a[1].lower()

def get_attr_list(attr, tags):
    return [get_attr(attr, tag) for tag in tags]
    

def get_attr_freq(attr, tagname, tags):
    tokens = tag_by_type(tagname, tags)
    attrs = get_attr_list(attr, tokens)
    d = {x: attrs.count(x) for x in attrs}
    return sorted([(x, d[x]) for x in d.keys()], key=getKey, reverse=True)

def get_attr_listset(attr, tagname, tags):
    return [x.split() for (x,y) in get_attr_freq(attr, tagname, tags) if x != None]

def getTagAttr(attrName, tag):
    """
    Returns the value of an attribute of the given tag

    Args:
    attrName: A string denoting the name of the tag attribute
    tag: A tuple of the form (tagName, [(attr1, value1), ..., (attrn, valuen)])

    Returns:
    attr: A tuple of the format (attribute, value)

    Returns None if no such attribute is found
    """
    for attr in tag[ATTRS]: 
        if attr[ATTR_NAME] == attrName:
            return attr
    return None
            


def getTagList(tagName='SPATIAL_ENTITY', xmlDir=ISO_GOLD_DIR):
    """
    Returns a list of all tags whose name is tagName.
    Gathers tags from all xml files recursively from the xmlDir.

    Args:
    tagName: Denotes the name/type of the tag.
    xmlDir: Denotes the directory where the xml files are stored.

    Returns:
    tagList: A list of all tags of the type tagName
    """
    allTags = _dir_to_list(xmlDir)
    return [tag for tag in allTags if tag[TAGNAME] == tagName]

def getTagListAttrs(attrName = TEXT, tagList = getTagList()):
    """
    Collects the attributes of a given list of tags

    Args:
    attribute: A string denoting the name of the tag attribute
    tagList: A list of tags, generally all of the same tagName

    Returns:
    attributes: A list of tuples of the form (attribute, value)
    """
    attrs = [getTagAttr(attrName, tag) for tag in tagList]
    return attrs

def getAttrValues(attrList):
    return [attr[ATTR_VALUE] for attr in attrList if attr]

def extent2List(extent):
    words = extent.split()
    return [sw.sub(word) for word in words]

#way too slow, also there are some issues...
def classify_extent(extent, labels, tagDir=ISO_GOLD_DIR):
    """
    Classifies an extent into a label by using
    the wup macro average similarity between that extent and the extents
    of the labels.
    """
    labelTags = [(label, getTagList(label, tagDir)) for label in labels]
    labelValues = [(label, getAttrValues(getTagListAttrs(tagList=tags))) for (label, tags) in labelTags]
    wordClasses = []
    for (label, values) in labelValues:
        setValues = list(set(values))
        newValues = []
        for value in setValues:
            newValues.append(extent2List(value))
        wordClasses.append((label, newValues))
    return wc.classify(extent2List(extent), wordClasses)

def average_wup(fromWords, toWords):
    fromSynsets = [wn.synsets(sw.sub(x), wn.NOUN)[0] for x in fromWords if wn.synsets(sw.sub(x), wn.NOUN)]
    toSynsets = [wn.synsets(sw.sub(x), wn.NOUN)[0] for x in toWords if wn.synsets(sw.sub(x), wn.NOUN)]
    total_wup = 0
    total_words = 0
    for fromSynset in fromSynsets:
        total_from = 0
        total_from_words = 0
        for toSynset in toSynsets:
            total_from += fromSynset.wup_similarity(toSynset)
            total_from_words += 1
            if total_from_words == 0:
                total_from = 0
                total_from_words = 1
        total_wup += (total_from / total_from_words)
        total_words += 1
    if total_wup == 0:
        return 0
    return total_wup / total_words

def classify_extent(tagText, labels = ['SPATIAL_ENTITY', 'PLACE', 'PATH'], tags = _dir_to_list(ISO_GOLD_DIR)):
    label_grams = {label : get_attr_listset('text', label, tags) for label in labels}
    words = tagText.split()
    words = [w.lower() for w in words]
    d = {label: label_grams[label] for label in labels}
    for label in labels:
        d[label] = [x for y in d[label] for x in y]
    wups = [(average_wup(words, d[label]), label) for label in labels]
    return max(wups)


