'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from b_identify_types import Tag, get_tag_and_no_tag_indices
from util.demo import Demo
import re

class SignalTag(Tag):
    # LABEL EXTRACT
    def semantic_type(self):
    # semantic_type ( DIRECTIONAL | TOPOLOGICAL | DIR_TOP ) 
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
    def __init__(self, train_path='./data/train_dev', test_path = './data/test_dev'):
        super(SignalDemo, self).__init__(train_path = train_path, test_path = test_path)
        self.indices_function = get_signal_tag_indices
        self.extent_class = SignalTag

class SignalSemanticTypeDemo(SignalDemo):
    def get_label_function(self):
        return  lambda x: str(x.semantic_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
    
# subdivide SignalSemanticTypeDemo() into 2 tasks  
class SignalDirectionalDemo(SignalDemo):
    def get_label_function(self):
        return  lambda x: str(x.is_directional())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class SignalTopologicalDemo(SignalDemo):
    def get_label_function(self):
        return  lambda x: str(x.is_topological())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
        
    
if __name__ == "__main__":

    d = SignalSemanticTypeDemo()
    d.run_demo()

    d = SignalDirectionalDemo()
    d.run_demo()

    d = SignalTopologicalDemo()
    d.run_demo()
