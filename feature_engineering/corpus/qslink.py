# -*- coding: utf-8 -*-

"""Module to build training sequences for QSLINKs

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""
from collections import defaultdict
from itertools import chain, combinations, permutations
import re

from space_document import *
from util import is_full_qslink

labels = ['PLACE', 'SPATIAL_ENTITY', 'PATH', 'MOTION', 'NONMOTION_EVENT']
attributes = ['fromID', 'toID', 'trigger']

id_pattern = re.compile(r'[0-9]+')

def collapse_lexes(lexes):
    """Returns all lexes which are spatial elements.

    Iterates over a list of sorted lexes from first to last,
    collapsing all lexes which share the same ISO-space tag,
    and ignoring all lexes whose label is not an ISO-Space spatial element.

    """
    new_lexes = []
    prev_id = ''
    for (i, lex) in enumerate(lexes):
        if lex.attrib['id'] != prev_id:
            new_lexes.append(lex)
            prev_id = lex.attrib['id']
    return new_lexes                       
            
def id_to_type(ID):
    return id_pattern.sub('', ID)

def attrvalues_to_link(attrs, values, links):
    for link in links:
        is_match = True
        for (attr, value) in zip(attrs, values):
            if link.attrib[attr] != value:
                is_match = False
                break
        if is_match:
            return link
    return False

def qs(doc):
    train = []
    links = [link for link in doc.linkdict['QSLINK'] if is_full_qslink(link)]
    for sent in doc.sents:
        lexes = collapse_lexes([lex for lex in sent if lex.attrib['label'] in labels])
        pairs = list(permutations(lexes, 2))
        triggers = [lex for lex in sent if lex.attrib['label'] == 'SPATIAL_SIGNAL']
        for trigger in triggers:
            triggerID = trigger.attrib['id']
            if triggerID == 's27':
                print 'found it'
            for (figure, ground) in pairs:
                figureID = figure.attrib['id']
                groundID = ground.attrib['id']
                if figureID == 'se34' and groundID == 'se35':
                    print 'yo found both them tags'
                    print triggerID, figureID, groundID
                ids = [figureID, groundID, triggerID]
                link = attrvalues_to_link(attributes, ids, links)
                train.append((link, trigger, figure, ground))
    positives = [x for x in train if x[0] != False]
    if len(positives) < len(links):
        print "Created less positive links than possible!"
        print doc.filepath
    elif len(positives) > len(links):
        print "Created more positive links than possible!"
        print doc.filepath
    return train

"""
t = Space_Document('/users/sethmachine/desktop/Train++/ANC/WhereToJapan/Ginza.xml')
q = qs(t)
positives = [x for x in q if x[0] != False]
links = [link for link in t.linkdict['QSLINK'] if is_full_qslink(link)]
l = links
p = positives
p = [x[0] for x in positives]
s = [x for x in l if x not in p]
ids = ['se34', 'se35', 's27']
link = attrvalues_to_link(attributes, ids, links)
"""
