'''
Created on Nov 3, 2014

@author: ACL73
'''
from b_identify_types import Tag, get_tag_and_no_tag_indices
from util.demo import Demo
import re
import os

class MotionSignalTag(Tag):
    # LABEL EXTRACT
    def motion_signal_type(self):
        # motion_type ( MANNER | PATH | COMPOUND )
        return self.tag['motion_signal_type']

def is_motion_tag(tag):
    tag_id = tag.get('id', '')
    return bool(re.findall('^ms\d+', tag_id))

def get_motion_signal_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_motion_tag)


class MotionSignalDemo(Demo):
    def __init__(self, train_path='./data/train_dev', test_path = './data/test_dev'):
        super(MotionSignalDemo, self).__init__(train_path = train_path, test_path = test_path)
        self.indices_function = get_motion_signal_tag_indices
        self.extent_class = MotionSignalTag

class MotionSignalTypeDemo(MotionSignalDemo):
    def get_label_function(self):
        return lambda x: str(x.motion_signal_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


if __name__ == "__main__":

#     d = MotionSignalTypeDemo()
#     d.run_demo()

    d = MotionSignalTypeDemo()
    type_labels, test_data = d.generate_labels()
    
    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)

        tag = extent.document.query_extents('MOTION_SIGNAL', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['motion_signal_type'] = type_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
