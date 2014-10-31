'''
Created on Oct 31, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
'''
#===============================================================================
from identify_spans import *
#===============================================================================

# DEMO 2
def upper_case(test_data):
    pred = []
    for x in test_data:
        if str.isupper(str(x.token[0][0].encode('utf-8'))) and \
        x.next_tokens != [] and \
        str.isupper(str(x.next_tokens[0][0].encode('utf-8'))):
            pred.append('True')
        else:
            pred.append('False')
    return pred

def noun(test_data):
    """ do current token and next both have noun pos tags? """
    pred = []
    for x in test_data:
        if nltk.pos_tag(x.token[:1])[0][1][0] == 'N' and \
        x.next_tokens != [] and \
        nltk.pos_tag(x.next_tokens[0][:1])[0][1][0] == 'N':
            pred.append('True')
        else:
            pred.append('False')
    return pred

def matching_tag(test_data):
    """ do current token and next have same pos tag? """
    pred = []
    for x in test_data:
        if x.next_tokens != [] and \
        nltk.pos_tag(x.token[:1])[0][1][0] == nltk.pos_tag(x.next_tokens[0][:1])[0][1][0]:
            pred.append('True')
        else:
            pred.append('False')
    return pred

def all_false(test_data):
    """ have all predictions be False"""
    pred = []
    for x in test_data:
        pred.append('False')
    return pred
#===============================================================================

def span_rule_demo(doc_path = './training', split=0.8, tagged_only=False):
    """ test some simple heuristics """
    c = Corpus(doc_path)    
    if tagged_only:
        test_data = []
        for x in  c.instances():
            if x.tag != {}:
                test_data.append(x)    
    else:
        test_data = list(c.instances())

    label = lambda x: str(x.unconsumed_tag())
    features = [lambda x: x]
    clf = SKClassifier(LogisticRegression(), label, features)
    clf.add_labels(['True', 'False']) #binary classifier
    pred = upper_case(test_data)
    clf.evaluate(pred, [label(x) for x in test_data])