'''
Created on Dec 19, 2014

@author: Aaron Levine
'''
from b_identify_types import *
from c_fill_tag_attrs import *
from d_fill_link_attrs import *

from util.demo import Demo
import sys
import numpy as np


# DEMO for SE.a task
class SpatialElementDemo(Demo):
    def __init__(self, test_path, gold_path):
        super(SpatialElementDemo, self).__init__(train_path = '', test_path = test_path, 
                                                 gold_path = gold_path)
        self.indices_function = get_tag_and_no_tag_indices
        self.extent_class = Extent

    def get_label_function(self):
        return lambda x: str(bool(x.tag))

    def get_feature_functions(self):
        return []

# demo for LINK.a tasks
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
tag_types = ['PATH', 'PLACE', 
             'MOTION', 'NONMOTION_EVENT',
             'SPATIAL_ENTITY'] 

se_b_demo_list = dict([(name, 
                        lambda test_path, 
                            gold_path: TypesDemo(name, 
                                                 train_path = '',
                                                 test_path = test_path, 
                                                 gold_path = gold_path)) 
                        for name in tag_types])

se_c_demo_list = {
                  'MOTION - motion_type': MotionTypeDemo, 
                  'MOTION - motion_class': MotionClassDemo, 
                  'MOTION - motion_sense': MotionSenseDemo,
                 
                  'NONMOTION_EVENT - mod': EventModDemo, 
                  'NONMOTION_EVENT - countable': EventCountableDemo,
                 
                  'PATH - dimensionality': PathDimensionalityDemo, 
                  'PATH - form': PathFormDemo, 
                  'PATH - countable': PathCountableDemo, 
                  'PATH - mod': PathModDemo,
                  
                  'PLACE - dimensionality': PlaceDimensionalityDemo, 
                  'PLACE - form': PlaceFormDemo, 
                  'PLACE - countable': PlaceCountableDemo, 
                  'PLACE - mod': PlaceModDemo,
                  
                  'SPATIAL_ENTITY - dimensionality': EntityDimensionalityDemo, 
                  'SPATIAL_ENTITY - form': EntityFormDemo, 
                  'SPATIAL_ENTITY - countable': EntityCountableDemo, 
                  'SPATIAL_ENTITY - mod': EntityModDemo,
                 }

link_a_demo_list = {
                    # motion assures movelink
                    'MOVELINK': lambda test_path, gold_path: 
                                    TypesDemo('MOTION', 
                                              train_path = '',
                                              test_path = test_path, 
                                              gold_path = gold_path), 
                    # TOP spatial signal assures qslink
                    'QSLINK': SignalTopologicalDemo, 
                    # DIR spatial signal assures qslink                        
                    'OLINK': SignalDirectionalDemo,
                    }

link_b_demo_list = {
                    'MOVELINK - source': MovelinkSourceExentsDemo,
                    'MOVELINK - goal': MovelinkGoalExentsDemo,
                    'MOVELINK - midPoint': MovelinkMidpointExentsDemo,
                    'MOVELINK - landmark': MovelinkLandmarkDemo,
                    'MOVELINK - motion': MovelinkLandmarkDemo,
                    'MOVELINK - motion_signalID': MovelinkMotionSignalIDExentsDemo,
                    'MOVELINK - pathID': MovelinkPathIDExentsDemo,
                    'MOVELINK - goal_reached': MovelinkGoalReachedDemo,
                     
                    'QSLINK - relType': QSLinkRelTypeDemo,

                    'OLINK - referencePt': OLinkRefPtExtentDemo,                    
                    'OLINK - relType': OLinkRelTypeDemo,
                    'OLINK - projective': OLinkProjectiveDemo,
                    'OLINK - frame_type': OLinkFrameTypeDemo,
                    }

# helper functions
def evaluate_all(demo_list, hyp_path, gold_path):

    p = []
    r = []
    f = []
    a = []
    
    for tag_name, Demo in demo_list.iteritems():
        print '\n\n' + '=' * 10 + ' {} '.format(tag_name) + '=' * 10
        d = Demo(test_path = hyp_path, gold_path = gold_path)
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

def config_1_eval(hyp_1_a, hyp_1_b, hyp_1_c, hyp_1_d, hyp_1_e, gold_path, outpath):
    # 1a
    sys.stdout = open(os.path.join(outpath, '1a.txt'), 'w')
    print 'Identify spans of spatial elements including locations, paths, events and other spatial entities.'
    print '\n' * 2
    print '=' * 10 + ' IS SPATIAL ELEMENT: ' + '=' * 10
    test = SpatialElementDemo(test_path = hyp_1_a, gold_path = gold_path)
    test.evaluate()
 
    # 1b
    sys.stdout = open(os.path.join(outpath, '1b.txt', 'w'))
    print 'Classify spatial elements according to type: PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY.'
    evaluate_all(se_b_demo_list, hyp_1_b, gold_path)
  
    # 1c
    sys.stdout = open(os.path.join(outpath, '1c.txt', 'w'))
    evaluate_all(se_c_demo_list, hyp_1_c, gold_path)
     
    # 1d
    p = []
    r = []
    f = []
    a = []

    sys.stdout = open(os.path.join(outpath, '1d.txt', 'w'))
    print '=' * 10 + 'MOVELINK' + '=' * 10 
    d = IsMovelinkDemo(test_path = hyp_1_d, gold_path = gold_path)
    cm = d.evaluate_movelink()
    p.append(np.mean(cm.compute_precision()))
    r.append(np.mean(cm.compute_recall()))
    f.append(np.mean(cm.compute_f1()))
    a.append(np.mean(cm.compute_accuracy()))

    print '=' * 10 + 'QSLINK' + '=' * 10 
    d = IsOlinkDemo(test_path = hyp_1_d, gold_path = gold_path)
    cm = d.evaluate_qs_o_link()
    p.append(np.mean(cm.compute_precision()))
    r.append(np.mean(cm.compute_recall()))
    f.append(np.mean(cm.compute_f1()))
    a.append(np.mean(cm.compute_accuracy()))
 
    print '=' * 10 + 'OLINK' + '=' * 10 
    d = IsQSlinkDemo(test_path = hyp_1_d, gold_path = gold_path)
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

    # 1e
    sys.stdout = open(os.path.join(outpath, '1e.txt', 'w'))
    evaluate_all(link_b_demo_list, hyp_1_a, gold_path)


