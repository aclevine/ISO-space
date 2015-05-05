#!/usr/bin/env python
'''
Created on Sep 19, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type. (MOTION_SIGNAL tag)
'''
from util.b_identify_types import Tag, get_tag_and_no_tag_indices
from util.model.baseline_classifier import Classifier
import re

class MotionSignalTag(Tag):
    # LABEL EXTRACT
    def motion_signal_type(self):
        # motion_type ( MANNER | PATH | COMPOUND )
        return self.tag['motion_signal_type']

def is_motion_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^ms\d+', tag_id))

def get_motion_signal_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_motion_tag)


class MotionSignalClassifier(Classifier):
    def __init__(self, train_path = '', test_path = '', gold_path = ''):
        super(MotionSignalClassifier, self).__init__(train_path = train_path, test_path = test_path, 
                                               gold_path = gold_path)
        self.indices_function = get_motion_signal_tag_indices
        self.extent_class = MotionSignalTag

class MotionSignalTypeClassifier(MotionSignalClassifier):
    def get_label_function(self):
        return lambda x: str(x.motion_signal_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
