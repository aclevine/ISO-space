'''
Created on Dec 19, 2014

@author: Aaron Levine
'''
from d_move_link import *
from d_olink import *
from d_qs_link import *
import os
from c_motion import get_motion_tag_indices, MotionTag
from util.Corpora.corpus import HypotheticalCorpus
from c_spatial_signal import SignalTag

def get_tag_id(extent, label):
    """ find tag ID based on tag offset prediction"""
    tag_offset = int(label)
    if tag_offset > 0:
        if extent.next_tags:
            return extent.next_tags[tag_offset-1]['id']
    if tag_offset < 0:
        if extent.prev_tags:
            return extent.prev_tags[tag_offset]['id']         
    return ''

def make_links(train_path, test_path, out_path, 
               index_filter, tag_class, link_name, id_prefix):
    # make olink
    test_data = HypotheticalCorpus(test_path)
    test_data = list(test_data.extents(index_filter,
                                       tag_class))
    #parse into XML tags
    id_number = 0
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename

    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            id_number = 0
            curr_doc = extent.document
            doc_name = curr_doc.basename
        tag = {'name': link_name, 
               'id': '{}{}'.format(id_prefix, id_number),
               'trigger': extent.tag['id']
               }
        extent.document.insert_tag(tag)
        id_number += 1
    curr_doc.save_xml(os.path.join(out_path, doc_name))
    



def generate_qslinks(train_path, test_path, out_path):

    # make olink
    make_links(train_path, test_path, out_path, 
               get_top_tag_indices, SignalTag, 
               'QSLINK', 'qsl')


    # generate labels
    from_id = QSLinkFromIDDemo(train_path = train_path, test_path = test_path)
    from_labels, test_data = from_id.generate_labels()
 
    to_id = QSLinkToIDDemo(train_path = train_path, test_path = test_path)
    to_labels, _ = to_id.generate_labels()
 
    rel_type = QSLinkRelTypeDemo(train_path = train_path, test_path = test_path)
    rel_type_labels, _ = rel_type.generate_labels()
          
     #parse into XML tags    
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename

    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        tag = extent.document.query_links(['QSLINK'], extent.tag['trigger'])[0]
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)        
        # trajector
        from_offset = int(from_labels[offsets])
        if from_offset > 0:
            from_tag = extent.next_tags[min(from_offset, len(extent.next_tags)) - 1]
        else:
            from_tag = extent.prev_tags[max(from_offset, -1 * len(extent.prev_tags))]
        tag.attrs['trajector'] = from_tag['id']
        tag.attrs['fromID'] = from_tag['id']
        tag.attrs['fromText'] = from_tag['text']
        # landmark
        to_offset = int(to_labels[offsets])
        if to_offset > 0:
            from_tag = extent.next_tags[min(to_offset, len(extent.next_tags)) - 1]
        else:
            from_tag = extent.prev_tags[max(to_offset, -1 * len(extent.prev_tags))]
        tag.attrs['landmark'] = from_tag['id']
        tag.attrs['toID'] = from_tag['id']
        tag.attrs['toText'] = from_tag['text']
        # rel_type
        tag.attrs['relType'] = rel_type_labels[offsets]        
                 
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join(test_path, doc_name))
    curr_doc.save_xml(os.path.join(out_path, doc_name))



def generate_olinks(train_path, test_path, out_path):
    # make olink
    test_data = HypotheticalCorpus(test_path)
    test_data = list(test_data.extents(get_dir_tag_indices,
                                          SignalTag))

    #parse into XML tags    
    id_number = 0
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            id_number = 0
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
        tag = {'name': 'OLINK', 
               'id': '{}{}'.format('ol', id_number),
               'trigger': extent.tag['id']
               }
        extent.document.insert_tag(tag)
        id_number += 1
    curr_doc.save_xml(os.path.join(out_path, doc_name))

    # generate labels
    from_id = OLinkFromIDDemo(train_path = train_path, test_path = test_path)
    from_labels, test_data = from_id.generate_labels()
 
    to_id = OLinkToIDDemo(train_path = train_path, test_path = test_path)
    to_labels, _ = to_id.generate_labels()
 
    rel_type = OLinkRelTypeDemo(train_path = train_path, test_path = test_path)
    rel_type_labels, _ = rel_type.generate_labels()
         
    reference = OLinkReferencePtDemo(train_path = train_path, test_path = test_path)
    ref_labels, _ = reference.generate_labels()
 
    projective = OLinkProjectiveDemo(train_path = train_path, test_path = test_path)
    proj_labels, _ = projective.generate_labels()

    frame = OLinkFrameTypeDemo(train_path = train_path, test_path = test_path)
    frame_labels, _ = projective.generate_labels()
 
    #parse into XML tags
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename

    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        tag = extent.document.query_links(['OLINK'], extent.tag['trigger'])[0]
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)        
        # trajector
        from_offset = int(from_labels[offsets])
        if from_offset > 0:
            from_tag = extent.next_tags[min(from_offset, len(extent.next_tags)) - 1]
        else:
            from_tag = extent.prev_tags[max(from_offset, -1 * len(extent.prev_tags))]
        tag.attrs['trajector'] = from_tag['id']
        tag.attrs['fromID'] = from_tag['id']
        tag.attrs['fromText'] = from_tag['text']
        # landmark
        to_offset = int(to_labels[offsets])
        if to_offset > 0:
            from_tag = extent.next_tags[min(to_offset, len(extent.next_tags)) - 1]
        else:
            from_tag = extent.prev_tags[max(to_offset, -1 * len(extent.prev_tags))]
        tag.attrs['landmark'] = from_tag['id']
        tag.attrs['toID'] = from_tag['id']
        tag.attrs['toText'] = from_tag['text']
        # referencePt
        ref_value = ref_labels[offsets]
        if ref_value.isalpha():
            tag.attrs['referencePt'] = ref_value
        else:
            tag.attrs['referencePt'] = get_tag_id(extent, ref_value)        
        # rel_type
        tag.attrs['relType'] = rel_type_labels[offsets]        
        #frame_type
        tag.attrs['frame_type'] = frame_labels[offsets]
        # projective
        tag.attrs['projective'] = proj_labels[offsets]
                 
    curr_doc.save_xml(os.path.join(out_path, doc_name))

        

