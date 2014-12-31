# -*- coding: utf-8 -*-

"""Representation of a CRFSuite instance.

This module contains the classfor a CRFSuite instance.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

KEY = 0
VALUE = 1

class Instance(object):
    """Wrapper a CRFSuite training instance.

    A training instance is a single line with the true class label
    followed by its associated features, each separated by a tab ('\t')
    character.  
    
    Args:
        label: The true class label for the instance.
        features: A dictionary mapping a string key to its
            string feature value.
    
    Attributes:
        label: The true class label for the instance.
        features: A dictionary mapping a string key to its
            string feature value.
        
    """
    def __init__(self, label='', features={}, bos=False, eos=False):
        self.label = label
        self.features = features
        self.bos = bos
        self.eos = eos

    def add(self, feature):
        """Adds a feature to the instance.

        Args:
            feature: A tuple of the form (key, value),
                where key, value are both strings.

        Returns:
            None
            
        """
        self.features[feature[KEY]] = feature[VALUE]

    def addDict(self, featuredict):
        self.features = dict(self.features.items() + featuredict.items())

    def feature_list(self):
        return [''.join([key, '=', self.features[key]])
                for key in self.features]

    def __repr__(self):
        string = '\t'.join([self.label] +
                         [key + '=' + self.features[key] for key in self.features])
        if self.bos:
            string += '\t__BOS__'
        if self.eos:
            string += '\t__EOS__\n'
        return string.encode('utf-8')
        
        
