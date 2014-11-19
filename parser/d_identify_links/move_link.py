'''
Created on Nov 13, 2014

@author: Aaron Levine
'''

from c_identify_attirbutes.path import PathTag
from util.demo import Demo
from Corpora.corpus import Corpus
from c_identify_attirbutes.motion import get_motion_tag_indices


class MoveLinkTag(PathTag):

    def __init__(self, sent, tag_dict, front, back):
        ''' use motion tags as a head to associate move-links with sentences'''
        super(MoveLinkTag, self).__init__(sent, tag_dict, front, back)
        head = tag_dict.get(self.lex[0].begin, {})
        self.tag = tag_dict.get(head['id'], {})

    # LABEL EXTRACT
    # Want to select position of tag in surrounding sentence, not tag itself.
    
    # skip trigger and from_id - move-links were identified using them
            
    def source(self):
        '''source IDREF'''
        target = self.tag['source']
        

    def goal(self):
        '''goal IDREF'''
        return self.tag['goal']

    def mid_point(self):
        '''midPoint IDREF'''
        return self.tag['midPoint']
    
    def mover(self):
        '''mover IDREF'''
        return self.tag['mover']

    def landmark(self):
        '''landmark IDREF'''
        return self.tag['landmark']

    def goal_reached(self):
        '''goal_reached ( YES | NO | UNCERTAIN )'''
        return self.tag.get('goal_reached', '')
    
    def path_id(self):
        '''pathID IDREF'''
        return self.tag['pathID']

    def motion_signal_id(self):
        '''motion_signalID IDREFS'''
        return self.tag['motion_signalID']

    # FEATURE EXTRACT

# DEMO
class MoveLinkDemo(Demo):
    def __init__(self, doc_path = '../training', split=0.8):
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
        return [lambda x: x.prev(),
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

    
#     source = MoveLinkSourceDemo()  
#     source.run_demo()
# 
#     goal = MoveLinkGoalDemo()
#     goal.run_demo()
# 
#     mid_point = MoveLinkMidPointDemo()  
#     mid_point.run_demo()
# 
#     mover = MoveLinkMoverDemo()  
#     mover.run_demo()
# 
#     d = MoveLinkLandmarkDemo()  
#     d.run_demo()
# 
    d = MoveLinkGoalReachedDemo()  
    d.run_demo()


    