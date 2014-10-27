#!/usr/bin/env python
'''
Created on July 30, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c) Identify their attributes according to type.
'''
#===============================================================================
from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier
from Corpora.corpus import Corpus
from se_a import Instance

import re
#===============================================================================

type_keys = {'PATH': ['p'], 'PLACE': ['pl'], 'MOTION': ['m'], 'NONMOTION_EVENT': ['e'], 
             'SPATIAL_ENTITY': ['se'], # spatial elements
             'SPATIAL_SIGNAL': ['s'], # spatial signal
             'MOTION_SIGNAL': ['ms'], # motion signal
             'HAS_TAG': ['p', 'pl', 'm', 'e', 'se', 's', 'ms']
             }

class Corpus_SE_C(Corpus_SE_B):
    def instances(self, element_type):
        '''create a set of instances'''
        super.self.instances()
    
#         type_key = type_keys[element_type]
#         docs = self.documents()
#         for doc in docs:    
#             # sort tag info by start offset
#             sd = {}
#             tags = doc.consuming_tags()
#             for t in tags:
#                 sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    
#             # construct instance objects from corpus data    
#             front = 0
#             done = False
#             for s in doc.tokenizer.tokenize_text().sentences:
#                 unconsumed_tag = {}
#                 sent = s.as_pairs() # [ (token, lexeme obj), (token, lexeme obj), ...]
#                 for i in range(len(sent)):
#                     token = sent [i] # (token, lexeme obj)
#                     tag = sd.get(token[1].begin, {})          
#                     if unconsumed_tag == {}:
#                         front = i           
#                         if int(tag.get("end", -1)) <= token[1].end:
#                             done = True
#                         else:
#                             unconsumed_tag = tag
#                     else:
#                         if int(unconsumed_tag.get("end", -1)) == token[1].end:
#                             done = True
#                             unconsumed_tag = {}
#                     if done:
#                         done = False
#                         for key in type_key:
#                             if self.tag != {} and re.findall('%s\d+' % key, self.tag['id']):
#                                 token = [t for t, l in sent[front:i+1]]
#                                 lex = [l for t, l in sent[front:i+1]]
#                                 before = sent[:front]
#                                 after = sent [i+1:]
#                                 inst = Instance(token, lex, before, after, tag)
#                                 yield inst    

