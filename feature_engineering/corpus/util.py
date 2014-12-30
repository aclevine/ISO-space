# -*- coding: utf-8 -*-

"""Utility functions.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""
from __future__ import division
from collections import defaultdict
from itertools import chain, combinations
import os, re

def is_full_qslink(link):
    is_full = True
    attrs = ['fromText', 'toText', 'trigger']
    for attr in attrs:
        if attr not in link.attrib or not link.attrib[attr]:
            is_full = False
    return is_full

def is_same_qslink(link1, link2):
    is_match = True
    attrs = ['fromText', 'toText', 'trigger']
    for attr in attrs:
        if link1.attrib[attr] != link2.attrib[attr]:
            is_full = False
    return is_full
    

def getXmls(dirpath, recursive=True):
    files = []
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            if f.endswith('.xml'):
                files.append(fpath)
        if recursive:
            if os.path.isdir(fpath):
                files += getXmls(fpath, recursive)
    return files

def all_subsets(ss):
  return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))

def check(attribs, subset, link):
    for attrib in attribs:
        if attrib in subset:
            if link.attrib[attrib]:
                continue
        elif attrib not in subset:
            if link.attrib[attrib]:
                return False
    return True

def subset_str(subset):
    return '_'.join([x for x in subset])

id_pattern = re.compile(r'[0-9]+')

def link_stats(linkdict):
    z = {}
    types = {}
    for link_type in ['QSLINK', 'OLINK', 'MOVELINK']:
        qs = linkdict[link_type]
        attribs = ['toText', 'fromText', 'trigger']
        d = defaultdict(list)
        thistype = defaultdict(int)
        for link in qs:
            for subset in all_subsets(attribs):
                if check(attribs, subset, link):
                    d[subset_str(subset)].append(link)
                    thistype[id_pattern.sub('', link.attrib['toID']) + '_to'] += 1
                    thistype[id_pattern.sub('', link.attrib['fromID']) + '_from'] += 1
                    thistype[id_pattern.sub('', link.attrib['trigger'])] += 1
                    break
        qs_count = len(qs)
        print "============ " + link_type + " ============"
        print "Total links of link type " + link_type + " : " + str(qs_count)
        for key in d.keys():
            count = len(d[key])
            percent = count * 1.0 / qs_count
            print "Total number of links of type <" + key + "> : " + str(count)
            print "Percent of links of type <" + key + "> : " + str(percent)
            print '\n'
        z[link_type] = d
        types[link_type] = thistype
    return (types, z)
