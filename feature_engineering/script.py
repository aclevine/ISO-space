# -*- coding: utf-8 -*-

import argparse
import os, re, sys

from dirs import getXmls
from process import Feature_Process



parser = argparse.ArgumentParser(description='Add features to document(s).')

parser.add_argument('source', metavar='S', type=str,
                    help='source directory for documents to process')

                    
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
        
