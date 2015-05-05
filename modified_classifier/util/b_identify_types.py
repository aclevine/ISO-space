#!/usr/bin/env python
"""
Created on Sep 19, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

b) Classify spatial elements according to type: 
PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY,
MOTION_SIGNAL, SPATIAL_SIGNAL
"""
from util.corpora.corpus import Extent, HypotheticalCorpus
from util.model.baseline_classifier import Classifier, copy_folder
import re
import nltk
import os
import resources.dicts
from resources.dicts import Clusters, Vectors

# resources
type_keys = {'PATH': ['p'], 'PLACE': ['pl'], 'MOTION': ['m'], 'NONMOTION_EVENT': ['e'],
             'SPATIAL_ENTITY': ['se'],  # spatial elements
             'SPATIAL_SIGNAL': ['s'],  # spatial signal
             'MOTION_SIGNAL': ['ms'],  # c_motion signal
             'HAS_TAG': ['p', 'pl', 'm', 'e', 'se', 's', 'ms'],
             'EVENT': ['e', 'm', 'ne'],
             'SIGNAL': ['s', 'nss'],
             }

tag_types = {'PATH': {'form': '', 'countable': '', 'dimensionality': '', 'mod': ''}, 
             'PLACE': {'form': '', 'countable': '', 'dimensionality': '', 'mod': ''}, 
            'MOTION': {'motion_class': '', 'motion_sense': '', 'motion_type': ''},
            'NONMOTION_EVENT': {'mod': '', 'countable': ''},
            'SPATIAL_ENTITY': {'form': '', 'countable': '', 'dimensionality': '', 'mod': ''}, 
            'MOTION_SIGNAL': {'motion_signal_type': ''}, 
            'SPATIAL_SIGNAL': {'semantic_type': ''},
            }

clusters = Clusters(os.path.join(os.path.dirname(os.path.abspath(resources.dicts.__file__)),
                                    'classes.sorted.txt'))

vectors = Vectors(os.path.join(os.path.dirname(os.path.abspath(resources.dicts.__file__)),
                               'classes.sorted.txt'))

# feature / label extractors
class Tag(Extent):
    """a class for loading tokens from XML doc with surrounding token and tag data"""    
    # LABEL EXTRACT
    def is_type(self, element_type):
        """ check if tag id matches given element type. untagged tokens always come back false """
        type_key = type_keys[element_type]
        for key in type_key:
            if self.tag != {} and re.findall('^{}\d+'.format(key), self.tag['id']):
                return True
        return False

    def ner_tag(self):
        try:
            return {'ner':self.feats[0]['ner']}
        except:
            return {'ner':u'O'}

    def type(self):
        """ get tag type """
        return self.tag['id']

    # # c) Identify their attributes according to type.
    def has_attribute(self, attribute_name):
        """ check tag dictionary of instance for attribute. """
        if self.tag.has_key(attribute_name) and self.tag[attribute_name] != '':
            return True
        else:
            return False

    def get_attribute(self, attribute_name):
        """ check tag dictionary of instance for attribute. if attribute doesn't exist, return the empty string. """
        if self.tag.has_key(attribute_name):
            return self.tag[attribute_name] 
        else:
            return ''
        
    # FEATURE EXTRACT
    def cluster_class(self):
        return {'cluster':clusters.dict[str(len(self.token))]}

    def word2vec(self):
        return {'vec[{}]'.format(i):value for i,value in enumerate(vectors.dict[str(len(self.token))])}

    def bag_of_words(self, n):
        """ returns 2n+1 words surrounding target"""
        tokens = self.token
        tokens.extend([tok for tok, _ in self.prev_tokens[len(self.prev_tokens) - n:]])
        tokens.extend([tok for tok, _ in self.next_tokens[:n]])
        return {'bag_' + tok:True for tok in tokens}

    def curr_token(self):
        """ pull prev n tokens in sentence before target word."""
        return {'curr_extent_' + ' '.join(self.token):True}

    def curr_tokens(self):
        return {'curr_tokens_' + tok:True for tok in self.token}

    def curr_pos_tags(self):
        return {'curr_tags_' + nltk.pos_tag(tok)[0][1]:True for tok in self.token}

    def curr_token_count(self):
        """ pull prev n tokens in sentence before target word."""
        return {'curr_count_' + str(len(self.token)):True}

    def trigram(self, n):
        trigram=[]
        for tok, lex in self.prev_tokens[-1:]:
            trigram.append(tok)
        trigram.append(self.token)
        for tok, lex in self.next_tokens[:1]:
            trigram.append(tok)   
        return {'trigram':'_'.join(trigram)}

    def prev_trigram(self, n):
        trigram=[]
        for tok, lex in self.prev_tokens[-2:]:
            trigram.append(tok)
        trigram.append(self.token)
        return {'trigram[-1]':'_'.join(trigram)}

    def next_trigram(self, n):
        trigram=[]
        trigram.append(self.token)
        for tok, lex in self.next_tokens[:2]:
            trigram.append(tok)   
        return {'trigram[+1]':'_'.join(trigram)}

    def prev_n_bag_of_words(self, n):
        """ pull prev n tokens in sentence before target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'prev_' + str(n) + 
                '_' + tok:True for tok, _ 
                in self.prev_tokens[len(self.prev_tokens) - n:]}

    def next_n_bag_of_words(self, n):
        """ pull next n tokens in sentence after target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'next_' + str(n) + 
                '_' + tok:True for tok, _ 
                in self.next_tokens[:n]}

    def prev_n_bag_of_pos_tags(self, n):
        """ pull prev n tokens in sentence before target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'prev_tag_' + str(n) + 
                '_' + nltk.pos_tag(tok)[0][1]:True for tok, _ 
                in self.prev_tokens[len(self.prev_tokens) - n:]}

    def next_n_bag_of_pos_tags(self, n):
        """ pull next n tokens in sentence after target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'next_tag_' + str(n) + 
                '_' + nltk.pos_tag(tok)[0][1]:True for tok, _ 
                in self.next_tokens[:n]}
    
    def ordered_prev_n_bag_of_words(self, n):
        """ pull prev n tokens in sentence before target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {str(i) + 'prev_' + str(n) + 
                '_' + tok:True for i, (tok, _)
                in enumerate(self.prev_tokens[len(self.prev_tokens) - n:])}

    def ordered_next_n_bag_of_words(self, n):
        """ pull next n tokens in sentence after target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {str(i) + 'next_' + str(n) + 
                '_' + tok:True for i, (tok, _) 
                in enumerate(self.next_tokens[:n])}
    
    def part_of_speech(self):
        tokens = [tok for tok, _ in self.prev_tokens] + self.token + [tok for tok, _ in self.next_tokens]
        return
    
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
        _, lex = sentence[i]  # (token, lexeme obj)
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
                end = i + 1
                indices.append((start, end)) 
                done = False
    return indices

