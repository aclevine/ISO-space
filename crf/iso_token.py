# -*- coding: utf-8 -*-

"""Wrapper around a token used for machine learning.

"""

import re

import nltk
import stanford.taggers.pos as pos

import tagdoc as td

#gold = td.sp

GET_TUPLE = re.compile(r'(?<=\()[^\)]+')
U = re.compile(r'^ u\'')

class Token(object):
    """Wrapper around a token used for machine learning

    Representation of a token to be classified by a ML algorithm.

    Args:
        word: The raw string representing the token in a text.

    Attributes:
        word: The raw string representing the token in a text.
        pos: A list of possible part-of-speech tags for the token.
        sentence: The string sentence where the token is found.
        text: The entire string text where the token is found.
        label: The (possibly true) class label for the token.
    
    """
    def __init__(self, word, sent, start, end, tokens, label, pos=True):
        self.word = word
        self.sent = sent
        self.start = start
        self.end = end
        self.posTokens = []
        self.tokens = [x for x in tokens if x[-1]]
        if pos:
            try:
                self.posTokens = pos.tag(sent)
            except:
                pass
        self.label = label
        self.pos = ''
        self.dict = {}
        #self._get_pos()

    def _get_pos(self):
        if len(self.tokens) == len(self.posTokens):
            for x,token in enumerate(self.tokens):
                self.dict[int(token[0])] = x
            self.pos = self.posTokens[self.dict[self.start]][-1]
                
    def __repr__(self):
        return self.word


def parseTokenList(string):
    l = []
    rawTuples = GET_TUPLE.findall(string)
    for x in rawTuples:
        z = x.split(',')
        s = ''
        t = []
        for y in z:
            s = U.sub('', y)
            s = s.replace('\'', '')
            s = s.replace(' ', '')
            t.append(s)
        #t = [y.replace('\'', '').replace(' ', '') for y in z]
        l.append(tuple(t))
    return l
         

def saveToken(token):
    return '\t'.join([token.word, token.sent.replace('\n', ''), str(token.start), str(token.end), str(token.posTokens), str(token.tokens), token.label]).encode('utf-8')

def loadTokens(filename = '/users/sethmachine/desktop/ISO-Space/crf/tokens.txt'):
    tokens = []
    with open(filename) as f:
        for line in f:
            attrs = line.split('\t')
            #return parseTokenList(attrs[5])
            token = Token(attrs[0], attrs[1], int(attrs[2]), int(attrs[3]), parseTokenList(attrs[5]), attrs[6], False)
            token.posTokens = parseTokenList(attrs[4])
            token._get_pos()
            tokens.append(token)
    return tokens
            
#sp = [Token(x.word, x.sent, x.sentStart, x.sentEnd, x.tokens, x.name) for x in gold]
sp = loadTokens()
s = [x for x in sp if x.posTokens and len(x.word.split()) == 1]
