# -*- coding: utf-8 -*-

"""Wrapper for Lex xml tag.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

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
        return attrs#.encode('utf-8')
        return ''.join(['<lex', attrs, '>', self.text, '</lex>']).encode('utf-8')
