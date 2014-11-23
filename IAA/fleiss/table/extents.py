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
cmd_subfolder = cmd_subfolder.replace('IAA/fleiss/table', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import xml.etree.ElementTree as ET

import numpy
import table
import util.util

class Table(table.Table):
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
    def __init__(self, xmls, unmatch=True):
        super(Table, self).__init__(xmls)
        self.unmatch = unmatch
    
    def build_rows(self):
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
                        if util.util.is_tag_match(tag, otherTag):
                            match.append(otherTag)
                            otherTags.remove(otherTag)
                            unmatched = False
                            break
                    if unmatched and self.unmatch:
                        match.append(ET.Element('NONE'))
                if self.unmatch:
                    rows.append(match)
                elif len(match) == self.numXmls:
                    rows.append(match)
        self.rows = rows
