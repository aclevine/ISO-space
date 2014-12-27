'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from b_identify_types import Tag, get_tag_and_no_tag_indices
from util.model.demo import Classifier
import re
from _warnings import warn

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
        trigger_tag, from_tag, to_tag = self.token
        links = self.document.query_links(['QSLINK'], trigger_tag['id'])
        if links:
            link = links[0]
            try:
                link_from_tag = self.document.query(link['fromID'])
                link_to_tag = self.document.query(link['toID'])
            except KeyError:
                warning = "malformed QSLINK {} tag in {}".format(link['id'], self.document.basename)
                warn(warning, RuntimeWarning)
                link_from_tag = self.document.query('')
                link_to_tag = self.document.query('')
            except Exception as e:
                raise e
            if link_from_tag and link_to_tag:
                if link_to_tag['start'] == to_tag['start'] and link_to_tag['end'] == to_tag['end'] \
                and link_from_tag['start'] == from_tag['start'] and link_from_tag['end'] == from_tag['end']:
                    return True
        return False

    def is_olink(self):
        trigger_tag, from_tag, to_tag = self.token
        links = self.document.query_links(['OLINK'], trigger_tag['id'])
        if links:
            link = links[0]
            try:
                link_from_tag = self.document.query(link['fromID'])
                link_to_tag = self.document.query(link['toID'])
            except KeyError:
                warning = "malformed OLINK {} tag in {}".format(link['id'], self.document.basename)
                warn(warning, RuntimeWarning)
                return False
            except Exception as e:
                raise e                
            if link_from_tag and link_to_tag:
                if link_to_tag['start'] == to_tag['start'] and link_to_tag['end'] == to_tag['end'] and \
                link_from_tag['start'] == from_tag['start'] and link_from_tag['end'] == from_tag['end']:
                    return True
        return False

# FILTER
def is_signal_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^s\d+', tag_id))

def get_signal_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_signal_tag)


# MODELS
class SignalClassifier(Classifier):
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

