# -*- coding: utf-8 -*-

"""Code to compute Fleiss' Kappa

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os
import re

#import main.fleiss_table as fl_table
#import table.tokens
#import table.extents
#import table.links

#row types
TOKEN = 0
EXTENT = 1
LINK = 2
#token spans
START = 0
END = 1

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = '/users/sethmachine/desktop/Adjudication/47_N_27_E'

#regex to collect only certain xml/dir names
dir_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+', re.IGNORECASE)
xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

def is_tag_match(tag1, tag2):
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
    
def getTable(xmls, tableType=TOKEN, unmatch=True):
    if tableType == TOKEN:
        print 'got here'
        f = table.tokens.Table(xmls)
    elif tableType == EXTENT:
        f = table.extents.Table(xmls, unmatch=unmatch)
    elif tableType == LINK:
        f = table.links.Table(xmls)
    f.build_rows()
    f.build_table()
    return f.table
        
def perm(keys, keyValues):
    """Returns a list of all permutations of a sequence of keys

    Given a sequence of keys and a corresponding dictionary for
    their values, this function uses a dynamic programming approach
    to iteratively compute all possible permutations of the key values
    in order of the list of keys given.

    Args:
        keys: A list of keys for the dictionary keyValues.
        keyValues: A dictionary which has defined values for all keys.

    Returns:
        List of all permutations of keys and their associated key values.

    """
    n = len(keys)
    trellis = {}
    trellis[0] = [[x] for x in keyValues[keys[0]]]
    for x in xrange(0 + 1, n):
        trellis[x] = []
        for value in keyValues[keys[x]]:
            l = [value]
            for entry in trellis[x - 1]:
                trellis[x].append(entry + l)
    return trellis[n - 1]

def permute(tags, linktype, semantics):
    """Returns a list of all tag relations for that linktype

    Generates a list of all possible relations between a given set
    of tags, where each relation matches the semantics of that linktype.
    The semantics is an n-tuple, where each element contains the possible
    tag types corresponding to that link attribute.

    Args:
        tags: A list of ElementTree.Element tags.
        linktype: A string denoting the link type, e.g. 'QSLINK'.
        semantics: A list mapping each link attribute to its possible tag types.
                The length of the list indicates the valency of the relation.

    Returns:
        A list of all possible tag relations for the linktype.

    """
    keyTags = {} #all tags which match a given key
    keys = semantics.keys()
    keySize = len(keys)
    for key in keys:
        keyTags[key] = [tag for tag in tags if tag.tag in semantics[key] and tag.attrib['text']]
    trellis = {}
    return perm(keys, keyTags)

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
    if token[START] >= int(curr.attrib['start']) and token[END] <= int(curr.attrib['end']):
        return curr
    if token[START] > int(curr.attrib['end']):
        return binary_search(token, sorted_tags[index + 1:size], counter + 1)
    elif token[END] < int(curr.attrib['start']):
        return binary_search(token, sorted_tags[0:index], counter + 1)
    else: #if we get here, the token somehow overlaps extents!
        return None
