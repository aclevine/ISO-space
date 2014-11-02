# -*- coding: utf-8 -*-

"""Fleiss' Kappa for inter-annotator agreement.

This module builds the table for calculating Fleiss' Kappa (κ).
Only the numpy library is required; otherwise the extents and tags
are extracted with the ElementTree module.

This module by itself does not compute Fleiss' Kappa; use an outside
module to take the table as input.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"parser/Corpora")))
cmd_subfolder = cmd_subfolder.replace('fleiss/', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import re
import numpy
import tokenizer
import xml.etree.ElementTree as ET

xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

#global list of ISO-Space tags which have extents, i.e. not relations.
ISO_CATEGORIES = ['PLACE', 'PATH', 'SPATIAL_ENTITY', 'NONMOTION_EVENT',
                  'MOTION', 'SPATIAL_SIGNAL', 'MOTION_SIGNAL', 'MEASURE', 'NONE']

#example files, change these according to location on computer
ISO_FILE = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP/45_N_22_E.xml"
f1 = '/users/sethmachine/desktop/WhereToLosAngeles_HOLLYWOOD-MS-p1.xml'
f2 = '/users/sethmachine/desktop/WhereToLosAngeles_HOLLYWOOD-AB-p1.xml'

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = os.path.join(ADJUDICATED_PATH, '47_N_27_E')

#row types
EXTENT = 0
TOKEN = 1

#token spans
START = 0
END = 1

def binary_search(token, sorted_tags, counter=1):
    if not sorted_tags: #token isn't tagged in any extent
        return None
    size = len(sorted_tags)
    index = size / 2
    curr = sorted_tags[index]
    if token[START] >= int(curr.attrib['start']) and token[END] <= int(curr.attrib['end']):
        return curr
    if token[START] > int(curr.attrib['end']):
        return binary_search(token, sorted_tags[index + 1:size], counter + 1)
    elif token[END] < int(curr.attrib['start']):
        return binary_search(token, sorted_tags[0:index], counter + 1)
    else: #if we get here, the token somehow overlaps extents!
        return None
    

class Fleiss_Table:
    def __init__(self, xmls, categories=ISO_CATEGORIES):
        self.xmls = xmls
        self.numXmls = len(xmls)
        self.categories = ISO_CATEGORIES
        self.rows = []
        self.table = None
        
    def _is_tag_match(self, tag1, tag2):
        """Determines if two tags have the same extent.

        Two tags are have the same extent if the start and end indices match.
        This does not necessarily mean the tags have the same category.

        Args:
            tag1: An xml based tag as from ElementTree
            tag2: An xml based tag as from ElementTree

        Returns:
            True if the tags' indices match, False otherwise.
        """
        if tag1.attrib['start'] == tag2.attrib['start'] and tag1.attrib['end'] == tag2.attrib['end']:
                return True
        return False

    def _get_tokens(self, xml):
        """Gets lex tokens for an xml
        """
        text = ET.parse(xml).getroot().find('TEXT').text
        tk = tokenizer.Tokenizer(text)
        tk.tokenize_text()
        return [token[1][0] for token in tk.tokens]
        
    def _get_tagdict(self):
        """Returns a dictionary mapping each rater to his/her tags
        """
        if not self.xmls:
            raise ValueError, "xmls input must contain at least one element"
        if not self.categories:
            raise ValueError, "categories must contain at least one element"
        tagdict = {} #tagdict[n] = tags for annotator #n
        for annotator, xml in enumerate(self.xmls):
            root = ET.parse(xml).getroot()
            #ignores non-consuming tags
            tagdict[annotator] = [child for child in root.find(TAGS) if child.tag in self.categories and child.attrib['text']]
        return tagdict
    
    def _build_token_rows(self):
        tagdict = self._get_tagdict()
        tokens = self._get_tokens(self.xmls[0])
        rows = []
        for token in tokens:
            match = []
            for xml in xrange(0, self.numXmls):
                tags = tagdict[xml]
                tags.sort(key=lambda x: int(x.attrib['start']))
                #print token
                tag = binary_search(token, tags)
                if tag != None:
                    match.append(tag)
                else:
                    match.append(ET.Element('NONE'))
            rows.append(match)
        return rows
    
    def _build_extent_rows(self, use_unmatched=True):
        tagdict = self._get_tagdict()
        rows = [] #list of lists
        for xml in tagdict.keys():
            tags = tagdict[xml]
            for tag in tags:
                match = [tag]
                for otherXml in xrange(0, self.numXmls):
                    unmatched = True
                    if otherXml == xml:
                        continue
                    otherTags = tagdict[otherXml]
                    for otherTag in otherTags:
                        if tag_matches(tag, otherTag):
                            match.append(otherTag)
                            otherTags.remove(otherTag)
                            unmatched = False
                            break
                    if unmatched and use_unmatched:
                        match.append(ET.Element('NONE'))
                if use_unmatched:
                    rows.append(match)
                elif len(match) == self.numXmls:
                    rows.append(match)
        return rows
        
    def build_rows(self, rowType=EXTENT, use_unmatched=True):
        if rowType == EXTENT:
            self.rows = self._build_extent_rows(use_unmatched)
        elif rowType == TOKEN:
            self.rows = self._build_token_rows()

    def build_table(self):
        if not self.rows:
            raise ValueError, "call build_rows before building table"
        self.table = numpy.zeros((len(self.rows), len(self.categories)), dtype=int)
        for row, matched in enumerate(self.rows):
            for tag in matched:
                column = self.categories.index(tag.tag)
                self.table[row][column] += 1
        

def getXmls(path):
    """Finds all xml files in a flat directory.

    Collects all xml files which match the xml_pattern.
    The pattern excludes files with suffixes like "extentsLocked."

    Args:
        path: A string absolute path for the directory.

    Returns:
        A list of all xml files matching xml_pattern.
    """
    files = []
    for f in os.listdir(path):
        fpath = os.path.join(path, f)
        if xml_pattern.match(f):
            files.append(fpath)
    return files

test = getXmls(TEST_PATH)

#relevant value names
TEXT = 'TEXT'
TAGS = 'TAGS'
#index of first xml for IAA
FIRST = 0


def tag_matches(tag1, tag2):
    """Determines if two tags have the same extent.

    Two tags are have the same extent if the start and end indices match.
    This does not necessarily mean the tags have the same category.

    Args:
        tag1: An xml based tag as from ElementTree
        tag2: An xml based tag as from ElementTree

    Returns:
        True if the tags' indices match, False otherwise.
    """
    if tag1.attrib['start'] == tag2.attrib['start'] and tag1.attrib['end'] == tag2.attrib['end']:
            return True
    return False

def get_tagdict(xmls, categories=ISO_CATEGORIES):
    if not xmls:
        raise ValueError, "xmls input must contain at least one element"
    if not categories:
        raise ValueError, "categories must contain at least one element"
    tagdict = {} #for mapping each annotator to the extents
    for annotator, xml in enumerate(xmls):
        root = ET.parse(xml).getroot()
        #only grabs tags with given categories and ignores non-consuming tags
        tagdict[annotator] = [child for child in root.find(TAGS) if child.tag in ISO_CATEGORIES and child.attrib['text']]
    return tagdict

def get_rows(xmls, categories=ISO_CATEGORIES, use_unmatched=True):
    """Builds the rows for each table entry
    """
    tagdict = get_tagdict(xmls, categories)
    numXmls = len(xmls) #number of annotators
    rows = [] #list of lists
    for xml in tagdict.keys():
        tags = tagdict[xml]
        for tag in tags:
            match = [tag]
            for otherXml in xrange(0, numXmls):
                unmatched = True
                if otherXml == xml:
                    continue
                otherTags = tagdict[otherXml]
                for otherTag in otherTags:
                    if tag_matches(tag, otherTag):
                        match.append(otherTag)
                        otherTags.remove(otherTag)
                        unmatched = False
                        break
                if unmatched and use_unmatched:
                    match.append(ET.Element('NONE'))
            if use_unmatched:
                rows.append(match)
            elif len(match) == numXmls:
                rows.append(match)
    return rows

def get_table(xmls, categories=ISO_CATEGORIES, use_unmatched=True):
    """Builds the table for computing Fleiss' Kappa.

    Constructs a numpy.zeros array of dimensions m * n, representing agreement amongst annotators.
    m is the number of extents over all annotators and n is the number of categories/labels.
    The extents are only considered if, for all xmls, that exact extent (based on ``tag_equals``)
    exists in the other xmls.  Otherwise the extent is ignored.
    Currently this does not consider non-consuming tags and ignores them.

    Args:
        xmls: A list of file paths, where each element is an annotated xml.
            The xmls should all be mark up for the same text.
        categories: A list of categories/tag types that are possible labels for
            any given extent.  By default it includes all possible ISO-Space extents.

    Returns:
        An m * n numpy.zeros array, where each entry ij represents the number of
        annotators who assigned label n_j to extent m_i.  The total across all rows
        sums to the number of xmls/annotators.
    """
    matched_tags = get_rows(xmls, categories, use_unmatched)
    fleiss_table = numpy.zeros((len(matched_tags), len(categories)), dtype=int)
    for row, matched in enumerate(matched_tags):
        for tag in matched:
            column = categories.index(tag.tag)
            fleiss_table[row][column] += 1
    return fleiss_table
    
#uncomment for a quick test run
#f = get_table([f1, f2])        
r = get_rows(test)       

f = Fleiss_Table(test)
tokens = f._get_tokens(test[0])
tagdict = f._get_tagdict()
tags = tagdict[0]
tags.sort(key=lambda x: int(x.attrib['start']))
t = tokens[5]

"""for key in tagdict.keys():
	tags = tagdict[key]
	tags.sort(key=lambda x: int(x.attrib['start']))
	for x in tokens:
		binary_search(x, tags)"""