def generate_movelinks(train_path, test_path, out_path):
    # make movelink
    train_corpus = HypotheticalCorpus(test_path)
    test_data = list(train_corpus.extents(get_motion_tag_indices,
                                        MotionTag))

    #parse into XML tags    
    id_number = 0
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            id_number = 0
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
        tag = {'name': 'MOVELINK', 
               'id': '{}{}'.format('mvl', id_number),
               'fromID': extent.tag['id'],
               'fromText': extent.document.text()[int(extent.tag['start']): int(extent.tag['end'])],
               'trigger': extent.tag['id']
               }
        extent.document.insert_tag(tag)
        id_number += 1
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))

    # fill attributes    
    d = MoveLinkMoverDemo(train_path = train_path, test_path = test_path)  
    mover_labels, test_data = d.generate_labels()
 
    d = MoveLinkSourceDemo(train_path = train_path, test_path = test_path)  
    source_labels, test_data = d.generate_labels()
   
    d = MoveLinkGoalDemo(train_path = train_path, test_path = test_path)
    goal_labels, _ = d.generate_labels()
    
    d = MoveLinkMidPointDemo(train_path = train_path, test_path = test_path)  
    midpoint_labels, _ = d.generate_labels()
   
    d = MoveLinkLandmarkDemo(train_path = train_path, test_path = test_path)  
    landmark_labels, _ = d.generate_labels()
      
    d = MoveLinkGoalReachedDemo(train_path = train_path, test_path = test_path)  
    goal_reached_labels, _ = d.generate_labels()

    #parse into XML tags
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename

    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        tag = extent.document.query_links(['MOVELINK'], extent.tag['trigger'])[0]
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)        
        # mover
        mover_offset = int(mover_labels[offsets])
        if mover_offset == 0 or (mover_offset > 0 and not extent.next_tags) or (mover_offset < 0 and not extent.prev_tags):
            tag.attrs['mover'] = ''
            tag.attrs['toID'] = tag.attrs['fromID']
            tag.attrs['toText'] = tag.attrs['fromText']                     
        else:
            if mover_offset > 0:
                mover_tag = extent.next_tags[min(mover_offset, len(extent.next_tags)) - 1]
            else:
                mover_tag = extent.prev_tags[max(mover_offset, -1 * len(extent.prev_tags))]
            tag.attrs['mover'] = mover_tag['id']
            tag.attrs['toID'] = mover_tag['id']
            tag.attrs['toText'] = mover_tag['text']
        # source 
        tag.attrs['source'] = get_tag_id(extent, source_labels[offsets])        
        # goal
        tag.attrs['goal'] = get_tag_id(extent, goal_labels[offsets])                
        # midpoint
        tag.attrs['midpoint'] = get_tag_id(extent, midpoint_labels[offsets])                
        # landmark
        tag.attrs['landmark'] = get_tag_id(extent, landmark_labels[offsets])
        #goal_reached   
        tag.attrs['goal_reached'] = goal_reached_labels[offsets]
            
    curr_doc.save_xml(os.path.join(out_path, doc_name))
    

if __name__ == "__main__":

    train_path = './data/training'
    test_path = './data/final/test/configuration1/c'
    out_path = './data/final/test/configuration1/d'

    generate_qslinks(train_path, test_path, out_path)
    generate_olinks(train_path, test_path, out_path)
    generate_movelinks(train_path, test_path, out_path)
