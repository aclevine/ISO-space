'''
Created on Sep 19, 2014

@author: ACL73

# 1) Spatial Elements (SE):
    ## a) Identify spans of spatial elements including locations, paths, events and other spatial entities.    
'''
#===============================================================================
from Corpora.corpus import Corpus
from sklearn.linear_model import LogisticRegression 
from SKClassifier import SKClassifier

import nltk
#===============================================================================

class Instance:
    '''a class for loading tokens from XML doc with surrounding token and tag data'''
    def __init__(self, token, lex, prev_tokens, next_tokens, tag):
        self.token = token
        self.lex = lex
        self.prev_tokens = prev_tokens
        self.next_tokens = next_tokens
        self.tag = tag

    # LABEL EXTRACT
    def unconsumed_tag(self):
        """does tag span multiple tokens?"""
        if int(self.tag.get("end", -1)) == self.lex[0].end:
            return True
        else:
            return False
    
    # FEATURE EXTRACT
    def upper_case(self):
        """ is token upper case"""
        if str.isupper(str(self.token[0][0].encode('utf-8'))):
            return {'upper_case':True}
        else:
            return {'upper_case':False}

    def next_upper_case(self):
        """ is next token upper case"""
        if self.next_tokens != [] and str.isupper(str(self.next_tokens[0][0].encode('utf-8'))):
            return {'next_upper_case':True}
        else:
            return {'next_upper_case':False}

    def prev_upper_case(self):
        """ is next token upper case"""
        if self.prev_tokens != [] and str.isupper(str(self.prev_tokens[-1][0].encode('utf-8'))):
            return {'prev_upper_case':True}
        else:
            return {'prev_upper_case':False}

    def pos_tag(self):
        tag = nltk.pos_tag(self.token[:1])[0][1]
        return {'pos_tag': tag}

    def next_pos_tag(self):
        if self.next_tokens != []:
            tag = nltk.pos_tag(self.next_tokens[0][:1])[0][1]
            return {'next_pos_tag': tag}
        return {'next_pos_tag': 'None'}

    def prev_pos_tag(self):
        if self.prev_tokens != []:
            tag = nltk.pos_tag(self.prev_tokens[-1][:1])[0][1]
            return {'prev_pos_tag': tag}
        return {'prev_pos_tag': 'None'}

    def simple_tag(self):
        tag = nltk.pos_tag(self.token[:1])[0][1]
        return {'simple_tag': tag[0]}

    def next_simple_tag(self):
        if self.next_tokens != []:
            tag = nltk.pos_tag(self.next_tokens[0][:1])[0][1]
            return {'next_simple_tag': tag[0]}
        return {'next_simple_tag': 'None'}

    def prev_simple_tag(self):
        if self.prev_tokens != []:
            tag = nltk.pos_tag(self.prev_tokens[-1][:1])[0][1]
            return {'prev_simple_tag': tag[0]}
        return {'prev_simple_tag': 'None'}


class Corpus_SE_A(Corpus):
    def instances(self):
        '''create a set of instances'''
        docs = self.documents()
        for doc in docs:    
            # sort tag info by start offset
            sd = {}
            tags = doc.consuming_tags()
            for t in tags:
                sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    
            # construct instance objects from corpus data    
            front = 0
            done = False
            for s in doc.tokenizer.tokenize_text().sentences:
                sent = s.as_pairs() # [ (token, lexeme obj), (token, lexeme obj), ...]
                for i in range(len(sent)):
                    token = sent [i] # (token, lexeme obj)
                    tag = sd.get(token[1].begin, {})                
                    front = i
                    done = True
                    if done:
                        done = False
                        token = [t for t, l in sent[front:i+1]]
                        lex = [l for t, l in sent[front:i+1]]
                        before = sent[:front]
                        after = sent [i+1:] 
                        inst = Instance(token, lex, before, after, tag)
                        yield inst

#===============================================================================

# DEMO
def span_model_demo(doc_path = './training', split=0.8):
    
    c = Corpus_SE_A(doc_path)    
    inst = list(c.instances())
    i = int(len(inst) * split)
    train_data = inst[:i]
    test_data = inst[i:]
     
    features = [lambda x: x.upper_case(),
                lambda x: x.next_upper_case(),
                lambda x: x.prev_upper_case(),
                lambda x: x.pos_tag(),
                lambda x: x.next_pos_tag(),
                lambda x: x.prev_pos_tag(),
                lambda x: x.simple_tag(),
                lambda x: x.next_simple_tag(),
                lambda x: x.prev_simple_tag()]
    
    label = lambda x: str(x.unconsumed_tag())
    
    clf = SKClassifier(LogisticRegression(), label, features)
    clf.add_labels(['True', 'False']) #binary classifier
    clf.train(train_data)
    pred = clf.classify(test_data)    
    clf.evaluate(pred, [label(x) for x in test_data])

#===============================================================================

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
    pred = []
    for x in test_data:
        if x.next_tokens != [] and \
        nltk.pos_tag(x.token[:1])[0][1][0] == nltk.pos_tag(x.next_tokens[0][:1])[0][1][0]:
            pred.append('True')
        else:
            pred.append('False')
    return pred

def all_false(test_data):
    pred = []
    for x in test_data:
        pred.append('False')
    return pred





def span_rule_demo(doc_path = './training', split=0.8):
    c = Corpus_SE_A(doc_path)    
    test_data = list(c.instances())
    
    label = lambda x: str(x.unconsumed_tag())
    features = [lambda x: x]

    clf = SKClassifier(LogisticRegression(), label, features)
    clf.add_labels(['True', 'False']) #binary classifier

    pred = upper_case(test_data)

    clf.evaluate(pred, [label(x) for x in test_data])


if __name__ == "__main__":

    span_model_demo()
    
    
    
    