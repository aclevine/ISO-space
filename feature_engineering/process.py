# -*- coding: utf-8 -*-

"""Code to reprocess ISO-Space xmls and add new features

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os, re

from corpus.space_document import Space_Document
from corpus.space_corpus import Space_Corpus
from dirs import mkparentdirs, setup_newdir, test
from sparser.sparser import p2edges as p
from sparser.ledge import ledge, ledges
from stanford.taggers import pos
from stanford.taggers import ner
import tagdoc as td
#from tagdoc import binary_search#,doc
from util.binary_search import binary_search
from util.lex import Lex
#from util.sentence import Sentence
from util.unicode import ureplace as u
from util.unicode import u2ascii

GOLDDIR = '/users/sethmachine/desktop/Tokenized'
NEWDIR = '/users/sethmachine/desktop/TokenizedPlus/'
TESTDIR = '/users/sethmachine/desktop/Test'

xml_tokens_pattern = re.compile(r'<TOKENS>.+</TOKENS>', re.DOTALL)
sentence_pattern = re.compile(r'<s>.+?</s>', re.DOTALL)
lex_attrs_pattern = re.compile(r'(?<=<lex)[^>]+')

#d = Space_Document('/users/sethmachine/desktop/Tokenized/RFC/Amazon.xml')

"""
def process(tagdoc, golddir, newdir='', suffix='++', renew=False, debug=False):
    path = setup_newdir(tagdoc, golddir, newdir, suffix, renew=renew)
    if not path:
        return
    mkparentdirs(path)
    w = open(tagdoc.filename, 'r')
    t = w.read()
    w.close()
    #grab only tags which have a text extent
    iso_tags = [x for x in tagdoc.tags if 'start' in x.attribNames]
    iso_tags.sort(key=lambda x: int(x.attrib['start'])) #sort for binary search
    for (i,m) in enumerate(re.finditer(sentence_pattern, t)):
        sentence = tagdoc.sentences[i]
        old_lexes = sentence.getchildren()
        raw_sentence = m.group()
        tokens = [''.join([c if ord(c) < 128 else u2ascii[c] for c in x.text]).encode('utf-8') for x in old_lexes]
        pos_tags = pos.tag(tokens)
        ner_tags = ner.tag(tokens)
        edges = []
        try:
            if debug:
                print ' '.join([x for x in tokens])
            edges = p(' '.join([x for x in tokens]), split=True)
        except:
            pass
        c = 0
        for (j, n) in enumerate(re.finditer(lex_attrs_pattern, raw_sentence)):
            old_lex = old_lexes[j]
            new_lex = Lex(old_lex.text, old_lex.attrib)
            attributes = n.group()
            tag = binary_search((int(old_lex.attrib['begin']), int(old_lex.attrib['end']), old_lex.text), iso_tags)
            label = 'None'
            if type(tag) != type(None):
                label = tag.name
            new_lex.add(('label', label))
            if type(tag) != type(None):
                    new_lex.addAll([(key, tag.attrib[key]) for key in tag.attrib])
            if pos_tags:
                if tokens[j] == pos_tags[c][0]:
                    new_lex.add(('pos', pos_tags[c][1]))
                    pos_tags.remove(pos_tags[c])
            if ner_tags: #this error case comes up for RFC/Durango.xml
                if tokens[j] == ner_tags[c][0]:
                    new_lex.add(('ner', ner_tags[c][1]))
                    ner_tags.remove(ner_tags[c])
            if edges:
                sparser_edge = ledge(edges, tokens[j])
                if sparser_edge:
                    if sparser_edge.keyvalues:
                        keyvalues = sparser_edge.keyvalues[sparser_edge.keyvalues.keys()[0]]
                        new_lex.addAll([(key, keyvalues[key]) for key in keyvalues])
            t = t.replace(attributes, str(new_lex))
    w = open(path, 'w')
    print>>w, t
    w.close()
    print test(tagdoc, td.TagDoc(path))
