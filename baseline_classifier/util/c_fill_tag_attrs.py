'''
Created on Dec 19, 2014

@author: Aaron Levine
'''

from util.c_path import *
from util.c_motion_signal import *
from util.c_motion import *
from util.c_nonmotion_event import *
from util.c_path import *
from util.c_place import *
from util.c_spatial_entity import *
from util.c_spatial_signal import *
from util.model.demo import copy_folder
import os

def generate_motion_attr(train_path, test_path, out_path):
    # generate labels
    d = MotionTypeClassifier(train_path = train_path, test_path = test_path)
    motion_type_labels, test_data = d.generate_labels()
     
    d = MotionClassClassifier(train_path = train_path, test_path = test_path)
    motion_class_labels, _ = d.generate_labels()
     
    d = MotionSenseClassifier(train_path = train_path, test_path = test_path)
    motion_sense_labels, _ = d.generate_labels()

    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)

        tags = extent.document.query_extents(['MOTION'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]        
        tag.attrs['motion_type'] = motion_type_labels[offsets]
        tag.attrs['motion_class'] = motion_class_labels[offsets]
        tag.attrs['motion_sense'] = motion_sense_labels[offsets]

    curr_doc.save_xml(os.path.join(out_path, doc_name))


def generate_motion_signal_attr(train_path, test_path, out_path):
    # generate labels
    d = MotionSignalTypeClassifier(train_path = train_path, test_path = test_path)
    motion_signal_type_labels, test_data = d.generate_labels()

    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
        tags = extent.document.query_extents(['MOTION_SIGNAL'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]
            tag.attrs['motion_signal_type'] = motion_signal_type_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    curr_doc.save_xml(os.path.join(out_path, doc_name))
    

def generate_event_attr(train_path, test_path, out_path):
    # generate labels
    mod = EventModClassifier(train_path = train_path, test_path = test_path)
    event_mod_labels, test_data = mod.generate_labels()
            
    count = EventCountableClassifier(train_path = train_path, test_path = test_path)
    event_count_labels, _ = count.generate_labels()        
 
    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tags = extent.document.query_extents(['NONMOTION_EVENT'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]
            tag.attrs['mod'] = event_mod_labels[offsets]
            tag.attrs['countable'] = event_count_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    curr_doc.save_xml(os.path.join(out_path, doc_name))
    
    
def generate_path_attr(train_path, test_path, out_path):
    # generate labels
    d = PathDimensionalityClassifier(train_path = train_path, test_path = test_path)
    path_dimension_labels, test_data = d.generate_labels()
       
    d = PathFormClassifier(train_path = train_path, test_path = test_path)
    path_form_labels, _ = d.generate_labels()
                                         
    d = PathCountableClassifier(train_path = train_path, test_path = test_path)
    path_count_labels, _ = d.generate_labels()
   
    d = PathModClassifier(train_path = train_path, test_path = test_path)
    path_mod_labels, _ = d.generate_labels()
 
    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tags = extent.document.query_extents(['PATH'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]
            tag.attrs['form'] = path_form_labels[offsets]
            tag.attrs['countable'] = path_count_labels[offsets]  
            tag.attrs['dimensionality'] = path_dimension_labels[offsets]
            tag.attrs['mod'] = path_mod_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    curr_doc.save_xml(os.path.join(out_path, doc_name))
 

def generate_place_attr(train_path, test_path, out_path):
    # generate labels
    d = PlaceDimensionalityClassifier(train_path = train_path, test_path = test_path)
    place_dimension_labels, test_data = d.generate_labels()
        
    d = PlaceFormClassifier(train_path = train_path, test_path = test_path)
    place_form_labels, _ = d.generate_labels()
        
    d = PlaceCountableClassifier(train_path = train_path, test_path = test_path)
    place_count_labels, _ = d.generate_labels()
        
    d = PlaceModClassifier(train_path = train_path, test_path = test_path)
    place_mod_labels, _ = d.generate_labels()
 
    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tags = extent.document.query_extents(['PLACE'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]
            tag.attrs['form'] = place_form_labels[offsets]
            tag.attrs['countable'] = place_count_labels[offsets]  
            tag.attrs['dimensionality'] = place_dimension_labels[offsets]
            tag.attrs['mod'] = place_mod_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    curr_doc.save_xml(os.path.join(out_path, doc_name))
    
    
def generate_entity_attr(train_path, test_path, out_path):
    # generate labels
    d = EntityDimensionalityClassifier(train_path = train_path, test_path = test_path)
    entity_dimension_labels, test_data = d.generate_labels()
        
    d = EntityFormClassifier(train_path = train_path, test_path = test_path)
    entity_form_labels, _ = d.generate_labels()
        
    d = EntityCountableClassifier(train_path = train_path, test_path = test_path)
    entity_count_labels, _ = d.generate_labels()
        
    d = EntityModClassifier(train_path = train_path, test_path = test_path)
    entity_mod_labels, _ = d.generate_labels()
 
    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
         
        tags = extent.document.query_extents(['SPATIAL_ENTITY'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]
            tag.attrs['form'] = entity_form_labels[offsets]
            tag.attrs['countable'] = entity_count_labels[offsets]  
            tag.attrs['dimensionality'] = entity_dimension_labels[offsets]
            tag.attrs['mod'] = entity_mod_labels[offsets]
    curr_doc.save_xml(os.path.join(out_path, doc_name))


def generate_signal_attr(train_path, test_path, out_path):
    # generate labels
    d = SignalSemanticTypeClassifier(train_path = train_path, test_path = test_path)
    signal_type_labels, test_data = d.generate_labels()
     
    # labels -> tagged doc
    curr_doc = test_data[0].document
    doc_name = curr_doc.basename
    for extent in test_data:
        if doc_name != extent.document.basename:
            curr_doc.save_xml(os.path.join(out_path, doc_name))
            curr_doc = extent.document
            doc_name = curr_doc.basename
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tags = extent.document.query_extents(['SPATIAL_SIGNAL'], extent.lex[0].begin, extent.lex[-1].end)
        if tags:
            tag = tags[0]
        tag.attrs['semantic_type'] = signal_type_labels[offsets]
    curr_doc.save_xml(os.path.join(out_path, doc_name))

    
def generate_attributes(train_path, test_path, out_path):

    generate_motion_attr(train_path, test_path, out_path)
    generate_motion_signal_attr(train_path, test_path, out_path)
    generate_event_attr(train_path, test_path, out_path)
    generate_path_attr(train_path, test_path, out_path)
    generate_place_attr(train_path, test_path, out_path)
    generate_entity_attr(train_path, test_path, out_path)
    generate_signal_attr(train_path, test_path, out_path)


if __name__ == "__main__":

    training_path = './data/training'
    hyp_c = './data/final/test/configuration1/c'
    hyp_d = './data/final/test/configuration1/d'
    generate_attributes(training_path, hyp_c, hyp_c)

    copy_folder(hyp_c, hyp_d)
    
