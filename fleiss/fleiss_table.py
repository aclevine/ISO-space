# -*- coding: utf-8 -*-

"""Fleiss' Kappa for inter-annotator agreement.

This module builds the table for calculating Fleiss' Kappa (κ).
Only the numpy library is required; otherwise the extents and tags
are extracted with the ElementTree module.

This module by itself does not compute Fleiss' Kappa; use an outside
module to take the table as input.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import numpy
import xml.etree.ElementTree as ET

#global list of ISO-Space tags which have extents, i.e. not relations.
ISO_CATEGORIES = ['PLACE', 'PATH', 'SPATIAL_ENTITY', 'NONMOTION_EVENT',
                  'MOTION', 'SPATIAL_SIGNAL', 'MOTION_SIGNAL', 'MEASURE']

#example files, change these according to location on computer
ISO_FILE = "/users/sethmachine/desktop/iso-space2/sprl_to_iso-space/CP/45_N_22_E.xml"
f1 = '/users/sethmachine/desktop/WhereToLosAngeles_HOLLYWOOD-MS-p1.xml'
f2 = '/users/sethmachine/desktop/WhereToLosAngeles_HOLLYWOOD-AB-p1.xml'

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

def get_table(xmls, categories = ISO_CATEGORIES):
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
    if not xmls:
        raise ValueError, "xmls input must contain at least one element"
    if not categories:
        raise ValueError, "categories must contain at least one element"
    tag_dict = {} #for mapping each annotator to the extents
    tags = [] #all tags/extents from all annotators
    for annotator, xml in enumerate(xmls):
        root = ET.parse(xml).getroot()
        #only grabs tags with given categories and ignores non-consuming tags
        tag_dict[annotator] = [child for child in root.find(TAGS) if child.tag in ISO_CATEGORIES and child.attrib['text']]
        tags += tag_dict[annotator]
    numXmls = len(xmls) #number of annotators
    matched_tags = [] #list of lists
    unmatched_tags = [] #for debugging purposes
    for tag in tag_dict[FIRST]:
        matched = []
        matched.append(tag)
        #iterate through all other xmls
        #in order to find a match for this tag/extent
        for i in xrange(FIRST + 1, numXmls):
            for otherTag in tag_dict[i]:
                if tag_matches(tag, otherTag):
                    matched.append(otherTag)
                    tag_dict[i].remove(otherTag)
                    break
        if len(matched) == numXmls:
            matched_tags.append(matched)
        else:
            unmatched_tags.append(tag)
        #don't uncomment this line below; it would break the function
        #tag_dict[FIRST].remove(tag)
    #build the numpy array
    fleiss_table = numpy.zeros((len(matched_tags), len(ISO_CATEGORIES)), dtype=int)
    for row, matched in enumerate(matched_tags):
        for tag in matched:
            column = ISO_CATEGORIES.index(tag.tag)
            fleiss_table[row][column] += 1
    return fleiss_table
    
#uncomment for a quick test run
#f = get_table([f1, f2])        
        
        





