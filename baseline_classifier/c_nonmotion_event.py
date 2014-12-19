'''
Created on Nov 3, 2014

@author: ACL73
'''
from c_path import PathTag
from b_identify_types import get_tag_and_no_tag_indices
from util.demo import Demo
import re

'''
<!ATTLIST NONMOTION_EVENT elevation IDREF #IMPLIED >
<!ATTLIST NONMOTION_EVENT mod CDATA #IMPLIED >
<!ATTLIST NONMOTION_EVENT countable ( TRUE | FALSE ) #IMPLIED >
'''

class EventTag(PathTag):
    # LABEL EXTRACT
    
    # FEATURE EXTRACT
    def test(self):
        return

def is_event_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^e\d+', tag_id))

def get_event_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_event_tag)

class EventDemo(Demo):
    def __init__(self, train_path='./data/train_dev', test_path = './data/test_dev'):
        super(EventDemo, self).__init__(train_path = train_path, test_path = test_path)
        self.indices_function = get_event_tag_indices
        self.extent_class = EventTag

class EventCountableDemo(EventDemo):
    def get_label_function(self):
        return  lambda x: str(x.countable())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EventElevationDemo(EventDemo):
    def get_label_function(self):
        return  lambda x: str(x.elevation())

    def get_elevation_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EventModDemo(EventDemo):
    def get_label_function(self):
        return  lambda x: str(x.mod())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":

    d = EventElevationDemo()
    d.run_demo()

    d = EventModDemo()
    d.run_demo()

    d = EventCountableDemo()
    d.run_demo()
    
