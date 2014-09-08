#!/usr/bin/env python
import json

from nltk import word_tokenize
import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer

from feature_extract import *
from util.alphabet import Alphabet
from util.evaluator import ConfusionMatrix
from gensim import corpora, models, similarities

#inst =  (tag, tok, body)
def label(inst):
    return inst[0]

def token(inst):
    return inst[1]

def body(inst):
    return inst[2]

class SKClassifier():
    def __init__(self, clf, ffuncs):
        self.feature_funcs = ffuncs
        self.clf = clf
        self.labels = Alphabet()
        self.features = DictVectorizer() 
        self.model_info = {} #keys = feature extractors; values = data for feature extractors
    
    def add_labels(self, labels):
        for label in labels:
            self.labels.add(label)

    def featurize(self, instances, test=False):
        X = []
        y = []
        #instance = (path, (body, subject, label))
        for inst in instances:
            try:
                y.append(self.labels.get_index(label(inst)))
            except KeyError:
                if not test:
                    print "Couldn't find %s in set of labels. ^C if this is a problem." % label(inst)
            feats = get_fsets(self.feature_funcs, body(inst), '', self.model_info)
            #feats.update(get_fsets(self.feature_funcs, [token(instance)], 'word', self.model_info))
            X.append(feats)
        if test:
            return (self.features.transform(X), y)
        else:
            return (self.features.fit_transform(X), y)

    def train(self, instances):
        X, y = self.featurize(instances)
        self.clf.fit(X, y)
    
    def classify(self, instances, probs=False):
        X, y = self.featurize(instances, test=True)
        if probs:
            pred = self.clf.predict_proba(X)
            return [(self.labels.get_label(np.argmax(pred[i:])), np.max(pred[i:])) for i in xrange(len(pred))]
        else:
            pred = self.clf.predict(X)
            return [self.labels.get_label(i) for i in pred]
    
    def evaluate(self, pred, actual):
        cm = ConfusionMatrix(self.labels)
        cm.add_data([self.labels.get_index(x) for x in pred], [self.labels.get_index(x) for x in actual])
        cm.print_out()
    
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
        #with open(os.path.join(path, 'testSet.txt'), 'w') as fo:
        #    fo.write('\n'.join([x[0] for x in testset]))
        with open(os.path.join(path, 'featureSet.txt'), 'w') as fo:
            fo.write('\n'.join([x.__name__ for x in features]))
