#!/usr/bin/env python
"""
Created on Dec 20, 2014

@author: Aaron Levine
@email: aclevine@brandeis.edu

generate documents for configuration 3 tasks
"""
import re, os
from util.model.baseline_classifier import copy_folder
from util.d_fill_link_attrs import generate_qslinks, generate_olinks,\
    generate_movelinks


if __name__ == "__main__":
    
    with open('config.txt') as fo:
        text = fo.read()
    train_path = re.findall('TRAINING_PATH *= *(.*)', text)[0]
    gen_path = re.findall('CONFIG_3_GEN_PATH *= *(.*)', text)[0]


    parent_path = os.path.dirname(gen_path)    
    hyp_a = os.path.join(parent_path, '3a')
    hyp_b = os.path.join(parent_path, '3b')  
    
    
    # 2b + c
    copy_folder(gen_path, hyp_a)
    generate_qslinks(train_path, hyp_a, hyp_a)
    generate_olinks(train_path, hyp_a, hyp_a)
    generate_movelinks(train_path, hyp_a, hyp_a)

    copy_folder(hyp_a, hyp_b)