'''
Created on Sep 9, 2014

@author: ACL73
'''

import Corpora.corpus as zach
import Corpora.tokenizer as mark

if __name__ == "__main__":
    
    
    
    #1) LOAD TRAINING DATA INTO DESIRED FORMAT
    c = zach.Corpus('./train')
     
    #===========================================================================
    # for d in c.documents():
    #     print d.text()
    #     print d.tags()
    #===========================================================================
         
     
    doc = list(c.documents())[0]
    tags = doc.consuming_tags()
    for t in tags:
        print t.attrs
    
#===============================================================================
#     text = doc.text()
#     t = mark.Tokenizer(text)
#     x = t.tokenize_text()
# 
#     
#     x.print_as_xmlstring() #XML TOKENS WITH SENTENCES AND OFFSETS
#     
#     for t in doc.tags():
#         print t # XML TOKENS, OFFSETS, SPATIAL DATA
# 
#     
#===============================================================================
    



        
        # NEED: 
            # TOKEN
            # SURROUNDING WORDS (sentence?)
            # LABEL EXTRACTOR
         
    
    