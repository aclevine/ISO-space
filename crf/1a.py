# -*- coding: utf-8 -*-

"""Builds generated ISO-Space tags given a CRFSuite model.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from collections import defaultdict
from lxml import etree
import xml.etree.ElementTree as ET

from crfsuite.instance import Instance
from crfsuite.sequence import Sequence
from dirs import *
from pycrfsuite import Tagger
from space_document import Space_Document
from space_corpus import Space_Corpus, train, test, config_1b

"""
<PLACE comment="amount=one" continent="" countable="TRUE"
    country="" ctv="" dcl="FALSE" dimensionality="" domain="" elevation=""
	end="1152" form="NOM" gazref="" gquant="" id="pl13" latLong="" mod=""
	scopes="" start="1146" state="" text="school" type="" />
"""

HEADER = '<?xml version="1.0" encoding="UTF-8" ?>'
TASK_ROOT = 'SpaceEvalTaskv1.2'
TAGS_ROOT = 'TAGS'
TOKENS_ROOT = 'TOKENS'
FEATURES_ROOT = 'FEATURES'
INDIR = '/users/sethmachine/desktop/Test++'

obj_attrib = {'countable':'TRUE', 'dimensionality':'', 'form':'NOM'}
motion_attrib = {'motion_class':'', 'motion_sense':'', 'motion_type':''}
measure_attrib = {'unit':'', 'value':''}
ssignal_attrib = {'semantic_type':''}
msignal_attrib = {'motion_signal_type':''}

attribs = {'PLACE':obj_attrib, 'PATH':obj_attrib, 'SPATIAL_ENTITY':obj_attrib,
           'MOTION':motion_attrib, 'SPATIAL_SIGNAL':ssignal_attrib,
           'MOTION_SIGNAL':msignal_attrib, 'MEASURE':measure_attrib}
ids = {'PLACE':'pl', 'PATH':'p', 'SPATIAL_ENTITY':'se', 'MOTION':'m',
       'NONMOTION_EVENT':'e', 'SPATIAL_SIGNAL':'s', 'MOTION_SIGNAL':'ms',
       'MEASURE':'me'}

def gen(corpus=test, model='m.model', indir=INDIR, outdir=''):
    tagger = Tagger()
    tagger.open(model)
    for doc in corpus.documents:
        path = setup_newdir(doc.filepath, olddir=indir, newdir=outdir,
                            suffix='--', renew=True)
        if not path:
            continue
        mkparentdirs(path)
        task = etree.Element(TASK_ROOT)
        tags = etree.Element(TAGS_ROOT)
        tokens = etree.Element(TOKENS_ROOT)
        task.append(tags)
        task.append(tokens)
        sents = doc.sentences
        seqs = doc.sequence_list()
        tagged_seqs = [tagger.tag(seq) for seq in seqs]
        freq_dict = defaultdict(int)
        for (sent, seq, tagged_seq) in zip(sents, seqs, tagged_seqs):
            s = etree.Element('s')
            for (lex, feat, label) in zip(sent.getchildren(), seq, tagged_seq):
                    lex_tag = etree.Element(lex.tag, lex.attrib)
                    lex_tag.text = lex.text
                    s.append(lex_tag)
                    if label != 'None':
                        iso_tag = etree.Element(label)
                        if label in attribs:
                            for key in attribs[label]:
                                iso_tag.attrib[key] = attribs[label][key]
                        iso_tag.attrib['text'] = lex.text
                        iso_tag.attrib['id'] = ids[label] + str(freq_dict[label])
                        lex_tag.attrib['id'] = iso_tag.attrib['id']
                        freq_dict[label] += 1
                        tags.append(iso_tag)
            tokens.append(s)
        s = etree.tostring(task, pretty_print=True)
        with open(path, 'w') as f:
            print>>f, HEADER
            print>>f, s

gen()

