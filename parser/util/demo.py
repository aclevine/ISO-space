'''
Created on Oct 31, 2014

@author: ACL73

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from Corpora.corpus import Corpus, Extent
from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier
from abc import abstractmethod

class Demo(object):
    def __init__(self, doc_path = './training', split=0.8):
        self.doc_path = doc_path
        self.split = split
        self.label_function = self.get_label_function()
        self.feature_functions = self.get_feature_functions()

    @abstractmethod        
    def get_label_function(self):
        return None
    
    @abstractmethod
    def get_feature_functions(self):
        return []
         
    def run_demo(self, verbose=0):
        c = Corpus(self.doc_path)
        extents = list(c.extents(self.indices_function, 
                                 self.extent_class))
        i = int(len(extents) * self.split)
        train_data = extents[:i]
        test_data = extents[i:]
        if verbose >= 1:
            print "data loaded"
        labels = [self.label_function(x) for x in extents]
        if verbose >= 2:
            fd = {}
            for l in labels:
                fd[l] = fd.get(l, 1) + 1
            print fd
        clf = SKClassifier(LogisticRegression(), 
                           self.label_function, 
                           self.feature_functions)
        clf.add_labels(set(labels))
        clf.train(train_data)
        if verbose >= 1:
            print "model trained"
        pred = clf.classify(test_data)
        clf.evaluate(pred, [self.label_function(x) for x in test_data])