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
from b_identify_types.identify_types import Corpus_SE_B
from a_identify_spans.identify_spans import Instance

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
        instances = super.self.instances()
        filter()


