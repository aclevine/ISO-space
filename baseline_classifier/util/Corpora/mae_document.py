import nltk
import xml.etree.ElementTree as ET
from mimetypes import guess_type
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from tokenizer import *

class MAE_Document:
    """A document object is constructed from an XML document file whose c_path is supplied as an initialization parameter. The XML DOM tree is expected to have the form of a MAE/MAI annotation (MAE is written by Amber Stubbs (astubbs@cs.brandeis.edu) and its documentation can be downloaded from http://code.google.com/p/mae-annotation/). The document should contain text within a <TEXT></TEXT> element whose content is CDATA[[]], and a <TAGS></TAGS> element containing offset annotations referring to the text. The document also instantiates a tokenizer for itself so that the document's text content may be tokenized for further processing."""
    def __init__(self, path):
        self.path = path
        self.supported_doc_types = ['application/xml', 'text/plain']
        self.doc_type = self.set_doc_type()
        self.text = self.extract_text()
        self.tokenizer = Tokenizer(self.text)
        self.sentences = self.tokenizer.tokenize_text().sentences
        self.tags = self.extract_tags()
        self.doc_id = self.get_doc_id()
        self.indexed_sentences = self.index_sentences()
    
    def get_doc_id(self):
        file = open(self.path, 'r')
        name = file.name
        file.close()
        return hash(name) ^ hash(file)
        
    def set_doc_type(self):
        doc_type = guess_type(self.path)[0]
        if not doc_type in self.supported_doc_types:
            raise UnsupportedMIMETypeError(doc_type)
        return doc_type
        
    def extract_text(self):
        """Returns the document's text as a string. If the document is determined to be an XML, the text is taken from <TEXT></TEXT> element if the document is an XML."""
        doc_text = ""
        if self.doc_type == 'application/xml':
            # doc_text = fix(ET.parse(self.c_path).findall('TEXT')[0].text)
            doc_text = ET.parse(self.path).findall('TEXT')[0].text
        if self.doc_type[0] == 'text/plain':
            file = open(self.path, 'r')
            doc_text = file.read()
            file.close()
        return doc_text
            
    def extract_tags(self):
        """Returns a list of dictionaries with attribute:value key-value pairs representing the tag elements from the <TAGS></TAGS> element of the XML DOM-tree if there is one."""
        doc_tags = []
        if self.doc_type == 'application/xml':
            doc_tags = [get_tag_attributes(tag) for tag in ET.parse(self.path).findall('TAGS')[0]]
        return doc_tags
        
    def index_sentences(self):
        """Function that returns sentences as lists of dictionaries where each dictionary key is a token and its values represent its attributes."""
        sentences = self.sentences
        tags = self.tags
        # Get a list of sentences where each sentence is a list of lexes represented as (start, end, token) 3-tuples
        lexed = [lex_tokenize(sentence_token) for sentence_token in sentences]
        # Get a list of part-of-speech-tagged sentences where each sentence is a list of tagged tokens represented as (token, pos_tag) 2-tuples
        pos_tagged = [pos_tag([token[2] for token in sentence]) for sentence in lexed]
    
        def zip_sents(l1, l2):
            """This function zips two lists together, but, unlike Python's built-in zip() method, instead of stripping out extra items from the longer list, it appends empty lists to the shorter list so that no items from the longer list are lost."""
            zipped = zip(l1, l2)
            # In case the lists are not of equal length
            if len(l1) != len(l2):
                shorter = l2 if (len(l2) < len(l1)) else l1
                longer = l1 if (len(l1) > len(l2)) else l2
                # Append all the remaining pairs with None as a placeholder for missing values from the shorter list
                for index in range(len(shorter), len(longer)):
                    if len(l1) > len(l2):
                        zipped.append((l1[index], []))
                    else:
                        zipped.append(([], l2[index]))
            return zipped
    
        # This loop is only intended for tokenizer debugging purposes
        pairs = zip_sents(lexed, pos_tagged)
        # Loop over each pair of tokenized sentences
        for index in range(len(pairs)):
            (lex_s, pos_s) = pairs[index]
            # In case the sentences have different lengths
            if len(lex_s) != len(pos_s):
                # Identify the sentence
                print "\nSentence %d beginning at character offset %d:" % (index, lex_s[0][0])
                print 'Lexed sentence has      %d token(s)' % len(lex_s)
                print 'PoS-tagged sentence has %d token(s)' % len(pos_s)
                two_column_format = '%-25s %-25s'
                print two_column_format % ("Lex", "PoS")
                # Loop over each index in the zipped list and print the tokens at each index to show where Marc's and the NLTKK tokenizers differ
                for index in range(zip_sents(lex_s, pos_s)):
                    (lex, pos) = ("---None---", "---None---")
                    if lex_s[index]:
                        lex = lex_s[index][-1]
                    if pos_s[index]:
                        pos = pos_s[index][0]
                    print two_column_format % (lex, pos)
        
        # Instantiate a stemmer (there are other stemmers provided by NLTK besides the Porter stemmer)
        stemmer = PorterStemmer()
    
        # Set up a list to keep track of indexed sentences
        indexed_sentences = []
    
        # Loop over pairs of lexed and pos-tagged sentences
        for (lexed_sent, pos_tagged_sent) in zip_sents(lexed, pos_tagged):
            # set up a list to keep track of the indices in the sentence
            indexed_sentence = []
            # In case lexed_sent isn't empty
            if lexed_sent:
                # Loop over pairs of lex and pos-tagged tokens in the sentence
                for (lex, pos) in zip_sents(lexed_sent, pos_tagged_sent):
                    # In case the lex isn't empty
                    if lex:
                        # Populate dictionary with features that are derived from the text itself
                        # features = ['start', 'end', 'text', 'orth', 'textlc', 'stem', 'pos', 'lemma', 'tag', ...]
                        feature_dict = {}
                        feature_dict['doc_id'] = self.doc_id
                        feature_dict['start'] = lex[0]  # start offset
                        feature_dict['end'] = lex[1]  # end offset
                        text = unicode(lex[2])  # unicode
                        feature_dict['text'] = text  # token text
                        feature_dict['orth'] = orth(text)  # orthographic
                        feature_dict['textlc'] = text.lower()  # lowercase
                        feature_dict['stem'] = stemmer.stem(
                            feature_dict['textlc']
                        )  # stemmed text
                        feature_dict['pos'] = None  # part of speech
                        feature_dict['lemma'] = None  # lemmatized token string
                        if pos and (lex[-1] == pos[0]):
                            feature_dict['pos'] = pos[1]  # NLTK tagger's PoS
                            word_net_pos = get_wordnet_pos(feature_dict['pos'])
                            lemma = wordnet.morphy(
                                feature_dict['textlc'],
                                word_net_pos
                            )
                        if lemma and word_net_pos:
                            feature_dict['lemma'] = unicode(lemma)  # lemmatized text
                        feature_dict['tag'] = None  # Default to no tag type
                        # Populate extra features based on annotation (if any)
                        # Loop over annotated tags
                        for tag in tags:
                            lex_span = (
                                feature_dict['start'],
                                feature_dict['end']
                            )
                            tag_span = (
                                tag['start'],
                                tag['end']
                            )
                            # In case the span of the token was annotated as an extent tag
                            if lex_span == tag_span:
                                # Fill additional features from the annotation attributes
                                for key in tag.keys():
                                    feature_dict[key] = tag[key]
                        # Append the dictionary to the list of tokens
                        indexed_sentence.append(feature_dict)
            # Append the sentence to the list of indexed sentences
            indexed_sentences.append(indexed_sentence)
        return indexed_sentences

