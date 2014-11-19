__author__ = "Zachary Yocum"
__email__  = "zyocum@brandeis.edu"

import os
from warnings import warn
import bs4
from bs4 import BeautifulSoup

dummy_tag = bs4.element.Tag(name='NULL')

# Classes
class Extent(object):
    """A class for loading tagged data from XML doc 
    with surrounding token and tag data"""
    def __init__(self, sent, tag_dict, front, back):
        self.token = [t for t, l in sent[front:back]]
        self.lex = [l for t, l in sent[front:back]]
        self.prev_tokens = sent[:front]
        self.next_tokens = sent [back:] 
        self.tag = tag_dict.get(self.lex[0].begin, {})
        self.prev_tags = [tag_dict.get(l.begin, {}) for t, l in self.prev_tokens 
                     if l.begin in tag_dict.keys()]
        self.next_tags = [tag_dict.get(l.begin, {}) for t, l in self.next_tokens 
                     if l.begin in tag_dict.keys()]

class Document(BeautifulSoup):
    """A class for working with MAE annotation XMLs."""
    def __init__(self, doc_file):
        super(Document, self).__init__(doc_file.read(), "xml")
        from tokenizer import Tokenizer
        self.name = doc_file.name
        self.basename = os.path.basename(self.name)
        self.dirname = os.path.dirname(self.name)
        self.tokenizer = Tokenizer(self.text())
        self.tokenizer.tokenize_text()
    
    def __repr__(self):
        return "Document:{d}".format(d=os.path.basename(self.name))
    
    def root(self):
        return self.children.next()
    
    def task(self):
        return self.root().name
    
    def text(self):
        return u''.join(self.find('TEXT').contents)
    
    def tags(self, ttypes=None):
        from bs4.element import Tag
        is_tag = lambda item : isinstance(item, Tag)
        tags = filter(is_tag, self.find('TAGS').children)
        if ttypes:
            tags = filter(lambda tag : tag.name in ttypes, tags)
        return tags
        
    def consuming_tags(self):
        is_extent_tag = lambda t : t.attrs.has_key('start')
        is_consuming = lambda t : int(t.attrs['start']) >= 0
        return filter(is_consuming, filter(is_extent_tag, self.tags()))

    def sort_tags_by_begin_offset(self):
        """Make dictionary of tag objects keyed on their 'start' field.
        
        Used for matching tags to tokens using offsets"""
        tag_dict = {}
        tags = self.tags()
        for t in tags:
            # load entity / event / signal tags
            if 'start' in t.attrs:
                tag_dict[int(t.attrs['start'])] = t.attrs # {start offset: xml tokens, offsets, spatial data}    
            # load movelink tags
            if 'trigger' in t.attrs:
                tag_dict[t.attrs['trigger']] = t.attrs
            # load qslinks
            # load olinks
        return tag_dict

    def extents(self, indices_function, extent_class=Extent):
        tag_dict = self.sort_tags_by_begin_offset()
        for s in self.tokenizer.tokenize_text().sentences:
            sent = s.as_pairs() # [ (token, lexeme obj), (token, lexeme obj), ...]
            offsets = indices_function(sent, tag_dict)
            for begin, end in offsets:
                extent = extent_class(sent, tag_dict, begin, end)
                yield extent
    
    def validate(self):
        is_valid = True
        tag_count = len(self.tags())
        if tag_count <= 0:
            is_valid = False
            warning = '\n\t'.join(['No tag elements found', "File : '{doc}'"])
            warn(warning, RuntimeWarning)
        for tag in self.consuming_tags():
            start, end = int(tag.attrs['start']), int(tag.attrs['end'])
            extent = slice(start, end)
            text_attribute = tag.attrs['text'].encode('utf-8')
            text_slice = self.text()[extent].encode('utf-8').replace('\n', ' ')
            if text_attribute != text_slice:
                is_valid = False
                warning = 'Misaligned extent tag' + '\n\t'.join([
                    "File : '{doc}'"
                    'Span  : [{start}:{end}]',
                    "Tag   : '{id}'",
                    "Text  : '{text}'",
                    "Slice : '{slice}'"
                ]).format(
                    doc=self.name,
                    start=start,
                    end=end,
                    id=tag.attrs['id'],
                    text=text_attribute,
                    slice=text_slice
                )
                warn(warning, RuntimeWarning)
        return is_valid
    
    def make_xml(self):
        # XML tag elements
        header_tag = '<?xml version="1.0" encoding="UTF-8" ?>'
        root_tag = '<' + self.task() + '>'
        text_tag = '<TEXT>'
        tags_tag = '<TAGS>'
        text_content = '<![CDATA[' + self.text().encode('utf-8') + ']]>'
        tags_content = '\n'.join(
            [tag.encode('utf-8') for tag in self.tags()]
        )
        # Make the XML DOM tree by joining all the tag elements
        return '\n'.join(
            [
                header_tag,
                wrap(
                    root_tag,
                    '\n'.join(
                        [
                            wrap(text_tag, text_content, sep=''),
                            wrap(tags_tag, tags_content),
                            self.tokenizer.get_tokenized_as_xml().encode('utf-8')
                        ]
                    )
                )
            ]
        )

class Corpus(object):
    """A class for working with collections of Documents."""
    def __init__(self, directory, pattern='.*\.xml', recursive=True):
        super(Corpus, self).__init__()
        self.directory = directory
        self.pattern = pattern
        self.recursive = recursive
        self.validate()
    
    def documents(self):
        candidates = find_files(self.directory, self.pattern, self.recursive)
        for xml_path in filter(is_xml, candidates):
            with open(xml_path, 'r') as file:
                yield Document(file)
    
    def extents(self, indices_function, extent_class=Extent):
        for doc in self.documents():
            tag_dict = doc.sort_tags_by_begin_offset()
            for s in doc.tokenizer.tokenize_text().sentences:
                sent = s.as_pairs() # [ (token, lexeme obj), (token, lexeme obj), ...]
                offsets = indices_function(sent, tag_dict)
                for begin, end in offsets:
                    extent = extent_class(sent, tag_dict, begin, end)
                    yield extent

              
    def validate(self):
        map(Document.validate, self.documents())

# Helper functions for generating XML
def wrap(tag, content, sep='\n'):
    return sep.join([tag, content, close_tag(tag)])

def close_tag(tag):
    return tag.replace('<', '</', 1)

# General functions
def validate_mime_type(file_path, valid_mime_types):
    from mimetypes import guess_type
    mime_type, encoding = guess_type(file_path)
    valid = mime_type in valid_mime_types
    if not valid:
        warning = '\n\t'.join([
            'Invalid MIME type',
            'File : {path}',
            'Type : {type}'
        ])
        warn(warning.format(path=file_path, type=mime_type), RuntimeWarning)
    return valid

def is_xml(file_path):
    return validate_mime_type(file_path, set(['application/xml', 'text/xml']))

def find_files(directory='.', pattern='.*', recursive=True):
    import re
    if recursive:
        return (os.path.join(directory, filename)
            for directory, subdirectories, filenames in os.walk(directory)
            for filename in filenames if re.match(pattern, filename))
    else:
        return (os.path.join(directory, filename)
            for filename in os.listdir(directory)
            if re.match(pattern, filename))
