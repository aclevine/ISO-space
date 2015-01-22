'''
Created on Dec 19, 2014

@author: Aaron Levine

functions for:
    -extracting features to be evaluated for each sub-task
    -calculating recall, precision, f1 and accuracy measures using 
        model.sk_classifier.py and model.evaluator.py
    -taking mean of recall, precision, f1 and accuracy for each sub-task
'''
from util.b_identify_types import *
from util.c_fill_tag_attrs import *
from util.d_fill_link_attrs import *

from util.model.demo import Classifier
import sys
import numpy as np

# classifier for SE.a task
class SpatialElementClassifier(Classifier):
    def __init__(self, test_path, gold_path):
        super(SpatialElementClassifier, self).__init__(train_path = '', test_path = test_path, 
                                                 gold_path = gold_path)
        self.indices_function = get_tag_and_no_tag_indices
        self.extent_class = Extent

    def get_label_function(self):
        return lambda x: str(bool(x.tag))

    def get_feature_functions(self):
        return []

# classifier for LINK.a tasks
def is_movelink_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^mvl\d+', tag_id))

def get_movelink_indices(sentence, tag_dict):
    get_tag_and_no_tag_indices(sentence, tag_dict, is_movelink_tag)


def is_olink_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^ol\d+', tag_id))

def get_olink_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_olink_tag)

def is_qslink_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^qsl\d+', tag_id))

def get_qslink_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_qslink_tag)

# helper variables
tag_types = ['PATH', 
             'PLACE', 
             'MOTION', 
             'NONMOTION_EVENT',
             'SPATIAL_ENTITY',
             ] 

def load_classifier(name):
    return lambda test_path, gold_path: TypesClassifier(type_name = name, 
                                                        train_path = '',
                                                        test_path = test_path, 
                                                        gold_path = gold_path)

se_b_demo_list = dict([(x, load_classifier(x)) for x in tag_types])

se_c_demo_list = {
                  'MOTION - motion_type': MotionTypeClassifier, 
                  'MOTION - motion_class': MotionClassClassifier, 
                  'MOTION - motion_sense': MotionSenseClassifier,
                 
                  'NONMOTION_EVENT - mod': EventModClassifier, 
                  'NONMOTION_EVENT - countable': EventCountableClassifier,
                 
                  'PATH - dimensionality': PathDimensionalityClassifier, 
                  'PATH - form': PathFormClassifier, 
                  'PATH - countable': PathCountableClassifier, 
                  'PATH - mod': PathModClassifier,
                  
                  'PLACE - dimensionality': PlaceDimensionalityClassifier, 
                  'PLACE - form': PlaceFormClassifier, 
                  'PLACE - countable': PlaceCountableClassifier, 
                  'PLACE - mod': PlaceModClassifier,
                  
                  'SPATIAL_ENTITY - dimensionality': EntityDimensionalityClassifier, 
                  'SPATIAL_ENTITY - form': EntityFormClassifier, 
                  'SPATIAL_ENTITY - countable': EntityCountableClassifier, 
                  'SPATIAL_ENTITY - mod': EntityModClassifier,
                 }

link_a_demo_list = {
                    # motion assures movelink
                    'MOVELINK': lambda test_path, gold_path: 
                                    TypesClassifier('MOTION', 
                                              train_path = '',
                                              test_path = test_path, 
                                              gold_path = gold_path), 
                    # TOP spatial signal assures qslink
                    'QSLINK': SignalTopologicalClassifier, 
                    # DIR spatial signal assures qslink                        
                    'OLINK': SignalDirectionalClassifier,
                    }

link_b_demo_list = {
                    'MOVELINK - source': MovelinkSourceExentsClassifier,
                    'MOVELINK - goal': MovelinkGoalExentsClassifier,
                    'MOVELINK - midPoint': MovelinkMidpointExentsClassifier,
                    'MOVELINK - landmark': MovelinkLandmarkClassifier,
                    'MOVELINK - motion': MovelinkLandmarkClassifier,
                    'MOVELINK - motion_signalID': MovelinkMotionSignalIDExentsClassifier,
                    'MOVELINK - pathID': MovelinkPathIDExentsClassifier,
                    'MOVELINK - goal_reached': MovelinkGoalReachedClassifier,
                     
                    'QSLINK - relType': QSLinkRelTypeClassifier,

                    'OLINK - referencePt': OLinkRefPtExtentClassifier,                    
                    'OLINK - relType': OLinkRelTypeClassifier,
                    'OLINK - projective': OLinkProjectiveClassifier,
                    'OLINK - frame_type': OLinkFrameTypeClassifier,
                    }


# helper functions
def evaluate_all(demo_list, hyp_path, gold_path):

    p = []
    r = []
    f = []
    a = []
    
    for tag_name, classifier in demo_list.iteritems():
        print '\n\n' + '=' * 10 + ' {} '.format(tag_name) + '=' * 10
        d = classifier(test_path = hyp_path, gold_path = gold_path)
        cm = d.evaluate()
        p.append(np.mean(cm.compute_precision()))
        r.append(np.mean(cm.compute_recall()))
        f.append(np.mean(cm.compute_f1()))
        a.append(np.mean(cm.compute_accuracy()))
    
    print '\n' * 2 + '=' * 10 + 'OVERALL' + '=' * 10 
    print 'mean precision: {}'.format(np.mean(p))
    print 'mean recall: {}'.format(np.mean(r))
    print 'mean f1: {}'.format(np.mean(f))
    print 'mean accuracy: {}'.format(np.mean(a))