def get_tag_attributes(element):
    """Returns a dictionary given a tag element whose keys are attributes of the element and whose values are the attribute values. Also, a 'type' key is added based on the tag label assigned in the annotation."""
    # Dictionary to keep track of tag attribute value key-pairs
    d = {}
    
    extent_tag_keys = set(['id', 'text', 'start', 'end'])
    link_tag_keys = set(['id', 'fromText', 'toText', 'fromID', 'toID'])
    
    # In case the element is an extent tag
    if extent_tag_keys.issubset(set(element.keys())):
        for key in extent_tag_keys:
            d[key] = element.get(key)
        d['tag'] = element.tag
        # Cast start and end offset attribute values as integers
        d['start'] = int(d['start'])
        d['end'] = int(d['end'])
    # In case the element is a link tag
    if link_tag_keys.issubset(set(element.keys())):
        for key in link_tag_keys:
            d[key] = element.get(key)
        d['tag'] = element.tag
        # Link tags have no textual extent, so their start/end offset values are assigned specially (like non-consuming tags)
        d['start'] = -1
        d['end'] = -1
    return d
    
def get_element_span(element):
    """Returns a span as a 2-tuple (start, end) given an element representing an extent tag."""
    return (element.get('start'), element.get('end'))
    
def get_tag_span(tag):
    """Returns the start and end character offsets of a given tag as a 2-tuple
(start, end)."""
    return (tag['start'], tag['end'])
    
def span_in_span(span1, span2):
    """ Tests if span1 is included in span2. Spans are expected to be 2-tuples of (start, end) character offsets."""
    # span1
    start1 = span1[0]
    end1 = span1[1]
    # span2
    start2 = span2[0]
    end2 = span2[1]
    # check if span2 includes span1 or not
    return (start2 <= start1) and (end2 >= end1)
    
def is_type(indexed_token, tag_type):
    """Tests if the given token was tagged with the given tag type."""
    return indexed_token.has_key('tag') and (indexed_token['tag'] == tag_type)
    
def lex_tokenize(tokenized_sentence):
    """Returns a list of lexes from a given tokenizer.TokenizedSentence instance. Each lex is represented as a 3-tuples of (start, end, token)."""
    return [(lex.begin, lex.end, lex.text) for (token, lex) in tokenized_sentence.as_pairs()]
    
def pos_tag(sentence):
    """Returns a list of part-of-speech-tagged tokens from a given sentence---a list of tokens. Each token is represented as a 2-tuple of (token, pos-tag)."""
    return nltk.pos_tag(sentence)

def orth(string):
    """Returns a feature label as a string based on the capitalization and other orthographic characteristics of the string."""
    if string.isdigit():
        return 'DIGIT'
    elif string.isalnum():
        if string.islower():
            return 'LOWER'
        elif string.istitle():
            return 'TITLE'
        elif string.isupper():
            return 'UPPER'
        else:
            return 'MIXED'
    elif string.isspace():
        return 'SPACE'
    else:
        return 'OTHER'

def get_wordnet_pos(treebank_tag):
    """Function to translate TreeBank PoS tags into PoS tags that WordNet 
    understands."""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# ## Exceptions
class UnsupportedMIMETypeError(Exception):
    """An exception to be raised if an unsupported MIME type is encountered."""
    def __init__(self, doc_type):
        self.doc_type = doc_type
    
    def __str__(self):
        return repr(self.doc_type)
