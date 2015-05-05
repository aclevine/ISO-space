#!/usr/bin/env python
"""
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu
"""
import re, os
from util.model.baseline_classifier import copy_folder
from util.d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
from util.c_fill_tag_attrs import generate_attributes
from util.ab_identify_spans_types import generate_elements_types, make_crf


if __name__ == "__main__":
    
    # pre-1a
    with open('config.txt') as fo:
        text = fo.read()
    train_path = re.findall('TRAINING_PATH *= *(.*)', text)[0]
    gen_path = re.findall('CONFIG_1_GEN_PATH *= *(.*)', text)[0]
    
    parent_path = os.path.dirname(gen_path)    
    hyp_a = os.path.join(parent_path, '1a')
    hyp_b = os.path.join(parent_path, '1b')  
    hyp_c = os.path.join(parent_path, '1c')   
    hyp_d = os.path.join(parent_path, '1d')
    hyp_e = os.path.join(parent_path, '1e')
        
    # 1a + 1b
    generate_elements_types(train_path, gen_path, hyp_a, make_crf)
    copy_folder(hyp_a, hyp_b)

    # 1c
    copy_folder(hyp_b, hyp_c)
    generate_attributes(train_path, hyp_c, hyp_c)
 
    #1d + e
    copy_folder(hyp_c, hyp_d)
    generate_qslinks(train_path, hyp_d, hyp_d)
    generate_olinks(train_path, hyp_d, hyp_d)
    generate_movelinks(train_path, hyp_d, hyp_d)
 
    copy_folder(hyp_d, hyp_e)
