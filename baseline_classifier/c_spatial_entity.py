'''
Created on Oct 27, 2014

@author: ACL73
'''
from c_path import PathTag
from b_identify_types import get_tag_and_no_tag_indices
from util.demo import Demo

import re

class EntityTag(PathTag):
    # LABEL EXTRACT

    # FEATURE EXTRACT
    def test(self):
        return
    
def is_entity_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^se\d+', tag_id))


def get_entity_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_entity_tag)

# DEMO
class EntityDemo(Demo):
    def __init__(self, train_path='./data/train_dev', test_path = './data/test_dev'):
        super(EntityDemo, self).__init__(train_path = train_path, test_path = test_path)
        self.indices_function = get_entity_tag_indices
        self.extent_class = EntityTag

class EntityDimensionalityDemo(EntityDemo):  
    def get_label_function(self):
        return  lambda x: str(x.dimensionality())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EntityFormDemo(EntityDemo):
    def get_label_function(self):
        return  lambda x: str(x.form())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EntityCountableDemo(EntityDemo):
    def get_label_function(self):
        return  lambda x: str(x.countable())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EntityModDemo(EntityDemo):
    def get_label_function(self):
        return  lambda x: str(x.mod())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":
    d = EntityDimensionalityDemo()
    d.run_demo()
     
    d = EntityFormDemo()
    d.run_demo()
     
    d = EntityCountableDemo()
    d.run_demo()
     
    d = EntityModDemo()
    d.run_demo()
