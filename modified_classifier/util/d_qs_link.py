#!/usr/bin/env python
"""
Created on Nov 13, 2014

@author: Aaron Levine

if signal: 
    dir_top = d_olink + qslink
    top = qslink
    dir = d_olink
    
build dictionary of "trigger entities" for qslinks without signal triggers?
"""
from util.d_olink import OLinkTag
from util.model.baseline_classifier import Classifier
import re
from util.b_identify_types import get_tag_and_no_tag_indices

class QSLinkTag(OLinkTag):
    def __init__(self, sent, tag_dict, movelink_tag_dict, olink_tag_dict, 
                 qslink_tag_dict, feat_dict, front, back, basename, doc):
        """ use c_motion tags as a head to associate move-links with sentences"""
        super(QSLinkTag, self).__init__(sent, tag_dict, movelink_tag_dict, olink_tag_dict, 
                                       qslink_tag_dict, feat_dict, front, back, basename, doc)
        head = tag_dict.get(self.lex[0].begin, {})
        self.tag = qslink_tag_dict.get(head['id'], {})

   
    def is_qslink(self):
        if self.tag.get('id', ''):
            return {'is_QSLink': True}
        else:
            return {'is_QSLink': False}

    def rel_type(self):
        """ relType ( IN | OUT | DC | EC | PO | TPP | ITPP | NTPP | INTPP | EQ ) """
        return self.tag.get('relType', 'NOT_QSLINK')
            
# TAG TYPE FILTER
def is_top_tag(tag):
    """ load c_path / pu / spatial entity / c_spatial_signal / c_nonmotion_event / c_motion heads"""
    tag_id = tag.get('id', '')
    if bool(re.findall('^s\d+', tag_id)):
        sem_type = tag.get('semantic_type', '')
        if sem_type == 'TOPOLOGICAL' or sem_type == 'DIR_TOP':
            return True
    return False
    
def get_top_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_top_tag)

# test variables
class QSLinkClassifier(Classifier):
    def __init__(self,  train_path='', test_path = '', gold_path = '', ):
        super(QSLinkClassifier, self).__init__(train_path = train_path, test_path = test_path,
                                         gold_path = gold_path)
        self.indices_function = get_top_tag_indices
        self.extent_class = QSLinkTag

class QSLinkIsLinkClassifier(QSLinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.is_qs_link())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class QSLinkFromIDClassifier(QSLinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.from_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                lambda x: x.surrounding_tag_types(),
                lambda x: x.surrounding_tag_text(),
                lambda x: x.prev_tag_count(),
                lambda x: x.next_tag_count(),
                ]

class QSLinkToIDClassifier(QSLinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.to_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                lambda x: x.surrounding_tag_types(),
                lambda x: x.surrounding_tag_text(),
                lambda x: x.prev_tag_count(),
                lambda x: x.next_tag_count(),
                ]

class QSLinkRelTypeClassifier(QSLinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.rel_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class QSLinkTrajectorClassifier(QSLinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.trajector())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class QSLinkLandmarkClassifier(QSLinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.landmark())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
