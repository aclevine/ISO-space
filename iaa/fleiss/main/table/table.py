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
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"baseline_classifier/util/Corpora")))
cmd_subfolder = cmd_subfolder.replace('IAA/fleiss/main/table', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import re
import xml.etree.ElementTree as ET

from util.util import *
import numpy
import tokenizer

#row types
TOKEN = 0
EXTENT = 1
LINK = 2 #for links

#token spans
START = 0
END = 1

class Table(object):
    """Wrapper for building a table for Fleiss' Kappa.

    Args:
        xmls: A list of absolute paths to annotated xmls of the same document

    Attributes:
        xmls: A list of absolute paths to annotated xmls of the same document
        numXmls: The number of xmls (i.e. annotators / raters)
        categories: A list of extent based tag types
        rows: A list of all the table entries by row
        table: A 2D numpy.zeros array used to compute Fleiss' Kappa
        
    """
    def __init__(self, xmls):
        self.xmls = xmls
        self.numXmls = len(xmls)
        self.categories = []
        self.rows = []
        self.table = None
        self.docLen = 0
                    
    def _get_tagdict(self):
        """Returns a dictionary mapping each xml to its tags.

        Args:
            None

        Returns:
            A dictionary where dict[n] = all tags in xml #n

        """
        if not self.xmls:
            raise ValueError, "xmls input must contain at least one element"
        tagdict = {} #tagdict[n] = tags for annotator #n
        categories = []
        for annotator, xml in enumerate(self.xmls):
            root = ET.parse(xml).getroot()
            self.docLen = len(root.find('TEXT').text)
            tags = []
            for child in root.find('TAGS'):
                if 'text' in child.attrib.keys(): #make sure it's not a link
                    if child.attrib['text']: #ignore non-consuming tags
                        tags.append(child)
                        if child.tag not in categories:
                            categories.append(child.tag)
            tagdict[annotator] = tags
        categories.append('NONE')
        self.categories = categories
        return tagdict
    
    def build_rows(self):
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
        self.rows = rows
            
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
            raise ValueError, "Call build_rows before building table."
        self.table = numpy.zeros((len(self.rows), len(self.categories)), dtype=int)
        for row, matched in enumerate(self.rows):
            for tag in matched:
                column = self.categories.index(tag.tag)
                self.table[row][column] += 1
