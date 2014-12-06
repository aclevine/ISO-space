__author__ = "Zachary Yocum"
__email__  = "zyocum@brandeis.edu"

import os
from warnings import warn
from bs4 import BeautifulSoup as BS, CData
from bs4.element import Tag

dummy_tag = Tag(name='NULL')

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
        self.prev_tags = [
            tag_dict.get(l.begin, {}) for t, l in self.prev_tokens 
            if l.begin in tag_dict.keys()
        ]
        self.next_tags = [
            tag_dict.get(l.begin, {}) for t, l in self.next_tokens 
            if l.begin in tag_dict.keys()
        ]

class Document(BS):
    """A class for working with MAE annotation XMLs."""
    def __init__(self, doc_file):
        super(Document, self).__init__(doc_file.read(), "xml")
        from tokenizer import Tokenizer
        self.root = self.children.next()
        self.task = self.root.name
        self.name = doc_file.name
        self.basename = os.path.basename(self.name)
        self.dirname = os.path.dirname(self.name)
        self.tokenizer = Tokenizer(self.text())
        self.tokenizer.tokenize_text()
    
    def __repr__(self):
        return "Document:{d}".format(d=os.path.basename(self.name))
    
    def text(self):
        return u''.join(map(lambda t : t.decode_contents(), self('TEXT')))
    
    def tags(self, ttypes=None):
        """Return all annotation tags whose type is in ttypes (if ttypes is unspecified, all tags are returned)."""
        is_tag = lambda item : isinstance(item, Tag)
        tags = filter(is_tag, self.find('TAGS').children)
        if ttypes:
            tags = filter(lambda tag : tag.name in ttypes, tags)
        return tags
    
    def add_attribute(self, attribute, value=u'', ttypes=None):
        """Add an attribute to a tag (and possibly specify it's value)."""
        for tag in self.tags(ttypes):
            if not attribute in tag.attrs.keys():
                tag[attribute] = value
    
    def rename_attribute(self, old_ttype, new_ttype, ttypes=None):
        """Change the name of attributes for all tags with the given ttypes."""
        for tag in self.tags(ttypes):
            if tag.attrs.get(old_ttype):
                tag.attrs[new_ttype] = tag.attrs.pop(old_ttype)
    
    def rename_tag(self, old_ttype, new_ttype):
        """Rename a tag."""
        for tag in self.tags([old_ttype]):
            tag.name = new_ttype
    
    def rename_task(self, new_task):
        """Rename the document task (the XML root tag type)."""
        self.task = new_task
    
    def consuming_tags(self):
        """Return extent annotation tags with non-negative starting offsets."""
        is_extent_tag = lambda t : t.attrs.has_key('start')
        is_consuming = lambda t : int(t['start']) >= 0
        return filter(is_consuming, filter(is_extent_tag, self.tags()))

    def sort_tags_by_begin_offset(self):
        """Make dictionary of tag objects keyed on their 'start' field.
        
        Used for matching tags to tokens using offsets"""
        tag_dict = {}
        tags = self.tags()
        for t in tags:
            # load entity / event / signal tags
            if 'start' in t.attrs:
                # { start offset: xml tokens, offsets, spatial data }
                tag_dict[int(t['start'])] = t.attrs
            # load movelink tags
            if 'trigger' in t.attrs:
                tag_dict[t['trigger']] = t.attrs
            # load qslinks
            # load olinks
        return tag_dict

    def extents(self, indices_function, extent_class=Extent):
        tag_dict = self.sort_tags_by_begin_offset()
        for s in self.tokenizer.tokenize_text().sentences:
            # [ (token, lexeme obj), (token, lexeme obj), ... ]
            sent = s.as_pairs()
            offsets = indices_function(sent, tag_dict)
            for begin, end in offsets:
                extent = extent_class(sent, tag_dict, begin, end)
                yield extent
    
    def validate(self):
        is_valid = True
        tag_count = len(self.tags())
        if not (tag_count > 0):
            is_valid = False
            warning = '\n'.join([
                'No tag elements found',
                "\tFile : '{doc}'"
            ]).format(doc=self.name)
            warn(warning, RuntimeWarning)
        for tag in self.consuming_tags():
            start, end = int(tag['start']), int(tag['end'])
            extent = slice(start, end)
            text_attribute = tag['text'].encode('utf-8')
            text_slice = self.text()[extent].encode('utf-8').replace('\n', ' ')
            if text_attribute != text_slice:
                is_valid = False
                warning = '\n'.join([
                    'Misaligned extent tag',
                    "\tFile : '{doc}'"
                    '\tSpan  : [{start}:{end}]',
                    "\tTag   : '{id}'",
                    "\tText  : '{text}'",
                    "\tSlice : '{slice}'"
                ]).format(
                    doc=self.name,
                    start=start,
                    end=end,
                    id=tag['id'],
                    text=text_attribute,
                    slice=text_slice
                )
                warn(warning, RuntimeWarning)
        return is_valid
    
    def get_xml(self):
        xml = u'<?xml version="1.0" encoding="UTF-8" ?>\n'
        root = Tag(name=self.task)
        text = Tag(name='TEXT')
        text.append(CData(self.text()))
        tags = self.TAGS
        tokens = (BS(
            self.tokenizer.get_tokenized_as_xml().encode('utf-8'), 
            'xml'
        )).TOKENS
        elements = [u'\n', text, u'\n', tags, u'\n', tokens, u'\n']
        for element in elements:
            root.append(element)
        xml += unicode(root)
        return xml
    
    def save_xml(self, file):
        if isinstance(file, basestring):
            with open(file, 'wb') as file:
                file.write(self.get_xml().encode('utf-8'))
        else:
            file.write(self.get_xml().encode('utf-8'))

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
