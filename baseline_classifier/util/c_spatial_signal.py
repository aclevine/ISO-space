'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from util.b_identify_types import Tag, get_tag_and_no_tag_indices
from util.iso_space_classifier import ISOSpaceClassifier
import re

class SignalTag(Tag):
    # LABEL EXTRACT
    def semantic_type(self):
    # semantic_type ( DIRECTIONAL | TOPOLOGICAL | DIR_TOP ) 
        return self.tag['semantic_type']

    def is_directional(self):
        if self.tag['semantic_type'] in ['DIR_TOP', 'TOPOLOGICAL']:
            return True
        else:
            return False
            
    def is_topological(self):
        if self.tag['semantic_type'] in ['DIR_TOP', 'DIRECTIONAL']:
            return True
        else:
            return False

    def is_qslink(self):
        trigger_id, from_id, to_id = map(lambda x: x['id'], self.token)
        links = self.document.query_links(['QSLINK'], trigger_id)
        if links:
            link = links[0]
            if link['fromID'] == from_id and link['toID'] == to_id:
                return True
        return False

    def is_olink(self):
        trigger_id, from_id, to_id = map(lambda x: x['id'], self.token)
        links = self.document.query_links(['OLINK'], trigger_id)
        if links:
            link = links[0]
            if link['fromID'] == from_id and link['toID'] == to_id:
                return True
        return False

# FILTER
def is_signal_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^s\d+', tag_id))

def get_signal_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_signal_tag)


# MODELS
class SignalClassifier(ISOSpaceClassifier):
    def __init__(self, train_path = '', test_path = '', gold_path = ''):
        super(SignalClassifier, self).__init__(train_path = train_path, test_path = test_path, 
                                         gold_path = gold_path)
        self.indices_function = get_signal_tag_indices
        self.extent_class = SignalTag

class SignalSemanticTypeClassifier(SignalClassifier):
    def get_label_function(self):
        return  lambda x: str(x.semantic_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
    
# subdivide SignalSemanticTypeClassifier() into 2 tasks  
class SignalDirectionalClassifier(SignalClassifier):
    def get_label_function(self):
        return  lambda x: str(x.is_directional())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class SignalTopologicalClassifier(SignalClassifier):
    def get_label_function(self):
        return  lambda x: str(x.is_topological())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
        

class IsOlinkClassifier(SignalClassifier):
    def get_label_function(self):
        return  lambda x: str(x.is_olink())

    def get_feature_functions(self):
        return []

class IsQSlinkClassifier(SignalClassifier):
    def get_label_function(self):
        return  lambda x: str(x.is_qslink())

    def get_feature_functions(self):
        return []
