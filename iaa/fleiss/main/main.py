# -*- coding: utf-8 -*-

"""Code to compute Fleiss' Kappa.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import os
import re

import algorithm as fl
import numpy
import table.tokens
import table.extents
import table.links

#turn this off to debug overflows/NaN
numpy.seterr(all='ignore')

#row types
TOKEN = 0
EXTENT = 1
LINK = 2
#token spans
START = 0
END = 1

#path to folder containing all xmls to be adjudicated
ADJUDICATED_PATH = '/users/sethmachine/desktop/Adjudication'
TEST_PATH = '/users/sethmachine/desktop/Adjudication/47_N_27_E'

#regex to collect only certain xml/dir names
dir_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+', re.IGNORECASE)
xml_pattern = re.compile(r'[0-9]+_[a-z]+_[0-9]+_[a-z]+\-[a-z][0-9]+\-p[0-9]+\.xml', re.IGNORECASE)

def getTable(xmls, tableType=TOKEN, unmatch=True, linkType='METALINK'):
    """Returns a Table used to compute Fleiss' Kappa.

    This function returns a Table object based on the tableType argument.

    Args:
        xmls: A list of paths to annotated xmls for the same task.
        tableType: What we are scoring for agreement:
            tokens, extents, or links.
        unmatch: Whether to consider only exact matches for extents.
        linkType: The link type we are checking IAA for.

    Returns:
        A Table object used to compute Fleiss' Kappa.

    """
    if tableType == TOKEN:
        f = table.tokens.Table(xmls)
    elif tableType == EXTENT:
        f = table.extents.Table(xmls, unmatch=unmatch)
    elif tableType == LINK:
        f = table.links.Table(xmls, linkType=linkType)
    f.build_rows()
    f.build_table()
    return f
        
def getXmls(path, phase='p2'):
    """Finds all xml files in a flat directory.

    Collects all xml files which match the xml_pattern.
    The pattern excludes files with suffixes like "extentsLocked."

    Args:
        path: A string absolute path for the directory.
        phase: A suffix on the xml file name used to discriminate
            between tag annotation and link annotation.

    Returns:
        A list of all xml files matching xml_pattern.
    """
    files = []
    phase_pattern = re.compile(phase + '\.xml$')
    for f in os.listdir(path):
        fpath = os.path.join(path, f)
        if phase_pattern.search(f):
            files.append(fpath)
    return files

def getXmlDict(path, d={}, dname='', phase='p2'):
    """Finds all xml files recursively in a directory, storing them in a dictionary.

    Searches recursively from the top directory for all xml files.
    For each directory that it passes, a dictionary entry is made
    which maps that directory name to all the xmls found in it.

    Args:
        path: A string absolute path for the directory.
        d: A dictionary object (ignore this argument).
        dname: A dictionary key (ignore this argument).
        phase: A suffix on the xml file name used to discriminate
            between tag annotation and link annotation.

    Returns:
        A dictionary mapping each directory name to a list of xmls inside it.
    """
    phase_pattern = re.compile(phase + '\.xml$')
    if dname:
        d[dname] = []
    for f in os.listdir(path):
        fpath = os.path.join(path, f)
        if os.path.isfile(fpath):
            if phase_pattern.search(f):
                d[dname].append(fpath)
        elif os.path.isdir(fpath): #and dir_pattern.match(f):
            d = dict(d.items() + getXmlDict(fpath, d, f, phase).items())
    return {x:d[x] for x in d.keys() if d[x] and len(d[x]) > 1}

def fleiss(xmls, unmatch=True, rowType=TOKEN, linkType='QSLINK'):
    """Computes Fleiss' Kappa between lists of xmls.

    Calculates Fleiss' Kappa given a list of xmls.  If xmls
    is a dictionary, Fleiss' Kappa is computed for each key.
    Otherwise, a single Fleiss' Kappa is computed.

    Args:
        xmls: A list of xmls for a single task or a dictionary
        where each key is a different task.

    Returns:
        If xmls is a dictionary:
            A dictionary mapping each task to its Fleiss' Kappa score.
        Else:
            Fleiss' Kappa score for the single task.
    """
    useLinks = False
    if rowType == LINK:
        useLinks = True
    if type(xmls) == dict:
        #w = open('/users/sethmachine/desktop/lenn.txt', 'w')
        #u = open('/users/sethmachine/desktop/len2.txt', 'w')
        coord = '\\addplot[color=red,mark=x] coordinates{'
        data = []
        s = '['
        z = '['
        fleiss_scores = {}
        #tags.sort(key=lambda x: int(x.attrib['start']))
        for key in xmls.keys():
            try: #crashes if a table doesn't have any instances of a linkType
                table = getTable(xmls[key], rowType, unmatch, linkType)
                s += str(table.docLen) + ', '
                score = fl.fleiss_wikpedia(table.table)
                #why getting NaN on MOVELINK
                #if numpy.isnan(score):
                    #score = 1.0
                z += str(score) + ', '
                fleiss_scores[key] = score
                data.append((table.docLen, score))
            except:
                pass
        s += ']'
        z += ']'
        #print>>w, s
        #print>>w, z
        data.sort(key=lambda x: x[0])
        for (x,y) in data:
            coord += '(' + str(x) + ',' + str(y) + ')'
        coord += '};'
        #print>>u, coord
        #w.close()
        #u.close()
        return fleiss_scores
    table = getTable(xmls, rowType, unmatch, linkType)
    score = fl.fleiss_wikpedia(table.table)
    #why is this failing for links but not tokens on GuerroNegro?
    if numpy.isnan(score):
        score = 1.0
    return score

def print_fleiss(scores):
    """Prints Fleiss' Kappa scores for each task.

    Use this to print the scores for Fleiss' Kappa.
    This will also compute the average kappa for a given set of tasks.

    Args:
        scores: A dictionary of xml keys to Fleiss' Kappas
            or simply Fleiss' Kappa for a single task.

    Returns:
        None.  Use this to get output for command line script.

    """
    if isinstance(scores, dict):
        avg = 0.0
        for key in scores.keys():
            avg += scores[key]
            print key + ": " + str(scores[key])
        print "Average: " + str((avg / len(scores.keys())))
    else:
        print scores


#w = '/users/sethmachine/desktop/g'
#xmls = getXmls(w, phase='p4')
#t = fleiss(xmls, rowType=LINK, linkType = 'OLINK')
#d = t._get_linkdict()
