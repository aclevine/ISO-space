#!/usr/bin/env python
"""
Created on Sep 19, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

a) Identify spans of spatial elements including locations, 
paths, events and other spatial entities.    
"""
import os, nltk
from util.corpora.corpus import Extent
from util.model.baseline_classifier import Classifier


class Token(Extent):
    """pull labels and features for classifying tag extents using individual tokens"""
    # LABEL EXTRACT
    def unconsumed_tag(self):
        """does tag span multiple tokens?"""
        if int(self.tag.get("end", -1)) == self.lex[0].end:
            return True
        else:
            return False
    
    # FEATURE EXTRACT
    def upper_case(self):
        """ is token upper case"""
        if str.isupper(str(self.token[0][0].encode('utf-8'))):
            return {'upper_case':True}
        else:
            return {'upper_case':False}

    def next_upper_case(self):
        """ is next token upper case"""
        if self.next_tokens != [] and str.isupper(str(self.next_tokens[0][0].encode('utf-8'))):
            return {'next_upper_case':True}
        else:
            return {'next_upper_case':False}

    def prev_upper_case(self):
        """ is next token upper case"""
        if self.prev_tokens != [] and str.isupper(str(self.prev_tokens[-1][0].encode('utf-8'))):
            return {'prev_upper_case':True}
        else:
            return {'prev_upper_case':False}

    def pos_tag(self):
        """ Part of speech tag for token"""
        tag = nltk.pos_tag(self.token[:1])[0][1]
        return {'pos_tag': tag}

    def next_pos_tag(self):
        """ Part of speech tag for next token"""
        if self.next_tokens != []:
            tag = nltk.pos_tag(self.next_tokens[0][:1])[0][1]
            return {'next_pos_tag': tag}
        return {'next_pos_tag': 'None'}

    def prev_pos_tag(self):
        """ Part of speech tag for prev token"""
        if self.prev_tokens != []:
            tag = nltk.pos_tag(self.prev_tokens[-1][:1])[0][1]
            return {'prev_pos_tag': tag}
        return {'prev_pos_tag': 'None'}

    def simple_tag(self):
        """ 
        First letter of speech tag for token
        (N, V, P, etc.)
        """
        tag = nltk.pos_tag(self.token[:1])[0][1]
        return {'simple_tag': tag[0]}

    def next_simple_tag(self):
        """ First letter of speech tag for next token"""
        if self.next_tokens != []:
            tag = nltk.pos_tag(self.next_tokens[0][:1])[0][1]
            return {'next_simple_tag': tag[0]}
        return {'next_simple_tag': 'None'}

    def prev_simple_tag(self):
        """ First letter of speech tag for prev token"""
        if self.prev_tokens != []:
            tag = nltk.pos_tag(self.prev_tokens[-1][:1])[0][1]
            return {'prev_simple_tag': tag[0]}
        return {'prev_simple_tag': 'None'}


    def curr_token(self):
        """ All characters in current extent """
        return {'curr_extent_' + ' '.join(self.token):True}

    def curr_tokens(self):
        """ tokens in current extent """
        return {'curr_tokens_' + tok:True for tok in self.token}

    def curr_pos_tags(self):
        """ part of speech tags in current extent """        
        return {'curr_tags_' + nltk.pos_tag(tok)[0][1]:True for tok in self.token}

    def curr_token_count(self):
        """ pull prev n tokens in sentence before target word."""
        return {'curr_count_' + str(len(self.token)):True}

    def prev_n_bag_of_words(self, n):
        """ pull prev n tokens in sentence before target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'prev_' + str(n) + 
                '_' + tok:True for tok, lex 
                in self.prev_tokens[len(self.prev_tokens) - n:]}

    def next_n_bag_of_words(self, n):
        """ pull next n tokens in sentence after target word."""
        if n > len(self.next_tokens):
            n = len(self.next_tokens)
        return {'next_' + str(n) + 
                '_' + tok:True for tok, lex 
                in self.next_tokens[:n]}

#===============================================================================

def get_token_indices(sentence, tag_dict):
    indices = []
    for i in range(len(sentence)):
        start = i
        end = i + 1
        indices.append((start, end))
    return indices

class Spans_Classifier(Classifier):
    def __init__(self, train_path, test_path):
        super(Spans_Classifier, self).__init__(train_path = train_path, test_path = test_path)
        self.feature_functions = [
                                    lambda x: x.upper_case(),
                                    lambda x: x.next_upper_case(),
                                    lambda x: x.prev_upper_case(),
                                    lambda x: x.pos_tag(),
                                    lambda x: x.next_pos_tag(),
                                    lambda x: x.prev_pos_tag(),
                                    lambda x: x.simple_tag(),
                                    lambda x: x.next_simple_tag(),
                                    lambda x: x.prev_simple_tag(),
                                    lambda x: x.curr_token(),
                                    lambda x: x.curr_tokens(),
                                    lambda x: x.next_n_bag_of_words(3),
                                    lambda x: x.prev_n_bag_of_words(3),                                    
                                 ] 
        self.label_function = lambda x: str(x.unconsumed_tag())
        self.indices_function = get_token_indices
        self.extent_class = Token


def generate_elements(train_path, test_path, out_path):
    """ train model with corpus in train_path,
    classify spanning tags for docs in test_path, 
    write xmls of docs with new tags to out_path """
    # make outpath
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    # classify test_data
    d = Spans_Classifier(train_path, test_path)
    pred, test_data = d.generate_labels()

    # parse into XML tags    
    ongoing = False
    id_number = 0
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            id_number = 0
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
        if pred[offsets] == 'True':
            if not ongoing:
                start = extent.lex[0].begin
                ongoing = True
        else:
            if ongoing:
                ongoing = False
            else:
                start = extent.lex[0].begin
            tag = {'name': 'SPATIAL_EXTENT', 
                   'start': start, 
                   'end': extent.lex[-1].end,
                   'text': extent.document.text()[start: extent.lex[-1].end],
                   'id': 'sx{}'.format(id_number)}
            extent.document.insert_tag(tag)
            id_number += 1
    curr_doc.save_xml(os.path.join(out_path, doc_name))


if __name__ == "__main__":
    
    # DEMO
    train_path = './data/training'
    test_path = './data/final/test/configuration1/'
    outpath = './data/final/test/configuration1/1'
    
    generate_elements(train_path, test_path, outpath)
    
    