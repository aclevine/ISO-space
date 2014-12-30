# -*- coding: utf-8 -*-

"""Wrapper for an ISO-Space annotated document.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from collections import defaultdict
from itertools import chain, combinations, permutations
import xml.etree.ElementTree as ET

#number of core arguments to a link, e.g.
#a qslink has a figure and a ground
LINK_VALENCY = 2

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


class Space_Document(object):
    """Wrapper for an ISO-Space annotated document.

    """
    def __init__(self, filepath=''):
        self.filepath = filepath
        self.root = ET.parse(filepath).getroot()
        self.text = self.root.find('TEXT').text
        self.ET_tags = self.root.find('TAGS')
        self.tags = [child for child in self.ET_tags if 'LINK' not in child.tag and 'start' in child.attrib]
        self.tags.sort(key=lambda x: int(x.attrib['start']))
        self.links = [child for child in self.ET_tags if 'LINK' in child.tag]
        self.sents = [child for child in self.root.find('TOKENS')]
        self.lexes = [lex for sent in self.sents for lex in sent.getchildren()]
        self.linkdict = self.get_linkdict()
        
    def get_linkdict(self):
        link_types = {link.tag for link in self.links}
        linkdict = {link_type:[] for link_type in link_types}
        for link in self.links:
            linkdict[link.tag].append(link)
        return linkdict

    def is_tuple_link(self, argids, link_type):
        for link in self.linkdict[link_type]:
            for (arg, ID) in argids:
                if link.attrib[arg] != ID:
                    if argids == [('toID', 'pl8'), ('fromID', 'e14'), ('trigger', 's3')]:
                        print 'fuck'
                        return (link, argids)
                    return False
            return True
                    
    def train_qslinks(self):
        train = []
        labels = ['PLACE', 'SPATIAL_ENTITY', 'PATH', 'MOTION', 'NONMOTION_EVENT']
        for sent in self.sents:
            sent_children = sent.getchildren()
            lexes = [lex for lex in sent_children if lex.attrib['label'] in labels]
            pairs = permutations(lexes, LINK_VALENCY)
            for child in lexes:
                if child.attrib['id'] == 'e14':
                    print 'found it wow'
                    return [x for x in pairs]
            triggers = [lex for lex in sent_children if lex.attrib['label'] == 'SPATIAL_SIGNAL']
            for lex in triggers:
                for (toArg, fromArg) in pairs:
                    a = lexes_to_argids(['toID', 'fromID', 'trigger'], [toArg, fromArg, lex])
                    #print a
                    if a == [('toID', 'pl8'), ('fromID', 'e14'), ('trigger', 's3')]:
                        print 'wtf'
                    if a == [('toID', 'pl0'), ('fromID', 'e5'), ('trigger', 's0')]:
                        print 'found it'
                        print self.is_tuple_link(a, 'QSLINK')
                    label = self.is_tuple_link(a, 'QSLINK')
                    if label == False:
                        train.append(('None', toArg, fromArg, lex))
                    else:
                        #print label.attrib
                        train.append(('QSLINK', toArg, fromArg, lex))
        return train
                        
                    
def lexes_to_argids(args, lexes):
    return [(arg, lex.attrib['id']) for (arg, lex) in zip(args, lexes)]
                    
def trigger_to_link(trigger, links):
    for link in links:
        if 'trigger' in link.attrib:
            if link.attrib['trigger'] == trigger.attrib['id']:
                return link
    return False
        
def id_to_lex(ID, lexes):
    for lex in lexes:
        if 'id' in lex.attrib:
            if lex.attrib['id'] == ID:
                return lex
    return False

labels = ['PLACE', 'SPATIAL_ENTITY', 'PATH', 'MOTION', 'NONMOTION_EVENT']

def link_dist(sent, links):
    dist = []
    lexes = collapse_lexes([lex for lex in sent if 'id' in lex.attrib])
    triggers = [lex for lex in sent if lex.attrib['label'] == 'SPATIAL_SIGNAL']
    for trigger in triggers:
        link = trigger_to_link(trigger, links)
        if type(link) != bool:
            toLex = id_to_lex(link.attrib['toID'], lexes)
            fromLex = id_to_lex(link.attrib['fromID'], lexes)
            if toLex in lexes and fromLex in lexes and trigger in lexes:
                if type(toLex) != bool and type(fromLex) != bool:
                    toDist = lexes.index(trigger) - lexes.index(toLex)
                    fromDist = lexes.index(trigger) - lexes.index(fromLex)
                    dist.append((sent, link, ('toDist', toDist), ('fromDist', fromDist)))
    return dist
            
            
            
        
        
        
    
    
            
            

        

#t = Space_Document('/users/sethmachine/desktop/Train++/RFC/Amazon.xml')
#q = t.linkdict['QSLINK']
#d = t.train_qslinks()
