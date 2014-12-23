# -*- coding: utf-8 -*-

"""Utility functions for using Stanford NLP taggers.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"baseline_classifier/Corpora")))
cmd_subfolder = cmd_subfolder.replace('feature_engineering/stanford/taggers/util', '')
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
    
import numpy
import tokenizer

def get_tokens(text):
    """Uses ISO-Space Tokenizer to tokenize a string.

    """
    tk = tokenizer.Tokenizer(text)
    tk.tokenize_text()
    return [token[1][0][2] for token in tk.tokens]
    

