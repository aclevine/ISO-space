# -*- coding: utf-8 -*-

"""Code to compute Fleiss' Kappa

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os
import re

import fleiss_alg as fl
import fleiss_table as fl_table

#row types
EXTENT = 0
TOKEN = 1
LINK = 2 #for links
#token spans
START = 0
END = 1

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = '/users/sethmachine/desktop/Adjudication/47_N_27_E'

#regex to collect only certain xml/dir names
dir_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+', re.IGNORECASE)
xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

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

def getXmls(path, phase='p2'):
    """Finds all xml files in a flat directory.

    Collects all xml files which match the xml_pattern.
    The pattern excludes files with suffixes like "extentsLocked."

    Args:
        path: A string absolute path for the directory.
        phase: A suffix on the xml file name used to discriminate
            between tag annotation and link annotation.

    Returns:
        A list of all xml files matching xml_pattern.
    """
    files = []
    phase_pattern = re.compile(phase + '\.xml$')
    for f in os.listdir(path):
        fpath = os.path.join(path, f)
        if phase_pattern.search(f):
            files.append(fpath)
    return files

def getXmlDict(path, d={}, dname='', phase='p2'):
    """Finds all xml files recursively in a directory, storing them in a dictionary.

    Searches recursively from the top directory for all xml files.
    For each directory that it passes, a dictionary entry is made
    which maps that directory name to all the xmls found in it.

    Args:
        path: A string absolute path for the directory.
        d: A dictionary object (ignore this argument).
        dname: A dictionary key (ignore this argument).
        phase: A suffix on the xml file name used to discriminate
            between tag annotation and link annotation.

    Returns:
        A dictionary mapping each directory name to a list of xmls inside it.
    """
    phase_pattern = re.compile(phase + '\.xml$')
    if dname:
        d[dname] = []
    for f in os.listdir(path):
        fpath = os.path.join(path, f)
        if os.path.isfile(fpath):
            if phase_pattern.search(f):
                d[dname].append(fpath)
        elif os.path.isdir(fpath): #and dir_pattern.match(f):
            d = dict(d.items() + getXmlDict(fpath, d, f, phase).items())
    return {x:d[x] for x in d.keys() if d[x] and len(d[x]) > 1}

def fleiss(xmls, unmatch=True, rowType=TOKEN):
    """Computes Fleiss' Kappa between lists of xmls.

    Calculates Fleiss' Kappa given a list of xmls.  If xmls
    is a dictionary, Fleiss' Kappa is computed for each key.
    Otherwise, a single Fleiss' Kappa is computed.

    Args:
        xmls: A list of xmls for a single task or a dictionary
        where each key is a different task.

    Returns:
        If xmls is a dictionary:
            A dictionary mapping each task to its Fleiss' Kappa score.
        Else:
            Fleiss' Kappa score for the single task.
    """
    useLinks = False
    if rowType == LINK:
        useLinks = True
    if type(xmls) == dict:
        fleiss_scores = {}
        for key in xmls.keys():
            f = fl_table.Fleiss_Table(xmls[key], isLinks=useLinks)
            f.build_rows(rowType, unmatch)
            f.build_table()
            score = fl.fleiss_wikpedia(f.table)
            fleiss_scores[key] = score
        return fleiss_scores
    f = fl_table.Fleiss_Table(xmls, isLinks=useLinks)
    f.build_rows(rowType, unmatch)
    f.build_table()
    return fl.fleiss_wikpedia(f.table)
