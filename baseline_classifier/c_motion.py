'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from b_identify_types import Tag, get_tag_and_no_tag_indices
from util.model.demo import Classifier
import re
import os
from _warnings import warn

class MotionTag(Tag):
    # LABEL EXTRACT
    def motion_type(self):
        ''' motion_type ( MANNER | PATH | COMPOUND ) '''
        return self.tag['motion_type']
 
    def motion_class(self):
        ''' motion_class ( MOVE | MOVE_EXTERNAL | MOVE_INTERNAL | LEAVE | REACH | CROSS | DETACH | HIT | FOLLOW | DEVIATE | STAY ) '''
        return self.tag['motion_class']
     
    def motion_sense(self):
        # motion_sense ( LITERAL | FICTIVE | INTRINSIC_CHANGE )
        return self.tag['motion_sense']

    def is_move_link(self):
#         return True
        trigger_tag, _, to_tag = self.token
        links = self.document.query_links(['MOVELINK'], trigger_tag['id'])
        if links:
            link = links[0]
            try:
                link_to_tag = self.document.query(link['toID'])
            except KeyError:
                warning = "malformed MOVELINK {} tag in {}".format(link['id'], self.document.basename)
                warn(warning, RuntimeWarning)
                link_to_tag = self.document.query('')
            except Exception as e:
                raise e
            if link_to_tag:
                if link_to_tag['start'] == to_tag['start'] and link_to_tag['end'] == to_tag['end']:
                    return True
        return False

# TAG TYPE FILTER
def is_motion_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^m\d+', tag_id))

def get_motion_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_motion_tag)

# DEMOS
class MotionClassifier(Classifier):
    def __init__(self, train_path = '', test_path = '', gold_path = ''):
        super(MotionClassifier, self).__init__(train_path = train_path, test_path = test_path,
                                         gold_path = gold_path)
        self.indices_function = get_motion_tag_indices
        self.extent_class = MotionTag

class MotionTypeClassifier(MotionClassifier):
    def get_label_function(self):
        return lambda x: str(x.motion_type())

    def get_feature_functions(self):
        return [
                lambda x: x.curr_token(),
                lambda x: x.curr_tokens(),
#                 lambda x: x.prev_n_bag_of_words(3),
#                 lambda x: x.next_n_bag_of_words(3),
                lambda x: x.curr_pos_tags()
                ]

class MotionClassClassifier(MotionClassifier):
    def get_label_function(self):
        return lambda x: str(x.motion_class())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MotionSenseClassifier(MotionClassifier):
    def get_label_function(self):
        return lambda x: str(x.motion_sense())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


class IsMovelinkClassifier(MotionClassifier):
    def get_label_function(self):
        return lambda x: str(x.is_move_link())

    def get_feature_functions(self):
        return []


if __name__ == "__main__":

    d = MotionTypeClassifier()
    d.run_demo()
       
    d = MotionClassClassifier()
    d.run_demo()
          
    d = MotionSenseClassifier()
    d.run_demo()

