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
import xml.etree.ElementTree as ET

from util.util import *
import numpy
import tokenizer
import table

class Table(table.Table):
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
        super(Table, self).__init__(xmls)
        
    def _get_tokens(self, xml):
        """Gets lex tokens from an xml.

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
