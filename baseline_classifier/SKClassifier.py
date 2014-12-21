#!/usr/bin/env python
'''
Created on Sep 16, 2014

@author: Einar Froyen, Aaron Levine
'''
import json

import os
import numpy as np
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer

from util.alphabet import Alphabet
from util.evaluator import ConfusionMatrix

class SKClassifier():
    def __init__(self, clf, lfunc, ffuncs):
        self.feature_funcs = ffuncs
        self.label_extract = lfunc
        self.clf = clf
        self.labels = Alphabet()
        self.features = DictVectorizer() 
        self.model_info = {}  # keys = feature extractors; values = data for feature extractors
    
    def add_labels(self, labels):
        for label in labels:
            self.labels.add(label)

    def featurize(self, instances, test=False):
        X = []
        y = []
        # instance = (c_path, (body, subject, label))
        for inst in instances:
            # # LABEL EXTRACTOR
            y.append(self.labels.get_index(self.label_extract(inst)))
            # # FEAT EXTRACTOR0
            feats = {}
            for f in self.feature_funcs:
                feats.update(f(inst))
            X.append(feats)
        if test:
            return (self.features.transform(X), y)
        else:
            return (self.features.fit_transform(X), y)

    def train(self, instances):
        X, y = self.featurize(instances)
        self.clf.fit(X, y)
    
    def classify(self, instances, probs=False, keys=[]):
        X, y = self.featurize(instances, test=True)        
        if probs:
            pred = self.clf.predict_proba(X)
            if keys:
                keyed_pred = {}
                for i in range(len(keys)):
                    keyed_pred[keys[i]] = self.labels.get_label(pred[i])
                return keyed_pred
            else:
                return [(self.labels.get_label(np.argmax(pred[i:])), 
                         np.max(pred[i:])) 
                        for i in xrange(len(pred))]
        else:
            pred = self.clf.predict(X)
            if keys:
                keyed_pred = {}
                for i in range(len(keys)):
                    keyed_pred[keys[i]] = self.labels.get_label(pred[i])
                return keyed_pred
            else:
                return [self.labels.get_label(i) for i in pred]
        
    def evaluate(self, pred, actual):
        cm = ConfusionMatrix(self.labels)
        if type(pred) == dict:
            prediction_list = []
            true_answer_list = []
            for offsets, pred in pred.iteritems():
                prediction_list.append(self.labels.get_index(pred))
                true_answer_list.append(self.labels.get_index(actual[offsets]))
            cm.add_data(prediction_list, true_answer_list)                
        else:
            cm.add_data([self.labels.get_index(x) for x in pred], [self.labels.get_index(x) for x in actual])
        cm.print_out()
        return cm
        
    def load_model(self, path):
        self.clf = joblib.load(os.path.join(path, 'model.pkl'))
        with open(os.path.join(path, 'labels.json'), 'r') as fo:
            self.labels = Alphabet.from_dict(json.load(fo))
        with open(os.path.join(path, 'model_info.json'), 'r') as fo:
            self.model_info = json.load(fo)            
        self.features = joblib.load(os.path.join(path, 'featvec.pkl'))
    
    def save_model(self, path, testset, features):
        if not os.path.exists(path):
            os.makedirs(path)
        joblib.dump(self.clf, os.path.join(path, 'model.pkl'))
        with open(os.path.join(path, 'labels.json'), 'w') as fo:
            json.dump(self.labels.to_dict(), fo)
        with open(os.path.join(path, 'model_info.json'), 'w') as fo:
            json.dump(self.model_info, fo)
        joblib.dump(self.features, os.path.join(path, 'featvec.pkl'))
        # with open(os.c_path.join(c_path, 'testSet.txt'), 'w') as fo:
        #    fo.write('\n'.join([x[0] for x in testset]))
        with open(os.path.join(path, 'featureSet.txt'), 'w') as fo:
            fo.write('\n'.join([x.__name__ for x in features]))
