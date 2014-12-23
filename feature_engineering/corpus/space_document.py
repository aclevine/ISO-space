# -*- coding: utf-8 -*-

"""WRapper for an ISO-Space annotated document.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from collections import defaultdict
import xml.etree.ElementTree as ET

class Space_Document(object):
    """Wrapper for an ISO-Space annotated document.

    """
    def __init__(self, filepath=''):
        self.filepath = filepath
        self.root = ET.parse(filepath).getroot()
        self.text = self.root.find('TEXT').text
        self.ET_tags = self.root.find('TAGS')
        self.tags = [child for child in self.ET_tags if 'LINK' not in child.tag and 'start' in child.attrib]
        self.tags.sort(key=lambda x: int(x.attrib['start']))
        self.links = [child for child in self.ET_tags if 'LINK' in child.tag]
        self.sentences = [child for child in self.root.find('TOKENS')]
        self.lexes = [child.getchildren() for child in self.sentences]

    def get_linkdict(self):
        linkdict = {}
        
            
        
        

#t = Space_Document('/users/sethmachine/desktop/Tokenized/RFC/Amazon.xml')
