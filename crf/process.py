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
#t = td.TagDoc('/users/sethmachine/desktop/Tokenized/CP/46_N_22_E.xml')
#t = td.TagDoc('/users/sethmachine/desktop/Tokenized/CP/47_N_25_E.xml')

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
        attrs = ''.join([' ' + x + '=\'' + self.keyvalues[x].replace("'", '') + '\'' for x in self.keyvalues])
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

def process(tagdoc, golddir, newdir='', renew=False, debug=False):
    if not newdir:
        newdir = golddir + '++'
    if not os.path.exists(newdir): #if the dir doesn't exist
        os.mkdir(newdir)
    path = newdir + tagdoc.filename.replace(golddir, '')
    print path
    if not renew:
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
            if debug:
                print ' '.join([x for x in tokens])
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


#an odd error with sparser
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/45_N_23_E.xml
Traceback (most recent call last):
  File "script.py", line 52, in <module>
    process.process(doc, golddir=args.source)
  File "/home/u/fall11/sdworman/iso-space/ISO-space/crf/process.py", line 148, in process
    edges = p(' '.join([x for x in tokens]), split=True)
  File "/home/u/fall11/sdworman/iso-space/ISO-space/crf/sparser/sparser.py", line 126, in p2edges
    new_edge = Edge(edgeStr)
  File "/home/u/fall11/sdworman/iso-space/ISO-space/crf/sparser/sparser.py", line 70, in __init__
    self.edges = [x for x in m.group('edge').split(' ') if x]
AttributeError: 'NoneType' object has no attribute 'group'
"""

#another odd error
#breaks on this sentence:
#Using field tracks we needed plenty of time to reach the village of Sinpetru German , where we met several very friendly women , who told us some interesting historical facts of their village .
#breaks at this spot on the word village/town: the [village] of Sinpetru German
"""
(p "(p "Using field tracks we needed plenty of time to reach the town of Sinpetru German , where we met several very friendly women , who told us some interesting historical facts of their town .")
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/46_N_21_E.xml
> Break: Another case of a category for the region: #<ref-category VILLAGE>
> While executing: SPARSER::GIVE-KIND-ITS-NAME, in process toplevel(2).
"""

"""
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/46_N_22_E.xml
> Break: Object passed in as 'individual' parameter is of
>        unexpected type: WORD
>        #<word "5">
> While executing: SPARSER::VALUE-OF, in process toplevel(2).
"""

#sparser parses this incorrectly
#edge: "gps '"
#which causes the string delimiter to overflow, making the xml formatted wrong
"""
The GPS 'said' that from here till the point we had 200 meters left (Point).
"""

#really?!
#26-Dec-2002 -- This confluence can be found 1,5 km to the west from Icafalau ( Ikafalva ) in Covasna county , Romania .
#sparser messes up on european style of measurements: x,y [measurement]
"""
/home/u/fall11/sdworman/iso-space/Tokenized++/CP/46_N_26_E.xml
> Break: Object passed in as 'individual' parameter is of
>        unexpected type: WORD
>        #<word "5">
> While executing: SPARSER::VALUE-OF, in process toplevel(2).
"""

#another error!
#the problem is here:
#( after printing some multimaps and a visit report or two ( always the optimist )
#there's an open paren inside but it has no matching close! haha
"""
Tokenized++/CP/47_N_25_E.xml
Fortunately Eastern Europe - even outside the EU is easy travelling for EU citizens and I was able to jump in the car ( after printing some multimaps and a visit report or two ( always the optimist ) and drive across Serbia , and Bulgaria to Romania with few hassles ( those there were concentrated on car insurance ) .
> Break: double parens
> While executing: MARK-OPEN-PAREN, in process listener(1).
> Type :GO to continue, :POP to abort, :R for a list of available restarts.
> If continued: Return from BREAK.
> Type :? for other options.
"""
