'''
Created on Sep 19, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

framework for logistic regression model, to demo viability of tagging scheme even
on a baseline classifier system. 
'''
from util.corpora.corpus import Corpus, HypotheticalCorpus
from sklearn.linear_model import LogisticRegression 
from util.model.sk_classifier import SKClassifier
from abc import abstractmethod
import os, shutil
from sklearn import hmm, tree,re

from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
from util.model.baseline_classifier import Classifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier

def starts_with_a(token):
    if token[0] == 'a':
        return True
    else:
        return False

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]    


def test_seq_preprocessing():
    # testing preprocessing
    with open('config.txt') as fo:
        text = fo.read()
    train_path = re.findall('TRAINING_PATH *= *(.*)', text)[0]
    gen_path = re.findall('CONFIG_1_GEN_PATH *= *(.*)', text)[0]
  
    x = Classifier(train_path=train_path,test_path=gen_path)
      
    train,test=x.generate_test_train()
    for e in train[:10]:
        print e.token
    print '=' * 10
 
    train,test=x.generate_sent_test_train()
    for s in train[:2]:
        print [e.token for e in s] 
    
def training_test():
    train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    
    trainer = pycrfsuite.Trainer(verbose=False)
    
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0, # coefficient for L1 penalty
        'c2': 1e-3, # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
        'feature.possible_transitions': True # include transitions that are possible, but not observed
    })

    trainer.train('conll2002-eng.crfsuite') #string = path to save file to    


def classify_test():
    test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]
    tagger = pycrfsuite.Tagger()
    tagger.open('conll2002-esp.crfsuite')
    for sent in X_test:
        print tagger.tag(sent)



def crf_testing_test():
    return


def fix_modified_xml():

    train_corpus = Corpus('./data/training')
    i = 0
    for doc in train_corpus.documents():
        name=doc.name.replace('training','Tokenized++')
        with open(name,'rb') as fo:
            text=fo.read()
            lines=text.split('\n')
        i=0
        for s in doc.tokenizer.tokenize_text().sentences:
            sent = s.as_pairs()
            for tok,lex in sent:
                while not re.match('\s*<lex',lines[i]):
                    i+=1
                lines[i] = re.sub("begin='\d+?'",
                             "begin='{}'".format(lex.begin),
                             lines[i])
                lines[i] = re.sub("start='\d+?'",
                             "".format(lex.begin),
                             lines[i])
                lines[i] = re.sub("end='\d+?'",
                             "end='{}'".format(lex.end),
                             lines[i])
                #print tok,',',lex.begin,',',lex.end
                #print re.findall('<lex .+?>(.+?)</lex>',lines[i])
                #print lines[i]
                i+=1
        with open(doc.name.replace('training','training++'),'wb') as fo:
            for line in lines:
                fo.write(re.sub('\r','',line)) #clean carriage returns
                fo.write('\n')


def fix_modified_test_xml():

    train_corpus = Corpus('./data/gold')
    i = 0
    for doc in train_corpus.documents():
        name=doc.name.replace('gold','Test++')
        with open(name,'r') as fo:
            text=fo.read()
            lines=text.split('\n')
        i=0
        for s in doc.tokenizer.tokenize_text().sentences:
            sent = s.as_pairs()
            for tok,lex in sent:
                while not re.match('\s*<lex',lines[i]):
                    i+=1
                lines[i] = re.sub("begin='\d+?'",
                             "begin='{}'".format(lex.begin),
                             lines[i])
                lines[i] = re.sub("start='\d+?'",
                             "".format(lex.begin),
                             lines[i])
                lines[i] = re.sub("end='\d+?'",
                             "end='{}'".format(lex.end),
                             lines[i])
                #print tok,',',lex.begin,',',lex.end
                #print re.findall('<lex .+?>(.+?)</lex>',lines[i])
                #print lines[i]
                i+=1
        with open(doc.name.replace('gold','gold++'),'wb') as fo:
            for line in lines:
                fo.write(re.sub('\r','',line)) #clean carriage returns
                fo.write('\n')


if __name__ == "__main__":

#     fix_modified_xml()
#     fix_modified_test_xml()

#     train_corpus = Corpus('./data/training++')
#     for doc in train_corpus.documents():
#         for k,v in doc.sort_feats_by_begin_offset().iteritems():
#             print v

    print len(' '.join(['test']))
            
            
#         for e in doc.feats():
#             print e.attrs
        
#         for s in doc.tokenizer.tokenize_text().sentences:
#             sent = s.as_pairs()
#             with open(doc.name,'r') as fo:
#                 text = fo.read()
#             for tok,lex in sent:
#                 print tok,',',lex.begin,',',lex.end
#                 feats = re.findall("<lex(.+?begin=.{b}.+?)>.+?</lex>".format(b=lex.begin),
#                                  text)[0]
#                 expanded_feats = {}
#                 for f in feats.split("' "):
#                     key_feat=f.split("='")
#                     if len(key_feat) == 2:
#                         k,f=key_feat
#                         expanded_feats[k]=f
#                 print expanded_feats
                
     
#     x = tree.DecisionTreeClassifier()
#     
#     x.fit([[1,2,3],[5,6,7]],[0,1])
#     print x.predict([5,6,6])
           
#     l = [[1,2,3],[4,5,6],[9,1,0]]
#     print [item for sublist in l for item in sublist]    

    #classify_test()
    
    