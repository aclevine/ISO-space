# -*- coding: utf-8 -*-

"""Module for statistics on QSLINKs.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

from nltk import FreqDist, ConditionalFreqDist

from space_corpus import train_corpus, training
import space_document
from qslink import *


#these are unattested (figure, ground) configurations for QSLINKs
#these have 0 counts, and mostly involve NONMOTION_EVENTs (e) being a ground
unattested = [('m', 'e'), ('p', 'e'), ('pl', 'e'), ('pl', 'm'), ('p', 'm')]

#these are very rare (figure, ground) configurations for QSLINKs
#these have counts of 4 or less over the whole training corpus
#most have counts of 1
rare = [('m', 'p'), ('e', 'm'), ('m', 'se'), ('se', 'm'),
        ('m', 'm'), ('e', 'e'), ('se', 'e'), ('p', 'se')]

id_pattern = re.compile(r'[0-9]+')

def get_type(ID):
	return id_pattern.sub('', ID)

def positive_instances(training):
    """Returns all instances which are positive (i.e. a QSLINK).

    """
    LABEL = 0
    return [instance for instance in training if instance[LABEL] != False]

def link_type_pairs(instances, singletons=False, types=False):
    FIGURE = 2
    GROUND = 3
    pairs = [(('figure', get_type(instance[FIGURE].attrib['id'])),
              ('ground', get_type(instance[GROUND].attrib['id'])))
             for instance in instances]
    if singletons:
        return [pair[0][-1] + ':' + pair[1][-1]
                for pair in pairs]
    if types:
        return [(pair[0][-1], pair[1][-1])
                for pair in pairs]        
    return pairs

def link_types(instances):
    pairs = link_type_pairs(instances)
    return [instance for pair in pairs for instance in pair]
        
def filter_configurations(training, illegals=unattested):
    """Filters out (figure, ground) configurations from training pairs.

    Filters out (figure, ground) configurations in the illegals list.
    Each configuration comes of the form (type1, type2), where type1, type2
    are ISO-Space tag types.  The training set consists of all possible
    (figure, ground) configurations for each trigger (=spatial signal) in
    a given sentence.  Use this function to eliminate unattested or very rare
    combinations, which can significantly reduce the training space.

    Args:
        training: A list of training instances for creating QSLINKs.
            Each instance is a 4-tuple of the form
            (label, trigger, figure, ground).
        illegals: A list of type configurations to prune from the training
            instances.  Each element is of the form (type1, type2),
            where each type is a string denoting that ISO-Space tag type.

    Returns:
        A list of all training sequences whose (figure, ground) configurations
        exclude those in illegals.
        
    """
    filt = []
    for link in training:
        is_match = True
        for (figure, ground) in illegals:
            figure_type = get_type(link[2].attrib['id'])
            ground_type = get_type(link[3].attrib['id'])
            if figure_type == figure and ground_type == ground:
                is_match = False
                break
        if is_match:
            filt.append(link)
    return filt

def link_distances(docs):
    """Returns a list of (figure, ground) distances from their trigger.

    Returns a list of the distances each figure, ground in an attested
    QSLINK are from their trigger.  The distance is calculated linearly,
    including only those instances in a sentence which are ISO-Space tags.
    
    A negative value means the spatial argument occurs after the trigger,
    whereas a positive value means the spatial argument occurs before the
    trigger.

    Args:
        docs: A list of Space_Document objects.

    Returns:
        A list of 4-tuples, where each 4-tuple is of the form
        (sentence, link, (toDist, value1), (fromDist, value2)), where toDist
        denotes the ground's distance from the trigger, and likewise
        fromDist denotes the figure's distance from the trigger.
        sentence is the ElementTree element representation of the sentence
        where the QSLINK is found, and QSLINK is likewise the ElementTree
        Element representation of the actual QSLINK.

    """
    distances = []
    for doc in docs:
        #grab only links which have figures, grounds, triggers
        #that aren't non-consuming or null
        links = [link for link in doc.linkdict['QSLINK']
                 if link.attrib['fromText'] and link.attrib['toText']
                 and link.attrib['trigger']]
        for sent in doc.sents:
            distances += space_document.link_dist(sent, links)
    return distances

def link_distance_pairs(docs, singletons=False, types=False):
    distances = link_distances(docs)
    pairs = [(x[-2], x[-1]) for x in distances]
    if singletons:
        return [str(pair[0][-1]) + ':' + str(pair[1][-1])
                for pair in pairs]
    if types:
        return [('to=' + str(pair[0][-1]), 'from=' + str(pair[1][-1]))
                for pair in pairs] 
    return pairs

def pair_deobsfucate(pair):
    """Deobsfucates a (type, value) pair.

    """
    tag_type = pair[0]
    if tag_type == 'toDist':
        tag_type = 'ground'
    elif tag_type == 'fromDist':
        tag_type = 'figure'
    return (tag_type, pair[-1])
    

def link_distance_singletons(docs):
    pairs = link_distance_pairs(docs)
    return [pair_deobsfucate(child) for pair in pairs for child in pair]

#these are unattested ground distances
#a negative number means that many tags past the spatial signal
#a positive number means that many tags before the spatial signal
ground_dist_unattested = [x for x in xrange(-9,-3)] + [7]


d = link_distance_pairs(train_corpus.documents, types=True)
t = link_distance_singletons(train_corpus.documents)
positives = positive_instances(training)
l = link_type_pairs(positives, singletons=False, types=True)
w = link_type_pairs(positives, singletons=True, types=False)
r = link_types(positives)
    
