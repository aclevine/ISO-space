'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from util.b_identify_types import get_tag_and_no_tag_indices, Tag
from util.model.demo import Classifier
import re

# check with Zach about what we're actually covering
class PathTag(Tag):
    # LABEL EXTRACT
    def begin_id(self):
        '''beginID IDREFS'''
        return self.tag['beginID']

    '''midIDs IDREFS'''
    def mid_ids(self):
        return self.tag['midIDs']
        
    def form(self):
        '''form ( NAM | NOM )'''
        return self.tag['form']

    def countable(self):
        '''countable ( TRUE | FALSE )'''
        return self.tag['countable']

    def elevation(self):
        ''' evelation <OPEN_CLASS>'''
        return self.tag['elevation']

    # USUALLY BLANK
    def dimensionality(self):
        '''dimensionality ( POINT | LINE | AREA | VOLUME )'''
        return self.tag['dimensionality']
   
    # USUALLY BLANK
    def mod(self):
        '''mod <OPEN_CLASS>'''
        return self.tag['mod']
        # this really needs to be tagged data if we want to use it.
    
# TAG TYPE FILTER
def is_path_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^p\d+', tag_id))

def get_path_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_path_tag)

# DEMOS
class PathClassifier(Classifier):
    def __init__(self, train_path = '', test_path = '', gold_path = ''):
        super(PathClassifier, self).__init__(train_path = train_path, test_path = test_path, 
                                       gold_path = gold_path)
        self.indices_function = get_path_tag_indices
        self.extent_class = PathTag

class PathDimensionalityClassifier(PathClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.dimensionality())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


class PathFormClassifier(PathClassifier):
    def get_label_function(self):
        return  lambda x: str(x.form())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PathCountableClassifier(PathClassifier):
    def get_label_function(self):
        return  lambda x: str(x.countable())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PathElevationClassifier(PathClassifier):
    def get_label_function(self):
        return  lambda x: str(x.elevation())

    def get_elevation_functions(self):
        return [lambda x: x.curr_token(),
                ]

class PathModClassifier(PathClassifier):
    def get_label_function(self):
        return  lambda x: str(x.mod())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":
    d = PathDimensionalityClassifier()
    d.run_demo()
    
    d = PathFormClassifier()
    d.run_demo()
    
    d = PathCountableClassifier()
    d.run_demo()

    d = PathElevationClassifier()
    d.run_demo()

    d = PathModClassifier()
    d.run_demo()
   
