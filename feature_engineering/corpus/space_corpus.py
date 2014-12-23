# -*- coding: utf-8 -*-

"""WRapper for a corpus of ISO-Space documents.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os
import xml.etree.ElementTree as ET

from space_document import Space_Document

train = '/users/sethmachine/desktop/Train++'
test = '/users/sethmachine/desktop/Test++'

class Space_Corpus(object):
    """Wrapper for a corpus of ISO-Space annotated documents.

    Args:
        dirpath: An absolute filepath to the top level directory
            containing valid and annotated ISO-Space xmls.
        recursive: If True, the class will search all subdirectories
            exhaustively, collecting all ISO-Space xmls.

    Attributes:
        dirpath: An absolute filepath to the top level directory
            containing valid and annotated ISO-Space xmls.
        xmls: A list of the absolute filepaths of all ISO-Space xmls
            in the corpus.
        documents: A list of all ISO-Space documents in the corpus.
        
    """
    def __init__(self, dirpath='', recursive=True):
        self.dirpath = dirpath
        self.xmls = getXmls(dirpath)
        self.documents = (Space_Document(xml) for xml in self.xmls)

            
def getXmls(dirpath, recursive=True):
    files = []
    for f in os.listdir(dirpath):
        fpath = os.path.join(dirpath, f)
        if os.path.isfile(fpath):
            if f.endswith('.xml'):
                files.append(fpath)
        if recursive:
            if os.path.isdir(fpath):
                files += getXmls(fpath, recursive)
    return files
