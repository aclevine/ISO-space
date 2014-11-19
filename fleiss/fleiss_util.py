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

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = '/users/sethmachine/desktop/Adjudication/47_N_27_E'

#regex to collect only certain xml/dir names
dir_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+', re.IGNORECASE)
xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

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

    Calculates Fleiss' Kappa given a list of xmls.  If the xmls
    is a dictionary, Fleiss' Kappa is computed for each key.
    Otherwise, a single Fleiss' Kappa is computed.

    Args:
        xmls: A list of xmls or a dictionary where each key is a different task.

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
