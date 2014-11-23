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
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"baseline_classifier/Corpora")))
cmd_subfolder = cmd_subfolder.replace('fleiss/', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import re
import xml.etree.ElementTree as ET

from fleiss_util import *
from util.link_semantics import INT_LINKS
import numpy
import tokenizer

xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

#global list of ISO-Space tags which have extents, i.e. not relations.
ISO_CATEGORIES = ['PLACE', 'PATH', 'SPATIAL_ENTITY', 'NONMOTION_EVENT', 'EVENT',
                  'MOTION', 'SPATIAL_SIGNAL', 'MOTION_SIGNAL', 'MEASURE', 'NONE']

ISO_LINKS = ['QSLINK', 'NONE']

#example files, change these according to location on computer
ISO_FILE = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP/45_N_22_E.xml"
f1 = '/users/sethmachine/desktop/WhereToLosAngeles_HOLLYWOOD-MS-p1.xml'
f2 = '/users/sethmachine/desktop/WhereToLosAngeles_HOLLYWOOD-AB-p1.xml'

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = os.path.join(ADJUDICATED_PATH, '47_N_27_E')

#p2 for tags
#p4 for extents

#row types
TOKEN = 0
EXTENT = 1
LINK = 2 #for links

#token spans
START = 0
END = 1

class Fleiss_Table:
    """Wrapper for building a table for Fleiss' Kappa.

    Args:
        xmls: A list of absolute paths to annotated xmls of the same document
        categories: A list of extent based tag types

    Attributes:
        xmls: A list of absolute paths to annotated xmls of the same document
        numXmls: The number of xmls (i.e. annotators / raters)
        categories: A list of extent based tag types
        rows: A list of all the table entries by row
        table: A 2D numpy.zeros array used to compute Fleiss' Kappa
        
    """
    def __init__(self, xmls, categories=ISO_CATEGORIES, isLinks=False):
        self.xmls = xmls
        self.numXmls = len(xmls)
        self.categories = categories
        self.links = ISO_LINKS
        self.isLinks = isLinks
        self.semantics = INT_LINKS['QSLINK']
        self.rows = []
        self.table = None
        
    def _is_tag_match(self, tag1, tag2):
        """Determines if two tags have the same span.

        True if the start and end indices match.
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

    def _is_link_match(self, relation, link):
        """Determines if a relation of tags and a link match.            
        """
        keys = self.semantics.keys()
        for x in xrange(0, len(keys)):
            if relation[x].attrib['id'] != link.attrib[keys[x]]:
                return False
        return True
            

    def _get_tokens(self, xml):
        """Gets lex tokens for an xml.

        Uses Tokenizer from Corpora to tokenize xml text.

        Args:
            xml: An absolute path to an annotated xml

        Returns:
            A list of tokens of the form (start, end, word)

        """
        text = ET.parse(xml).getroot().find('TEXT').text
        tk = tokenizer.Tokenizer(text)
        tk.tokenize_text()
        return [token[1][0] for token in tk.tokens]
    
    def _get_linkdict(self):
        """Returns a dictionary mapping each xml to its links

        Args:
            None

        Returns:
            A dictionary where dict[n] = all links in xml #n

        """
        if not self.xmls:
            raise ValueError, "xmls input must contain at least one element"
        if not self.categories:
            raise ValueError, "categories must contain at least one element"
        linkdict = {} #tagdict[n] = tags for annotator #n
        for annotator, xml in enumerate(self.xmls):
            root = ET.parse(xml).getroot()
            #ignores non-consuming tags
            linkdict[annotator] = [child for child in root.find('TAGS') if child.tag in self.links]
        return linkdict
        
    def _get_tagdict(self):
        """Returns a dictionary mapping each xml to its tags.

        Args:
            None

        Returns:
            A dictionary where dict[n] = all tags in xml #n

        """
        if not self.xmls:
            raise ValueError, "xmls input must contain at least one element"
        if not self.categories:
            raise ValueError, "categories must contain at least one element"
        tagdict = {} #tagdict[n] = tags for annotator #n
        for annotator, xml in enumerate(self.xmls):
            root = ET.parse(xml).getroot()
            #ignores non-consuming tags
            tagdict[annotator] = [child for child in root.find('TAGS') if child.tag in self.categories and child.attrib['text']]
        return tagdict
    
    def _build_token_rows(self):
        """Creates rows based on tokens.

        Each token is considered as an object to be given a label.
        In our case, the label is the tag associated with that token.

        Args:
            None

        Returns:
            A list of rows, where for each token there is a row
            of the form: [a_1, ..., a_n] where a_i is the number of
            raters who assigned that token the ith label/tag type.

        """
        tagdict = self._get_tagdict()
        tokens = self._get_tokens(self.xmls[0])
        rows = []
        for token in tokens:
            match = []
            for xml in xrange(0, self.numXmls):
                tags = tagdict[xml]
                tags.sort(key=lambda x: int(x.attrib['start']))
                tag = binary_search(token, tags)
                if tag != None: #interestingly we can't do "if tag:"
                    match.append(tag)
                else:
                    match.append(ET.Element('NONE'))
            rows.append(match)
        return rows
    
    def _build_extent_rows(self, use_unmatched=True):
        """Creates rows based on tag extents/text.

        Each extent is the entire text associated with a given tag.

        Args:
            use_unmatched: If True, every unique tag extent is given its
                own row.  If False, only extents whose exact span is assigned
                a label across all annotators are considered for the rows.

        Returns:
            A list of rows, where for each extent there is a row
            of the form: [a_1, ..., a_n] where a_i is the number of raters
            who assigned that extent the ith label/tag type.
            
        """                
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
                        if self._is_tag_match(tag, otherTag):
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

    def _build_link_rows(self, use_unmatched=True):
        """Creates rows based on links.

        Each tag is associated with a link.

        Args:
            use_unmatched: If True, every unique tag extent is given its
                own row.  If False, only extents whose exact span is assigned
                a label across all annotators are considered for the rows.

        Returns:
            A list of rows, where for each extent there is a row
            of the form: [a_1, ..., a_n] where a_i is the number of raters
            who assigned that extent the ith label/tag type.
            
        """                
        tagdict = self._get_tagdict()
        linkdict = self._get_linkdict()
        tags = tagdict[0] #all tags should be the same
        permutations = permute(tags, 'QSLINK', INT_LINKS['QSLINK'])
        rows = [] #list of lists
        for relation in permutations:
            row = []
            for xml in tagdict.keys():
                unmatched=True
                links = linkdict[xml]
                for link in links:
                    if self._is_link_match(relation, link):
                        row.append(ET.Element('QSLINK'))
                        unmatched=False
                        break
                if unmatched:
                    row.append(ET.Element('NONE'))
            rows.append(row)
        return rows
        
    def build_rows(self, rowType=EXTENT, use_unmatched=True):
        """Fills in the rows attribute.

        Rows can be made to be extent based, which considers only
        text within a tag.  Rows can also be token based, which considers
        all tokens in the document.

        Note: This must be called before calling ``build_table``.

        Args:
            rowType: 0 if considering extents, 1 if considering tokens.
            use_unmatched: If True, every unique tag extent is given its
                own row.  If False, only extents whose exact span is assigned
                a label across all annotators are considered for the rows

        Returns:
            None

        """
        if rowType == EXTENT:
            self.rows = self._build_extent_rows(use_unmatched)
        elif rowType == LINK:
            self.rows = self._build_link_rows()
        elif rowType == TOKEN:
            self.rows = self._build_token_rows()

    def build_table(self):
        """Constructs the table for computing Fleiss' Kappa

        This creates an M x N numpy.zeros array, where M is the number
        of objects being categorized and N is the number of possible labels
        that can be assigned to an object (at most one label per object).

        Each table entry e_ij is the number of annotators/raters who assigned
        the ith object the jth label.  Each row must sum to the number of total
        annotators, i.e. sum^{N}_{j = 0} e_ij = ``self.numXmls``.

        Note: ``build_rows`` must be called before this.
        
        Args:
            None
        Returns:
            None

        """
        if not self.rows:
            raise ValueError, "call build_rows before building table"
        if self.isLinks:
            self.categories = ISO_LINKS
        self.table = numpy.zeros((len(self.rows), len(self.categories)), dtype=int)
        for row, matched in enumerate(self.rows):
            for tag in matched:
                column = self.categories.index(tag.tag)
                self.table[row][column] += 1
        
def yo():
    return getXmls('/users/sethmachine/desktop/test', 'p4')

#test = Fleiss_Table(yo())
#f = test._get_linkdict()
    
#uncomment for a quick test run
#f = get_table([f1, f2])        
#r = get_rows(test)       

#f = Fleiss_Table(test)
#tokens = f._get_tokens(test[0])
#tagdict = f._get_tagdict()
#tags = tagdict[0]
#tags.sort(key=lambda x: int(x.attrib['start']))
#t = tokens[5]
