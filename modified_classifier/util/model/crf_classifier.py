'''
Created on Apr 17, 2015

@author: Aaron Levine
@email: aclevine@brandeis.edu

generalized class for loading data into crfsuite model
'''

from sk_classifier import SKClassifier
import pycrfsuite

class CRFClassifier(SKClassifier):

    def featurize(self, sentence, test=False):
        """ create a list of sequential features ('sentences' of features) """
        X = []
        y = []
        # instance = (c_path, (body, subject, label))
        for inst in sentence:
            # LABEL EXTRACTOR
            y.append(self.label_extract(inst))
            # FEAT EXTRACTOR
            feats = []
            for f in self.feature_funcs:
                f = [u'{}={}'.format(name, value) for name, value in f(inst).iteritems()]
                feats.extend(f)
            X.append(feats)
        return (X, y)

    def train(self, sentences, model_path='tmp.crfsuite'):
        trainer = pycrfsuite.Trainer(verbose=False)        
        self.model_path=model_path
        for sent in sentences:
            X_train, y_train = self.featurize(sent)
            trainer.append(X_train, y_train)
        trainer.set_params({
            'c1': 1.0,   # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': 50,  # stop earlier
            'feature.possible_transitions': True # include transitions that are possible, but not observed
        })
        trainer.train(self.model_path)
    
    def classify(self, sentences, probs=False, keys=[]):
        tagger = pycrfsuite.Tagger()
        tagger.open(self.model_path)
        if probs:
            return "not yet supported"
        else:
            pred = []
            for sent in sentences:
                X, y = self.featurize(sent, test=True)
                if X:
                    tags = tagger.tag(X)
                pred.extend(tags)
            if keys:
                keyed_pred = {}
                for i in range(len(keys)):
                    keyed_pred[keys[i]] = pred[i]
                return keyed_pred
            else:
                return pred

