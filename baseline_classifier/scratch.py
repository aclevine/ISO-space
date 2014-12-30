'''
Created on Sep 9, 2014

@author: Aaron Levine
'''
import numpy
import nltk


if __name__ == "__main__":    
    
    text = "eat the bees"
    tokens = nltk.word_tokenize(text)

    print nltk.pos_tag(tokens)
    
    print nltk.prase
    
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
