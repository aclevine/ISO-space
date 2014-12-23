# -*- coding: utf-8 -*-

"""Wrapper for S(entence) xml tag.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from lex import Lex

class Sentence(object):
    """Wrapper around a S(entence) ElementTree Element.

    """
    def __init__(self):
        self.lexes = []

    def add(self, lex):
        self.lexes.append(lex)

    def __repr__(self):
        lexStr = ''.join(['\t' + str(lex) + '\n' for (i, lex) in enumerate(self.lexes)])
        return ''.join(['<s>\n', lexStr, '</s>'])
