'''
Created on Sep 9, 2014

@author: Aaron Levine
'''
import numpy
import Corpora.corpus as xml
import nltk

def build_instances_kai(doc_path = './test'):
    '''get basic sense of manipulating xml docs'''
    c = xml.Corpus(doc_path)

    for doc in list(c.documents()):        
        # sort tag info by start offset
        sd = {}
        tags = doc.consuming_tags()
        for t in tags:
            sd[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    
        # construct instance objects from corpus data    
        punct = [u'\u201c', u'\u201d', u'\u2014', u'\u2019s', u'(', u')']
        start = 0
        end = 0
        last_pos = ""
        for s in doc.tokenizer.tokenize_text().sentences:
            sent = s.as_pairs()
            for i in range(len(sent)):
                ## a) Identify spans of spatial elements including locations, paths, events and other spatial entities.
                pos = nltk.pos_tag([sent[i][0]])[0][1]
                if pos.startswith('NN') and last_pos.startswith('NN')\
                and sent[i][0] not in punct and sent[i-1][0] not in punct:
                        end = end + 1
                else:
                    if end > start + 1:
                        token = [t for t, l in sent[start:end]]
                        lexes = [l for t, l in sent[start:end]]
                        before = sent[:start] # [ (token, lexeme obj), (token, lexeme obj), ...]
                        after = sent [end+1:] # [ (token, lexeme obj), (token, lexeme obj), ...]
                        tag = sd.get( lexes[0].begin, {})            
                        print token         
                    start = i
                    end = i + 1
                last_pos = pos
                #inst = Instance(token, lexes, before, after, tag)                         
                #yield inst


if __name__ == "__main__":
    
    y = numpy.zeros(4)
    x = numpy.zeros(4)
    x[0] += 1

    print numpy.add(y, x)
    

    
    
    
    
    
    #print nltk.pos_tag([u'\u201c'])

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
