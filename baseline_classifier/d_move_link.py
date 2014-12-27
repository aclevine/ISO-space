'''
Created on Nov 13, 2014

@author: Aaron Levine
'''

from c_path import PathTag
from util.model.demo import Classifier
from util.corpora.corpus import Corpus
from c_motion import get_motion_tag_indices
import re


class MovelinkTag(PathTag):

    def __init__(self, sent, tag_dict, movelink_tag_dict, olink_tag_dict, qslink_tag_dict, front, back, basename, doc):
        ''' use c_motion tags as a head to associate move-links with sentences'''
        super(MovelinkTag, self).__init__(sent, tag_dict, movelink_tag_dict, olink_tag_dict, qslink_tag_dict, front, back, basename, doc)
        head = tag_dict.get(self.lex[0].begin, {})
        self.tag = movelink_tag_dict.get(head['id'], {})
        
    # LABEL EXTRACT
    
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
        return self.tag.get('goal_reached', '')
    
    def path_id(self):
        '''pathID IDREF'''
        return self.tag_position('pathID')


    def motion_signal_id(self):
        '''motion_signalID IDREFS'''
        return self.tag_position('motion_signalID')

    # EVAL LABELS    
    def source_extents(self):
        tag_id = self.tag.get('source', '')
        target_tag = self.document.query(tag_id)
        if tag_id and target_tag:
            return "{},{}".format(target_tag['start'], target_tag['end'])
        else:
            return "-1,-1"
    
    def goal_extents(self):
        tag_id = self.tag.get('goal', '')
        target_tag = self.document.query(tag_id)
        if tag_id and target_tag:
            return "{},{}".format(target_tag['start'], target_tag['end'])
        else:
            return "-1,-1"
    
    def mid_point_extents(self):
        tag_id = self.tag.get('midPoint', '')
        target_tag = self.document.query(tag_id)
        if tag_id and target_tag:
            return "{},{}".format(target_tag['start'], target_tag['end'])
        else:
            return "-1,-1"

    def landmark_extents(self):
        tag_id = self.tag.get('landmark', '')
        target_tag = self.document.query(tag_id)
        if tag_id and target_tag:
            return "{},{}".format(target_tag['start'], target_tag['end'])
        else:
            return "-1,-1"
    
    def motion_signal_id_extents(self):        
        tag_id = self.tag.get('motion_signalID', '')        
        target_tag = self.document.query(tag_id)
        if tag_id and target_tag:
            return "{},{}".format(target_tag['start'], target_tag['end'])
        else:
            return "-1,-1"

    def path_id_extents(self):        
        tag_id = self.tag.get('pathID', '')
        target_tag = self.document.query(tag_id)
        if tag_id and target_tag:
            return "{},{}".format(target_tag['start'], target_tag['end'])
        else:
            return "-1,-1"
                    
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
class MovelinkClassifier(Classifier):
    def __init__(self, train_path='', test_path = '', gold_path = ''):
        super(MovelinkClassifier, self).__init__(train_path = train_path, test_path = test_path,
                                           gold_path = gold_path)
        self.indices_function = get_motion_tag_indices
        self.extent_class = MovelinkTag

class MovelinkTriggerClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.trigger())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkSourceClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.source())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkGoalClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.goal())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                lambda x: x.prev_tag_count(),
                lambda x: x.next_tag_count(),
                lambda x: x.prev_tag_types(),
                lambda x: x.next_tag_types(),
                ]

class MovelinkMidPointClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.mid_point())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkMoverClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.mover())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkLandmarkClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.landmark())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkGoalReachedClassifier(MovelinkClassifier):  
    def get_label_function(self):
        return  lambda x: str(x.goal_reached())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkGoalPathIdClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.path_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkGoalMotionSignalIDClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.motion_signal_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class MovelinkPathIDClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.path_signal_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

# FOR EVAL
class MovelinkSourceExentsClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.source_extents())

    def get_feature_functions(self):
        return []

class MovelinkGoalExentsClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.goal_extents())

    def get_feature_functions(self):
        return []

class MovelinkMidpointExentsClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.mid_point_extents())

    def get_feature_functions(self):
        return []

class MovelinkPathIDExentsClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.path_id_extents())

    def get_feature_functions(self):
        return []

class MovelinkMotionSignalIDExentsClassifier(MovelinkClassifier):
    def get_label_function(self):
        return  lambda x: str(x.motion_signal_id_extents())

    def get_feature_functions(self):
        return []


if __name__ == "__main__":
    
    source = MovelinkSourceClassifier()  
    source.run_demo()
 
    goal = MovelinkGoalClassifier()
    goal.run_demo()
  
    mid_point = MovelinkMidPointClassifier()  
    mid_point.run_demo()
 
    mover = MovelinkMoverClassifier()  
    mover.run_demo()
 
    d = MovelinkLandmarkClassifier()  
    d.run_demo()
    
    d = MovelinkGoalReachedClassifier()  
    d.run_demo()
