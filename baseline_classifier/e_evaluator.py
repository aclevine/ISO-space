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

# DEMOS
class SpatialElementDemo(Demo):
    def __init__(self, test_path, gold_path):
        super(SpatialElementDemo, self).__init__(train_path = '', test_path = test_path, 
                                                 gold_path = gold_path)
        self.feature_functions = []
        self.label_function = lambda x: str(bool(x.tag))
        self.indices_function = get_tag_and_no_tag_indices
        self.extent_class = Extent

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

if __name__ == "__main__":

    gold_path = './data/final/gold'

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

    # THESE ALL NEED TO CHANGE TO LABEL EXTENT EXTRACTORS
    link_b_demo_list = {
                        'MOVELINK - mover': MoveLinkMoverDemo,
                        'MOVELINK - source': MoveLinkSourceDemo,
                        'MOVELINK - goal': MoveLinkGoalDemo,
                        'MOVELINK - midPoint': MoveLinkMidPointDemo,
                        'MOVELINK - landmark': MoveLinkLandmarkDemo,
                        'MOVELINK - goal_reached': MoveLinkGoalReachedDemo,
                        
                        'QSLINK - trajector': QSLinkFromIDDemo,
                        'QSLINK - landmark': QSLinkToIDDemo,
                        'QSLINK - relType': QSLinkRelTypeDemo,
                        
                        'OLINK - trajector': OLinkFromIDDemo,
                        'OLINK - landmark': OLinkToIDDemo,
                        'OLINK - relType': OLinkRelTypeDemo,
                        'OLINK - referencePt': OLinkReferencePtDemo,
                        'OLINK - projective': OLinkProjectiveDemo,
                        'OLINK - frame_type': OLinkFrameTypeDemo,
                        }

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
    sys.stdout = open('./results/baseline/1d.txt', 'w')    
    evaluate_all(link_a_demo_list, hyp_1_d, gold_path)

    # 1e
#     sys.stdout = open('./results/baseline/1e.txt', 'w')
#     evaluate_all(link_b_demo_list, hyp_1_e, gold_path)

    #===========================================================================

    hyp_2_a = './data/final/test/configuration2/a'
    hyp_2_b = './data/final/test/configuration2/b'
    hyp_2_c = './data/final/test/configuration2/c'

    # CONFIG 2
    # 2a

    # 2b

    # 2c

    #===========================================================================

    hyp_3_a = './data/final/test/configuration3/a'
    hyp_3_b = './data/final/test/configuration3/b'

    # CONFIG 3
    # 3a

    # 3b


