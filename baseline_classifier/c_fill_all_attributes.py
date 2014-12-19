'''
Created on Dec 19, 2014

@author: Aaron Levine
'''

from c_path import *
from c_motion_signal import *
from c_motion import *
from c_nonmotion_event import *
from c_path import *
from c_place import *
from c_spatial_entity import *
from c_spatial_signal import *

def generate_doc(inpath, outpath):

    d = MotionTypeDemo(train_path = inpath, test_path = outpath)
    motion_type_labels, test_data = d.generate_labels()
     
    d = MotionClassDemo(train_path = inpath, test_path = outpath)
    motion_class_labels, _ = d.generate_labels()
     
    d = MotionSenseDemo(train_path = inpath, test_path = outpath)
    motion_sense_labels, _ = d.generate_labels()

    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)

        tag = extent.document.query_extents('MOTION', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['motion_type'] = motion_type_labels[offsets]
        tag.attrs['motion_class'] = motion_class_labels[offsets]
        tag.attrs['motion_sense'] = motion_sense_labels[offsets]

        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))

    #====================================================================
      
    d = MotionSignalTypeDemo(train_path = inpath, test_path = outpath)
    motion_signal_type_labels, test_data = d.generate_labels()

    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
        tag = extent.document.query_extents('MOTION_SIGNAL', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['motion_signal_type'] = motion_signal_type_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
    

    #====================================================================
           
    d = EventModDemo(train_path = inpath, test_path = outpath)
    event_mod_labels, test_data = d.generate_labels()
            
    d = EventCountableDemo(train_path = inpath, test_path = outpath)
    event_count_labels, _ = d.generate_labels()        
 
    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tag = extent.document.query_extents('NONMOTION_EVENT', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['mod'] = event_mod_labels[offsets]
        tag.attrs['countable'] = event_count_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
 
    #====================================================================
   
    d = PathDimensionalityDemo(train_path = inpath, test_path = outpath)
    path_dimension_labels, test_data = d.generate_labels()
       
    d = PathFormDemo(train_path = inpath, test_path = outpath)
    path_form_labels, _ = d.generate_labels()
                                         
    d = PathCountableDemo(train_path = inpath, test_path = outpath)
    path_count_labels, _ = d.generate_labels()
   
    d = PathModDemo(train_path = inpath, test_path = outpath)
    path_mod_labels, _ = d.generate_labels()
 
    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tag = extent.document.query_extents('PATH', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['form'] = path_form_labels[offsets]
        tag.attrs['countable'] = path_count_labels[offsets]  
        tag.attrs['dimensionality'] = path_dimension_labels[offsets]
        tag.attrs['mod'] = path_mod_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
 
       
    #====================================================================
   
    d = PlaceDimensionalityDemo(train_path = inpath, test_path = outpath)
    place_dimension_labels, test_data = d.generate_labels()
        
    d = PlaceFormDemo(train_path = inpath, test_path = outpath)
    place_form_labels, _ = d.generate_labels()
        
    d = PlaceCountableDemo(train_path = inpath, test_path = outpath)
    place_count_labels, _ = d.generate_labels()
        
    d = PlaceModDemo(train_path = inpath, test_path = outpath)
    place_mod_labels, _ = d.generate_labels()
 
    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tag = extent.document.query_extents('PLACE', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['form'] = place_form_labels[offsets]
        tag.attrs['countable'] = place_count_labels[offsets]  
        tag.attrs['dimensionality'] = place_dimension_labels[offsets]
        tag.attrs['mod'] = place_mod_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
   
    #====================================================================
   
    d = EntityDimensionalityDemo(train_path = inpath, test_path = outpath)
    entity_dimension_labels, test_data = d.generate_labels()
        
    d = EntityFormDemo(train_path = inpath, test_path = outpath)
    entity_form_labels, _ = d.generate_labels()
        
    d = EntityCountableDemo(train_path = inpath, test_path = outpath)
    entity_count_labels, _ = d.generate_labels()
        
    d = EntityModDemo(train_path = inpath, test_path = outpath)
    entity_mod_labels, _ = d.generate_labels()
 
    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
         
        tag = extent.document.query_extents('SPATIAL_ENTITY', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['form'] = entity_form_labels[offsets]
        tag.attrs['countable'] = entity_count_labels[offsets]  
        tag.attrs['dimensionality'] = entity_dimension_labels[offsets]
        tag.attrs['mod'] = entity_mod_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))
   
    #====================================================================
   
    d = SignalSemanticTypeDemo(train_path = inpath, test_path = outpath)
    signal_type_labels, test_data = d.generate_labels()
     
    doc_name = test_data[0].document.basename
    for extent in test_data:
        offsets = "{a},{b},{c}".format(a=extent.basename,
                                       b=extent.lex[0].begin, 
                                       c=extent.lex[-1].end)
 
        tag = extent.document.query_extents('SPATIAL_SIGNAL', extent.lex[0].begin, extent.lex[-1].end)[0]
        tag.attrs['semantic_type'] = signal_type_labels[offsets]
        if doc_name != extent.document.basename:
            doc_name = extent.document.basename
            extent.document.save_xml(os.path.join('data', 'test_dev', doc_name))
    test_data[-1].document.save_xml(os.path.join('data', 'test_dev', doc_name))


if __name__ == "__main__":

    inpath = './data/training'
    outpath = './data/test_dev'
    generate_doc(inpath, outpath)
        

