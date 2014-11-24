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

import argparse
import os
import re
import sys

import main.algorithm as fl
from main.main import *



parser = argparse.ArgumentParser(description='Compute Fleiss\' Kappa.')

parser.add_argument('source', metavar='S', type=str,
                    help='source directory for computing IAA')

parser.add_argument('--type', type=str, dest='type', choices=['tokens', 'extents', 'links'],
                    default='tokens', help='specify the object to check IAA for: tokens, extents, or links')

parser.add_argument('--linkType', dest='linkType', default='QSLINK', type=str,
                    help='link type to check IAA for')

parser.add_argument('--suffix', default='', type=str,
                    help='only collects xmls whose file name ends in suffix')

parser.add_argument('--exact', dest='exact', action='store_const',
                    const=True, default=False,
                    help='only considers extents across all annotators')

parser.add_argument('--recursive', dest='search', action='store_const',
                    const=getXmlDict, default=getXmls,
                    help='specify to search top directory recursively')
                    
args = parser.parse_args()
tableType = 0
print args
if args.type == 'tokens':
    tableType = TOKEN
elif args.type == 'extents':
    tableType = EXTENT
elif args.type == 'links':
    tableType = LINK
scores = fleiss(args.search(args.source, phase=args.suffix), args.exact, tableType, linkType=args.linkType)

if isinstance(scores, dict):
    avg = 0.0
    for key in scores.keys():
        avg += scores[key]
        print key + ": " + str(scores[key])
    print "Average: " + str((avg / len(scores.keys())))
else:
    print scores

    
    

        
