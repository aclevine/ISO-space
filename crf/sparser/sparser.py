# -*- coding: utf-8 -*-

"""Wrapper for calling David McDonald's CCL Sparser.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os, subprocess, sys, inspect
import re

currdir = os.path.split(inspect.getfile( inspect.currentframe() ))[0]
SPARSER = os.path.join(currdir, 'sparser')

test = "Biking south from Salta, green forest eventually gave away to desert landscape, and I again found myself biking long stretches of desert between small towns."

#gets all the sparser edges from a formatted string
edges_pattern = re.compile(r'e[0-9]+[^\n]+', re.DOTALL)
#parse each edge into its attributes
edge_value_pattern = re.compile(r'(?P<edge>(e[0-9]+ )+) +(?P<label1>[^" ]*)[^"]+"(?P<word>[^"]+)"(?P<colon> :: )?(?P<label2>[^\n]{3,})?')

edge_number_pattern = re.compile(r'#<edge(?P<num>[0-9]+)')
edge_keyvalue_pattern = re.compile(r'(?P<key>[^:\n]+): (?P<value>[^\n]+)')
arrows_pattern = re.compile(r'[<>]')
b = re.compile(r'BEGIN-EDGES')

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
        The output of Sparser's p(arse) function.  Note: this formatted
        string needs to be parsed to get meaningful labels out of it.

    """
    process = subprocess.Popen([sparser_path, string], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out

class Edge(object):
    """Wrapper for a Sparser edge.

    Args:
        edgeStr: The formatted string representation of the edge.

    Attributes:
        edgeStr: The formatted string representation of the edge.
        edges: A list of strings denoting the Sparser edges of this object.
        label1: The primary Sparser semantic label for the edge.  Note that
            this will be empty if the edge is ambiguous (=2 or more labels).
        word: The string token/phrase of the edge.
        label2: The Sparser semantic labels assigned to the edge if it
            is ambiguous (=2 or more labels).
            
    """
    def __init__(self, edgeStr):
        m = edge_value_pattern.search(edgeStr)
        self.edgeStr = edgeStr
        self.edges = [x for x in m.group('edge').split(' ') if x]
        self.label1 = m.group('label1')
        self.word = m.group('word')
        self.label2 = m.group('label2')
        self.edgeDict = {x.replace('e', ''):[] for x in self.edges}
        self.keyvalues = {}
        

    def __repr__(self):
        return self.edgeStr

def split_edge(edge):
    """Splits an edge into n edges.

    """
    words = edge.word.split(' ')
    if len(words) > 1:
        new_edges = []
        #note that the edgeStrs will be the same!
        #but the actually `word` attribute will be different
        for word in words:
            e = Edge(edge.edgeStr)
            e.word = word
            #e.edgeStr = word
            e.keyvalues = edge.keyvalues
            new_edges.append(e)
        return new_edges
    return None
            
        

vill_pattern = re.compile(r'(the )?(village|town) of')
comm_pattern = re.compile(r'(?P<l>[0-9]+),(?P<r>[0-9]+)')

def p2edges(string, sparser_path=SPARSER, split=False):
    """Wrapper around p(arse) to get actual edges output.

    This function calls Sparser's p(arse) function on a string,
    then parses the output in order to turn it into an Edge object,
    which is a wrapper around the values given from the Sparser edge.

    Args:
        string: The natural language text to be parsed by Sparser.
        sparser_path: The path to the Sparser executable.

    Returns:
        A list of Edge objects, each representing a Sparser edge and
        its corresponding values.

    """
    string = string.replace('the options that I or my', 'the options that or my')
    string = string.replace('$ " ', '') 
    string = string.replace('two ( ', 'two ')
    string = vill_pattern.sub('the city of', string)
    string = comm_pattern.sub('\g<l>.\g<r>', string) #handle european format
    #string = string.replace('a 3,5 hour wait', 'a 3 hour wait')
    out = p(string, sparser_path)
    if not b.search(out):
        return None
    (parse, edges) = p(string, sparser_path).split('BEGIN-EDGES')
    edges = edges.split('BEGIN-EDGE')[:-1]
    edges = [(edge_number_pattern.findall(e)[0], edge_keyvalue_pattern.findall(e)) for e in edges]
    edgesStr = edges_pattern.findall(parse)
    real_edges = []
    for edgeStr in edgesStr:
        new_edge = Edge(edgeStr)
        edge_keyvalues = {}
        cached = None
        for e in new_edge.edgeDict:
            for i in xrange(0, len(edges)):
                #print edges[i][0], e
                if edges[i][0] == e:
                    edge_keyvalues = {x[0]:arrows_pattern.sub('', x[1]) for x in edges[i][1]}
                    new_edge.keyvalues[e] = edge_keyvalues
                    cached = edges[i]
                    break
            if cached:
                edges.remove(cached)
        real_edges.append(new_edge)
    if split:
        l = []
        for x in real_edges:
            s = split_edge(x)
            if s:
                l += [y for y in s]
            else:
                l.append(x)
        return l
        #return [e for edges in real_edges for e in split_edge(edges)]
    return real_edges


#test case:
#print p(test)
