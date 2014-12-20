'''
Created on Dec 19, 2014

@author: Aaron Levine
'''
from b_identify_types import get_tag_and_no_tag_indices, get_tag_only_indices, Tag,\
    TypesDemo
from util.demo import Demo
from util.Corpora.corpus import Extent
import re
import numpy as np
from c_motion import MotionTypeDemo, MotionSenseDemo, MotionClassDemo

# 1a
def is_element(tag):
    tag_id = tag.get('id', '')
    for pattern in ['p', 'pl', 'm', 'e', 'se']:
        if re.findall('^{}\d+'.format(pattern), tag_id):
            return True    
    return False

def get_elements(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_element)

class Demo1A(Demo):
    def __init__(self, test_path = './data/test_dev', gold_path = './data/gold_dev'):
        super(Demo1A, self).__init__(train_path = '', test_path = test_path, gold_path = gold_path)
        self.feature_functions = []
        self.label_function = lambda x: str(bool(x.tag))
        self.indices_function = get_tag_and_no_tag_indices  # get_tag_and_no_tag_indices
        self.extent_class = Extent


if __name__ == "__main__":

    x = './data/test_dev_c/'
    y = './data/gold_dev/'
    
#     test = Demo1A(test_path = x, gold_path = y)
#     cm = test.evaluate()
# 
#     print "=" * 50
#     
#     # 1b
#     tag_types = ['PATH', 'PLACE', 
#                 'MOTION', 'NONMOTION_EVENT',
#                 'SPATIAL_ENTITY']
# 
#     p = []
#     r = []
#     f = []
#     a = []    
#     for t_type in tag_types:
#         print '\n{}'.format(t_type)
#         test = TypesDemo(t_type, test_path = x, gold_path = y)
#         cm = test.evaluate()   
#         p.append(cm.compute_precision())
#         r.append(cm.compute_recall())
#         f.append(cm.compute_f1())
#         a.append(cm.compute_accuracy())
# 
#     print 'mean precision: {}'.format(np.mean(p))
#     print 'mean recall: {}'.format(np.mean(r))
#     print 'mean f1: {}'.format(np.mean(f))
#     print 'mean accuracy: {}'.format(np.mean(a))
     
    print "=" * 50


    d = MotionTypeDemo(test_path = x, gold_path = y)
    d.evaluate()
       
    d = MotionClassDemo(test_path = x, gold_path = y)
    d.evaluate()
          
    d = MotionSenseDemo(test_path = x, gold_path = y)
    d.evaluate()
