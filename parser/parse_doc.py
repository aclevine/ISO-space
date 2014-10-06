'''
Created on Sep 19, 2014

@author: ACL73
'''
#===============================================================================
import Corpora.corpus as xml
#===============================================================================

class Instance:
    '''a class for loading tokens from XML doc with surrounding token and tag data'''
    def __init__(self, token, lex, prev_tokens, next_tokens, tag):
        self.token = token
        self.lex = lex
        self.prev_tokens = prev_tokens
        self.next_tokens = next_tokens
        self.tag = tag


def build_instances(doc_iter):
    '''get basic sense of manipulating xml docs'''
    for doc in list(doc_iter):    
        # sort tag info by start offset
        sd = {}
        tags = doc.consuming_tags()
        for t in tags:
            sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    

        # construct instance objects from corpus data    
        for s in doc.tokenizer.tokenize_text().sentences:
            #initialize pointers
            start = 0
            end = 1
            nonconsumed_tag = {}
            sent = s.as_pairs()
            for i in range(len(sent)): 
                token = sent [i] # (token, lexeme obj)
                # pull tag info
                if nonconsumed_tag != {}:
                    tag = nonconsumed_tag
                else:                    
                    tag = sd.get( token[1].begin, {})
                if tag != {} and int(tag["end"]) > token[1].end:
                    nonconsumed_tag = tag
                    end = i+1
                else:
                    nonconsumed_tag = {}
                print [t for t, l in token[start:end]]
                       
                #===============================================================
                # before = sent[:i] # [ (token, lexeme obj), (token, lexeme obj), ...]
                # after = sent [i+1:] # [ (token, lexeme obj), (token, lexeme obj), ...]
                # inst = Instance(token[0], token[1], before, after, tag)
                # yield inst
                #===============================================================