"""

class Feature_Process(object):
    """Wrapper for adding features to ISO-Space xmls.

    """
    def __init__(self, xmls, golddir, newdir='', suffix='++',
                 feature_functions=[], renew=False, debug=False):
        self.xmls = xmls
        self.golddir = golddir
        self.newdir = newdir
        self.suffix = suffix
        self.feature_functions = feature_functions
        self.renew = renew
        self.debug = debug
        self.heavy = False

    def process(self):
        for xml in self.xmls:
            path = setup_newdir(xml, self.golddir, self.newdir,
                                self.suffix, self.renew)
            if not path:
                continue
            mkparentdirs(path)
            with open(xml, 'r') as oldfile:
                text = oldfile.read()
            doc = Space_Document(xml)
            tags = [tag for tag in doc.tags if 'start' in tag.attrib]
            new_text = text
            for (i,m) in enumerate(re.finditer(sentence_pattern, text)):
                sentence = doc.sentences[i]
                doc_lexes = sentence.getchildren()
                xml_sentence = m.group()
                tokens = [''.join([c if ord(c) < 128
                                   else u2ascii[c]
                                   for c in x.text]).encode('utf-8')
                          for x in doc_lexes]
                (pos_tags, ner_tags, edges) = ([], [], [])
                if self.heavy:
                    pos_tags = pos.tag(tokens)
                    ner_tags = ner.tag(tokens)
                    try:
                        if self.debug:
                            print ' '.join([x for x in tokens])
                        edges = p(' '.join([x for x in tokens]), split=True)
                    except:
                        'somehow got here'
                c = 0
                for (j, n) in enumerate(re.finditer(lex_attrs_pattern,
                                                    xml_sentence)):
                    doc_lex = doc_lexes[j]
                    new_lex = Lex(doc_lex.text, doc_lex.attrib)
                    attributes = n.group()
                    tag = binary_search((int(doc_lex.attrib['begin']),
                                         int(doc_lex.attrib['end']),
                                         doc_lex.text), tags)
                    label = 'None'
                    if type(tag) != type(None):
                        label = tag.tag
                    new_lex.add(('label', label))
                    new_lex.add(('word', new_lex.text.encode('utf-8')))
                    if type(tag) != type(None):
                            new_lex.addAll([(key.encode('utf-8'), tag.attrib[key].encode('utf-8')) for key in tag.attrib])
                    greedyEdge = p(tokens[j], split=True)
                    if greedyEdge:
                        gedge = greedyEdge[0]
                        if gedge.keyvalues and gedge.m:
                            keyvalues = gedge.keyvalues[gedge.keyvalues.keys()[0]]
                            new_lex.addAll([('L' + key, keyvalues[key]) for key in keyvalues])
                    if pos_tags:
                        if tokens[j] == pos_tags[c][0]:
                            new_lex.add(('pos', pos_tags[c][1]))
                            pos_tags.remove(pos_tags[c])
                    if ner_tags: #this error case comes up for RFC/Durango.xml
                        if tokens[j] == ner_tags[c][0]:
                            new_lex.add(('ner', ner_tags[c][1]))
                            ner_tags.remove(ner_tags[c])
                    if edges:
                        sparser_edge = ledge(edges, tokens[j])
                        if sparser_edge:
                            if sparser_edge.keyvalues:
                                keyvalues = sparser_edge.keyvalues[sparser_edge.keyvalues.keys()[0]]
                                new_lex.addAll([(key, keyvalues[key]) for key in keyvalues])
                    new_lex.addAll([function(new_lex) for function in self.feature_functions])
                    new_text = new_text.replace(attributes, str(new_lex))
            w = open(path, 'w')
            print>>w, new_text
            w.close()
            #print test(tagdoc, td.TagDoc(path))
"""
f = Feature_Process([d.filepath], GOLDDIR,
                    newdir='YOO', renew=True, debug=True)

f.heavy=True
f.debug = False

f.process()
"""
            
"""
def process(tagdoc, golddir, newdir='', suffix='++', renew=False, debug=False):
    path = setup_newdir(tagdoc, golddir, newdir, suffix, renew=renew)
    if not path:
        return
    mkparentdirs(path)
    w = open(tagdoc.filename, 'r')
    t = w.read()
    w.close()
    #grab only tags which have a text extent
    iso_tags = [x for x in tagdoc.tags if 'start' in x.attribNames]
    iso_tags.sort(key=lambda x: int(x.attrib['start'])) #sort for binary search
    for (i,m) in enumerate(re.finditer(sentence_pattern, t)):
        sentence = tagdoc.sentences[i]
        old_lexes = sentence.getchildren()
        raw_sentence = m.group()
        tokens = [''.join([c if ord(c) < 128 else u2ascii[c] for c in x.text]).encode('utf-8') for x in old_lexes]
        pos_tags = pos.tag(tokens)
        ner_tags = ner.tag(tokens)
        edges = []
        try:
            if debug:
                print ' '.join([x for x in tokens])
            edges = p(' '.join([x for x in tokens]), split=True)
        except:
            pass
        c = 0
        for (j, n) in enumerate(re.finditer(lex_attrs_pattern, raw_sentence)):
            old_lex = old_lexes[j]
            new_lex = Lex(old_lex.text, old_lex.attrib)
            attributes = n.group()
            tag = binary_search((int(old_lex.attrib['begin']), int(old_lex.attrib['end']), old_lex.text), iso_tags)
            label = 'None'
            if type(tag) != type(None):
                label = tag.name
            new_lex.add(('label', label))
            if type(tag) != type(None):
                    new_lex.addAll([(key, tag.attrib[key]) for key in tag.attrib])
            if pos_tags:
                if tokens[j] == pos_tags[c][0]:
                    new_lex.add(('pos', pos_tags[c][1]))
                    pos_tags.remove(pos_tags[c])
            if ner_tags: #this error case comes up for RFC/Durango.xml
                if tokens[j] == ner_tags[c][0]:
                    new_lex.add(('ner', ner_tags[c][1]))
                    ner_tags.remove(ner_tags[c])
            if edges:
                sparser_edge = ledge(edges, tokens[j])
                if sparser_edge:
                    if sparser_edge.keyvalues:
                        keyvalues = sparser_edge.keyvalues[sparser_edge.keyvalues.keys()[0]]
                        new_lex.addAll([(key, keyvalues[key]) for key in keyvalues])
            t = t.replace(attributes, str(new_lex))
    w = open(path, 'w')
    print>>w, t
    w.close()
    print test(tagdoc, td.TagDoc(path))
"""
        

def printchild(s):
	return ''.join([x.text + ', ' for x in s.getchildren()])