def evaluate_links(hyp_path, gold_path):
    """ LINK.a task evaluations """
    p = []
    r = []
    f = []
    a = []
    
    print '\n' * 2 + '=' * 10 + 'MOVELINK' + '=' * 10 
    d = IsMovelinkClassifier(test_path = hyp_path, gold_path = gold_path)
    cm = d.evaluate_movelink()
    p.append(np.mean(cm.compute_precision()))
    r.append(np.mean(cm.compute_recall()))
    f.append(np.mean(cm.compute_f1()))
    a.append(np.mean(cm.compute_accuracy()))

    print '\n' * 2 + '=' * 10 + 'QSLINK' + '=' * 10 
    d = IsQSlinkClassifier(test_path = hyp_path, gold_path = gold_path)
    cm = d.evaluate_qs_o_link()
    p.append(np.mean(cm.compute_precision()))
    r.append(np.mean(cm.compute_recall()))
    f.append(np.mean(cm.compute_f1()))
    a.append(np.mean(cm.compute_accuracy()))
  
    print '\n' * 2 + '=' * 10 + 'OLINK' + '=' * 10 
    d = IsOlinkClassifier(test_path = hyp_path, gold_path = gold_path)
    cm = d.evaluate_qs_o_link()
    p.append(np.mean(cm.compute_precision()))
    r.append(np.mean(cm.compute_recall()))
    f.append(np.mean(cm.compute_f1()))
    a.append(np.mean(cm.compute_accuracy()))
     
    print '\n' * 2 + '=' * 10 + 'OVERALL' + '=' * 10 
    print 'mean precision: {}'.format(np.mean(p))
    print 'mean recall: {}'.format(np.mean(r))
    print 'mean f1: {}'.format(np.mean(f))
    print 'mean accuracy: {}'.format(np.mean(a))


def config_1_eval(hyp_1_a, hyp_1_b, hyp_1_c, hyp_1_d, hyp_1_e, gold_path, outpath):
    """calculate metrics for tasks 1a - 1e, print to text files"""
    # 1a
    with open(os.path.join(outpath, '1a.txt'), 'w') as fo:
        sys.stdout = fo
        print 'Identify spans of spatial elements including locations, paths, events and other spatial entities.'
        print '\n' * 2
        evaluate_all({'IS SPATIAL ELEMENT': SpatialElementClassifier}, hyp_1_a, gold_path)
    # 1b
    with open(os.path.join(outpath, '1b.txt'), 'w') as fo:
        sys.stdout = fo
        print 'Classify spatial elements according to type: PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY.'
        evaluate_all(se_b_demo_list, hyp_1_b, gold_path)
    # 1c
    with open(os.path.join(outpath, '1c.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_all(se_c_demo_list, hyp_1_c, gold_path)
    # 1d
    with open(os.path.join(outpath, '1d.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_links(hyp_1_d, gold_path)
    # 1e
    with open(os.path.join(outpath, '1e.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_all(link_b_demo_list, hyp_1_a, gold_path)


def config_2_eval(hyp_2_a, hyp_2_b, hyp_2_c, gold_path, outpath):
    """calculate metrics for tasks 2a - 2c, print to text files"""
    # 2a
    with open(os.path.join(outpath, '2a.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_all(se_c_demo_list, hyp_2_a, gold_path)
    # 2b
    with open(os.path.join(outpath, '2b.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_links(hyp_2_b, gold_path)
    # 2c
    with open(os.path.join(outpath, '2c.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_all(link_b_demo_list, hyp_2_c, gold_path)


def config_3_eval(hyp_3_a, hyp_3_b, gold_path, outpath):
    """calculate metrics for tasks 3a - 3b, print to text files"""
    # 3a
    with open(os.path.join(outpath, '3a.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_links(hyp_3_a, gold_path)
    # 3b
    with open(os.path.join(outpath, '3b.txt'), 'w') as fo:
        sys.stdout = fo
        evaluate_all(link_b_demo_list, hyp_3_b, gold_path)


# EVALUATE FROM SINGLE FINAL OUTPUT
def config_1_eval_single(hyp_path, gold_path, outpath):
    """calculate metrics for tasks 1a - 1e using single set of annotated files"""
    config_1_eval(hyp_path, hyp_path, hyp_path, hyp_path, hyp_path, gold_path, outpath)

def config_2_eval_single(hyp_path, gold_path, outpath):
    """calculate metrics for tasks 2a - 2c using single set of annotated files"""
    config_2_eval(hyp_path, hyp_path, hyp_path, gold_path, outpath)

def config_3_eval_single(hyp_path, gold_path, outpath):
    """calculate metrics for tasks 3a - 3b using single set of annotated files"""
    config_3_eval(hyp_path, hyp_path, gold_path, outpath)

if __name__ == "__main__":

    #TESTING
    hyp_path = '../data/task8_hrijp_crf_vw_system_submission'
    gold_path = '../data/gold'
    outpath = '../results/honda'
    
    config_1_eval_single(hyp_path, gold_path, outpath)