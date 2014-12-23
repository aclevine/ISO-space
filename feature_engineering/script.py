# -*- coding: utf-8 -*-

"""Script to add additional features to ISO-Space gold standard.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import argparse
import os, re, sys

from dirs import getXmls
from process import Feature_Process



parser = argparse.ArgumentParser(description='Add features to document(s).')

parser.add_argument('source', metavar='S', type=str,
                    help='source directory for documents to process')

"""
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

parser.add_argument('--plot', dest='plot', action='store_const',
                    const=True, default=False,
                    help='generates a plot in LaTeX')
"""
                    
args = parser.parse_args()
tableType = 0
print args
print args.source

xmls = getXmls(args.source)
#gold = process.td.TagDir(args.source)

f = Feature_Process(xmls, golddir=args.source, renew=False, debug=False)
f.heavy = True

f.process()

#for doc in gold.docs:
    #process.process(doc, golddir=args.source, renew=False)

print 'Done!'
quit()
"""
if args.type == 'tokens':
    tableType = TOKEN
elif args.type == 'extents':
    tableType = EXTENT
elif args.type == 'links':
    tableType = LINK

if not args.plot: #we aren't building any plots
    scores = fleiss(args.search(args.source, phase=args.suffix), args.exact, tableType, linkType=args.linkType)
    print_fleiss(scores)

elif args.plot: #let's build a plot
    scoreDict = {}
    #scoreDict['tokens'] = fleiss(args.search(args.source, phase=args.suffix), args.exact, TOKEN, linkType=args.linkType)
    #scoreDict['extents'] = fleiss(args.search(args.source, phase=args.suffix), True, EXTENT, linkType=args.linkType)
    #scoreDict['match extents'] = fleiss(args.search(args.source, phase=args.suffix), False, EXTENT, linkType=args.linkType)
    scoreDict['QSLINK'] = fleiss(args.search(args.source, phase=args.suffix), args.exact, LINK, linkType='QSLINK')
    scoreDict['OLINK'] = fleiss(args.search(args.source, phase=args.suffix), True, LINK, linkType='OLINK')
    #scoreDict['match extents'] = fleiss(args.search(args.source, phase=args.suffix), False, EXTENT, linkType=args.linkType)
    z = lp.Line_Plot(scoreDict, 'Yo')
    z.make_tex()
    print z.tex
"""
        
    
    

        
