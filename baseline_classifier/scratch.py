'''
Created on Sep 9, 2014

@author: Aaron Levine
'''
import numpy
import nltk
from util.corpora.corpus import Corpus

if __name__ == "__main__":    

    
    c = Corpus('./data/dev')
    
    for doc in c.documents():
        print doc.query('m4')
    

#     y = numpy.zeros(4)

#     x = numpy.zeros(4)
#     x[0] += 1
# 
#     print numpy.add(y, x)
    

    
    
    
    
    
    # print nltk.pos_tag([u'\u201c'])

#===============================================================================
#     split = 0.8
#     docs = [1, 2, 3, 4]
# 
#     i = int(len(docs) * split)
#     train_docs = docs[:i]
#     test_docs = docs[i:]
#     
#     print train_docs
#     print test_docs
# 
#     
#===============================================================================
