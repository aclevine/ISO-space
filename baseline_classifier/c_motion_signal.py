'''
Created on Nov 3, 2014

@author: ACL73
'''
from b_identify_types import Tag, get_tag_and_no_tag_indices
from util.demo import Demo
import re

class MotionSignalTag(Tag):
    # LABEL EXTRACT
    def motion_signal_type(self):
        # motion_type ( MANNER | PATH | COMPOUND )
        return self.tag['motion_signal_type']

def is_motion_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^ms\d+', tag_id))

def get_motion_signal_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_motion_tag)

class MotionSignalDemo(Demo):
    def __init__(self, doc_path='./training', split=0.8):
        super(MotionSignalDemo, self).__init__(doc_path, split)
        self.indices_function = get_motion_signal_tag_indices
        self.extent_class = MotionSignalTag

class MotionSignalTypeDemo(MotionSignalDemo):
    def get_label_function(self):
        return lambda x: str(x.motion_signal_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":
    d = MotionSignalTypeDemo()
    d.run_demo()
