# -*- coding: utf-8 -*-

"""Fleiss' Kappa for inter-annotator agreement.

This module builds the table for calculating Fleiss' Kappa (κ).
Only the numpy library is required; otherwise the extents and tags
are extracted with the ElementTree module.

This module by itself does not compute Fleiss' Kappa; use an outside
module to take the table as input.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os
import re
import numpy
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
        
