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
cmd_subfolder1 = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"baseline_classifier/Corpora")))
cmd_subfolder2 = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"")))
cmd_subfolder1 = cmd_subfolder1.replace('fleiss/', '')
cmd_subfolder2 = cmd_subfolder2.replace('/table', '')
if cmd_subfolder1 not in sys.path:
    sys.path.insert(0, cmd_subfolder1)
    sys.path.insert(0, cmd_subfolder2)
import re
import xml.etree.ElementTree as ET

import util.util
from util.link_semantics import INT_LINKS
import numpy
import tokenizer
import table

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
EXTENT = 0
TOKEN = 1
LINK = 2 #for links

#token spans
START = 0
END = 1

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
    def __init__(self, xmls, linkType='QSLINK'):
        super(Table, self).__init__(xmls)
        self.linkType = linkType
        self.links = [linkType, 'NONE']
        self.semantics = INT_LINKS[linkType]

    def _is_link_match(self, relation, link):
        """Determines if a relation of tags and a link match.            
        """
        keys = self.semantics.keys()
        for x in xrange(0, len(keys)):
            if relation[x].attrib['id'] != link.attrib[keys[x]]:
                return False
        return True
            
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
        
    def build_rows(self):
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
        permutations = util.util.permute(tags, self.linkType, self.semantics)
        rows = [] #list of lists
        for relation in permutations:
            row = []
            for xml in tagdict.keys():
                unmatched=True
                links = linkdict[xml]
                for link in links:
                    if self._is_link_match(relation, link):
                        #print relation, link, xml
                        row.append(ET.Element(self.linkType))
                        unmatched=False
                        break
                if unmatched:
                    row.append(ET.Element('NONE'))
            rows.append(row)
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
            raise ValueError, "call build_rows before building table"
        self.table = numpy.zeros((len(self.rows), len(self.links)), dtype=int)
        for row, matched in enumerate(self.rows):
            for tag in matched:
                column = self.links.index(tag.tag)
                self.table[row][column] += 1
        
