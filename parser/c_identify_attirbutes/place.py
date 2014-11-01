'''
Created on Oct 27, 2014

@author: ACL73
'''
from path import PathTag
from b_identify_types.identify_types import get_tag_and_no_tag_indices
from util.demo import Demo
from abc import abstractmethod

import re

class PlaceTag(PathTag):
    # LABEL EXTRACT

    # FEATURE EXTRACT
    def test(self):
        return
    
def is_place_tag(tag):
    tag_id = tag.get('id', '')
    return re.findall('^pl\d+', tag_id)

def get_place_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_place_tag)

# DEMO
class PlaceDemo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
        self.doc_path = doc_path
        self.split = split
        self.label_function = self.get_label_function()
        self.feature_functions = self.get_feature_functions()
        self.indices_function = get_place_tag_indices
        self.extent_class = PlaceTag

    @abstractmethod        
    def get_label_function(self):
        return None
        
    @abstractmethod
    def get_feature_functions(self):
        return []


class PlaceDimensionalityDemo(PlaceDemo):  
    def get_label_function(self):
        return  lambda x: str(x.dimensionality())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


class PlaceFormDemo(PlaceDemo):
    def get_label_function(self):
        return  lambda x: str(x.form())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PlaceCountableDemo(PlaceDemo):
    def get_label_function(self):
        return  lambda x: str(x.countable())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PlaceModDemo(PlaceDemo):
    def get_label_function(self):
        return  lambda x: str(x.mod())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


if __name__ == "__main__":
    d = PlaceDimensionalityDemo()
    d.run_demo(verbose=2)
     
    d = PlaceFormDemo()
    d.run_demo()
     
    d = PlaceCountableDemo()
    d.run_demo()
     
    d = PlaceModDemo()
    d.run_demo()

