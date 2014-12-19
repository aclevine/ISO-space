# -*- coding: utf-8 -*-

"""Representation of a CRFSuite training sequence.

This module contains the classfor a CRFSuite training sequence.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from instance import Instance

class Sequence(object):
    """Wrapper a CRFSuite training sequence.

    CRFSuite expects a training sequence as a set of lines,
    where each line contains the true class label with its features,
    each separated by a tab ('\t') character.  The first instance in
    the sequence is always given the __BOS__ feature (beginning of sequence),
    and the last instance is given the __EOS__ feature (end of sequence).
    

    Args:
        None
    
    Attributes:
        instances: A list of linearly CRFSuite Instances,
            each of which has a label and a set of discrete features.
        
    """
    def __init__(self):
        self.instances = []

    def add(self, instance):
        """Adds an instance to the training sequence.

        """
        #reset the __BOS__, __EOS__ features
        if self.instances:
            self.instances[0].bos = False
            self.instances[-1].eos = False
        self.instances.append(instance)

    def __repr__(self):
        #add in the __BOS__, __EOS__ features
        self.instances[0].bos = True
        self.instances[-1].eos = True
        return '\n'.join([str(instance) for instance in self.instances])
        
    

        
        
