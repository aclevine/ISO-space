'''
Created on Nov 13, 2014

@author: Aaron Levine
'''

from c_path import PathTag
from util.demo import Demo
from Corpora.corpus import Corpus
from c_motion import get_motion_tag_indices
import re


class MoveLinkTag(PathTag):

    def __init__(self, sent, tag_dict, movelink_tag_dict, olink_tag_dict, qslink_tag_dict, front, back, basename):
        ''' use c_motion tags as a head to associate move-links with sentences'''
        super(MoveLinkTag, self).__init__(sent, tag_dict, movelink_tag_dict, olink_tag_dict, qslink_tag_dict, front, back, basename)
        head = tag_dict.get(self.lex[0].begin, {})
        self.tag = movelink_tag_dict.get(head['id'], {})
        
    # LABEL EXTRACT
    # Want to select position of tag in surrounding sentence, not tag itself.
    
    # skip trigger and from_id - move-links were identified using them
    def tag_position(self, attribute_key):
        '''
        0 = empty field for movelink attribute
        +n = movelink attribute is n tags right of c_motion tag
        -n = movelink attribute is n tags left of c_motion tag
        '''
        if attribute_key in self.tag:
            target = self.tag[attribute_key]
            i = -1
            for tag in reversed(self.prev_tags):
                if tag['id'] == target:
                    return i
                i -= 1
            i = 1
            for tag in self.next_tags:
                if tag['id'] == target:
                    # print tag['id']
                    return i
                i += 1
        return 0

    def source(self):
        '''source IDREF'''
        return self.tag_position('source')
        
    def goal(self):
        '''goal IDREF'''
        return self.tag_position('goal')

    def mid_point(self):
        '''midPoint IDREF'''
        return self.tag_position('midPoint')
    
    def mover(self):
        '''mover IDREF'''
        return self.tag_position('mover')

    def landmark(self):
        '''landmark IDREF'''
        return self.tag_position('landmark')

    def goal_reached(self):
        '''goal_reached ( YES | NO | UNCERTAIN )'''
        if self.tag.get('goal_reached', '') == '':
            print self.tag.get('id', 'no_tag')
        return self.tag.get('goal_reached', '')
    
    def path_id(self):
        '''pathID IDREF'''
        return self.tag['pathID']

    def motion_signal_id(self):
        '''motion_signalID IDREFS'''
        return self.tag_position('motion_signalID')

    # FEATURE EXTRACT
    def prev_tag_count(self):
        return {'prev_tag_count': len(self.prev_tags)}
    
    def next_tag_count(self):
        return {'next_tag_count': len(self.next_tags)}

    def prev_tag_types(self):
        i = -1
        feat_dict = {}
        for tag in reversed(self.prev_tags):
            feat_dict['prev_tag_%d_type' % i] = re.findall('[a-z]+', tag['id'])[0]
            i -= 1
        return feat_dict
            
    def next_tag_types(self):
        i = 1
        feat_dict = {}
        for tag in self.next_tags:
            feat_dict['next_tag_%d_type' % i] = re.findall('[a-z]+', tag['id'])[0]
            i += 1
        return feat_dict

# DEMO
class MoveLinkDemo(Demo):
    def __init__(self, doc_path='./training', split=0.8):
        super(MoveLinkDemo, self).__init__(doc_path, split)
        self.indices_function = get_motion_tag_indices
        self.extent_class = MoveLinkTag

class MoveLinkTriggerDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.trigger())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MoveLinkSourceDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.source())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MoveLinkGoalDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.goal())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                lambda x: x.prev_tag_count(),
                lambda x: x.next_tag_count(),
                lambda x: x.prev_tag_types(),
                lambda x: x.next_tag_types(),
                ]

class MoveLinkMidPointDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.mid_point())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MoveLinkMoverDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.mover())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MoveLinkLandmarkDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.landmark())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MoveLinkGoalReachedDemo(MoveLinkDemo):  
    def get_label_function(self):
        return  lambda x: str(x.goal_reached())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MoveLinkGoalPathIdDemo(MoveLinkDemo):
    def get_label_function(self):
        return  lambda x: str(x.path_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

if __name__ == "__main__":
    
    source = MoveLinkSourceDemo()  
    source.run_demo()
 
    goal = MoveLinkGoalDemo()
    goal.run_demo()
  
    mid_point = MoveLinkMidPointDemo()  
    mid_point.run_demo()
 
    mover = MoveLinkMoverDemo()  
    mover.run_demo()
 
    d = MoveLinkLandmarkDemo()  
    d.run_demo()
    
    d = MoveLinkGoalReachedDemo()  
    d.run_demo()
