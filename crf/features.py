# -*- coding: utf-8 -*-

"""Feature extraction for a CRF

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import xml.etree.ElementTree as ET
import re

import numpy
import tagdoc as td

#change this according to your file system
GOLD_DIR = "/users/sethmachine/desktop/Tokenized"

#global list of ISO-Space tags which have extents, i.e. not relations.
ISO_CATEGORIES = ['PLACE', 'PATH', 'SPATIAL_ENTITY', 'NONMOTION_EVENT',
                  'MOTION', 'SPATIAL_SIGNAL', 'MOTION_SIGNAL', 'MEASURE', 'NONE']

def binary_search(token, sorted_tags, counter=1):
    """A simple binary search to determine which tag contains the token.

    Performs a binary search across all sorted_tags, sorted by start spans
    from least to greatest.  A tag matches a given token if the token's
    start and end spans are within that tag's start/end spans.
    Takes at most log(len(sorted_tags)) iterations.

    Args:
        token: A lexer token of the form (start, end, word), where
            start is the index of where the token begins,
            end is the index of where the token ends,
            and word is the actual token string.
        sorted_tags: A list of sorted ET tags from an annotated xml.
            The tags are sorted by the value of their start span.
        counter: An integer keeping track of the number of iterations,
            primarily for debugging purposes,
            i.e. counter <= log(len(sorted_tags))

    Returns:
        The tag which contains that token,
        or None if there is no tag which has that token.

    """
    if not sorted_tags: #token isn't tagged in any extent
        return None
    size = len(sorted_tags)
    index = size / 2
    curr = sorted_tags[index]
    if int(token.attrib['begin']) >= int(curr.attrib['start']) and int(token.attrib['end']) <= int(curr.attrib['end']):
        return curr
    if int(token.attrib['begin']) > int(curr.attrib['end']):
        return binary_search(token, sorted_tags[index + 1:size], counter + 1)
    elif int(token.attrib['end']) < int(curr.attrib['start']):
        return binary_search(token, sorted_tags[0:index], counter + 1)
    else: #if we get here, the token somehow overlaps extents!
        return None
    
def token_label(token, sorted_tags):
    """Returns the label of a given token.

    """
    tag = binary_search(token, sorted_tags)
    if tag == None:
        return 'None'
    return tag.tag

class CRF_Features:
    """Wrapper for extracting features for a CRF

    """
    def __init__(self, golddir=GOLD_DIR, categories=ISO_CATEGORIES):
        self.dir = golddir
        self.tagdir = td.TagDir(golddir)
        self.categories = categories

    def _get_tagdoc_tags(self):
        t = self.tagdir.docs[5]
        tags = [child for child in t.root.find('TAGS') if child.tag in self.categories and child.attrib['text']]
        tags.sort(key=lambda x: int(x.attrib['start']))
        return tags
        #return self.tagdir.docs[5].tags

    def label(self):
        w = open("train.txt", 'w')
        for tagdoc in self.tagdir.docs:
            tags = tagdoc.xmlTags
            tags.sort(key=lambda x: int(x.attrib['start']))
            for sentence in tagdoc.sentences:
                sequence = ""
                for index, lex in enumerate(sentence):
                    sequence += token_label(lex, tags)
                    sequence += "\tword=" + lex.text
                    if index == 0:
                        sequence += "\t__BOS__"
                    sequence += "\n"
                print>>w, sequence.encode('utf-8')
        w.close()
    
#test = td.GOLD_DIR
c = CRF_Features(GOLD_DIR)
z = c.label()
