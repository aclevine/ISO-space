'''
Created on Sep 9, 2014

@author: Aaron Levine
'''

import Corpora.corpus as zach
import Corpora.tokenizer as mark
import operator
from bs4 import BeautifulSoup
from Corpora.tokenizer import TokenizedSentence

# SORT TAGS

# BUILD INSTANCE


if __name__ == "__main__":

   
    # LOAD DOC
    c = zach.Corpus('./train')
    doc = list(c.documents())[1]
    tags = doc.consuming_tags()

    # SORT TAG INFO
    sd = {}
    for t in tags:
        sd[int(t.attrs['start'])] = t.attrs # START OFFSET: XML TOKENS, OFFSETS, SPATIAL DATA
    lexes = doc.tokenizer.lexes #[(<START>, <END>, <TOKEN>), ... ]

    # LOAD TRAINING DATA INTO DESIRED FORMAT
    sent_offsets = doc.tokenizer.sentences
    
    # BUILD INSTANCES: {token:String, lex:TokenizedLex, prev_tokens:list, next_tokens:list}
    inst_list = []
    for s in doc.tokenizer.tokenize_text().sentences:
        sent = s.as_pairs()
        for i in range(len(sent)):
            token = sent [i] # (token, lexeme obj)
            before = sent[:i] # [ (token, lexeme obj), (token, lexeme obj), ...]
            after = sent [i+1:] # [ (token, lexeme obj), (token, lexeme obj), ...]
            tag = sd.get( token[1].begin, {})
            
            print tag
                        
            inst = {'token': token[0],
                    'TokenizedLex': token[1], 
                   'prev_tokens': before, 
                   'next_tokens': after}
                        
            inst_list.append(inst)

    #print inst_list


    

    # NEXT: SEE ABOUT JOINING TOKENS


        


    #print sorted(sd)
    #sent_offsets = doc.tokenizer.sentences


    
    
    
    
    #===========================================================================
    # for t in doc.tokenizer.tokens: # sentence list, offsets
    #     print t
    #===========================================================================
    
    
    #===========================================================================
    # text = doc.text()
    # t = mark.Tokenizer(text)
    # x = t.tokenize_text()     
    # x.print_as_xmlstring() #XML TOKENS WITH SENTENCES AND OFFSETS
    #===========================================================================
     
     
    


    