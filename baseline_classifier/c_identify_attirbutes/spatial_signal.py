'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from b_identify_types.identify_types import Tag, get_tag_and_no_tag_indices
from util.demo import Demo
import re

class SignalTag(Tag):
    # LABEL EXTRACT
    def semantic_type(self):
    #semantic_type ( DIRECTIONAL | TOPOLOGICAL | DIR_TOP ) 
        return self.tag['semantic_type']

    def is_directional(self):
        if self.tag['semantic_type'] in ['DIR_TOP', 'TOPOLOGICAL']:
            return 'TOPOLOGICAL'
        else:
            return 'NOT_TOPOLOGICAL'
            
    def is_topological(self):
        if self.tag['semantic_type'] in ['DIR_TOP', 'DIRECTIONAL']:
            return 'DIRECTIONAL'
        else:
            return 'NOT_DIRECTIONAL'
    
# DEMO
def is_signal_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^s\d+', tag_id))

def get_signal_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_signal_tag)

class SignalDemo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
        super(SignalDemo, self).__init__(doc_path, split)
        self.indices_function = get_signal_tag_indices
        self.extent_class = SignalTag

class MotionSemanticTypeDemo(SignalDemo):
    def get_label_function(self):
        return  lambda x: str(x.semantic_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
    
# subdivide MotionSemanticTypeDemo() into 2 tasks  
class MotionDirectionalDemo(SignalDemo):
    def get_label_function(self):
        return  lambda x: str(x.is_directional())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MotionTopologicalDemo(SignalDemo):
    def get_label_function(self):
        return  lambda x: str(x.is_topological())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
        

    
if __name__ == "__main__":

#     d = MotionSemanticTypeDemo()
#     d.run_demo()

    d = MotionDirectionalDemo()
    d.run_demo()

    d = MotionTopologicalDemo()
    d.run_demo()
