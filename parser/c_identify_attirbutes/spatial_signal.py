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
    

if __name__ == "__main__":
    d = MotionSemanticTypeDemo()
    d.run_demo()
