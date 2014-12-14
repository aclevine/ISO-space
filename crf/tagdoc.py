# -*- coding: utf-8 -*-

"""Code to represent xml based annotation as Python objects.
"""
import os, sys, inspect
from os.path import basename
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"baseline_classifier/Corpora")))
cmd_subfolder = cmd_subfolder.replace('/crf', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
import xml.etree.ElementTree as ET
import tokenizer
import re

import stanford.taggers.pos as pos
import stanford.taggers.ner as ner
from sparser.sparser import p2edges as p
from util.unicode import ureplace as u
from util.unicode import u2ascii

                                      

SPRL_FILE = "/users/sethmachine/desktop//CP.gold/45 N 22 E.xml"
SPRL_DIR = "/users/sethmachine/desktop/CP.gold"
ISO_DIR = "/users/sethmachine/desktop/CP"
ISO_FILE = "/users/sethmachine/desktop/CP/45_N_22_E.xml"
ISO_GOLD_DIR = "/users/sethmachine/desktop/Tokenized"

TEST_DIR = "/users/sethmachine/desktop/new"

TEXT = 'TEXT'
TAGS = 'TAGS'

#global list of ISO-Space tags which have extents, i.e. not relations.
ISO_CATEGORIES = ['PLACE', 'PATH', 'SPATIAL_ENTITY', 'NONMOTION_EVENT',
                  'MOTION', 'SPATIAL_SIGNAL', 'MOTION_SIGNAL', 'MEASURE', 'NONE']

START = 0
END = 1


def get_unicode(tagdocs):
    chars = []
    for x in tagdocs:
        chars += [i for i in x.text if ord(i) >= 128]
    return chars
        
            

def binary_search(token, sorted_tags, counter=1):
    """A simple binary search to determine which tag contains the token.

    Performs a binary search across all sorted_tags, sorted by start spans
    from least to greatest.  A tag matches a given token if the token's
    start and end spans are within that tag's start/end spans.
    Takes at most log(len(sorted_tags)) iterations.

    Args:
        token: A lexer token of the form (start, end, word), where
            start is the index of where the token begins,
            end is the index of where the token ends,
            and word is the actual token string.
        sorted_tags: A list of sorted ET tags from an annotated xml.
            The tags are sorted by the value of their start span.
        counter: An integer keeping track of the number of iterations,
            primarily for debugging purposes,
            i.e. counter <= log(len(sorted_tags))

    Returns:
        The tag which contains that token,
        or None if there is no tag which has that token.

    """
    if not sorted_tags: #token isn't tagged in any extent
        return None
    size = len(sorted_tags)
    index = size / 2
    curr = sorted_tags[index]
    if token[START] >= int(curr.attrib['start']) and token[END] <= int(curr.attrib['end']):
        return curr
    if token[START] > int(curr.attrib['end']):
        return binary_search(token, sorted_tags[index + 1:size], counter + 1)
    elif token[END] < int(curr.attrib['start']):
        return binary_search(token, sorted_tags[0:index], counter + 1)
    else: #if we get here, the token somehow overlaps extents!
        return None

xml_tokens_pattern = re.compile(r'<TOKENS>.+</TOKENS>', re.DOTALL)
whitespace_pattern = re.compile(r' {2,}')
quote_pattern = re.compile(r'["\']')

def getText(tagDoc):
    w = open(tagDoc.filename, 'r')
    t = w.read()
    w.close()
    return xml_tokens_pattern.sub('', t)

def newXml(tagDoc):
    new_dir = '/users/sethmachine/desktop/TokenizedPlus'
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    #text = getText(tagDoc)
    print os.path.splitext(tagDoc.filename)[0]
    clip = tagDoc.filename.replace('/users/sethmachine/desktop/Tokenized/', '')
    new_filename = os.path.join(new_dir, clip)
    currdir = os.path.dirname(new_filename)
    stack = []
    while not os.path.exists(currdir):
        stack.append(currdir)
        currdir = os.path.dirname(currdir)
    while stack:
        pop = stack.pop()
        if not os.path.exists(pop):
            os.mkdir(pop)
    #new_filename = os.path.join(new_dir, basename(tagDoc.filename))
    #new_filename = ''.join((os.path.splitext(tagDoc.filename)[0], '-new', '.xml'))
    t = '<TOKENS>\n'
    oldText = tagDoc.text
    #oldText = whitespace_pattern.sub('', tagDoc.text)
    iso_tags = [x for x in tagDoc.tags if 'start' in x.attribNames]
    iso_tags.sort(key=lambda x: int(x.attrib['start']))
    for sent in tagDoc.tokenizer.sentences:
            s = '<s>'
            sentence = u(oldText[sent[0]:sent[1]])
            oldSent = sentence
            #strip unicode...
            #sentence = ''.join([i if ord(i) < 128 else '-' for i in sentence])
            #if oldSent != sentence:
                #return (oldSent, sentence)
            #sentence = whitespace_pattern.sub('', sentence)
            #return sentence
            edges = p(quote_pattern.sub('', sentence))
            tk = tokenizer.Tokenizer(oldSent)
            tk.tokenize_text()
            tokens = [x[1][0] for x in tk.tokens if x[1][0][-1]]
            return (tokens, edges, sentence)
            pos_tags = pos.tag(sentence)
            ner_tags = ner.tag(sentence)
            #if not tokens:
                #return (oldSent, sentence)
            for x in xrange(0, len(tokens)):
                    lex = ''
                    lexes = ''
                    token = tokens[x]
                    #this works and grabs the correct label.
                    label = binary_search((token[0] + sent[0], token[1] + sent[0], token[2]), iso_tags)
                    if type(label) != type(None):
                        label = label.name
                    #print token, label
                    try:
                        if token[-1] == pos_tags[x][0]:
                            begin = str(token[0])
                            end = str(token[1])
                            postag = pos_tags[x][1]
                            nertag = ner_tags[x][1]
                            word = token[-1]
                            lex = ''.join(('\t<lex ', 'begin=\'', str(token[0]), '\'', ' end=\'', str(token[1]), '\'',
                                                   ' pos=\'', pos_tags[x][1], '\'', ' ner=\'', ner_tags[x][1], '\'',
                                                   ' label=\'', str(label), '\'',
                                                   '>', token[-1], '</lex>'))
                            s = ''.join((s, '\n', lex))
                        else:
                            continue
                    except IndexError:
                            break
            s = ''.join((s, '\n', '</s>\n'))
            #if s == '<s>\n</s>\n':
                #return (sentence, oldSent)
            t = ''.join((t, s))
    new_lex = ''.join((t, '</TOKENS>'))
    w = open(tagDoc.filename, 'r')
    newText = w.read().decode('utf-8')
    w.close()
    w = open(new_filename, 'w')
    newText = xml_tokens_pattern.sub(new_lex, newText)
    print>>w, newText.encode('utf-8')
    w.close()
            
def clean(word):
    #word = word.replace(u'\xad', '')
    return word

class Tag:
    """
    A wrapper around a tag.
    """
    def __init__(self, name, attrib, text, tokenizer2):
        self.name = name
        self.attrib = attrib
        self.attribNames = attrib.keys()
        self.text = text
        self.tokenizer = tokenizer2
        self.tokens = []
        self.sent = ''
        self.word = ''
        self.sentStart = 0
        self.sentEnd = 0
        if 'start' in self.attribNames:
            self.start = int(attrib['start'])
            self.end = int(attrib['end'])
        if 'text' in self.attribNames:
            self.sentIndex = self._get_sentence()
            self.word = self.attrib['text']
            if self.sentIndex:
                self.sent = self.text[self.sentIndex[0]:self.sentIndex[1]]
                self.sentStart = -1 * (self.sentIndex[0] - self.start)
                self.sentEnd = -1 * (self.sentIndex[0] - self.end)
                tk = tokenizer.Tokenizer(self.sent)
                tk.tokenize_text()
                self.tokens = [x[1][0] for x in tk.tokens]
    def _get_sentence(self):
        for sent in self.tokenizer.sentences:
            if int(self.attrib['start']) >= sent[0] and int(self.attrib['end']) <= sent[1]:
                return sent
        
        

    def __eq__(self, x):
        return self.name == x.name and self.attrib['text'] == x.attrib['text']

    def __ne__(self, x):
        return not self.__eq__(self, x)

    def __hash__(self):
        return hash(id(self))
    
    def __repr__(self):
        return self.name + " " + str(self.attrib)
    
class TagDoc:
    """
    A wrapper around an xml annotated document.
    """
    def __init__(self, filepath):
        self.filename = filepath
        self.tree = ET.parse(filepath)
        self.categories = ISO_CATEGORIES
        self.root = self.tree.getroot()
        self.sentences = [child for child in self.root.find('TOKENS')]
        self.text = self.root.find(TEXT).text
        self.tokenizer = tokenizer.Tokenizer(self.text)
        self.tokenizer.tokenize_text()
        self.xmlTags = [child for child in self.root.find('TAGS') if child.tag in self.categories and child.attrib['text']]
        self.tags = [Tag(child.tag, child.attrib, self.text, self.tokenizer) for child in self.root.find(TAGS)]
        self.tagDict = getTagDict(self.tags)

    def _get_tags(self):
        for child in self.root.find(TAGS):
            tag = Tag(child.tag, child.attrib, self.text)
            
    def get_multiwords(self, name='TRAJECTOR'):
        """Returns a list of all tags with multiword extents
        """
        return [tag for tag in self.tagDict[name] if len(tag.attrib['text'].split()) > 1]
    
class TagDir:
    """
    A wrapper around a directory of xml annotated documents.
    """
    def __init__(self, dirpath):
        self.files = getXML(dirpath)
        self.docs = [TagDoc(f) for f in self.files]
        self.texts = [doc.text for doc in self.docs]
        self.tags = flatten([doc.tags for doc in self.docs])
        self.tagDict = getTagDict(self.tags)

    def get_multiwords(self, name='TRAJECTOR'):
        """Returns a list of all tags with multiword extents
        """
        return [tag for tag in self.tagDict[name] if len(tag.attrib['text'].split()) > 1]
    
def getXML(dirpath=ISO_GOLD_DIR):
    files = []
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            if f.endswith('.xml'):
                files.append(fpath)
        elif os.path.isdir(fpath):
            files += getXML(fpath)
    return files
                
def getTagDict(tags):
    d = {tag.name: [] for tag in tags}
    for tag in tags:
        d[tag.name].append(tag)
    return d

def flatten(l):
    return [item for sublist in l for item in sublist]


def testTokens(tagdocs):
    for doc in tagdocs:
        sentences = doc.sentences
        text = doc.text
        for sentence in sentences:
            for child in sentence.getchildren():
                childToken = child.text
                textToken = text[int(child.attrib['begin']):int(child.attrib['end'])]
                if childToken != textToken:
                    print childToken, " but got ", textToken
                    raise ValueError
                #else:
                    #print "Correct!: ", childToken, "==", textToken
    print "The Lex tokens offsets match all documents!"

def tagTypeCount(tagdoc):
    d = {}
    for tag in tagdoc.tags:
        if tag.name in d:
            d[tag.name] += 1
        else:
            d[tag.name] = 1
    return d

def writeTagTypeCounts(tagdocs):
    w = open('/users/sethmachine/desktop/tag-type-counts.txt', 'w')
    for doc in tagdocs:
        d = tagTypeCount(doc)
        print>>w, basename(doc.filename)
        for key in d.keys():
            print>>w, key + '\t' + str(d[key])
        print>>w, '\n'
    w.close()
            

#gold = TagDir(ISO_GOLD_DIR)

#lazy (1 doc)
#doc = TagDoc("/users/sethmachine/desktop/Tokenized/ANC/WhereToJapan/Asakusa.xml")
#w = open(doc.filename, 'r')
#t = w.read()
#w.close()

#nineteen examples get the wrong text spans for the tokens
#something very weird going on
#some problematic unicode, e.g. u'South\xadeast of'
#sp = [x for x in gold.tagDict['SPATIAL_SIGNAL'] if x.word == x.sent[x.sentStart:x.sentEnd]]
#t = TagDir(TEST_DIR)
#z = t.docs[0]
#tr = t.tagDict['TRAJECTOR']

