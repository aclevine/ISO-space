#!/usr/bin/env python
'''
Created on July 30, 2014

@author: Aaron Levine
'''

from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier
import Corpora.corpus as xml
import re


type_keys = {'PATH': 'p', 'PLACE': 'pl', 'MOTION': 'm', 'NONMOTION_EVENT': 'e', 'SPATIAL_ENTITY': 'se', # spatial elements
             'SPATIAL_SIGNAL': 's', # spatial signal
             'MOTION_SIGNAL': 'ms', # motion signal
             # motion relation
             # spatial config
             # spatial orientation
             }

class Instance:
    '''a class for loading tokens from XML doc with surrounding token and tag data'''
    def __init__(self, token, lex, prev_tokens, next_tokens, tag):
        self.token = token
        self.lex = lex
        self.prev_tokens = prev_tokens
        self.next_tokens = next_tokens
        self.tag = tag
        
    # 1) Spatial Elements (SE):
    ## a) Identify spans of spatial elements including locations, paths, events and other spatial entities.
    
    # > BASELINE TOKEN JOINING HERE <
        
    ## b) Classify spatial elements according to type: PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY.
    # LABEL EXTRACT
    def is_type(self, element_type):
        ''' check if tag id matches given element type. untagged tokens always come back false '''
        type_key = type_keys[element_type]
        if self.tag != {} and re.findall('%s\d+' % type_key, self.tag['id']):
            return True
        else:
            return False

    ## c) Identify their attributes according to type.
    def has_attribute(self, attribute_name):
        ''' check tag dictionary of instance for attribute. '''
        if self.tag.has_key(attribute_name) and self.tag[attribute_name] != '':
            return True
        else:
            return False

    def get_attribute(self, attribute_name):
        ''' check tag dictionary of instance for attribute. if attribute doesn't exist, return the empty string. '''
        if self.tag.has_key(attribute_name):
            return self.tag[attribute_name] 
        else:
            return ''
    
    # FEATURE EXTRACT
    def prev_n_bag_of_words(self, n):
        ''' pull prev n tokens in sentence before target word.'''
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {tok:True for tok, lex in self.prev_tokens[len(self.prev_tokens)-n:]}

    def next_n_bag_of_words(self, n):
        ''' pull next n tokens in sentence after target word.'''
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {tok:True for tok, lex in self.next_tokens[:n]}



# TESTING
def build_instances(doc_path = './train'):
    '''get basic sense of manipulating xml docs'''
    c = xml.Corpus(doc_path)

    for doc in list(c.documents()):    
        # sort tag info by start offset
        sd = {}
        tags = doc.consuming_tags()
        for t in tags:
            sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}
    
        # construct instance objects from corpus data    
        for s in doc.tokenizer.tokenize_text().sentences:
            sent = s.as_pairs()
            for i in range(len(sent)):
                token = sent [i] # (token, lexeme obj)
                before = sent[:i] # [ (token, lexeme obj), (token, lexeme obj), ...]
                after = sent [i+1:] # [ (token, lexeme obj), (token, lexeme obj), ...]
                tag = sd.get( token[1].begin, {})            
                inst = Instance(token[0], token[1], before, after, tag)                         
                yield inst
            

if __name__ == "__main__":

    train_data = [inst for inst in build_instances()]

    features = [lambda x: x.prev_n_bag_of_words(9), 
                lambda x: x.next_n_bag_of_words(9)]
        
    label = lambda x: str(x.is_type('PLACE'))   

    print [label(inst) for inst in train_data]
    
    clf = SKClassifier(LogisticRegression(), label, features)
    clf.add_labels(['True', 'False'])
    clf.train(train_data)

    pred = clf.classify(train_data)    
    print pred
    clf.evaluate(pred, [label(x) for x in train_data]) # SYSTEM WORKS (very poorly on two documents), HORRAY!

