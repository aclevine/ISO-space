# -*- coding: utf-8 -*-

"""Builds generated ISO-Space tags given a CRFSuite model.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from lxml import etree
import xml.etree.ElementTree as ET

from crfsuite.instance import Instance
from crfsuite.sequence import Sequence
from dirs import *
from pycrfsuite import Tagger
from space_document import Space_Document
from space_corpus import Space_Corpus, train, test

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
        for (sent, seq, tagged_seq) in zip(sents, seqs, tagged_seqs):
            for (lex, feat, label) in zip(sent.getchildren(), seq, tagged_seq):
                    lex_tag = etree.Element(lex.tag, lex.attrib)
                    lex_tag.text = lex.text
                    tokens.append(lex_tag)
                    if label != 'None':
                        iso_tag = etree.Element(label)
                        iso_tag.text = lex.text
                        tags.append(iso_tag)
        
        s = etree.tostring(task, pretty_print=True)
        with open(path, 'w') as f:
            print>>f, HEADER
            print>>f, s
                    
        
        
        
        
        
    