def get_tag_only_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, has_tag)

class TypesClassifier(Classifier):
    def __init__(self, type_name, train_path, test_path, gold_path):
        super(TypesClassifier, self).__init__(train_path = train_path, test_path = test_path, 
                                         gold_path = gold_path)
        self.label_function = lambda x: str(x.is_type(type_name))
        self.indices_function = get_tag_only_indices  # get_tag_and_no_tag_indices
        self.extent_class = Tag

    def get_feature_functions(self):
        return [
                lambda x:x.curr_token(),
                lambda x:x.ner_tag(),
                #lambda x:x.cluster_class(),
                #lambda x:x.word2vec(),
                lambda x: x.curr_pos_tags(),
                lambda x: x.next_n_bag_of_words(3),
                lambda x: x.prev_n_bag_of_words(3),
               ]

#===============================================================================
def make_sklearn(train_path, test_path, type_name):
    d = TypesClassifier(type_name, train_path, test_path, gold_path = '')
    pred, test_data = d.generate_labels()    
    return pred, test_data

def make_crf(train_path, test_path, type_name):
    d = TypesClassifier(type_name, train_path, test_path, gold_path = '')
    pred, test_data = d.generate_crf_labels()
    return pred, test_data

def generate_tags(train_path, test_path, clean_path, out_path, gen_model=make_sklearn):
    # make outpath
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    # clean data to write tags to
    clean_corpus = HypotheticalCorpus(clean_path)
    clean_data = list(clean_corpus.documents())
   
    for type_name, type_fields in tag_types.iteritems():
        # generate labels
        pred, test_data=gen_model(train_path, test_path, type_name)      
        # labels -> tagged docs
        id_number = 0
        i = 0
        curr_doc = clean_data[0]
        doc_name = curr_doc.basename
        for extent in test_data:
            if doc_name != extent.document.basename:
                curr_doc.save_xml(os.path.join(out_path, doc_name))
                id_number = 0
                i += 1
                curr_doc = clean_data[i]
                doc_name = curr_doc.basename
            
            offsets = "{a},{b},{c}".format(a=extent.basename,
                                           b=extent.lex[0].begin, 
                                           c=extent.lex[-1].end)
            if pred[offsets] == 'True':
                tag = {'name': type_name, 
                       'start': extent.tag['start'], 
                       'end': extent.tag['end'],
                       'text': extent.tag['text'],
                       'id': '{}{}'.format(type_keys[type_name][0], id_number),
                       }
                tag.update(type_fields)
                curr_doc.insert_tag(tag)
                id_number += 1
        # switch to established files
        curr_doc.save_xml(os.path.join(out_path, doc_name))
        clean_corpus = HypotheticalCorpus(out_path)
        clean_data = list(clean_corpus.documents())

#===============================================================================

if __name__ == "__main__":

    # DEMO
    train_path = '../data/training'
    test_path = '../data/modified/configuration1/1'
    clean_path = '../data/modified/configuration1/0'

    hyp_a = '../data/modified/configuration1/1a'    
    hyp_b = '../data/modified/configuration1/1b'   
    hyp_c = '../data/modified/configuration1/1c'   

    generate_tags(train_path, test_path, clean_path, hyp_a, make_crf)

    # copy to next stages
    copy_folder(hyp_a, hyp_b)
    copy_folder(hyp_a, hyp_c)

