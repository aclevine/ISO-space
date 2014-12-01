# -*- coding: utf-8 -*-

"""Wrapper for calling David McDonald's CCL Sparser.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os, subprocess, sys, inspect

currdir = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
SPARSER = os.path.join(currdir, 'sparser')

def p(string, sparser_path=SPARSER):
    """Calls Sparser's p(arse) function on given string.

    This takes a string as an argument and calls Sparser's p function on it,
    which returns a pre-formatted string denoting the (semantic) labels
    assigned to each token/phrase in the sentence.  The output itself must
    be parsed on its own to match each word to its Sparser label.

    Note: Sparser crashes fairly often, since it is completely hand-written.
        Be sure to handle cases where the call crashes.

    Args:
        string: The natural language text to be parsed by Sparser.
        sparser_path: The path to the Sparser executable.

    Returns:
        out: The output of Sparser's p(arse) function.  Note: this formatted
        string needs to be parsed to get meaningful labels out of it.

    """
    process = subprocess.Popen([sparser_path, string], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out