if __name__ == "__main__":

    gold_path = './data/final/gold'

    # CONIFG 1
    hyp_1_a = './data/final/test/configuration1/a'
    hyp_1_b = './data/final/test/configuration1/b'
    hyp_1_c = './data/final/test/configuration1/c'
    hyp_1_d = './data/final/test/configuration1/d'
    hyp_1_e = './data/final/test/configuration1/e'


#     # 1a
#     sys.stdout = open('./results/baseline/1a.txt', 'w')
#     print 'Identify spans of spatial elements including locations, paths, events and other spatial entities.'
#     print '\n' * 2
#     print '=' * 10 + ' IS SPATIAL ELEMENT: ' + '=' * 10
#     test = SpatialElementDemo(test_path = hyp_1_a, gold_path = gold_path)
#     test.evaluate()
# 
#     # 1b
#     sys.stdout = open('./results/baseline/1b.txt', 'w')
#     print 'Classify spatial elements according to type: PATH, PLACE, MOTION, NONMOTION_EVENT, SPATIAL_ENTITY.'
#     evaluate_all(se_b_demo_list, hyp_1_b, gold_path)
#  
#     # 1c
#     sys.stdout = open('./results/baseline/1c.txt', 'w')    
#     evaluate_all(se_c_demo_list, hyp_1_c, gold_path)
     
    # 1d
#     sys.stdout = open('./results/baseline/1d.txt', 'w')    
#     print '=' * 10 + 'MOVELINK' + '=' * 10 
#     d = IsMovelinkDemo(test_path = hyp_1_d, gold_path = gold_path)
#     cm = d.evaluate_movelink()
# 
#     print '=' * 10 + 'QSLINK' + '=' * 10 
#     d = IsOlinkDemo(test_path = hyp_1_d, gold_path = gold_path)
#     cm = d.evaluate_qs_o_link()
# 
#     print '=' * 10 + 'OLINK' + '=' * 10 
#     d = IsQSlinkDemo(test_path = hyp_1_d, gold_path = gold_path)
#     cm = d.evaluate_qs_o_link()


    # 1e
    sys.stdout = open('./results/baseline/1e.txt', 'w')
    evaluate_all(link_b_demo_list, hyp_1_a, gold_path)

    #===========================================================================

    hyp_2_a = './data/final/test/configuration2/a'
    hyp_2_b = './data/final/test/configuration2/b'
    hyp_2_c = './data/final/test/configuration2/c'

    # CONFIG 2
    # 2a
#     sys.stdout = open('./results/baseline/2a.txt', 'w')    
#     evaluate_all(se_c_demo_list, hyp_1_c, gold_path)
    
    # 2b
#     sys.stdout = open('./results/baseline/2b.txt', 'w')    
#     print '=' * 10 + 'MOVELINK' + '=' * 10 
#     d = IsMovelinkDemo(test_path = hyp_2_b, gold_path = gold_path)
#     cm = d.evaluate_movelink()
# 
#     print '=' * 10 + 'QSLINK' + '=' * 10 
#     d = IsOlinkDemo(test_path = hyp_2_b, gold_path = gold_path)
#     cm = d.evaluate_qs_o_link()
# 
#     print '=' * 10 + 'OLINK' + '=' * 10 
#     d = IsQSlinkDemo(test_path = hyp_2_b, gold_path = gold_path)
#     cm = d.evaluate_qs_o_link()


    # 2c
#     sys.stdout = open('./results/baseline/2c.txt', 'w')
#     evaluate_all(link_b_demo_list, hyp_2_c, gold_path)

    #===========================================================================

    hyp_3_a = './data/final/test/configuration3/a'
    hyp_3_b = './data/final/test/configuration3/b'

    # CONFIG 3

    # 3a
#     sys.stdout = open('./results/baseline/3a.txt', 'w')    
#     print '=' * 10 + 'MOVELINK' + '=' * 10 
#     d = IsMovelinkDemo(test_path = hyp_3_a, gold_path = gold_path)
#     cm = d.evaluate_movelink()
# 
#     print '=' * 10 + 'QSLINK' + '=' * 10 
#     d = IsOlinkDemo(test_path = hyp_3_a, gold_path = gold_path)
#     cm = d.evaluate_qs_o_link()
# 
#     print '=' * 10 + 'OLINK' + '=' * 10 
#     d = IsQSlinkDemo(test_path = hyp_3_a, gold_path = gold_path)
#     cm = d.evaluate_qs_o_link()

    # 3b
#     sys.stdout = open('./results/baseline/3b.txt', 'w')
#     evaluate_all(link_b_demo_list, hyp_3_b, gold_path)


    