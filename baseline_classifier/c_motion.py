'''
Created on Oct 27, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

c. Identify their attributes according to type.
'''
from b_identify_types import Tag, get_tag_and_no_tag_indices
from util.demo import Demo
import re
import os

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

# TAG TYPE FILTER
def is_motion_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^m\d+', tag_id))

def get_motion_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_motion_tag)

# DEMOS
class MotionDemo(Demo):
    def __init__(self, train_path='./data/train_dev', test_path = './data/test_dev'):
        super(MotionDemo, self).__init__(train_path = train_path, test_path = test_path)
        self.indices_function = get_motion_tag_indices
        self.extent_class = MotionTag

class MotionTypeDemo(MotionDemo):
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

class MotionClassDemo(MotionDemo):
    def get_label_function(self):
        return lambda x: str(x.motion_class())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MotionSenseDemo(MotionDemo):
    def get_label_function(self):
        return lambda x: str(x.motion_sense())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


if __name__ == "__main__":

#     d = MotionTypeDemo()
#     d.run_demo()
#       
#     d = MotionClassDemo()
#     d.run_demo()
#          
#     d = MotionSenseDemo()
#     d.run_demo()

    d = MotionTypeDemo()
    type_labels, test_data = d.generate_labels()
    
    d = MotionClassDemo()
    class_labels, _ = d.generate_labels()
           
    d = MotionSenseDemo()
    sense_labels, _ = d.generate_labels()

    doc_name = test_data[0].document.basename    
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)

        tag = extent.document.query_extents('MOTION', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['motion_type'] = type_labels[offsets]
        tag.attrs['motion_class'] = class_labels[offsets]
        tag.attrs['motion_sense'] = sense_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
    
