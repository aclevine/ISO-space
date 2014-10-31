'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''

from Corpora.corpus import Extent
from b_identify_types.identify_types import get_tag_and_no_tag_indices
import re
from util.demo import Demo

class Motion_Tags(Extent):
    # LABEL EXTRACT
    def motion_type(self):
        #motion_type ( MANNER | PATH | COMPOUND ) #REQUIRED >
        return self.tag['motion_type']
 
    def motion_class(self):
        #motion_class ( MOVE | MOVE_EXTERNAL | MOVE_INTERNAL | LEAVE | REACH | CROSS | DETACH | HIT | FOLLOW | DEVIATE | STAY ) #REQUIRED >
        return self.tag['motion_class']
     
    def motion_sense(self):
        #motion_sense ( LITERAL | FICTIVE | INTRINSIC_CHANGE ) #REQUIRED >
        return self.tag['motion_sense']
     
    # FEATURE EXTRACT
    def curr_token(self):
        ''' pull prev n tokens in sentence before target word.'''
        return {'curr_' + ' '.join(self.token):True}
    
# DEMO
def is_motion_tag(tag):
    id = tag.get('id', '')
    return re.findall('m\d+', id)

def get_motion_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_motion_tag)

class Motion_Type_Demo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
        self.doc_path = doc_path
        self.split = split
        self.feature_functions = [lambda x: x.curr_token(),
                                  ]
        self.label_function = lambda x: str(x.motion_type())
        self.indices_function = get_motion_tag_indices
        self.extent_class = Motion_Tags

class Motion_Class_Demo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
        self.doc_path = doc_path
        self.split = split
        self.feature_functions = [lambda x: x.curr_token(),
                                  ]
        self.label_function = lambda x: str(x.motion_class())
        self.indices_function = get_motion_tag_indices
        self.extent_class = Motion_Tags

class Motion_Sense_Demo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
        self.doc_path = doc_path
        self.split = split
        self.feature_functions = [lambda x: x.curr_token(),
                                  ]
        self.label_function = lambda x: str(x.motion_sense())
        self.indices_function = get_motion_tag_indices
        self.extent_class = Motion_Tags


if __name__ == "__main__":
    d = Motion_Type_Demo()
    d.run_demo()
    
    d = Motion_Class_Demo()
    d.run_demo()
    
    d = Motion_Sense_Demo()
    d.run_demo()
