# -*- coding: utf-8 -*-

"""Script to compute Fleiss' Kappa for inter-annotator agreement

This module computes Fleiss' Kappa score between a group of annotators over
the same document and its extents.  This module can be run in the commandline and either passed
a flat directory (i.e. a single document to check IAA) or a recursive directory (multiple documents).

Here is a sample line that computes Fleiss' Kappa for all annotated xmls in Adjudication
and saves it to a local text file.

python fleiss_main.py -r /users/sethmachine/desktop/Adjudication > fleiss.txt

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import getopt
import os
import re
import sys

import fleiss as fl
import fleiss_table as fl_table

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = os.path.join(ADJUDICATED_PATH, '47_N_27_E')

#regex to collect only certain xml/dir names
dir_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+', re.IGNORECASE)
xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

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

def getXmlDict(path=ADJUDICATED_PATH, d={}, dname='', use_pattern=True):
    """Finds all xml files recursively in a directory.

    Searches recursively from the top directory for all xml files.
    For each directory that it passes, a dictionary entry is made
    which maps that directory name to all the xmls found in it.

    Args:
        path: A string absolute path for the directory.
        d: A dictionary object (ignore this argument).
        dname: A dictionary key (ignore this argument).
        use_pattern: A flag to switch off a regex pattern (not in use yet).

    Returns:
        A dictionary mapping each directory name to a list of xmls inside it.
    """
    if dname:
        d[dname] = []
    for f in os.listdir(path):
        fpath = os.path.join(path, f)
        if os.path.isfile(fpath):
            if xml_pattern.match(f):
                d[dname].append(fpath)
        elif os.path.isdir(fpath) and dir_pattern.match(f):
            d = dict(d.items() + getXmlDict(fpath, d, f).items())
    return d

def fleiss(xmls = getXmlDict(), unmatch=True, rowType=fl_table.TOKEN):
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
    if type(xmls) == dict:
        fleiss_scores = {}
        for key in xmls.keys():
            f = fl_table.Fleiss_Table(xmls[key])
            f.build_rows(rowType, unmatch)
            f.build_table()
            score = fl.fleiss_wikpedia(f.table)
            fleiss_scores[key] = score
        return fleiss_scores
    f = fl_table.Fleiss_Table(xmls)
    f.build_rows(rowType, unmatch)
    f.build_table()
    return fl.fleiss_wikpedia(f.table)
            
def usage():
    print "Usage: [-r] [-m] [-x] path/to/directory"
    print "Specify the -r flag if the directory is recursive."
    print "Specify the -m flag to only consider exact matches."
    print "Specify the -x flag to consider extents instead of tokens."

def main(argv):
    recursive = False
    unmatch = True
    rowType = fl_table.TOKEN
    try:
        opts, args = getopt.getopt(argv, 'hrmxd', ['help', 'recursive', 'match', 'extents'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ('-r', '--recursive'):
            recursive = True
        elif opt in ('-m', '--match'):
            unmatch = False
        elif opt in ('-x', '--extents'):
            rowType = fl_table.EXTENT
    source = "".join(args)
    try:
        if recursive:
            avg = 0.0
            f = fleiss(getXmlDict(source), unmatch, rowType)
            for key in f.keys():
                print key, ':', f[key]
                avg += f[key]
            print "Average: " + str((avg / len(f.keys())))
        else:
            print fleiss(getXmls(source), unmatch, rowType)
    except OSError:
        print "The directory " + source + " does not exist."
        sys.exit(2)
        
if __name__ == '__main__':
    main(sys.argv[1:])
    
    

        
