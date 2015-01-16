'''
Created on Oct 27, 2014

@author: ACL73
'''
from util.c_path import PathTag
from util.b_identify_types import get_tag_and_no_tag_indices
from util.model.demo import Classifier

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
class EntityClassifier(Classifier):
    def __init__(self, train_path = '', test_path = '', gold_path = ''):
        super(EntityClassifier, self).__init__(train_path = train_path, test_path = test_path, 
                                         gold_path = gold_path)
        self.indices_function = get_entity_tag_indices
        self.extent_class = EntityTag

class EntityDimensionalityClassifier(EntityClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.dimensionality())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EntityFormClassifier(EntityClassifier):
    def get_label_function(self):
        return  lambda x: str(x.form())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EntityCountableClassifier(EntityClassifier):
    def get_label_function(self):
        return  lambda x: str(x.countable())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class EntityModClassifier(EntityClassifier):
    def get_label_function(self):
        return  lambda x: str(x.mod())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":
    d = EntityDimensionalityClassifier()
    d.run_demo()
     
    d = EntityFormClassifier()
    d.run_demo()
     
    d = EntityCountableClassifier()
    d.run_demo()
     
    d = EntityModClassifier()
    d.run_demo()
