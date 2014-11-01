'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from b_identify_types.identify_types import get_tag_and_no_tag_indices, Tag
from util.demo import Demo
import re

# check with Zach about what we're actually covering
class PathTag(Tag):
    # LABEL EXTRACT

    def form(self):
        '''form ( NAM | NOM )'''
        return self.tag['form']

    def countable(self):
        '''countable ( TRUE | FALSE )'''
        return self.tag['countable']

    # USUALLY BLANK
    def dimensionality(self):
        '''dimensionality ( POINT | LINE | AREA | VOLUME )'''
        return self.tag['dimensionality']
   
    # USUALLY BLANK
    def mod(self):
        '''mod <OPEN_CLASS>'''
        return self.tag['mod']
        # this really needs to be tagged data if we every seriously want to use it.

    
# TAG TYPE FILTER
def is_path_tag(tag):
    tag_id = tag.get('id', '')
    return re.findall('^p\d+', tag_id)

def get_path_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_path_tag)

# DEMOS
class PathDemo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
        super(PathDemo, self).__init__(doc_path, split)
        self.indices_function = get_path_tag_indices
        self.extent_class = PathTag

class PathDimensionalityDemo(PathDemo):  
    def get_label_function(self):
        return  lambda x: str(x.dimensionality())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


class PathFormDemo(PathDemo):
    def get_label_function(self):
        return  lambda x: str(x.form())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PathCountableDemo(PathDemo):
    def get_label_function(self):
        return  lambda x: str(x.countable())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PathModDemo(PathDemo):
    def get_label_function(self):
        return  lambda x: str(x.mod())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":
    d = PathDimensionalityDemo()
    d.run_demo()
    
    d = PathFormDemo()
    d.run_demo()
    
    d = PathCountableDemo()
    d.run_demo()
    
    d = PathModDemo()
    d.run_demo()
    