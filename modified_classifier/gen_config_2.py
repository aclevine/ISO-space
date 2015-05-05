#!/usr/bin/env python
"""
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

generate documents for configuration 2 tasks
"""
import re, os
from util.model.baseline_classifier import copy_folder
from util.d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks
from util.c_fill_tag_attrs import generate_attributes


if __name__ == "__main__":

    with open('config.txt') as fo:
        text = fo.read()
    train_path = re.findall('TRAINING_PATH *= *(.*)', text)[0]
    gen_path = re.findall('CONFIG_2_GEN_PATH *= *(.*)', text)[0]

    parent_path = os.path.dirname(gen_path)    
    hyp_a = os.path.join(parent_path, '2a')
    hyp_b = os.path.join(parent_path, '2b')  
    hyp_c = os.path.join(parent_path, '2c')   
    
    # 2a
    copy_folder(gen_path, hyp_a)
    generate_attributes(train_path, hyp_a, hyp_a)
  
    # 2b + c
    copy_folder(hyp_a, hyp_b)
    generate_qslinks(train_path, hyp_b, hyp_b)
    generate_olinks(train_path, hyp_b, hyp_b)
    generate_movelinks(train_path, hyp_b, hyp_b)
  
    copy_folder(hyp_b, hyp_c)
