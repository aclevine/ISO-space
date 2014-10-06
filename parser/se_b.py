#!/usr/bin/env python
'''
Created on July 30, 2014

@author: Aaron Levine
# 1) Spatial Elements (SE):
    ## b) Classify spatial elements according to type: PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY.    
'''

#===============================================================================
from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier
from Corpora.corpus import Corpus
from se_a import Instance

import re
#===============================================================================

type_keys = {'PATH': 'p', 'PLACE': 'pl', 'MOTION': 'm', 'NONMOTION_EVENT': 'e', 'SPATIAL_ENTITY': 'se', # spatial elements
             'SPATIAL_SIGNAL': 's', # spatial signal
             'MOTION_SIGNAL': 'ms', # motion signal
             'ANY': ''
             # motion relation
             # spatial config
             # spatial orientation
             }

class Instance(Instance):
    '''a class for loading tokens from XML doc with surrounding token and tag data'''    
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
        tokens = self.token
        tokens.extend([tok for tok, lex in self.prev_tokens[len(self.prev_tokens)-n:]])
        tokens.extend([tok for tok, lex in self.next_tokens[:n]])
        return {'prev_' + tok:True for tok in tokens}
        
    def curr_token(self):
        ''' pull prev n tokens in sentence before target word.'''
        return {'curr_' + ' '.join(self.token):True}

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

class Corpus_SE_B(Corpus):
    def instances(self):
        '''create a set of instances'''
        docs = self.documents()
        for doc in docs:    
            # sort tag info by start offset
            sd = {}
            tags = doc.consuming_tags()
            for t in tags:
                sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    
            # construct instance objects from corpus data    
            front = 0
            done = False
            for s in doc.tokenizer.tokenize_text().sentences:
                unconsumed_tag = {}
                sent = s.as_pairs() # [ (token, lexeme obj), (token, lexeme obj), ...]
                for i in range(len(sent)):
                    token = sent [i] # (token, lexeme obj)
                    tag = sd.get(token[1].begin, {})                
                    if unconsumed_tag == {}:
                        front = i                    
                        if int(tag.get("end", -1)) <= token[1].end:
                            done = True
                        else:
                            unconsumed_tag = tag
                    else:
                        if int(unconsumed_tag.get("end", -1)) == token[1].end:
                            done = True
                            unconsumed_tag = {}
                    if done:
                        done = False
                        token = [t for t, l in sent[front:i+1]]
                        lex = [l for t, l in sent[front:i+1]]
                        before = sent[:front]
                        after = sent [i+1:] 
                        inst = Instance(token, lex, before, after, tag)
                        yield inst

# TESTING

def build_train_test(doc_path = './training', split=0.8):
    c = Corpus_SE_B(doc_path)    
    inst = list(c.instances())
    i = int(len(inst) * split)
    train_inst = inst[:i]
    test_inst = inst[i:]

    return (train_inst, test_inst)
  
def all_false_classifier(test_data):
    # HIGHEST OCCURRING TAG: FALSE
    features = []
    label = lambda x: str(x.is_type('SPATIAL_ENTITY'))
    clf = SKClassifier(LogisticRegression(), label, features)
    clf.add_labels(['True', 'False']) #binary classifier    
    clf.evaluate(['False' for x in test_data], [label(x) for x in test_data])


def typing_demo():
    # random select train/test data    
    train_data, test_data = build_train_test()
 
    features = [lambda x: x.curr_token(),
                lambda x: x.prev_n_bag_of_words(100),
                lambda x: x.next_n_bag_of_words(100)]
    
    #features = [lambda x: x.bag_of_words(3)] #awful performance
    any_pred = ['False' for x in test_data]
    for type_name in ['PATH', 'PLACE', 'MOTION', 'NONMOTION_EVENT', 'SPATIAL_ENTITY']:
        label = lambda x: str(x.is_type(type_name))
       
        clf = SKClassifier(LogisticRegression(), label, features)
        clf.add_labels(['True', 'False']) #binary classifier
        clf.train(train_data)
       
        pred = clf.classify(test_data)    
        print '\n\n%s:' %(type_name)
        clf.evaluate(pred, [label(x) for x in test_data])
        for i, p in enumerate(pred):
            if p == 'True':
                any_pred[i] = 'True'

    print '\n\n%s:' %('ANY')
    any_label = lambda x: str(x.is_type('ANY'))
    clf.evaluate(any_pred, [any_label(x) for x in test_data])


if __name__ == "__main__":

    typing_demo()