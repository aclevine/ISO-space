# -*- coding: utf-8 -*-

"""Code to reprocess ISO-Space xmls and add new features
"""

import os
import re

import tagdoc as td
from tagdoc import binary_search#,doc
import tokenizer
from sparser.sparser import p2edges as p
import stanford.taggers.pos as pos
import stanford.taggers.ner as ner
from util.unicode import ureplace as u
from util.unicode import u2ascii

GOLDDIR = '/users/sethmachine/desktop/Tokenized'
NEWDIR = '/users/sethmachine/desktop/TokenizedPlus/'

#tokenization mistake in this file: line 171 has 2 sentences in 1 sentence
#t = td.TagDoc('/users/sethmachine/desktop/Tokenized/RFC/Hollywood.xml')

xml_tokens_pattern = re.compile(r'<TOKENS>.+</TOKENS>', re.DOTALL)
whitespace_pattern = re.compile(r' {2,}')
quote_pattern = re.compile(r'["\']')

class Sent(object):
    """Wrapper around a S(entence) ElementTree Element.

    """
    def __init__(self):
        self.lexes = []

    def add(self, lex):
        self.lexes.append(lex)

    def __repr__(self):
        lexStr = ''.join(['\t' + str(lex) + '\n' for (i, lex) in enumerate(self.lexes)])
        return ''.join(['<s>\n', lexStr, '</s>'])

class Lex(object):
    """Wrapper around a Lex ElementTree Element.

    """
    def __init__(self, text, keyvalues={}):
        self.text = text
        self.keyvalues = keyvalues

    def add(self, (key, value)):
        """Adds an attribute to the Lex object.

        """
        self.keyvalues[str(key)] = str(value)

    def addAll(self, keyvalues):
        self.keyvalues = dict(self.keyvalues.items() + {str(key):str(value) for (key, value) in keyvalues}.items())

    def __repr__(self):
        attrs = ''.join([' ' + x + '=\'' + self.keyvalues[x] + '\'' for x in self.keyvalues])
        return attrs.encode('utf-8')
        return ''.join(['<lex', attrs, '>', self.text, '</lex>']).encode('utf-8')
        

def mkparentdirs(path):
    """Creates mirrored parent directories at the newdir.

    If the path contains a hierarchical directory structure which does
    not exist yet in the path's target location, then this function
    will create each parent directory recursively to mirror the path's
    original directory structure.  E.g. "a/b/c/d.txt" would cause this function
    to create parent directories c, d if they did not exist from the top level
    directory a to the actual file d.txt.

    Args:
        path: The mirrored absolute path to the file.

    Returns:
        None.  Creates the directory structure of the path if it
            does not yet exist.
    
    """
    currdir = os.path.dirname(path)
    stack = []
    while not os.path.exists(currdir):
        stack.append(currdir)
        currdir = os.path.dirname(currdir)
    while stack:
        pop = stack.pop()
        if not os.path.exists(pop):
            os.mkdir(pop)

def test(doc1, doc2):
    """Compares two mirrored TagDoc objects.

    """
    for (sent1, sent2) in zip(doc1.sentences, doc2.sentences):
        for(child1, child2) in zip(sent1.getchildren(), sent2.getchildren()):
            if child1.text != child2.text:
                return (sent1, sent2)
    return True

def ledges(edges, tokens):
	l = []
	for token in tokens:
		for edge in edges:
			if token.lower() in edge.word.split(' '):
				l.append((token, edge))
				edges.remove(edge)
				break
	return l

def ledge(edges, token):
    for edge in edges:
        if token.lower() in edge.word.split(' '):
            edges.remove(edge)
            return edge
            
        
sentence_pattern = re.compile(r'<s>.+?</s>', re.DOTALL)
lex_attrs_pattern = re.compile(r'(?<=<lex)[^>]+')

def process(tagdoc, golddir, newdir=''):
    if not newdir:
        newdir = golddir + '++'
    if not os.path.exists(newdir): #if the dir doesn't exist
        os.mkdir(newdir)
    path = newdir + tagdoc.filename.replace(golddir, '')
    print path
    if os.path.exists(path): #don't redo our existing work :]
        print test(tagdoc, td.TagDoc(path))
        return
    mkparentdirs(path)
    w = open(tagdoc.filename, 'r')
    t = w.read()
    w.close()
    #grab only tags which have a text extent
    iso_tags = [x for x in tagdoc.tags if 'start' in x.attribNames]
    iso_tags.sort(key=lambda x: int(x.attrib['start'])) #sort for binary search
    for (i,m) in enumerate(re.finditer(sentence_pattern, t)):
        sentence = tagdoc.sentences[i]
        old_lexes = sentence.getchildren()
        raw_sentence = m.group()
        tokens = [''.join([c if ord(c) < 128 else u2ascii[c] for c in x.text]).encode('utf-8') for x in old_lexes]
        pos_tags = pos.tag(tokens)
        ner_tags = ner.tag(tokens)
        #print ' '.join([x for x in tokens])
        edges = []
        try:
            edges = p(' '.join([x for x in tokens]), split=True)
        except:
            pass
        c = 0
        for (j, n) in enumerate(re.finditer(lex_attrs_pattern, raw_sentence)):
            old_lex = old_lexes[j]
            new_lex = Lex(old_lex.text, old_lex.attrib)
            attributes = n.group()
            label = binary_search((int(old_lex.attrib['begin']), int(old_lex.attrib['end']), old_lex.text), iso_tags)
            if type(label) != type(None):
                label = label.name
            if pos_tags:
                if not ner_tags:
                    return (tokens, pos_tags, ner_tags)
                if tokens[j] == pos_tags[c][0]:
                    new_lex.addAll([('label', label), ('pos', pos_tags[c][1]), ('ner', ner_tags[c][1])])
                    if edges:
                        sparser_edge = ledge(edges, tokens[j])
                        if sparser_edge:
                            if sparser_edge.keyvalues:
                                keyvalues = sparser_edge.keyvalues[sparser_edge.keyvalues.keys()[0]]
                                new_lex.addAll([(key, keyvalues[key]) for key in keyvalues])
                    pos_tags.remove(pos_tags[c])
                    ner_tags.remove(ner_tags[c])
            t = t.replace(attributes, str(new_lex))
    w = open(path, 'w')
    print>>w, t
    w.close()
    print test(tagdoc, td.TagDoc(path))
        

def printchild(s):
	return ''.join([x.text + ', ' for x in s.getchildren()])
