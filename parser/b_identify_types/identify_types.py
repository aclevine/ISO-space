#!/usr/bin/env python
'''
Created on July 30, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

b) Classify spatial elements according to type: 
PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY.    
'''

#===============================================================================
from Corpora.corpus import Extent
from util.demo import Demo
import re
#===============================================================================
type_keys = {'PATH': ['p'], 'PLACE': ['pl'], 'MOTION': ['m'], 'NONMOTION_EVENT': ['e'], 
             'SPATIAL_ENTITY': ['se'], # spatial elements
             'SPATIAL_SIGNAL': ['s'], # spatial signal
             'MOTION_SIGNAL': ['ms'], # motion signal
             'HAS_TAG': ['p', 'pl', 'm', 'e', 'se', 's', 'ms']
             }

class Tag(Extent):
    '''a class for loading tokens from XML doc with surrounding token and tag data'''    
    # LABEL EXTRACT
    def is_type(self, element_type):
        ''' check if tag id matches given element type. untagged tokens always come back false '''
        type_key = type_keys[element_type]
        for key in type_key:
            if self.tag != {} and re.findall('%s\d+' % key, self.tag['id']):
                return True
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
#===============================================================================
def no_filter(tag):
    return True

def has_tag(tag):
    return tag
    
def get_tag_and_no_tag_indices(sentence, tag_dict, tag_filter=no_filter):
    unconsumed_tag = {}
    done = False
    indices = []
    for i in range(len(sentence)):
        token, lex = sentence[i] # (token, lexeme obj)
        tag = tag_dict.get(lex.begin, {})
        if tag_filter(tag):
            if unconsumed_tag == {}:
                start = i                    
                if int(tag.get("end", -1)) <= lex.end:
                    done = True
                else:
                    unconsumed_tag = tag
            else:
                if int(unconsumed_tag.get("end", -1)) == lex.end:
                    done = True
                    unconsumed_tag = {}
            if done:
                end = i+1
                indices.append( (start, end) ) 
                done = False
    return indices

def get_tag_only_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, has_tag)

class Types_Demo(Demo):
    def __init__(self, type_name, doc_path = '../training', split=0.8):
        self.doc_path = doc_path
        self.split = split
        self.feature_functions = [lambda x: x.curr_token(),
                                  lambda x: x.prev_n_bag_of_words(100),
                                  lambda x: x.next_n_bag_of_words(100)]
        self.label_function = lambda x: str(x.is_type(type_name))
        self.indices_function = get_tag_and_no_tag_indices
        self.extent_class = Tag

# TESTING
if __name__ == "__main__":

    for type_name in ['PATH', 
                      'PLACE', 'MOTION', 'NONMOTION_EVENT', 
                      'SPATIAL_ENTITY', 'MOTION_SIGNAL' 'HAS_TAG']:
        d = Types_Demo(type_name)
        d.run_demo()

    