# -*- coding: utf-8 -*-

"""Module to build training sequences for QSLINKs

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""
from collections import defaultdict
from itertools import chain, combinations, permutations
import re

from space_document import *

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

#['e7', 'pl1', 's1']

def qs(doc):
    train = []
    """
    links = [link for link in t.linkdict['QSLINK']
         if link.attrib['trigger'] and
         link.attrib['toText'] and link.attrib['fromText']]
    """
    links = doc.linkdict['QSLINK']
    for sent in doc.sents:
        lexes = collapse_lexes([lex for lex in sent if lex.attrib['label'] in labels])
        pairs = list(permutations(lexes, 2))
        triggers = [lex for lex in sent if lex.attrib['label'] == 'SPATIAL_SIGNAL']
        for trigger in triggers:
            triggerID = trigger.attrib['id']
            for (figure, ground) in pairs:
                figureID = figure.attrib['id']
                groundID = ground.attrib['id']
                ids = [figureID, groundID, triggerID]
                link = attrvalues_to_link(attributes, ids, links)
                train.append((link, trigger, figure, ground))
    return train

q = qs(t)
links = [link for link in t.linkdict['QSLINK']
         if link.attrib['trigger'] and
         link.attrib['toText'] and link.attrib['fromText']]
        
