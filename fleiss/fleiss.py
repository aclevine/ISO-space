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

import fleiss_alg as fl
import fleiss_table as fl_table
from fleiss_util import *

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = '/users/sethmachine/desktop/Adjudication/47_N_27_E'

#regex to collect only certain xml/dir names
dir_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+', re.IGNORECASE)
xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)


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
            if not f: #dictionary is empty
                raise ValueError, "No xml files could be found matching the pattern."
            for key in f.keys():
                print key, ':', f[key]
                avg += f[key]
            print "Average: " + str((avg / len(f.keys())))
        else:
            print fleiss(getXmls(source), unmatch, rowType)
    except OSError:
        print "The directory " + source + " does not exist."
        usage()
        sys.exit(2)
        
if __name__ == '__main__':
    main(sys.argv[1:])
    
    

        
