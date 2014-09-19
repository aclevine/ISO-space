#!/usr/bin/env python
'''
Created on July 30, 2014

@author: Aaron Levine
'''

#===============================================================================
from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier
import Corpora.corpus as xml
import re, nltk
#===============================================================================

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
    def bag_of_words(self, n):
        """ returns 2n+1 words surrounding target"""
        tokens = [self.token]
        tokens.extend([tok for tok, lex in self.prev_tokens[len(self.prev_tokens)-n:]])
        tokens.extend([tok for tok, lex in self.next_tokens[:n]])
        return {'prev_' + tok:True for tok in tokens}
        
    def curr_token(self):
        ''' pull prev n tokens in sentence before target word.'''
        return {'curr_' + self.token:True}

    def prev_n_bag_of_words(self, n):
        ''' pull prev n tokens in sentence before target word.'''
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'prev_' + tok:True for tok, lex in self.prev_tokens[len(self.prev_tokens)-n:]}

    def next_n_bag_of_words(self, n):
        ''' pull next n tokens in sentence after target word.'''
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'next_' + tok:True for tok, lex in self.next_tokens[:n]}


# TESTING
def build_instances(doc_path = './training'):
    '''get basic sense of manipulating xml docs'''
    c = xml.Corpus(doc_path)    
    nonconsumed_tag = {}
    for doc in list(c.documents()):    
        # sort tag info by start offset
        sd = {}
        tags = doc.consuming_tags()
        for t in tags:
            sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    
        # construct instance objects from corpus data    
        start = end = 0
        for s in doc.tokenizer.tokenize_text().sentences:
            sent = s.as_pairs()
            for i in range(len(sent)): 
                token = sent [i] # (token, lexeme obj)
                before = sent[:i] # [ (token, lexeme obj), (token, lexeme obj), ...]
                after = sent [i+1:] # [ (token, lexeme obj), (token, lexeme obj), ...]
                # split tags across tokens
                if nonconsumed_tag == {}:
                    tag = sd.get( token[1].begin, {})
                else:
                    tag = nonconsumed_tag
                if tag != {} and int(tag["end"]) > token[1].end:
                    nonconsumed_tag = tag
                else:
                    nonconsumed_tag = {}
                inst = Instance(token[0], token[1], before, after, tag)
                yield inst

            
def all_false_classifier(test_data):
    # HIGHEST OCCURRING TAG: FALSE
    features = []
    label = lambda x: str(x.is_type('SPATIAL_ENTITY'))
    clf = SKClassifier(LogisticRegression(), label, features)
    clf.add_labels(['True', 'False']) #binary classifier    
    clf.evaluate(['False' for x in test_data], [label(x) for x in test_data])


def typing_demo():
    # random select train/test data    
    train_data = []
    test_data = []
    for i, inst in enumerate(build_instances('./training')):
        if i%10 == 2 or i%10 == 5:
            test_data.append(inst)
        else:
            train_data.append(inst)
 
    features = [lambda x: x.curr_token(),
                lambda x: x.prev_n_bag_of_words(100),
                lambda x: x.next_n_bag_of_words(100)]
    
    #features = [lambda x: x.bag_of_words(3)] #awful performance
  
    for type_name in ['PATH', 'PLACE', 'MOTION', 'NONMOTION_EVENT', 'SPATIAL_ENTITY']:
        label = lambda x: str(x.is_type(type_name))
      
        clf = SKClassifier(LogisticRegression(), label, features)
        clf.add_labels(['True', 'False']) #binary classifier
        clf.train(train_data)
      
        pred = clf.classify(test_data)    
        print '\n\n%s:' %(type_name)
        clf.evaluate(pred, [label(x) for x in test_data])
        

if __name__ == "__main__":
    
    typing_demo()