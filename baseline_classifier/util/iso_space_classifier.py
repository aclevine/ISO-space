'''
Created on Oct 31, 2014

@author: ACL73

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
from util.Corpora.corpus import Corpus, HypotheticalCorpus
from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier
from abc import abstractmethod
import os
import shutil

class ISOSpaceClassifier(object):
    '''specify where system should pull training and test data from'''
    def __init__(self, train_path='./training', test_path=None, gold_path=None, split=0.8):
        self.train_path = train_path
        self.test_path = test_path
        self.gold_path = gold_path
        self.split = split
        self.label_function = self.get_label_function()
        self.feature_functions = self.get_feature_functions()

    @abstractmethod
    def get_label_function(self):
        return None
    
    @abstractmethod
    def get_feature_functions(self):
        return []

    def generate_test_train(self):
        """ create test and training instances based on provided paths """

        train_corpus = Corpus(self.train_path)
        extents = list(train_corpus.extents(self.indices_function,
                                            self.extent_class))
        # load test data
        if self.test_path:
            train_data = extents
            test_corpus = HypotheticalCorpus(self.test_path)
            test_data = list(test_corpus.extents(self.indices_function,
                                                 self.extent_class))
        else:
            i = int(len(extents) * self.split)
            train_data = extents[:i]
            test_data = extents[i:]
        return train_data, test_data

    def run_demo(self, verbose=0):
        """ test functionality of loading data, classification and evaluation """
        # load training data
        train_corpus = Corpus(self.train_path)
        extents = list(train_corpus.extents(self.indices_function,
                                            self.extent_class))
        # load test data
        if self.test_path:
            train_data = extents
            test_corpus = HypotheticalCorpus(self.test_path)
            test_data = list(test_corpus.extents(self.indices_function,
                                                 self.extent_class))
        else:
            i = int(len(extents) * self.split)
            train_data = extents[:i]
            test_data = extents[i:]
        # verbosity functionality
        if verbose >= 1:
            print "data loaded"
        labels = [self.label_function(x) for x in extents]
        if verbose >= 2:
            fd = {}
            for l in labels:
                fd[l] = fd.get(l, 1) + 1
            print fd
        # train model
        clf = SKClassifier(LogisticRegression(),
                           self.label_function,
                           self.feature_functions)
        clf.add_labels(set(labels))
        clf.train(train_data)
        if verbose >= 1:
            print "model trained"
        # classify
        pred = clf.classify(test_data, 
                            keys = ["{a},{b},{c}".format(a=extent.basename,
                                                         b=extent.lex[0].begin, 
                                                         c=extent.lex[-1].end)
                                    for extent in test_data])
        # evaluate
        if self.gold_path:
            gold_corpus = Corpus(self.gold_path)
            gold_data = list(gold_corpus.extents(self.indices_function,
                                            self.extent_class))
        else:
            gold_data = test_data
        gold_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                            self.label_function(extent)) 
                        for extent in gold_data])        
        clf.evaluate(pred, gold_labels)

                      
    def generate_labels(self, verbose=0):
        """return extents and label dictionary for generating proposed XML docs"""        
        
        # load data
        train_data, test_data = self.generate_test_train()
        labels = [self.label_function(x) for x in train_data]
        # reporting
        if verbose >= 1:
            print "data loaded"
        if verbose >= 2:
            fd = {}
            for l in labels:
                fd[l] = fd.get(l, 1) + 1
            print fd
        # train model
        clf = SKClassifier(LogisticRegression(),
                           self.label_function,
                           self.feature_functions)
        clf.add_labels(set(labels))
        clf.train(train_data)
        # reporting
        if verbose >= 1:
            print "model trained"
        # classify
        pred = clf.classify(test_data, 
                            keys = ["{a},{b},{c}".format(a=extent.basename,
                                                         b=extent.lex[0].begin, 
                                                         c=extent.lex[-1].end) 
                                    for extent in test_data]
                            )
        return pred, test_data


    def evaluate(self):
        """ given test and gold copora paths with matching docs, 
        compare proposed tags with actual tags """
        clf = SKClassifier(LogisticRegression(),
                           self.label_function,
                           self.feature_functions)

        # hyp
        test_corpus = Corpus(self.test_path)
        test_data = list(test_corpus.extents(self.indices_function,
                                             self.extent_class))
        test_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                            self.label_function(extent)) 
                        for extent in test_data])   
        clf.add_labels(test_labels.values())
        
        # ref
        gold_corpus = Corpus(self.gold_path)
        gold_data = list(gold_corpus.extents(self.indices_function,
                                            self.extent_class))
        gold_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                             self.label_function(extent)) 
                        for extent in gold_data])        

        for key in test_labels.keys():
            if key not in gold_labels:
                gold_labels[key] = 'False'
        for key in gold_labels.keys():
            if key not in test_labels:
                test_labels[key] = 'False'

        clf.add_labels(test_labels.values())        
        clf.add_labels(gold_labels.values())            
        cm = clf.evaluate(test_labels, gold_labels)
        # output dict for 
        return cm
    
    
    def evaluate_movelink(self):
        """ given test and gold copora paths with matching docs, 
        compare proposed tags with actual tags """
        clf = SKClassifier(LogisticRegression(),
                           self.label_function,
                           self.feature_functions)

        # hyp
        test_corpus = Corpus(self.test_path)
        test_data = list(test_corpus.move_link_triples(self.indices_function,
                                                       self.extent_class))
        test_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                            self.label_function(extent)) 
                        for extent in test_data])   
        clf.add_labels(test_labels.values())
        
        # ref
        gold_corpus = Corpus(self.gold_path)
        gold_data = list(gold_corpus.move_link_triples(self.indices_function,
                                                       self.extent_class))
        gold_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                             self.label_function(extent)) 
                        for extent in gold_data])        
        clf.add_labels(gold_labels.values())            
        cm = clf.evaluate(test_labels, gold_labels)
        # output dict for 
        return cm

    def evaluate_qs_o_link(self):
        """ given test and gold copora paths with matching docs, 
        compare proposed tags with actual tags """
        clf = SKClassifier(LogisticRegression(),
                           self.label_function,
                           self.feature_functions)

        # hyp
        test_corpus = Corpus(self.test_path)
        test_data = list(test_corpus.qs_o_link_triples(self.indices_function,
                                                       self.extent_class))
        test_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                            self.label_function(extent)) 
                        for extent in test_data])   
        clf.add_labels(test_labels.values())
        
        # ref
        gold_corpus = Corpus(self.gold_path)
        gold_data = list(gold_corpus.qs_o_link_triples(self.indices_function,
                                                       self.extent_class))
        gold_labels = dict([
                            ("{a},{b},{c}".format(a=extent.basename,
                                                  b=extent.lex[0].begin, 
                                                  c=extent.lex[-1].end),  
                             self.label_function(extent)) 
                        for extent in gold_data])        
        clf.add_labels(gold_labels.values())            
        cm = clf.evaluate(test_labels, gold_labels)
        # output dict for 
        return cm

    






def copy_folder(src, dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest)


