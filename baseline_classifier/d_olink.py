'''
Created on Nov 13, 2014

@author: Aaron Levine

if signal: 
    dir_top = olink + qslink
    top = qslink
    dir = olink

'''
from c_path import PathTag
from util.demo import Demo
import re
from b_identify_types import get_tag_and_no_tag_indices

class OLinkTag(PathTag):
    def __init__(self, sent, tag_dict, movelink_tag_dict, olink_tag_dict, 
                 qslink_tag_dict, front, back, basename):
        ''' use c_motion tags as a head to associate move-links with sentences'''
        super(OLinkTag, self).__init__(sent, tag_dict, movelink_tag_dict, olink_tag_dict, 
                                       qslink_tag_dict, front, back, basename)
        head = tag_dict.get(self.lex[0].begin, {})
        self.tag = olink_tag_dict.get(head['id'], {})

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
                    return i
                i += 1    
        return 0
   
    def is_olink(self):
        if self.tag.get('id', ''):
            return {'is_OLink': True}
        else:
            return {'is_OLink': False}

    def from_id(self):
        '''fromID IDREF'''
        return self.tag_position('fromID')

    def to_id(self):
        '''toID IDREF'''
        return self.tag_position('toID')
        
    def rel_type(self):
        ''' relType CDATA '''
        return self.tag.get('relType', 'NOT_OLINK')

    def trajector(self):
        '''trajector IDREF'''
        return self.tag_position('trajector')
    
    def landmark(self):
        '''landmark IDREF'''
        return self.tag_position('landmark')
    
#     def trigger(self):
#         '''source IDREF'''
#         return self.tag_position('trigger')
    
    def frame_type(self):
        '''frame_type ( ABSOLUTE | INTRINSIC | RELATIVE )'''
        return self.tag.get('frame_type', 'NOT_OLINK')

    def reference_pt(self):
        '''referencePt IDREF'''
        return self.tag_position('referencePt')

    def projective(self):
        '''projective ( TRUE | FALSE )'''
        return self.tag.get('projective', '')
    
# TAG TYPE FILTER
def is_dir_tag(tag):
    ''' load c_path / pu / spatial entity / c_spatial_signal / c_nonmotion_event / c_motion heads'''
    tag_id = tag.get('id', '')
    if bool(re.findall('^s\d+', tag_id)):
        sem_type = tag.get('semantic_type', '')
        if sem_type == 'DIRECTIONAL' or sem_type == 'DIR_TOP':
            return True
    return False    
    
def get_dir_tag_indices(sentence, tag_dict):
    return get_tag_and_no_tag_indices(sentence, tag_dict, is_dir_tag)

# # alternate method of selecting olinks, didn't work
# def is_tag(tag):
#     ''' load c_path / pu / spatial entity / c_spatial_signal / c_nonmotion_event / c_motion heads'''
#     tag_id = tag.get('id', '')
#     return any([
#                 bool(re.findall('^s\d+', tag_id)),
#                 bool(re.findall('^p\d+', tag_id)),
#                 bool(re.findall('^pl\d+', tag_id)),
#                 bool(re.findall('^se\d+', tag_id)),
#                 bool(re.findall('^e\d+', tag_id)),
#                 bool(re.findall('^m\d+', tag_id))
#                 ])
# 
# def get_tag_indices(sentence, tag_dict):
#     return get_tag_and_no_tag_indices(sentence, tag_dict, is_tag)


# TEST
class OLinkDemo(Demo):
    def __init__(self, doc_path='./training', split=0.8):
        super(OLinkDemo, self).__init__(doc_path, split)
        self.indices_function = get_dir_tag_indices
        self.extent_class = OLinkTag

class OLinkIsLinkDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.is_olink())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class OLinkFromIDDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.from_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class OLinkToIDDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.to_id())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class OLinkRelTypeDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.rel_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
        
class OLinkTrajectorDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.trajector())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class OLinkLandmarkDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.landmark())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
        
class OLinkTriggerDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.trigger())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]
    
class OLinkFrameTypeDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.frame_type())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class OLinkReferencePtDemo(OLinkDemo):      
    def get_label_function(self):
        return  lambda x: str(x.reference_pt())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]

class OLinkProjectiveDemo(OLinkDemo): 
    def get_label_function(self):
        return  lambda x: str(x.projective())

    def get_feature_functions(self):
        return [lambda x: x.curr_token(),
                ]


if __name__ == "__main__":
    
    from_id = OLinkFromIDDemo()
    from_id.run_demo()

    to_id = OLinkToIDDemo()
    from_id.run_demo()

    rel_type = OLinkRelTypeDemo()
    rel_type.run_demo()

    trajector = OLinkTrajectorDemo()
    trajector.run_demo()

    landmark = OLinkLandmarkDemo()
    landmark.run_demo()
        
    reference = OLinkReferencePtDemo()
    reference.run_demo()

    projective = OLinkProjectiveDemo()
    projective.run_demo()
